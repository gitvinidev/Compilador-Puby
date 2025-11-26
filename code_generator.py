from PubyVisitor import PubyVisitor
from PubyParser import PubyParser

class CodeGenerator(PubyVisitor):

    def __init__(self):
        self.code = []
        self.indent = 0

    def tab(self):
        return "    " * self.indent

    # ---------------------------
    # programa
    # ---------------------------
    def visitPrograma(self, ctx):
        for cmd in ctx.comando():
            self.visit(cmd)

        return "\n".join(self.code)

    # ---------------------------
    # escrita  → puts expr
    # ---------------------------
    def visitEscrita(self, ctx):
        if ctx.expressao():
            exprs = [self.visit(e) for e in ctx.expressao()]
            line = f"print({', '.join(exprs)})"
        else:
            line = "print()"

        self.code.append(self.tab() + line)

    # ---------------------------
    # leitura → x = gets
    # ---------------------------
    def visitLeitura(self, ctx):
        var = ctx.ID().getText()
        self.code.append(self.tab() + f"{var} = input()")

    # ---------------------------
    # atribuição → x = expr
    # ---------------------------
    def visitAtribuicao(self, ctx):
        var = ctx.ID().getText()
        expr = self.visit(ctx.expressao())
        self.code.append(self.tab() + f"{var} = {expr}")

    # ---------------------------
    # incremento → x++ / x--
    # ---------------------------
    def visitIncremento(self, ctx):
        var = ctx.ID().getText()
        op = ctx.OP_INC() or ctx.OP_DEC()

        if op.getText() == "++":
            self.code.append(self.tab() + f"{var} += 1")
        else:
            self.code.append(self.tab() + f"{var} -= 1")

    # ---------------------------
    # if / elsif / else
    # ---------------------------
    def visitCondicional(self, ctx):
        cond = self.visit(ctx.condicao())
        self.code.append(self.tab() + f"if {cond}:")
        self.indent += 1

        for c in ctx.corpo_if(0).comando():
            self.visit(c)
        self.indent -= 1

        # Elsif
        for i in range(len(ctx.ELSIF())):
            cond = self.visit(ctx.condicao(i+1))
            self.code.append(self.tab() + f"elif {cond}:")
            self.indent += 1
            for c in ctx.corpo_if(i+1).comando():
                self.visit(c)
            self.indent -= 1

        # Else
        if ctx.ELSE():
            self.code.append(self.tab() + "else:")
            self.indent += 1
            for c in ctx.corpo_if(len(ctx.ELSIF())+1).comando():
                self.visit(c)
            self.indent -= 1

    # ---------------------------
    # while
    # ---------------------------
    def visitEnquanto(self, ctx):
        cond = self.visit(ctx.condicao())
        self.code.append(self.tab() + f"while {cond}:")
        self.indent += 1
        for c in ctx.comando():
            self.visit(c)
        self.indent -= 1

    # ---------------------------
    # for x in a..b
    # ---------------------------
    def visitLaco_para(self, ctx):
        var = ctx.ID().getText()
        start = self.visit(ctx.intervalo().expressao(0))
        end   = self.visit(ctx.intervalo().expressao(1))

        self.code.append(self.tab() + f"for {var} in range({start}, {end}):")
        self.indent += 1
        for c in ctx.comando():
            self.visit(c)
        self.indent -= 1

    # ---------------------------
    # expressões (tudo em cascata)
    # ---------------------------
    def visitExpressao(self, ctx):
        return self.visit(ctx.logico_baixo())

    def visitLogico_baixo(self, ctx):
        txt = self.visit(ctx.not_baixo())
        suf = self.visit(ctx.logico_baixo_suf())
        return txt + suf

    def visitLogico_baixo_suf(self, ctx):
        if ctx.getChildCount() == 0:
            return ""
        op = ctx.getChild(0).getText()
        right = self.visit(ctx.not_baixo())
        return f" {op} " + right + self.visit(ctx.logico_baixo_suf())

    def visitNot_baixo(self, ctx):
        if ctx.NOT():
            return "not " + self.visit(ctx.not_baixo())
        return self.visit(ctx.logico_alto())

    def visitLogico_alto(self, ctx):
        txt = self.visit(ctx.rel())
        suf = self.visit(ctx.logico_alto_suf())
        return txt + suf

    def visitLogico_alto_suf(self, ctx):
        if ctx.getChildCount() == 0:
            return ""
        op = ctx.getChild(0).getText()
        right = self.visit(ctx.rel())
        return f" {op} " + right + self.visit(ctx.logico_alto_suf())

    def visitRel(self, ctx):
        base = self.visit(ctx.soma(0))
        out = base
        for i in range(1, len(ctx.soma())):
            op = ctx.OP_REL(i-1).getText()
            right = self.visit(ctx.soma(i))
            out += f" {op} {right}"
        return out

    def visitSoma(self, ctx):
        base = self.visit(ctx.mult(0))
        out = base
        for i in range(1, len(ctx.mult())):
            op = ctx.OP_ADD(i-1).getText()
            right = self.visit(ctx.mult(i))
            out += f" {op} {right}"
        return out

    def visitMult(self, ctx):
        base = self.visit(ctx.unario(0))
        out = base
        for i in range(1, len(ctx.unario())):
            op = ctx.OP_MUL(i-1).getText()
            right = self.visit(ctx.unario(i))
            out += f" {op} {right}"
        return out

    def visitUnario(self, ctx):
        if ctx.OP_NOT():
            return "!" + self.visit(ctx.unario())
        if ctx.OP_ADD():
            return ctx.OP_ADD().getText() + self.visit(ctx.unario())
        return self.visit(ctx.primario())

    def visitPrimario(self, ctx):
        if ctx.NUM():
            return ctx.NUM().getText()
        if ctx.STRING():
            return ctx.STRING().getText()
        if ctx.ID():
            return ctx.ID().getText()
        return "(" + self.visit(ctx.expressao()) + ")"
