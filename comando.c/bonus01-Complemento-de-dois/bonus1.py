
from manim import *
import random
import numpy as np
import struct

config.background_color = "#1E1E1E"
MarkupText.set_default(font = "Manrope")
Text.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")


class AulaCompleta(Scene):
    def construct(self):

        Inicio.construct(self)
        ComplementoDeDois.construct(self)
        Duvida.construct(self)
        BandeiraDeSinal.construct(self)
        SinalEMagnitude.construct(self)
        SomaPositivoNegativo.construct(self)
        SubtracoesNaCPU.construct(self)
        PesoNegativo.construct(self)
        Truque.construct(self)
        SeteMenosCinco.construct(self)
        CincoMenosCinco.construct(self)
        GrandeVantagem.construct(self)


class Inicio(Scene):
    def construct(self):

        computador = SVGMobject("assets/Computador.svg")
        computador.set_color(WHITE)
        computador.scale(3)

        negativos = Table(
            [["-1,", "-2,", "-3,"],
             ["-4,", "-5,", "-6,"],
             ["-7,", "-8,", "-9..."]],
             line_config={"stroke_width":0},
            v_buff=0.3,
            h_buff=0.3,)
        negativos.scale(0.7)
        negativos.move_to([-0.9, 1.3, 0])

        self.play(Write(computador), run_time=1.5)
        self.play(Create(negativos), run_time=1.3)
        self.play(FadeOut(computador),
                  FadeOut(negativos), run_time=0.8)
        self.wait()


class ComplementoDeDois(Scene):
    def construct(self):

        complemento_de_dois = Text("Complemento de Dois", weight=BOLD, font_size=80).scale(0.8)

        janela_fundo = RoundedRectangle(corner_radius=0.5, color=WHITE, stroke_color=WHITE, fill_opacity=1, height=5.0,
                         width=8.0)
        janela_fundo.scale(1.5)

        video = RoundedRectangle(corner_radius=0.5, color="#1E1E1E", stroke_color="#1E1E1E", fill_opacity=1, height=5.0,
                                  width=8.0)
        video.move_to([-1.5, 0.8, 0])

        video_lado1 = RoundedRectangle(corner_radius=0.5, color="#1E1E1E", stroke_color="#1E1E1E", fill_opacity=0.6, height=5.0,
                                 width=8.0)
        video_lado1.scale(0.35)
        video_lado1.move_to([4.25, 2.3, 0])

        video_lado2 = RoundedRectangle(corner_radius=0.5, color="#1E1E1E", stroke_color="#1E1E1E", fill_opacity=0.6,
                                       height=5.0,
                                       width=8.0)
        video_lado2.scale(0.35)
        video_lado2.move_to([4.25, 0.3, 0])

        video_lado3 = RoundedRectangle(corner_radius=0.5, color="#1E1E1E", stroke_color="#1E1E1E", fill_opacity=0.6,
                                       height=5.0,
                                       width=8.0)
        video_lado3.scale(0.35)
        video_lado3.move_to([4.25, -1.7, 0])

        videos_lado = VGroup(video_lado1, video_lado2, video_lado3)
        videos_lado.move_to([4.25, -0.1, 0])

        linha1 = Line(start=[-5.4, -2.2, 0], end=[0.5, -2.2, 0], color="#1E1E1E", stroke_width=12)
        linha1.set_opacity(0.8)

        linha2 = Line(start=[-5.4, -2.7, 0], end=[-1, -2.7, 0], color="#1E1E1E", stroke_width=10)
        linha2.set_opacity(0.5)

        linha3 = Line(start=[-5.4, -3, 0], end=[-1, -3, 0], color="#1E1E1E", stroke_width=10)
        linha3.set_opacity(0.5)

        linha4 = Line(start=[-5.4, -3.3, 0], end=[-1, -3.3, 0], color="#1E1E1E", stroke_width=10)
        linha4.set_opacity(0.5)

        linhas = VGroup(linha1, linha2, linha3, linha4)

        x = Text('X', color="#1E1E1E")
        x.scale(0.5)
        x.move_to([5.5, 3.3, 0])

        bits = ["0", "1", "0", "1"]

        bits_novos = ["1", "0", "1", "0"]

        caixas = VGroup()
        for i in range(len(bits)):
            quadrado = Square(color=WHITE)
            texto = Text(bits[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas.add(dupla)
        caixas.arrange(RIGHT, buff=0)
        caixas.move_to(video.get_center())
        caixas.scale(0.8)

        seta = Triangle(color=YELLOW, fill_opacity=0.5)
        seta.scale(0.3)
        seta.next_to(caixas[0][0], DOWN)

        texto_novo0 = Text(bits_novos[0]).move_to(caixas[0].get_center())
        texto_novo0.scale(1.2)

        texto_novo1 = Text(bits_novos[1]).move_to(caixas[1].get_center())
        texto_novo1.scale(1.2)

        texto_novo2 = Text(bits_novos[2]).move_to(caixas[2].get_center())
        texto_novo2.scale(1.2)

        texto_novo3 = Text(bits_novos[3]).move_to(caixas[3].get_center())
        texto_novo3.scale(1.2)

        texto_novo4 = Text('1', color="#AA77C7").move_to(caixas[3].get_center())
        texto_novo4.scale(1.2)

        mais_um = Text('+1', color=YELLOW)
        mais_um.next_to(caixas[3][0], UP)

        janela_completa = VGroup(janela_fundo, video, caixas, videos_lado, linhas, x)

        cursor = SVGMobject("assets/cursor.svg", fill_color=WHITE, stroke_color=BLACK, stroke_width=2)
        cursor.scale(0.5)
        cursor.move_to(RIGHT * 8)


        self.play(Write(complemento_de_dois))
        self.wait(0.5)
        self.play(FadeOut(complemento_de_dois))
        self.play(GrowFromCenter(janela_completa))
        self.wait()
        self.play(FadeIn(seta),
                  FadeTransform(caixas[0][1], texto_novo0), run_time=0.7)
        caixas[0].remove(caixas[0][1])
        caixas[0].add(texto_novo0)
        self.play(seta.animate.next_to(caixas[1][0], DOWN),
                  FadeTransform(caixas[1][1], texto_novo1), run_time=0.7)
        caixas[1].remove(caixas[1][1])
        caixas[1].add(texto_novo1)
        self.play(seta.animate.next_to(caixas[2][0], DOWN),
                  FadeTransform(caixas[2][1], texto_novo2), run_time=0.7)
        caixas[2].remove(caixas[2][1])
        caixas[2].add(texto_novo2)
        self.play(seta.animate.next_to(caixas[3][0], DOWN),
                  FadeTransform(caixas[3][1], texto_novo3), run_time=0.7)
        caixas[3].remove(caixas[3][1])
        caixas[3].add(texto_novo3)
        self.play(FadeOut(seta), run_time=0.7)
        self.play(FadeIn(mais_um), run_time=0.8)
        self.play(FadeOut(mais_um),
                  FadeTransform(texto_novo3, texto_novo4), run_time=0.8)
        caixas[3].remove(texto_novo3)
        caixas[3].add(texto_novo4)
        self.play(cursor.animate.move_to([5.8, 2.8, 0]))
        self.play(cursor.animate.scale(0.8), run_time=0.25)
        self.play(ShrinkToCenter(janela_completa),
                  cursor.animate.scale(1.2), run_time=0.35)
        self.wait(0.4)
        self.play(cursor.animate.move_to(RIGHT * 10))
        self.wait()


class Duvida(Scene):
    def construct(self):

        duvida = Text('Como representar\n números negativos?', t2c={'negativos':"#AA77C7"})
        duvida.scale(1.5)

        self.play(Write(duvida), run_time=0.9)
        self.play(FadeOut(duvida), run_time=0.9)
        self.wait()


class BandeiraDeSinal(Scene):
    def construct(self):

        bits = ['1', '0', '1','1']

        caixas = VGroup()
        for i in range(len(bits)):
            quadrado = Square(color=WHITE)
            texto = Text(bits[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas.add(dupla)
        caixas.arrange(RIGHT, buff=0)

        caixas[0][0].set_color("#AA77C7")

        bandeira = SVGMobject("assets/bandeira.svg")
        bandeira.set_color("#AA77C7")
        bandeira.scale(0.6)
        bandeira.next_to([-4.2, 1.7, 0])

        bit0 = Text('0').move_to(caixas[0].get_center())
        bit0.scale(1.6)

        positivo = Text('Positivo', color=YELLOW)
        positivo.next_to(caixas[0][0], DOWN)
        positivo.scale(0.9)

        negativo = Text('Negativo', color=YELLOW)
        negativo.next_to(caixas[0][0], DOWN)
        negativo.scale(0.9)

        self.play(FadeIn(caixas))
        self.play(caixas[0][0].animate.set_fill(color=WHITE, opacity=0.7), run_time=0.25)
        self.play(caixas[0][0].animate.set_fill(opacity=0), run_time=0.25)
        self.wait()
        self.play(FadeTransform(caixas[0][1], bit0),
                  Write(bandeira),
                  Write(positivo))
        self.wait(1.5)
        self.play(FadeTransform(bit0, caixas[0][1]),
                  Transform(positivo, negativo))
        self.wait()
        self.play(FadeOut(positivo),
                  FadeOut(bandeira))
        self.play(FadeOut(caixas))
        self.wait()


class SinalEMagnitude(Scene):
    def construct(self):

        sinal_e_magnitude = Text('Sinal e Magnitude', color="#AA77C7")
        sinal_e_magnitude.scale(1.8)

        circuito = SVGMobject("assets/CPU_nova.svg")
        circuito.set_color(WHITE)
        circuito.scale(1.8)
        circuito.move_to([0, -1, 0])

        self.play(Write(sinal_e_magnitude))
        self.wait()
        self.play(sinal_e_magnitude.animate.move_to([0, 2, 0]))
        self.play(FadeIn(circuito))
        self.wait()
        self.play(FadeOut(sinal_e_magnitude),
                  FadeOut(circuito))
        self.wait()


class SomaPositivoNegativo(Scene):
    def construct(self):

        bits1 = ['0', '1', '0', '1']

        caixas1 = VGroup()
        for i in range(len(bits1)):
            quadrado = Square(color=WHITE)
            texto = Text(bits1[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas1.add(dupla)
        caixas1.arrange(RIGHT, buff=0)

        bits2 = ['1', '1', '0', '1']

        caixas2 = VGroup()
        for i in range(len(bits2)):
            quadrado = Square(color=WHITE)
            texto = Text(bits2[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas2.add(dupla)
        caixas2.arrange(RIGHT, buff=0)
        caixas2.move_to([0, 0, 0])
        caixas2.scale(0.65)

        sinal_de_mais = Text('+', color=WHITE)
        sinal_de_mais.move_to([-3, 0, 0])

        linha = Line(start=[-2.8, -1, 0], end=[2.8, -1, 0], color=WHITE)

        bits3 = ['1', '0', '0', '1', '0']

        caixas3 = VGroup()
        for i in range(len(bits3)):
            quadrado = Square(color=WHITE)
            texto = Text(bits3[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas3.add(dupla)
        caixas3.arrange(RIGHT, buff=0)
        caixas3.move_to([-0.6, -2, 0])
        caixas3.scale(0.65)

        caixas3[0][0].set_opacity(0)

        bits4 = ['0', '0', '1', '0']

        caixas4 = VGroup()
        for i in range(len(bits4)):
            quadrado = Square(color=WHITE)
            texto = Text(bits4[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas4.add(dupla)
        caixas4.arrange(RIGHT, buff=0)
        caixas4.move_to([0, -2, 0])
        caixas4.scale(0.65)

        mais_um = Text('+1', color=YELLOW)
        mais_um.scale(0.5)
        mais_um.move_to([0.6, 2.9, 0])

        self.play(FadeIn(caixas1))
        self.wait()
        self.play(caixas1.animate.move_to([0, 1.9, 0]).scale(0.65))
        self.play(FadeIn(caixas2),
                  Write(sinal_de_mais),
                  Write(linha))
        self.wait()
        self.play(FadeIn(caixas3[4]))
        self.play(FadeIn(mais_um))
        self.play(FadeOut(mais_um),
                  FadeIn(caixas3[3]))
        mais_um.move_to([-2, 2.9, 0])
        self.wait(0.2)
        self.play(FadeIn(caixas3[2]))
        self.play(FadeIn(mais_um))
        self.play(FadeOut(mais_um),
                  FadeIn(caixas3[1]))
        self.wait(0.2)
        self.play(FadeIn(caixas3[0]))
        self.wait(0.5)
        self.play(Transform(caixas3, caixas4))
        self.wait()
        self.remove(caixas3)
        self.play(FadeOut(caixas1),
                  FadeOut(caixas2),
                  FadeOut(sinal_de_mais),
                  FadeOut(linha),
                  FadeOut(caixas4))
        self.wait()


class SubtracoesNaCPU (Scene):
    def construct(self):

        bits1 = ['0', '1', '0', '1']

        caixas1 = VGroup()
        for i in range(len(bits1)):
            quadrado = Square(color=WHITE)
            texto = Text(bits1[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas1.add(dupla)
        caixas1.arrange(RIGHT, buff=0)
        caixas1.move_to([-2, 3, 0])
        caixas1.scale(0.4)

        contorno1 = SurroundingRectangle(caixas1, color=YELLOW, buff=0, stroke_width=6)

        bits2 = ['0', '0', '1', '1']

        caixas2 = VGroup()
        for i in range(len(bits2)):
            quadrado = Square(color=WHITE)
            texto = Text(bits2[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas2.add(dupla)
        caixas2.arrange(RIGHT, buff=0)
        caixas2.move_to([-2, 2, 0])
        caixas2.scale(0.4)

        contorno2 = SurroundingRectangle(caixas2, color=YELLOW, buff=0, stroke_width=6)

        grupo1 = VGroup(caixas1, caixas2)
        chaves1 = Brace(grupo1, direction=RIGHT, color=YELLOW)

        texto_chaves1 = Text('Subtrair')
        texto_chaves1.next_to(chaves1, RIGHT)

        bits3 = ['0', '1', '0', '0']

        caixas3 = VGroup()
        for i in range(len(bits3)):
            quadrado = Square(color=WHITE)
            texto = Text(bits3[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas3.add(dupla)
        caixas3.arrange(RIGHT, buff=0)
        caixas3.move_to([-2, 0.5, 0])
        caixas3.scale(0.4)

        contorno3 = SurroundingRectangle(caixas3, color=YELLOW, buff=0, stroke_width=6)

        bits4 = ['1', '0', '1', '0']

        caixas4 = VGroup()
        for i in range(len(bits4)):
            quadrado = Square(color=WHITE)
            texto = Text(bits4[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas4.add(dupla)
        caixas4.arrange(RIGHT, buff=0)
        caixas4.move_to([-2, -0.5, 0])
        caixas4.scale(0.4)

        contorno4 = SurroundingRectangle(caixas4, color=YELLOW, buff=0, stroke_width=6)

        grupo2 = VGroup(caixas3, caixas4)
        chaves2 = Brace(grupo2, direction=RIGHT, color=YELLOW)

        texto_chaves2 = Text('Somar')
        texto_chaves2.next_to(chaves2, RIGHT)

        bits5 = ['0', '0', '1', '0']

        caixas5 = VGroup()
        for i in range(len(bits5)):
            quadrado = Square(color=WHITE)
            texto = Text(bits5[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas5.add(dupla)
        caixas5.arrange(RIGHT, buff=0)
        caixas5.move_to([-2, -2, 0])
        caixas5.scale(0.4)

        contorno5 = SurroundingRectangle(caixas5, color=YELLOW, buff=0, stroke_width=6)

        bits6 = ['0', '1', '0', '1']

        caixas6 = VGroup()
        for i in range(len(bits6)):
            quadrado = Square(color=WHITE)
            texto = Text(bits6[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas6.add(dupla)
        caixas6.arrange(RIGHT, buff=0)
        caixas6.move_to([-2, -3, 0])
        caixas6.scale(0.4)

        contorno6 = SurroundingRectangle(caixas6, color=YELLOW, buff=0, stroke_width=6)

        grupo3 = VGroup(caixas5, caixas6)
        chaves3 = Brace(grupo3, direction=RIGHT, color=YELLOW)

        texto_chaves3 = Text('Subtrair')
        texto_chaves3.next_to(chaves3, RIGHT)

        complemento_de_dois = Text("Complemento de Dois", weight=BOLD, font_size=80).scale(0.8)

        self.play(Write(caixas1),
                  Write(caixas2))
        self.play(Write(caixas3),
                  Write(caixas4))
        self.play(Write(caixas5),
                  Write(caixas6))
        self.play(ShowPassingFlash(contorno1),
                  ShowPassingFlash(contorno2), run_time=0.85)
        self.play(ShowPassingFlash(contorno3),
            ShowPassingFlash(contorno4), run_time=0.85)
        self.play(ShowPassingFlash(contorno5),
            ShowPassingFlash(contorno6), run_time=0.85)
        self.wait()
        self.play(Write(chaves1),
                  Write(texto_chaves1))
        self.play(Write(chaves2),
                  Write(texto_chaves2))
        self.play(Write(chaves3),
                  Write(texto_chaves3))
        self.wait()
        self.play(FadeOut(caixas1),
                  FadeOut(caixas2),
                  FadeOut(caixas3),
                  FadeOut(caixas4),
                  FadeOut(caixas5),
                  FadeOut(caixas6),
                  FadeOut(chaves1),
                  FadeOut(chaves2),
                  FadeOut(chaves3),
                  FadeOut(texto_chaves1),
                  FadeOut(texto_chaves2),
                  FadeOut(texto_chaves3))
        self.wait()
        self.play(Write(complemento_de_dois))
        self.play(FadeOut(complemento_de_dois))


class PesoNegativo(Scene):
    def construct(self):
        bits1 = ['0', '1', '0', '1']

        caixas = VGroup()
        for i in range(len(bits1)):
            quadrado = Square(color=WHITE)
            texto = Text(bits1[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas.add(dupla)
        caixas.arrange(RIGHT, buff=0)

        quatro = Text('4')
        quatro.scale(1.2)
        quatro.next_to(caixas[1], DOWN)

        dois = Text('2')
        dois.scale(1.2)
        dois.next_to(caixas[2], DOWN)

        um = Text('1')
        um.scale(1.2)
        um.next_to(caixas[3], DOWN)

        menos_oito = Text('-8', color="#AA77C7")
        menos_oito.scale(1.2)
        menos_oito.next_to(caixas[0], DOWN)

        numeros = VGroup(menos_oito, quatro, dois, um)

        multiplicacao = VGroup()
        for i in range(len(bits1)):
            vezes = Text('X')
            vezes.scale(0.4)
            multiplicacao.add(vezes)
        multiplicacao.arrange(RIGHT, buff=1.9)
        multiplicacao.next_to(numeros, UP * 1.8)

        numeros_soma = ['0', '4', '0', '1']

        conta = VGroup()
        for i in range(len(bits1)):
            soma = Text(numeros_soma[i])
            soma.scale(1.2)
            conta.add(soma)
        conta.arrange(RIGHT, buff=2.1)
        conta.move_to([0, -2, 0])

        mais_e_igual = ['+', '+', '+', '=']

        sinais = VGroup()
        for i in range(4):
            sinais_conta = Text(mais_e_igual[i])
            sinais_conta.scale(0.8)
            sinais.add(sinais_conta)
        sinais.arrange(RIGHT, buff=2.2)
        sinais.move_to([1.2, -2, 0])

        cinco = Text('5')
        cinco.scale(1.2)
        cinco.move_to([4.5, -2, 0])

        bits_novos = ['1', '0', '1', '1']

        caixas2 = VGroup()
        for i in range(len(bits_novos)):
            quadrado = Square(color=WHITE)
            texto = Text(bits_novos[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas2.add(dupla)
        caixas2.arrange(RIGHT, buff=0)

        menos_cinco = Text('-5', color="#AA77C7")
        menos_cinco.scale(1.2)
        menos_cinco.move_to([4.5, -2, 0])

        menos_oito_novo2 = Text('-8', color="#AA77C7")
        menos_oito_novo2.scale(1.2)
        menos_oito_novo2.move_to([-5, -2, 0])

        zero = Text('0', color="#AA77C7")
        zero.scale(1.2)
        zero.move_to([-2.7, -2, 0])

        dois_novo = Text('2', color="#AA77C7")
        dois_novo.scale(1.2)
        dois_novo.move_to([-0.1, -2, 0])

        self.play(Write(caixas))
        self.wait(0.4)
        bit_roxo = Text('0', color="#AA77C7").move_to(caixas[0].get_center())
        bit_roxo.scale(1.6)
        self.play(FadeTransform(caixas[0][1], bit_roxo), run_time=0.8)
        self.play(FadeTransform(bit_roxo, caixas[0][1]), run_time=0.8)
        self.wait(0.5)
        self.play(caixas.animate.move_to([0, 0.8, 0]))
        self.play(LaggedStart(
            Write(menos_oito),
            Write(quatro),
            Write(dois),
            Write(um), lag_ratio=0.9))
        self.wait(0.5)
        self.play(FadeIn(multiplicacao))
        conjunto = VGroup(caixas, numeros, multiplicacao)
        self.play(conjunto.animate.move_to([0, 1.2, 0]))
        chaves = Brace(conjunto, DOWN, color=YELLOW)
        self.play(Write(chaves))
        self.play(Write(conta))
        conjunto_conta = VGroup(conta, sinais)
        self.play(FadeIn(sinais),
                        conjunto_conta.animate.move_to([-0.8, -2, 0]))
        self.play(Write(cinco))
        self.wait()
        caixas2.move_to(caixas.get_center())
        self.play(FadeTransform(caixas, caixas2))
        self.play(FadeTransform(conta[0], menos_oito_novo2),
                  FadeTransform(conta[1], zero),
                  FadeTransform(conta[2], dois_novo))
        self.play(FadeTransform(cinco, menos_cinco))
        self.wait()
        self.play(FadeOut(mob) for mob in self.mobjects)
        self.wait()


class Truque(Scene):
    def construct(self):

        bits1 = ['0', '1', '0', '1']

        caixas = VGroup()
        for i in range(len(bits1)):
            quadrado = Square(color="#AA77C7")
            texto = Text(bits1[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas.add(dupla)
        caixas.arrange(RIGHT, buff=0)

        bits2 = ['1', '0', '1', '0']

        caixas2 = VGroup()
        for i in range(len(bits2)):
            quadrado = Square(color="#AA77C7")
            texto = Text(bits2[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas2.add(dupla)
        caixas2.arrange(RIGHT, buff=0)

        mais_um = Text('+1', color=YELLOW)
        mais_um.scale(0.8)
        mais_um.move_to([2.9, 1.5, 0])

        bits3 = ['1', '0', '1', '1']

        caixas3 = VGroup()
        for i in range(len(bits3)):
            quadrado = Square(color="#AA77C7")
            texto = Text(bits3[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas3.add(dupla)
        caixas3.arrange(RIGHT, buff=0)

        self.play(FadeIn(caixas))
        self.wait()
        self.play(FadeTransform(caixas, caixas2), run_time=1.2)
        self.wait()
        self.play(Write(mais_um))
        self.wait(0.5)
        self.play(FadeOut(mais_um),
                  FadeTransform(caixas2, caixas3), run_time=1.2)
        self.wait()
        self.play(FadeOut(mob) for mob in self.mobjects)
        self.wait()


class SeteMenosCinco(Scene):
    def construct(self):

        conta = Text('7 -5 = 7 + (-5)')
        conta.scale(2.2)

        bits1 = ['0', '1', '1', '1']

        caixas1 = VGroup()
        for i in range(len(bits1)):
            quadrado = Square(color=WHITE)
            texto = Text(bits1[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas1.add(dupla)
        caixas1.arrange(RIGHT, buff=0)
        caixas1.scale(0.8)
        caixas1.move_to([0, 2.5, 0])

        bits2 = ['1', '0', '1', '1']

        caixas2 = VGroup()
        for i in range(len(bits2)):
            quadrado = Square(color=WHITE)
            texto = Text(bits2[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas2.add(dupla)
        caixas2.arrange(RIGHT, buff=0)
        caixas2.scale(0.8)
        caixas2.move_to([0, 0.5, 0])

        sinal_de_mais = Text('+', color=WHITE)
        sinal_de_mais.move_to([-3.7, 0.4, 0])

        linha = Line(start=[-3.5, -0.6, 0], end=[3.5, -0.6, 0], color=WHITE)

        um_cima = Text('1', color="#AA77C7").move_to(caixas1[3].get_center())
        um_cima.scale(1.2)

        um_baixo = Text('1', color="#AA77C7").move_to(caixas2[3].get_center())
        um_baixo.scale(1.2)

        zero = Text('0')
        zero.scale(1.3)
        zero.move_to([2.38, -1.7, 0])

        bits3 = ['0', '0', '1', '0']

        caixas3 = VGroup()
        for i in range(len(bits3)):
            quadrado = Square(color=WHITE)
            texto = Text(bits3[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas3.add(dupla)
        caixas3.arrange(RIGHT, buff=0)
        caixas3.scale(0.8)
        caixas3.move_to([0, -1.4, 0])

        bit_solto = Text('1')
        bit_solto.scale(1.3)
        bit_solto.move_to([-4, -1.4, 0])

        caixa3_conjunto = VGroup(caixas3, bit_solto)
        caixa3_conjunto.move_to([-0.5, -1.7, 0])

        contorno = SurroundingRectangle(caixas3, color=YELLOW, buff=0, stroke_width=6)

        tudo = VGroup(
            caixas1, caixas2, sinal_de_mais, linha,
            um_cima, um_baixo, zero, caixa3_conjunto, contorno
        )
        tudo.move_to(DOWN * 0.1)

        igual_a_dois = Text('= 2')
        igual_a_dois.next_to(caixas3, RIGHT)
        igual_a_dois.scale(1.2)


        self.play(Write(conta), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(conta))
        self.wait()
        self.play(FadeIn(caixas1))
        self.wait(0.3)
        self.play(FadeIn(caixas2))
        self.wait(0.6)
        self.play(Write(linha),
                  Write(sinal_de_mais))
        self.play(FadeTransform(caixas1[3][1], um_cima), run_time=0.7)
        self.play(FadeTransform(um_cima, caixas1[3][1]), run_time=0.7)
        self.play(FadeTransform(caixas2[3][1], um_baixo), run_time=0.7)
        self.play(FadeTransform(um_baixo, caixas2[3][1]), run_time=0.7)
        self.play(FadeIn(caixas3[3]))
        self.wait(0.2)
        self.play(FadeIn(caixas3[2]))
        self.wait(0.2)
        self.play(FadeIn(caixas3[1]))
        self.wait(0.2)
        self.play(FadeIn(caixas3[0]))
        self.wait(0.2)
        self.play(FadeIn(bit_solto))
        self.wait(0.5)
        self.play(FadeOut(bit_solto))
        self.wait(0.5)
        self.play(ShowPassingFlash(contorno))
        self.play(Write(igual_a_dois))
        self.wait(0.6)
        self.play(FadeOut(mob) for mob in self.mobjects)
        self.wait()


class CincoMenosCinco(Scene):
    def construct(self):

        bits1 = ['0', '1', '0', '1']

        caixas1 = VGroup()
        for i in range(len(bits1)):
            quadrado = Square(color=WHITE)
            texto = Text(bits1[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas1.add(dupla)
        caixas1.arrange(RIGHT, buff=0)
        caixas1.scale(0.8)
        caixas1.move_to([0, 2, 0])

        bits2 = ['1', '0', '1', '1']

        caixas2 = VGroup()
        for i in range(len(bits2)):
            quadrado = Square(color=WHITE)
            texto = Text(bits2[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas2.add(dupla)
        caixas2.arrange(RIGHT, buff=0)
        caixas2.scale(0.8)
        caixas2.move_to([0, 0, 0])

        sinal_de_mais = Text('+', color=WHITE)
        sinal_de_mais.move_to([-3.7, 0, 0])

        linha = Line(start=[-3.5, -1, 0], end=[3.5, -1, 0], color=WHITE)

        bits3 = ['0', '0', '0', '0']

        caixas3 = VGroup()
        for i in range(len(bits3)):
            quadrado = Square(color=WHITE)
            texto = Text(bits3[i])
            texto.move_to(quadrado.get_center())
            texto.scale(1.6)
            dupla = VGroup(quadrado, texto)
            caixas3.add(dupla)
        caixas3.arrange(RIGHT, buff=0)
        caixas3.scale(0.8)
        caixas3.move_to([0, -2, 0])

        bit_solto = Text('1')
        bit_solto.scale(1.3)
        bit_solto.move_to([-4, -2, 0])

        self.play(FadeIn(caixas1))
        self.play(FadeIn(caixas2),
                  Write(sinal_de_mais),
                  Write(linha))
        self.play(FadeIn(caixas3[3]))
        self.wait(0.2)
        self.play(FadeIn(caixas3[2]))
        self.wait(0.2)  
        self.play(FadeIn(caixas3[1]))
        self.wait(0.2)
        self.play(FadeIn(caixas3[0]))
        self.wait(0.2)
        self.play(FadeIn(bit_solto))
        self.wait(0.3)
        self.play(FadeOut(bit_solto))
        self.wait()
        self.play(FadeOut(mob) for mob in self.mobjects)
        self.wait()


class GrandeVantagem(Scene):
    def construct(self):

        subtracao = Text('Subtração')
        subtracao.scale(1.2)
        subtracao.move_to([-3.7, 0, 0])

        adicao = Text('Adição comum')
        adicao.scale(1.2)
        adicao.move_to([3, 0, 0])

        seta = Arrow(start=[-2, 0, 0], end=[0.6, 0, 0], color=YELLOW)

        circuito = Text('Circuito pequeno e veloz', color="#AA77C7")
        circuito.scale(1.5)

        self.play(Write(subtracao))
        self.play(Create(seta))
        self.play(Write(adicao))
        self.wait()
        self.play(FadeOut(subtracao),
                  FadeOut(adicao),
                  FadeOut(seta))
        self.wait()
        self.play(Write(circuito))
        self.wait(1.2)
        self.play(FadeOut(circuito))
        self.wait()
