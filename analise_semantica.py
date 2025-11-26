# analise_semantica.py
import logging
from antlr4 import ParseTreeWalker
from PubyParser import PubyParser
from PubyListener import PubyListener
from erro import Erro

TIPO_NUM = "NUM"
TIPO_STRING = "STRING"
TIPO_BOOL = "BOOL"
TIPO_DESCONHECIDO = "DESCONHECIDO"
TIPO_INTERVALO = "INTERVALO"


class AnaliseSemantica(PubyListener):
    """
    Fase de análise semântica do Puby.

    O que ela faz:
    - Mantém uma tabela de símbolos { nome_variavel -> tipo }
    - Verifica uso de variável antes de inicialização
    - Verifica atribuições com troca de tipo (num -> string, etc.)
    - Garante que:
        * operandos de +, *, comparações (<, <=, ==, ...) sejam numéricos
        * limites de intervalo em 'for' sejam numéricos
        * condição de if/while seja booleana (expr relacional / lógica)
        * variáveis usadas em ++/-- sejam numéricas
    """

    def __init__(self, erro_handler: Erro):
        self.erro_handler = erro_handler
        self.logger = logging.getLogger("Puby")
        self.tabela_simbolos = {}

    # ------------------- ENTRADA PRINCIPAL -------------------

    def executarAnaliseSemantica(self, ast) -> bool:
        self.logger.info("Iniciando análise semântica...")

        if ast is None:
            self.erro_handler.registrar_erro(
                "SEMANTICO", 0, 0, "AST não fornecida para análise semântica."
            )
            return False

        walker = ParseTreeWalker()
        walker.walk(self, ast)

        if not self.erro_handler.tem_semantico:
            self.logger.info("Análise semântica concluída sem erros.")
            return True

        self.logger.error("Análise semântica concluída com erros.")
        return False

    # ------------------- HELPERS INTERNOS -------------------

    def _registrar_erro(self, ctx, mensagem: str):
        linha = 0
        coluna = 0
        if hasattr(ctx, "start") and ctx.start is not None:
            linha = ctx.start.line
            coluna = ctx.start.column
        self.erro_handler.registrar_erro("SEMANTICO", linha, coluna, mensagem)

    def _get_tipo(self, ctx):
        return getattr(ctx, "tipo", TIPO_DESCONHECIDO)

    # ========================================================
    #                        COMANDOS
    # ========================================================

    # leitura: ID '=' GETS ;
    def exitLeitura(self, ctx: PubyParser.LeituraContext):
        nome = ctx.ID().getText()
        antigo = self.tabela_simbolos.get(nome)

        # Decisão: entrada via gets será tratada como NUM (o code_generator converte para float)
        novo_tipo = TIPO_NUM

        if antigo and antigo != novo_tipo and antigo != TIPO_DESCONHECIDO:
            self._registrar_erro(
                ctx,
                f"Variável '{nome}' já utilizada como {antigo} e agora recebe valor {novo_tipo}.",
            )

        self.tabela_simbolos[nome] = novo_tipo

    # atribuicao: ID '=' expressao ;
    def exitAtribuicao(self, ctx: PubyParser.AtribuicaoContext):
        nome = ctx.ID().getText()
        tipo_expr = self._get_tipo(ctx.expressao())
        antigo = self.tabela_simbolos.get(nome)

        if (
            antigo
            and tipo_expr != TIPO_DESCONHECIDO
            and antigo != tipo_expr
            and antigo != TIPO_DESCONHECIDO
        ):
            self._registrar_erro(
                ctx,
                f"Variável '{nome}' já utilizada como {antigo} e agora recebe valor {tipo_expr}.",
            )

        # Mesmo que ainda seja DESCONHECIDO, registramos — futuras atribuições podem refinar
        self.tabela_simbolos[nome] = tipo_expr

    # incremento: ID (OP_INC | OP_DEC) ;
    def exitIncremento(self, ctx: PubyParser.IncrementoContext):
        nome = ctx.ID().getText()
        tipo = self.tabela_simbolos.get(nome)

        if tipo is None:
            self._registrar_erro(
                ctx,
                f"Variável '{nome}' utilizada em incremento/decremento antes de ser inicializada.",
            )
        elif tipo != TIPO_NUM:
            self._registrar_erro(
                ctx,
                f"Operadores ++/-- só são permitidos em variáveis numéricas, "
                f"mas '{nome}' é do tipo {tipo}.",
            )

    # laco_para: FOR ID IN intervalo DO ... END
    def exitLaco_para(self, ctx: PubyParser.Laco_paraContext):
        nome = ctx.ID().getText()
        tipo_intervalo = self._get_tipo(ctx.intervalo())

        if tipo_intervalo != TIPO_INTERVALO:
            # Em geral o erro já terá sido emitido em exitIntervalo
            self._registrar_erro(ctx, "Intervalo inválido no laço 'for'.")

        antigo = self.tabela_simbolos.get(nome)
        if antigo and antigo not in (TIPO_NUM, TIPO_DESCONHECIDO):
            self._registrar_erro(
                ctx,
                f"Variável de controle do laço 'for' '{nome}' deve ser numérica, "
                f"mas foi utilizada como {antigo}.",
            )

        self.tabela_simbolos[nome] = TIPO_NUM

    # intervalo: expressao RANGE expressao ;
    def exitIntervalo(self, ctx: PubyParser.IntervaloContext):
        inicio = self._get_tipo(ctx.expressao(0))
        fim = self._get_tipo(ctx.expressao(1))

        if inicio != TIPO_NUM or fim != TIPO_NUM:
            self._registrar_erro(
                ctx,
                "Limites de intervalo (inicio..fim) devem ser numéricos.",
            )
            ctx.tipo = TIPO_DESCONHECIDO
        else:
            ctx.tipo = TIPO_INTERVALO

    # condicao: expressao ;
    def exitCondicao(self, ctx: PubyParser.CondicaoContext):
        tipo_expr = self._get_tipo(ctx.expressao())

        if tipo_expr != TIPO_BOOL:
            self._registrar_erro(
                ctx,
                f"Condição deve ser booleana (resultado de comparação ou expressão lógica), "
                f"mas foi encontrada expressão do tipo {tipo_expr}.",
            )

        ctx.tipo = TIPO_BOOL

    # ========================================================
    #                       EXPRESSÕES
    # ========================================================

    # expressao: logico_baixo ;
    def exitExpressao(self, ctx: PubyParser.ExpressaoContext):
        ctx.tipo = self._get_tipo(ctx.logico_baixo())

    # logico_baixo: not_baixo logico_baixo_suf ;
    def exitLogico_baixo(self, ctx: PubyParser.Logico_baixoContext):
        # Para simplificar, propagamos o tipo principal (rel/booleana) já tratado em níveis abaixo
        ctx.tipo = self._get_tipo(ctx.not_baixo())

    # not_baixo: NOT not_baixo | logico_alto ;
    def exitNot_baixo(self, ctx: PubyParser.Not_baixoContext):
        if ctx.NOT():
            tipo_interno = self._get_tipo(ctx.not_baixo())
            if tipo_interno != TIPO_BOOL:
                self._registrar_erro(
                    ctx,
                    f"Operador 'not' aplicado a expressão do tipo {tipo_interno}, esperado BOOL.",
                )
            ctx.tipo = TIPO_BOOL
        else:
            ctx.tipo = self._get_tipo(ctx.logico_alto())

    # logico_alto: rel logico_alto_suf ;
    def exitLogico_alto(self, ctx: PubyParser.Logico_altoContext):
        # 'rel' é responsável por determinar se a expressão virou BOOL (comparação) ou manteve tipo numérico
        ctx.tipo = self._get_tipo(ctx.rel())

    # rel: soma (OP_REL soma)* ;
    def exitRel(self, ctx: PubyParser.RelContext):
        somas = ctx.soma()
        if not somas:
            ctx.tipo = TIPO_DESCONHECIDO
            return

        # Verifica se existe algum operador relacional (<, <=, >, >=, ==, !=)
        tem_rel = False
        try:
            ops = ctx.OP_REL()
            if not isinstance(ops, list):
                ops = [ops]
            tem_rel = any(op is not None for op in ops)
        except AttributeError:
            tem_rel = False

        if not tem_rel:
            # Sem comparador: só propaga o tipo da expressão aritmética
            ctx.tipo = self._get_tipo(somas[0])
            return

        # Com comparador: todos os operandos devem ser numéricos
        for s in somas:
            t = self._get_tipo(s)
            if t not in (TIPO_NUM, TIPO_DESCONHECIDO):
                self._registrar_erro(
                    ctx,
                    f"Operação relacional requer operandos numéricos, mas encontrou {t}.",
                )

        ctx.tipo = TIPO_BOOL

    # soma: mult (OP_ADD mult)* ;
    def exitSoma(self, ctx: PubyParser.SomaContext):
        mults = ctx.mult()
        if not mults:
            ctx.tipo = TIPO_DESCONHECIDO
            return

        tipo = self._get_tipo(mults[0])

        # Para simplificar, '+' é apenas numérico
        for m in mults[1:]:
            tdir = self._get_tipo(m)
            if tipo != TIPO_NUM or tdir != TIPO_NUM:
                self._registrar_erro(
                    ctx,
                    f"Operador '+' só é permitido entre valores numéricos "
                    f"(encontrado {tipo} e {tdir}).",
                )
                tipo = TIPO_DESCONHECIDO
                break
            tipo = TIPO_NUM

        ctx.tipo = tipo

    # mult: unario (OP_MUL unario)* ;
    def exitMult(self, ctx: PubyParser.MultContext):
        unarios = ctx.unario()
        if not unarios:
            ctx.tipo = TIPO_DESCONHECIDO
            return

        tipo = self._get_tipo(unarios[0])

        for u in unarios[1:]:
            tdir = self._get_tipo(u)
            if tipo != TIPO_NUM or tdir != TIPO_NUM:
                self._registrar_erro(
                    ctx,
                    f"Operadores multiplicativos só são permitidos entre valores numéricos "
                    f"(encontrado {tipo} e {tdir}).",
                )
                tipo = TIPO_DESCONHECIDO
                break
            tipo = TIPO_NUM

        ctx.tipo = tipo

    # unario: (alguma combinação) | primario ;
    def exitUnario(self, ctx: PubyParser.UnarioContext):
        # Implementação simples: se tiver primario, use o tipo dele;
        # senão, se tiver outro unario dentro, propaga.
        prim = None
        if hasattr(ctx, "primario"):
            prim = ctx.primario()

        if prim is not None:
            ctx.tipo = self._get_tipo(prim)
            return

        # Se for algo como "-unario" ou similar, propagamos o tipo do filho
        inner_list = []
        try:
            inner_list = ctx.unario()
        except TypeError:
            # API defensiva, caso ANTLR retorne um único contexto em vez de lista
            try:
                inner_list = [ctx.unario(0)]
            except Exception:
                inner_list = []

        if inner_list:
            ctx.tipo = self._get_tipo(inner_list[0])
        else:
            ctx.tipo = TIPO_DESCONHECIDO

    # primario: NUM | STRING | ID | '(' expressao ')' ;
    def exitPrimario(self, ctx: PubyParser.PrimarioContext):
        if ctx.NUM():
            ctx.tipo = TIPO_NUM
        elif ctx.STRING():
            ctx.tipo = TIPO_STRING
        elif ctx.ID():
            nome = ctx.ID().getText()
            tipo = self.tabela_simbolos.get(nome)
            if tipo is None:
                self._registrar_erro(
                    ctx,
                    f"Variável '{nome}' usada antes de ser inicializada.",
                )
                tipo = TIPO_DESCONHECIDO
            ctx.tipo = tipo
        elif ctx.expressao():
            ctx.tipo = self._get_tipo(ctx.expressao())
        else:
            ctx.tipo = TIPO_DESCONHECIDO
