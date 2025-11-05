# Puby – Compilador da Linguagem Puby (v0.1)

O **Puby** é um compilador educacional desenvolvido como projeto acadêmico para estudo dos princípios de construção de compiladores.  
A linguagem **Puby** foi inspirada em **Ruby e Perl**, buscando fornecer uma sintaxe simples, expressiva e acessível para fins didáticos.

Este projeto tem como objetivo aplicar na prática os conhecimentos de **Análise Léxica, Sintática, Semântica, Geração de Código Intermediário e Backend**, seguindo o pipeline real de um compilador moderno.

---

## 📌 Objetivos do Projeto

- Construir um compilador completo, modular e evolutivo para a linguagem Puby.
- Demonstrar, de forma prática, as etapas que compõem um compilador.
- Utilizar ferramentas profissionais, como **ANTLR4** (gerador de analisadores).
- Servir como referência acadêmica para estudantes de compiladores e linguagens formais.

---

## 🧠 Versão Atual: v0.1

Nesta versão, o compilador já possui:

| Etapa | Status | Descrição |
|--------|----------|------------------------|
| Análise Léxica | ✅ Concluída | Tokenização do código-fonte, detecção de símbolos e erros léxicos |
| Análise Sintática | ✅ Concluída | Validação estrutural e geração da AST |
| Análise Semântica | ⏳ Não iniciada | Regras semânticas da linguagem |
| TAC (Three Address Code) | 🚧 Futuro | Geração de código intermediário |
| Backend LLVM | 🚧 Futuro | Compilação para código nativo |

---

## 🧰 Tecnologias Utilizadas

- **Python 3**
- **ANTLR4** (para geração de analisadores)
- **Graphviz / DOT** (para visualização da AST)
- **VS Code** como ambiente de desenvolvimento

---

📂 Exemplos Usados

Os exemplos utilizados neste projeto foram class_triangulo.puby e pascal.puby.
O arquivo class_triangulo.puby realiza a validação de triângulos, verificando se os lados informados formam um triângulo válido e classificando-o de acordo com seus lados.
Já o arquivo pascal.puby gera o Triângulo de Pascal, exibindo as primeiras n linhas conforme o valor informado pelo usuário.

