from manim import *

config.background_color = "#1E1E1E"
Text.set_default(font="Manrope")
MarkupText.set_default(font="Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

# Paleta (documento de padronização)
ROXO = "#AA77C7"
ROXO_ESCURO = "#8728BE"
AZUL = BLUE          # "#58C4DD"
AZUL_ESCURO = BLUE_E # "#236B8E"
MONO = "DejaVu Sans Mono"
ERRO = RED_C
CERTO = GREEN_C


def limpa(cena, **kwargs):
    if cena.mobjects:
        cena.play(FadeOut(*cena.mobjects), **kwargs)
    cena.clear()


# ---------------- FITA DE BITS ----------------
def celula(bit, lado=0.9, font_size=40, cor=WHITE):
    quadrado = Square(side_length=lado, stroke_color=WHITE, stroke_width=2)
    texto = Text(str(bit), font_size=font_size, color=cor).move_to(quadrado)
    cel = VGroup(quadrado, texto)
    cel.tamanho_fonte = font_size
    return cel


def fita(bits, lado=0.9, font_size=40):
    return VGroup(*[celula(b, lado, font_size) for b in bits]).arrange(RIGHT, buff=0)


def troca_bit(cel, bit, cor=WHITE):
    novo = Text(str(bit), font_size=cel.tamanho_fonte, color=cor).move_to(cel[0])
    return Transform(cel[1], novo)


def pesos(fita_mob, valores, font_size=30, cor=GRAY_B):
    return VGroup(*[Text(str(v), font_size=font_size, color=cor).next_to(c, UP, buff=0.2)
                    for c, v in zip(fita_mob, valores)])


def cartao_bonus():
    # Mesmo cartão usado na aula 6 para anunciar esta aula bônus
    card = RoundedRectangle(corner_radius=0.1, color=ROXO_ESCURO, stroke_color=ROXO, fill_opacity=0.1,
                            height=1.9, width=7.6)
    texto = VGroup(
        Text("Aula bônus 1", font_size=48, color=ROXO, weight=BOLD),
        Text("Complemento de dois", font_size=38),
    ).arrange(DOWN, buff=0.18).move_to(card)
    return VGroup(card, texto)


def bloco_cpu(texto, cor=GRAY_B, largura=2.4, altura=0.7, font_size=24):
    caixa = RoundedRectangle(corner_radius=0.1, width=largura, height=altura, stroke_color=cor,
                             fill_color=cor, fill_opacity=0.12, stroke_width=2)
    return VGroup(caixa, Text(texto, font_size=font_size, color=cor).move_to(caixa))


# ---------------- SOMA BINÁRIA EM COLUNAS ----------------
class SomaBinaria:
    """Monta a conta armada a + b (4 bits) com vai-uns e o bit que transborda fora da fita."""

    def __init__(self, a, b, rotulo_a="", rotulo_b="", lado=0.9, font_size=40):
        self.a, self.b = a, b
        self.fa = fita(a, lado, font_size)
        self.fb = fita(b, lado, font_size).next_to(self.fa, DOWN, buff=0.25)
        self.mais = Text("+", font_size=font_size).next_to(self.fb, LEFT, buff=0.35)
        self.linha = Line(LEFT, RIGHT, stroke_width=3).set(width=self.fa.width + 1.4)
        self.linha.next_to(self.fb, DOWN, buff=0.3).align_to(self.fb, RIGHT).shift(RIGHT * 0.2)
        self.fr = fita(" " * len(a), lado, font_size).next_to(self.linha, DOWN, buff=0.3).align_to(self.fa, LEFT)
        self.lado = lado
        self.vai_uns = VGroup()
        self.rotulos = VGroup()
        for fita_mob, rotulo in ((self.fa, rotulo_a), (self.fb, rotulo_b)):
            r = Text(rotulo, font_size=34, color=GRAY_B).next_to(fita_mob, RIGHT, buff=0.6)
            self.rotulos.add(r)
        self.transbordo = None

    def contas(self):
        return VGroup(self.fa, self.fb, self.mais, self.linha, self.fr, self.rotulos)

    def montar(self, cena):
        cena.play(FadeIn(self.fa), FadeIn(self.rotulos[0]))
        cena.play(FadeIn(self.fb), FadeIn(self.mais), FadeIn(self.rotulos[1]))
        cena.play(Create(self.linha), FadeIn(self.fr))

    def somar(self, cena, tempos=(1.2, 0.6, 0.6, 0.6), pausa_primeira=0):
        carry = 0
        n = len(self.a)
        for k, i in enumerate(range(n - 1, -1, -1)):
            total = int(self.a[i]) + int(self.b[i]) + carry
            bit, carry = total % 2, total // 2
            coluna = VGroup(self.fa[i], self.fb[i])
            destaque = SurroundingRectangle(VGroup(coluna, self.fr[i]), color=ROXO, buff=0.06, corner_radius=0.08)
            animacoes = [troca_bit(self.fr[i], bit)]
            if carry:
                vai_um = Text("1", font_size=30, color=ROXO)
                if i > 0:
                    vai_um.next_to(self.fa[i - 1], UP, buff=0.12)
                    self.vai_uns.add(vai_um)
                    animacoes.append(FadeIn(vai_um, shift=UP * 0.2))
                else:
                    # sai da fita: fica fora das células, à esquerda do resultado
                    # posição do bit que transborda: uma "célula" à esquerda do resultado, sem quadrado
                    vai_um = Text("1", font_size=self.fr[0].tamanho_fonte, color=ROXO)
                    vai_um.move_to(self.fr[0].get_center() + LEFT * self.lado)
                    self.transbordo = vai_um
                    animacoes.append(FadeIn(vai_um, shift=LEFT * 0.3))
            cena.play(Create(destaque), run_time=tempos[k] * 0.4)
            cena.play(*animacoes, run_time=tempos[k] * 0.6)
            if k == 0 and pausa_primeira:
                cena.wait(pausa_primeira)
            cena.play(FadeOut(destaque), run_time=0.2)

    def descartar(self, cena, legenda="descartado"):
        if self.transbordo is None:
            return
        texto = Text(legenda, font_size=24, color=GRAY_B).next_to(self.transbordo, LEFT, buff=0.3)
        self.transbordo.set_color(ERRO)
        cena.play(Indicate(self.transbordo, color=ERRO, scale_factor=1.4), FadeIn(texto))
        cena.wait(0.8)
        cena.play(self.transbordo.animate.shift(DOWN * 1.2).set_opacity(0), texto.animate.set_opacity(0), run_time=1)
        cena.remove(self.transbordo, texto)


# ======================================================================
class AulaCompleta(Scene):
    def construct(self):
        Abertura.construct(self)
        Resumo.construct(self)
        Pergunta.construct(self)
        SinalMagnitude.construct(self)
        SomaSinalMagnitude.construct(self)
        CircuitosComplexos.construct(self)
        Genialidade.construct(self)
        PesoNegativo.construct(self)
        CincoPositivo.construct(self)
        CincoNegativo.construct(self)
        Truque.construct(self)
        PorQueMelhor.construct(self)
        SeteMenosCinco.construct(self)
        CincoMenosCinco.construct(self)
        Vantagem.construct(self)
        Final.construct(self)
        Creditos.construct(self)


# ---------------- INTRO ----------------
class Abertura(Scene):
    def construct(self):
        # "A forma como os computadores armazenam números negativos é genial!"
        menos5 = Text("-5", font_size=144)
        self.play(Write(menos5))
        self.wait(0.5)
        binario = fita("1011", lado=1.1, font_size=56)
        binario[0][1].set_color(ROXO)
        self.play(ReplacementTransform(menos5, binario))
        self.play(Flash(binario, color=ROXO, line_length=0.4, flash_radius=binario.width / 2 + 0.4))
        self.wait(1)

        # "Usamos um truque chamado Complemento de Dois."
        cartao = cartao_bonus()
        self.play(binario.animate.scale(0.6).to_edge(UP, buff=1.2))
        self.play(Create(cartao[0]), FadeIn(cartao[1], shift=UP * 0.2))
        self.wait(1.5)
        limpa(self)


class Resumo(Scene):
    def construct(self):
        # "Funciona assim: pega seu número em binário,"
        cinco = Text("5", font_size=72).move_to(UP * 1.6)
        tira = fita("0101", lado=1.0, font_size=48)
        self.play(Write(cinco))
        self.play(TransformFromCopy(cinco, tira))
        self.wait(0.5)

        # "inverte todos os bits"
        passo1 = Text("inverte todos os bits", font_size=32, color=ROXO).next_to(tira, DOWN, buff=0.5)
        self.play(FadeIn(passo1, shift=UP * 0.2))
        self.play(LaggedStart(*[troca_bit(c, 1 - int(b), ROXO) for c, b in zip(tira, "0101")], lag_ratio=0.2))
        self.wait(0.5)

        # "e soma um."
        passo2 = Text("+ 1", font_size=40, color=ROXO).next_to(passo1, DOWN, buff=0.3)
        self.play(FadeIn(passo2, shift=UP * 0.2))
        self.play(troca_bit(tira[2], 1), troca_bit(tira[3], 1),
                  *[c[1].animate.set_color(WHITE) for c in tira[:2]])
        resultado = Text("-5", font_size=72, color=ROXO).move_to(cinco)
        self.play(Transform(cinco, resultado))
        self.wait(1)

        # "Só isso, você poderia fechar o vídeo agora."
        tudo = VGroup(cinco, tira, passo1, passo2)
        janela = RoundedRectangle(corner_radius=0.15, width=tudo.width + 1.4, height=tudo.height + 1.4,
                                  stroke_color=GRAY_B, stroke_width=2).move_to(tudo)
        botao = VGroup(Square(side_length=0.45, stroke_color=GRAY_B, stroke_width=2),
                       Cross(stroke_color=ERRO, stroke_width=4).scale(0.15))
        botao.move_to(janela.get_corner(UR) + DL * 0.4)
        self.play(Create(janela), FadeIn(botao))
        self.play(Indicate(botao, color=ERRO, scale_factor=1.4), run_time=1)
        self.wait(1.5)
        limpa(self)


class Pergunta(Scene):
    def construct(self):
        # "Então surge a dúvida: como representar números negativos?"
        pergunta = Text("Como representar\nnúmeros negativos?", font_size=52, line_spacing=0.9,
                        t2c={"negativos": ROXO}).move_to(UP * 1)
        self.play(Write(pergunta), run_time=1.5)
        menos5 = Text("-5  =", font_size=48)
        incognita = fita("????", lado=0.9, font_size=40)
        VGroup(menos5, incognita).arrange(RIGHT, buff=0.4).next_to(pergunta, DOWN, buff=0.8)
        self.play(FadeIn(menos5), LaggedStart(*[GrowFromEdge(c, UP) for c in incognita], lag_ratio=0.1))
        self.wait(2)
        limpa(self)


class SinalMagnitude(Scene):
    def construct(self):
        # "A ideia mais intuitiva seria usar o bit mais à esquerda apenas como uma bandeira de sinal:"
        tira = fita("0101", lado=1.0, font_size=48)
        valor = Text("= 5", font_size=56).next_to(tira, RIGHT, buff=0.5)
        VGroup(tira, valor).move_to(DOWN * 0.2)
        self.play(FadeIn(tira), FadeIn(valor))
        haste = Line(ORIGIN, UP * 0.9, stroke_width=4, color=ROXO)
        pano = Polygon(UP * 0.9, UP * 0.55, UP * 0.725 + RIGHT * 0.5, stroke_width=0,
                       fill_color=ROXO, fill_opacity=1)
        bandeira = VGroup(haste, pano).next_to(tira[0], UP, buff=0.15)
        rotulo = Text("sinal", font_size=28, color=ROXO).next_to(bandeira, LEFT, buff=0.15)
        self.play(tira[0][0].animate.set_stroke(ROXO, width=5), Create(haste), FadeIn(pano, shift=RIGHT * 0.2),
                  FadeIn(rotulo))
        self.wait(1)

        # "0 para positivo e 1 para negativo."
        regra = Text("0 = positivo   1 = negativo", font_size=32, t2c={"0": ROXO, "1": ROXO}).next_to(tira, DOWN, buff=0.7)
        self.play(FadeIn(regra))
        self.play(Indicate(tira[0][1]))
        self.play(troca_bit(tira[0], 1, ROXO), Transform(valor, Text("= -5", font_size=56).move_to(valor)))
        self.wait(1.5)

        # "Esse método existe (Sinal e Magnitude), parece simples, mas cria grandes problemas para o hardware."
        titulo = Text("Sinal e Magnitude", font_size=52).to_edge(UP, buff=0.8)
        self.play(Write(titulo))
        self.wait(1.5)
        problema = Text("problemas para o hardware", font_size=32, color=ERRO).move_to(regra)
        self.play(FadeTransform(regra, problema))
        self.play(Wiggle(problema))
        self.wait(1.5)
        limpa(self)


class SomaSinalMagnitude(Scene):
    def construct(self):
        # "Se você tentar somar 5 positivo, que é 0101, com 5 negativo, que seria 1101,"
        titulo = Text("Sinal e Magnitude", font_size=40, color=GRAY_B).to_edge(UP, buff=0.6)
        conta = SomaBinaria("0101", "1101", rotulo_a="5", rotulo_b="-5")
        conta.contas().move_to(DOWN * 0.3)
        conta.fb[0][1].set_color(ROXO)
        self.add(titulo)
        conta.montar(self)
        self.wait(1.5)

        # "um somador digital tradicional resulta em 10010,"
        conta.somar(self, tempos=(0.8, 0.8, 0.8, 0.8))
        self.wait(1.5)

        # "no caso, o último bit transbordaria, e ficaria 0010."
        conta.descartar(self, legenda="transborda")
        resultado = Text("= 2", font_size=40, color=ERRO).next_to(conta.fr, RIGHT, buff=0.6)
        self.play(Write(resultado))
        esperado = Text("5 + (-5) deveria ser 0", font_size=30, color=ERRO).next_to(conta.fr, DOWN, buff=0.5)
        risco = Line(resultado.get_left() + LEFT * 0.1, resultado.get_right() + RIGHT * 0.1, color=ERRO, stroke_width=5)
        self.play(FadeIn(esperado, shift=UP * 0.2), Create(risco))
        self.wait(2)
        limpa(self)


class CircuitosComplexos(Scene):
    def construct(self):
        # "Para fazer subtrações, a CPU precisaria checar o sinal de cada número, comparar e decidir
        #  se vai somar ou subtrair."
        cpu = RoundedRectangle(corner_radius=0.2, width=4.2, height=3.6, stroke_color=WHITE, stroke_width=3)
        nome = Text("CPU", font_size=32).next_to(cpu, UP, buff=0.15)
        self.play(Create(cpu), Write(nome))
        checar = bloco_cpu("checar sinais")
        comparar = bloco_cpu("comparar")
        somar = bloco_cpu("somar", cor=AZUL, largura=1.6)
        subtrair = bloco_cpu("subtrair", cor=ROXO, largura=1.6)
        ramos = VGroup(somar, subtrair).arrange(RIGHT, buff=0.3)
        fluxo = VGroup(checar, comparar, ramos).arrange(DOWN, buff=0.45).move_to(cpu)
        setas = VGroup(
            Arrow(checar.get_bottom(), comparar.get_top(), buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.3),
            Arrow(comparar.get_bottom(), somar.get_top(), buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.3),
            Arrow(comparar.get_bottom(), subtrair.get_top(), buff=0.05, stroke_width=3, max_tip_length_to_length_ratio=0.3),
        )
        self.play(FadeIn(checar, shift=DOWN * 0.2))
        self.wait(0.8)
        self.play(GrowArrow(setas[0]), FadeIn(comparar, shift=DOWN * 0.2))
        self.wait(0.8)
        self.play(GrowArrow(setas[1]), GrowArrow(setas[2]), FadeIn(ramos, shift=DOWN * 0.2))
        self.wait(1.5)

        # "Isso exigiria circuitos gigantescos, lentos e complexos dentro do processador."
        cpu_grande = RoundedRectangle(corner_radius=0.2, width=11, height=5.6, stroke_color=WHITE, stroke_width=3)
        cpu_grande.shift(DOWN * 0.4)
        circuito = VGroup(fluxo, setas)
        self.play(Transform(cpu, cpu_grande), nome.animate.next_to(cpu_grande, UP, buff=0.15),
                  circuito.animate.scale(0.75).move_to(cpu_grande.get_left() + RIGHT * 2.1))
        extras = VGroup(*[bloco_cpu(t, largura=1.9, altura=0.55, font_size=18) for t in
                          ("checar sinais", "comparar", "trocar ordem", "inverter sinal",
                           "somar", "subtrair", "ajustar sinal", "comparar", "checar sinais")])
        extras.arrange_in_grid(rows=3, cols=3, buff=(0.35, 0.4)).move_to(cpu_grande.get_center() + RIGHT * 1.6)
        self.play(LaggedStart(*[FadeIn(e, scale=0.6) for e in extras], lag_ratio=0.12), run_time=2)
        adjetivos = Text("gigantesco  ·  lento  ·  complexo", font_size=34, color=ERRO).next_to(cpu_grande, DOWN, buff=0.25)
        self.play(Write(adjetivos))
        self.wait(2.5)
        limpa(self)


# ---------------- COMPLEMENTO DE DOIS ----------------
class Genialidade(Scene):
    def construct(self):
        # "É aqui que entra a genialidade do Complemento de Dois."
        titulo = Text("Complemento de dois", font_size=72, color=ROXO, weight=BOLD)
        self.play(Write(titulo), run_time=1.5)
        self.play(Flash(titulo, color=ROXO, line_length=0.5, flash_radius=titulo.width / 2 + 0.3, num_lines=16))
        self.wait(1.5)
        limpa(self)


class PesoNegativo(Scene):
    def construct(self):
        # "Nós simplesmente mudamos a regra de contagem: o bit mais significativo passa a ter um peso negativo."
        tira = fita("    ", lado=1.1, font_size=48).move_to(DOWN * 0.3)
        self.fita_pesos = tira  # usada por CincoPositivo e CincoNegativo
        self.play(LaggedStart(*[GrowFromEdge(c, UP) for c in tira], lag_ratio=0.1))
        msb = Text("bit mais significativo", font_size=28, color=ROXO).next_to(tira[0], DOWN, buff=0.4)
        self.play(tira[0][0].animate.set_stroke(ROXO, width=5), FadeIn(msb, shift=UP * 0.2))
        self.wait(3)

        # "Em um sistema de 4 bits, onde os pesos tradicionais do binário são 8, 4, 2 e 1,"
        chave = Brace(tira, DOWN, buff=0.15)
        quatro = Text("4 bits", font_size=30).next_to(chave, DOWN, buff=0.1)
        self.play(FadeOut(msb), GrowFromCenter(chave), FadeIn(quatro))
        linha_pesos = pesos(tira, [8, 4, 2, 1], font_size=40, cor=WHITE)
        rotulo = Text("pesos:", font_size=30, color=GRAY_B).next_to(linha_pesos, LEFT, buff=0.6)
        self.play(FadeIn(rotulo), LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in linha_pesos], lag_ratio=0.25))
        self.wait(3)

        # "no Complemento de Dois os pesos passam a ser -8, 4, 2 e 1."
        menos8 = Text("-8", font_size=40, color=ROXO).move_to(linha_pesos[0])
        self.play(Transform(linha_pesos[0], menos8))
        self.play(Circumscribe(linha_pesos[0], color=ROXO, buff=0.1))
        nota = Text("peso negativo", font_size=28, color=ROXO).next_to(linha_pesos[0], UP, buff=0.3)
        self.play(FadeIn(nota, shift=DOWN * 0.2))
        self.wait(4.5)
        self.play(FadeOut(VGroup(chave, quatro, nota)), tira[0][0].animate.set_stroke(WHITE, width=2))


class CincoPositivo(Scene):
    def construct(self):
        # Continua da cena anterior: fita vazia com os pesos -8, 4, 2, 1
        if not hasattr(self, "fita_pesos"):
            self.fita_pesos = fita("    ", lado=1.1, font_size=48).move_to(DOWN * 0.3)
            linha_pesos = pesos(self.fita_pesos, ["-8", 4, 2, 1], font_size=40, cor=WHITE)
            linha_pesos[0].set_color(ROXO)
            rotulo = Text("pesos:", font_size=30, color=GRAY_B).next_to(linha_pesos, LEFT, buff=0.6)
            self.add(self.fita_pesos, linha_pesos, rotulo)
        tira = self.fita_pesos

        # "Veja como funciona na prática. O número 5 positivo continua sendo 0101:"
        titulo = Text("5", font_size=60).to_edge(UP, buff=0.7)
        self.play(Write(titulo))
        self.play(LaggedStart(*[troca_bit(c, b) for c, b in zip(tira, "0101")], lag_ratio=0.15))
        self.wait(1)

        # "zero vezes -8, mais 4, mais 0, mais 1. Total: 5."
        termos = ["0 × (-8)", "+ 4", "+ 0", "+ 1", "= 5"]
        conta = VGroup(*[Text(t, font_size=36) for t in termos]).arrange(RIGHT, buff=0.25)
        conta.next_to(tira, DOWN, buff=0.8)
        conta[-1].set_color(ROXO)
        for i, termo in enumerate(conta[:4]):
            self.play(Indicate(tira[i]), FadeIn(termo, shift=UP * 0.15), run_time=0.8)
            self.wait(0.3)
        self.play(Write(conta[-1]))
        self.wait(1.5)
        self.play(FadeOut(conta), FadeOut(titulo))


class CincoNegativo(Scene):
    def construct(self):
        if not hasattr(self, "fita_pesos"):
            self.fita_pesos = fita("0101", lado=1.1, font_size=48).move_to(DOWN * 0.3)
            linha_pesos = pesos(self.fita_pesos, ["-8", 4, 2, 1], font_size=40, cor=WHITE)
            linha_pesos[0].set_color(ROXO)
            rotulo = Text("pesos:", font_size=30, color=GRAY_B).next_to(linha_pesos, LEFT, buff=0.6)
            self.add(self.fita_pesos, linha_pesos, rotulo)
        tira = self.fita_pesos

        # "Agora, como representamos o -5?"
        titulo = Text("-5", font_size=60, color=ROXO).to_edge(UP, buff=0.7)
        self.play(Write(titulo), *[troca_bit(c, 0) for c in tira])
        self.wait(1.5)

        # "Basta ligar o bit de menos 8 e somar o necessário para chegar a -5."
        conta = VGroup(*[Text(t, font_size=40) for t in ("-8", "+ 2", "+ 1", "= -5")]).arrange(RIGHT, buff=0.3)
        conta.next_to(tira, DOWN, buff=0.8)
        conta[-1].set_color(ROXO)
        self.play(troca_bit(tira[0], 1, ROXO), FadeIn(conta[0], shift=UP * 0.15))
        self.wait(1.5)

        # "Ou seja: -8 + 2 + 1."
        self.play(troca_bit(tira[2], 1), FadeIn(conta[1], shift=UP * 0.15))
        self.play(troca_bit(tira[3], 1), FadeIn(conta[2], shift=UP * 0.15))
        self.play(Write(conta[3]))
        self.wait(1)

        # "Em binário: 1011."
        binario = Text("1011", font_size=48, color=ROXO).next_to(conta, DOWN, buff=0.5)
        self.play(TransformFromCopy(tira, binario))
        self.wait(2)
        limpa(self)


class Truque(Scene):
    def construct(self):
        # "Existe também um truque prático para encontrar esse código: pegue o 5 positivo (0101),"
        titulo = Text("Truque", font_size=48, color=ROXO).to_edge(UP, buff=0.7)
        self.play(Write(titulo))
        conta = SomaBinaria("0101", "0001", rotulo_a="5", rotulo_b="")
        conta.contas().move_to(DOWN * 0.4)
        self.play(FadeIn(conta.fa), FadeIn(conta.rotulos[0]))
        self.wait(1.5)

        # "inverta todos os bits — obtendo 1010 —"
        inverter = Text("inverter", font_size=30, color=ROXO).next_to(conta.fa, RIGHT, buff=0.6)
        self.play(FadeTransform(conta.rotulos[0], inverter))
        self.play(LaggedStart(*[troca_bit(c, 1 - int(b), ROXO) for c, b in zip(conta.fa, "0101")], lag_ratio=0.2))
        conta.a = "1010"
        self.wait(1.5)

        # "e some 1."
        mais_um = Text("+ 1", font_size=30, color=ROXO).next_to(conta.fb, RIGHT, buff=0.6)
        self.play(FadeIn(conta.fb), FadeIn(conta.mais), FadeIn(mais_um), *[c[1].animate.set_color(WHITE) for c in conta.fa])
        self.play(Create(conta.linha), FadeIn(conta.fr))
        conta.somar(self, tempos=(0.6, 0.6, 0.6, 0.6))

        # "O resultado é 1011, exatamente o nosso menos 5."
        resultado = Text("= -5", font_size=40, color=ROXO).next_to(conta.fr, RIGHT, buff=0.6)
        self.play(Write(resultado))
        self.play(Circumscribe(VGroup(conta.fr, resultado), color=ROXO, buff=0.15))
        self.wait(2)
        limpa(self)


class PorQueMelhor(Scene):
    def construct(self):
        # "Mas por que essa estrutura seria melhor?"
        pergunta = Text("Por que isso é melhor?", font_size=60, t2c={"melhor": ROXO})
        self.play(Write(pergunta))
        self.wait(1.5)
        limpa(self)


class SeteMenosCinco(Scene):
    def construct(self):
        # "Vamos calcular 7 menos 5, que é o mesmo que somar 7 com menos 5."
        subtracao = Text("7 - 5", font_size=72)
        self.play(Write(subtracao))
        self.wait(2)
        soma = Text("7 + (-5)", font_size=72, t2c={"(-5)": ROXO})
        self.play(TransformMatchingShapes(subtracao, soma))
        self.wait(1.5)
        self.play(soma.animate.scale(0.6).to_edge(UP, buff=0.6))

        # "O número 7 é 0111. O número menos 5 é 1011."
        conta = SomaBinaria("0111", "1011", rotulo_a="7", rotulo_b="-5")
        conta.contas().move_to(DOWN * 0.4)
        conta.montar(self)
        self.wait(3)

        # "Somando bit a bit, exatamente como uma adição normal: 1 mais 1 dá 0 e sobe 1, e assim por diante."
        conta.somar(self, tempos=(1.6, 0.8, 0.8, 0.8), pausa_primeira=2)

        # "A soma binária resulta em 10010."
        self.wait(2.5)

        # "Como nosso registrador só guarda 4 bits, o quinto bit à esquerda simplesmente transborda e é
        #  descartado pelo hardware."
        chave = Brace(conta.fr, DOWN, buff=0.15, color=AZUL)
        registrador = Text("registrador: 4 bits", font_size=26, color=AZUL).next_to(chave, DOWN, buff=0.1)
        self.play(GrowFromCenter(chave), FadeIn(registrador))
        self.wait(1)
        conta.descartar(self)
        self.wait(1.5)

        # "O que sobra nos 4 bits restantes é exatamente o número 2."
        resultado = Text("= 2", font_size=40, color=CERTO).next_to(conta.fr, RIGHT, buff=0.6)
        self.play(Write(resultado))
        self.play(Circumscribe(VGroup(conta.fr, resultado), color=CERTO, buff=0.15))
        self.wait(3)
        limpa(self)


class CincoMenosCinco(Scene):
    def construct(self):
        # "E se somarmos 5 com menos 5?"
        titulo = Text("5 + (-5)", font_size=44, t2c={"(-5)": ROXO}).to_edge(UP, buff=0.6)
        self.play(Write(titulo))
        conta = SomaBinaria("0101", "1011", rotulo_a="5", rotulo_b="-5")
        conta.contas().move_to(DOWN * 0.4)
        conta.montar(self)
        self.wait(0.5)

        # "0101 mais 1011 resulta em 10000."
        conta.somar(self, tempos=(0.7, 0.7, 0.7, 0.7))
        self.wait(1)

        # "Descartando o bit que transbordou, o resultado que fica no registrador é 0000. Zero."
        conta.descartar(self)
        resultado = Text("= 0", font_size=40, color=CERTO).next_to(conta.fr, RIGHT, buff=0.6)
        self.play(Write(resultado))
        comparacao = Text("(no Sinal e Magnitude, dava 2)", font_size=24, color=GRAY_B).next_to(conta.fr, DOWN, buff=0.5)
        self.play(Circumscribe(VGroup(conta.fr, resultado), color=CERTO, buff=0.15), FadeIn(comparacao))
        self.wait(2)
        limpa(self)


class Vantagem(Scene):
    def construct(self):
        # "A grande vantagem do complemento de dois é transformar qualquer subtração em uma adição comum,"
        regra = Text("a - b", font_size=72)
        self.play(Write(regra))
        self.wait(0.8)
        nova = Text("a + (-b)", font_size=72, t2c={"(-b)": ROXO})
        self.play(TransformMatchingShapes(regra, nova))
        self.wait(1.5)
        self.play(nova.animate.scale(0.6).to_edge(UP, buff=0.6))

        # "assim, a CPU não precisa de circuitos separados só para essa operação:"
        antes = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.2, stroke_color=GRAY_C, stroke_width=2)
        blocos_antes = VGroup(*[bloco_cpu(t, largura=1.8, altura=0.5, font_size=16) for t in
                                ("checar sinais", "comparar", "somar", "subtrair", "ajustar sinal", "trocar ordem")])
        blocos_antes.arrange_in_grid(rows=3, cols=2, buff=(0.3, 0.3)).move_to(antes)
        grupo_antes = VGroup(antes, blocos_antes, Text("Sinal e Magnitude", font_size=24, color=GRAY_B).next_to(antes, UP, buff=0.15))
        depois = RoundedRectangle(corner_radius=0.2, width=4.6, height=3.2, stroke_color=WHITE, stroke_width=3)
        somador = bloco_cpu("somador", cor=AZUL, largura=2.2, altura=0.9, font_size=30).move_to(depois)
        grupo_depois = VGroup(depois, somador, Text("Complemento de dois", font_size=24, color=ROXO).next_to(depois, UP, buff=0.15))
        VGroup(grupo_antes, grupo_depois).arrange(RIGHT, buff=1.2).shift(DOWN * 0.5)
        self.play(FadeIn(grupo_antes))
        self.wait(1)
        self.play(Create(Cross(antes, stroke_color=ERRO, stroke_width=5)), grupo_antes.animate.set_opacity(0.4))
        self.wait(1)

        # "reutilizamos o circuito pequeno e super veloz de adição para subtração."
        self.play(Create(depois), FadeIn(grupo_depois[2]))
        self.play(GrowFromCenter(somador))
        operacoes = VGroup(Text("+", font_size=56, color=AZUL), Text("−", font_size=56, color=ROXO))
        operacoes.arrange(RIGHT, buff=1.6).next_to(somador, DOWN, buff=0.6)
        setas = VGroup(*[Arrow(op.get_top(), somador.get_bottom(), buff=0.1, stroke_width=3,
                               max_tip_length_to_length_ratio=0.25, color=op.get_color()) for op in operacoes])
        self.play(FadeIn(operacoes), GrowArrow(setas[0]), GrowArrow(setas[1]))
        self.play(Indicate(somador, color=AZUL, scale_factor=1.15))
        self.wait(2.5)
        limpa(self)


# ---------------- FINAL ----------------
class Final(Scene):
    def construct(self):
        # "Genial, né?"
        genial = Text("Genial, né?", font_size=80, t2c={"Genial": ROXO})
        self.play(Write(genial))
        self.wait(1.5)
        self.play(FadeOut(genial))

        logo = ImageMobject("assets/icon_c.png").scale(0.2)
        logoOrigin = logo.copy().move_to(UP * 8).rotate(PI)
        # O cursor
        cursorVinheta = ImageMobject("assets/cursor.png").move_to(DOWN * 6 + LEFT * 2).scale(0.05)

        self.play(
            logoOrigin.animate.become(logo),
            run_time=2
        )

        # Cursor aparece e se move
        self.play(cursorVinheta.animate.move_to(ORIGIN + RIGHT * 0.25 + DOWN * 0.45))
        self.play(cursorVinheta.animate.scale(0.8), run_time=0.1, rate_func=linear)  # Clica
        self.play(cursorVinheta.animate.scale(1.2), run_time=0.1, rate_func=linear)  #

        # Vinheta Puxada
        self.play(
            GrowFromCenter(Rectangle(color="#0A0A0A", fill_opacity=1, width=20, height=10), run_time=0.5)
        )
        self.clear()


class Creditos(Scene):
    def construct(self):
        fundo = Rectangle(color="#0A0A0A", fill_opacity=1, width=20, height=10)
        self.add(fundo)
        titulo = Text("Créditos", font_size=80, color=ROXO)

        def bloco(cargo, *nomes):
            return VGroup(Text(cargo, color=ROXO, font_size=60),
                          *[Text(n, font_size=50) for n in nomes]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        creditos = VGroup(
            bloco("Diretor", "Rainier R. Waki"),
            bloco("Tutor", "Alyson V. Isaluski"),
            bloco("Redator", "Eduardo M. de Souza"),
            bloco("Animadores", "Natália S. Kikuti", "Gabriel Covalski"),
        ).scale(0.6).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.8)
        creditos2 = VGroup(
            bloco("Editora", "Sophia B. Peraza"),
            bloco("Roteiristas", "Alyson V. Isaluski", "Kia de P. Marins"),
        ).scale(0.6).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=0.8)
        titulo.scale(0.6).to_edge(UP, buff=0.5).to_edge(RIGHT, buff=1)
        utfpr = ImageMobject("assets/utfpr.png").scale(0.4).to_corner(DR, buff=0.6)

        self.play(Write(titulo), FadeIn(utfpr))
        self.play(Write(creditos))
        self.wait(2)
        self.play(FadeOut(creditos))
        self.play(Write(creditos2))
        self.wait(2)
        self.play(FadeOut(creditos2), FadeOut(utfpr), FadeOut(titulo))
