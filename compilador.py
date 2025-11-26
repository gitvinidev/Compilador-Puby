import logging
from erro import Erro
from analise_lexica import AnaliseLexica
from analise_sintatica import AnaliseSintatica
from analise_semantica import AnaliseSemantica 
from code_generator import CodeGenerator


class Compilador:
    def __init__(self, nome_arquivo_fonte: str):
        self.nome_arquivo_fonte = nome_arquivo_fonte
        self.logger = logging.getLogger("Puby")
        self.erro_handler = Erro()

        self.analise_lexica_mod = AnaliseLexica(self.erro_handler)
        self.analise_sintatica_mod = AnaliseSintatica(self.erro_handler)
        self.analise_semantica_mod = AnaliseSemantica(self.erro_handler)

        

    def compilar(self):
        self.logger.info(f"--- Iniciando compilação do arquivo {self.nome_arquivo_fonte} ---")

        # ---------------------- ANÁLISE LÉXICA ----------------------
        self.logger.info("Fase Léxica iniciada...")
        tokens_log, token_stream = self.analise_lexica_mod.executarAnaliseLexica(self.nome_arquivo_fonte)

        if self.erro_handler.tem_lexico or not token_stream:
            self.logger.error("Fase Léxica falhou. Compilação interrompida.")
            return False

        self.logger.info("Fase Léxica concluída sem erros.")

        # ---------------------- ANÁLISE SINTÁTICA ----------------------
        self.logger.info("Fase Sintática iniciada...")
        try:
            ast = self.analise_sintatica_mod.executarAnaliseSintatica(token_stream)
        except Exception:
            self.logger.error("Fase Sintática falhou. Compilação interrompida.")
            return False

        if self.erro_handler.tem_sintatico or not ast:
            self.logger.error("Fase Sintática detectou erros. Compilação interrompida.")
            return False

        self.logger.info("Fase Sintática concluída sem erros. AST gerada com sucesso.")

        # ---------------------- ANÁLISE SEMÂNTICA ----------------------
        self.logger.info("Fase Semântica iniciada...")
        try:
            ok_semantica = self.analise_semantica_mod.executarAnaliseSemantica(ast)
        except Exception:
            self.logger.error("Fase Semântica falhou. Compilação interrompida.")
            return False

        if self.erro_handler.tem_semantico or not ok_semantica:
            self.logger.error("Fase Semântica detectou erros. Compilação interrompida.")
            return False

        self.logger.info("Fase Semântica concluída sem erros.")


        # ---------------------- EXPORTAÇÃO DA AST ----------------------
        base_nome = self.nome_arquivo_fonte.rsplit('.', 1)[0]

        try:
            dot_file = base_nome + ".dot"
            self.logger.info(f"Exportando AST para: {dot_file}")
            self.analise_sintatica_mod.exportarAST_DOT(ast, dot_file)
        except Exception:
            self.logger.error("Falha ao exportar AST. Compilação interrompida.")
            return False

        try:
            svg_file = base_nome + ".svg"
            self.logger.info(f"Gerando SVG: {svg_file}")
            self.analise_sintatica_mod.exportarAST_SVG(dot_file, svg_file)
        except Exception:
            self.logger.error("Falha ao gerar SVG. Compilação interrompida.")
            return False
        
        # ---------------------- GERAÇÃO DE CÓDIGO PYTHON ----------------------
        try:
            python_file = base_nome + ".py"
            self.logger.info(f"Gerando código Python: {python_file}")
            
            gerador = CodeGenerator(output_file=python_file)

            # O nó raiz da AST é "programa"
            gerador.generate(ast)

            self.logger.info(f"Código Python gerado com sucesso em {python_file}")

        except Exception as e:
            self.logger.error(f"Falha na geração de código Python: {e}")
            return False


        # ---------------------- SUCESSO FINAL ----------------------
        self.logger.info("Compilação concluída sem erros!")
        return True
