# Generated from Puby.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PubyParser import PubyParser
else:
    from PubyParser import PubyParser

# This class defines a complete generic visitor for a parse tree produced by PubyParser.

class PubyVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PubyParser#programa.
    def visitPrograma(self, ctx:PubyParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#comando.
    def visitComando(self, ctx:PubyParser.ComandoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#escrita.
    def visitEscrita(self, ctx:PubyParser.EscritaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#leitura.
    def visitLeitura(self, ctx:PubyParser.LeituraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#atribuicao.
    def visitAtribuicao(self, ctx:PubyParser.AtribuicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#condicional.
    def visitCondicional(self, ctx:PubyParser.CondicionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#corpo_if.
    def visitCorpo_if(self, ctx:PubyParser.Corpo_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#enquanto.
    def visitEnquanto(self, ctx:PubyParser.EnquantoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#laco_para.
    def visitLaco_para(self, ctx:PubyParser.Laco_paraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#intervalo.
    def visitIntervalo(self, ctx:PubyParser.IntervaloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#incremento.
    def visitIncremento(self, ctx:PubyParser.IncrementoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#condicao.
    def visitCondicao(self, ctx:PubyParser.CondicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#expressao.
    def visitExpressao(self, ctx:PubyParser.ExpressaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#logico_baixo.
    def visitLogico_baixo(self, ctx:PubyParser.Logico_baixoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#logico_baixo_suf.
    def visitLogico_baixo_suf(self, ctx:PubyParser.Logico_baixo_sufContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#not_baixo.
    def visitNot_baixo(self, ctx:PubyParser.Not_baixoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#logico_alto.
    def visitLogico_alto(self, ctx:PubyParser.Logico_altoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#logico_alto_suf.
    def visitLogico_alto_suf(self, ctx:PubyParser.Logico_alto_sufContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#rel.
    def visitRel(self, ctx:PubyParser.RelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#soma.
    def visitSoma(self, ctx:PubyParser.SomaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#mult.
    def visitMult(self, ctx:PubyParser.MultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#unario.
    def visitUnario(self, ctx:PubyParser.UnarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PubyParser#primario.
    def visitPrimario(self, ctx:PubyParser.PrimarioContext):
        return self.visitChildren(ctx)



del PubyParser