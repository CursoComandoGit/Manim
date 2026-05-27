from manim import *

import numpy as np
config.background_color = "#1E1E1E"
MarkupText.set_default(font = "Manrope")
Text.set_default(font = "Manrope")


def codigoComando(codeMedia: str, show_background=False):
    if not isinstance(codeMedia, str):
        raise TypeError("Passe uma string (o código ) como parâmetro")

    code = Code(
            code_string=codeMedia, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0 if not show_background else 1
                }
        )
    code.scale(1)
    return code


class AulaCompleta(MovingCameraScene):
    def construct(self):
          #--------PARTE1---------
          HelloWorld.construct(self)
          #GRAVAÇÃO DE TELA
          Funcao.construct(self)
          TiposFuncoes.construct(self)
          Curiosidade.construct(self)
          #PARTE2
          #--------PARTE3---------
          Main.construct(self)
          Paradigma.construct(self)
          Importar.construct(self)
          Linha1.construct(self)
          Biblioteca.construct(self)
          Aprender.construct(self)
          Final.construct(self)



#--------PARTE1---------
class HelloWorld(MovingCameraScene):
    def construct(self):
        helloworldstring = '''#include <stdio.h>

int main(){
    printf("Olá, mundo!");
    return 0;
}'''

        helloworldcode = codigoComando(helloworldstring)
        self.play(FadeIn(helloworldcode[0]), Write(helloworldcode[1][0]), run_time=1)
        self.wait(2.5)
        self.play(Write(helloworldcode[1][2]), Write(helloworldcode[1][4:6]), run_time=1)

        sublinhado = Underline(helloworldcode[1][2][3:9], color=WHITE)
        self.play(Create(sublinhado))
        self.play(FadeOut(sublinhado))

        sublinhado2 = Underline(helloworldcode[1][4][0:7], color=WHITE)
        self.play(Create(sublinhado2))
        self.play(FadeOut(sublinhado2))

        # self.play(Circumscribe(helloworldcode[1][2][0:9], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)
        # self.play(Circumscribe(helloworldcode[1][4], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)

        self.wait()
        self.play(Write(helloworldcode[1][3]), run_time=1)
        self.wait(2.3)

        prt = '''printf("Olá, mundo!");''' #nem precisava disso agr q percebi
        prtc = codigoComando(prt).move_to(helloworldcode[1][3])
        self.add(prtc)
        self.play(helloworldcode[1:].animate.set_opacity(0.4), 
                helloworldcode[1][3].animate.set_opacity(0), 
                self.camera.frame.animate.move_to(prtc).scale(0.5)
                )

        self.wait(2)
        #text = SurroundingRectangle(prtc[1][0][8:18], buff=0.05)
        self.play(Circumscribe(prtc[1][0][8:18], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)
        self.wait(1.5)
        self.play(Flash(prtc[1][0][7], color=WHITE, line_length=0.1), Flash(prtc[1][0][18], color=WHITE, line_length=0.1))
        self.wait(1.5)
        self.play(ApplyWave(prtc[1][0][8:18], amplitude=0.1), rate_func=linear, run_time=0.8)
        self.wait(2.2)

        self.play(FadeOut(*self.mobjects))
        self.play(self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN))

        self.wait()
        primeiro = Text("Vamos criar seu primeiro\n        programa em C?", font_size=70).scale(0.7)
        self.play(FadeIn(primeiro), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

#GRAVAÇÃO DE TELA

class Funcao(Scene):
    def construct(self):
        # # opção 1
        # self.clear()
        # funcao = Text("O que é uma função?", font_size=70, t2w={'função':BOLD})
        # self.play(Write(funcao), run_time=0.6)
        # sublinhar = Underline(funcao, color=PURPLE)
        # self.play(Create(sublinhar))
        # self.wait()

        # opção 2
        self.clear()
        funcao = Text("O que é uma função?", font_size=70, t2c={'função':PURPLE})
        self.play(Write(funcao), run_time=1.5)
        #sublinhar = Underline(funcao, color=PURPLE)
        #self.play(Create(sublinhar))
        self.wait()
        self.play(FadeOut(*self.mobjects))

        # tarefa = Text("Faça isso", font_size=35)
        # ret = RoundedRectangle(corner_radius=0.1, color = "#8728BE",stroke_color= "#AA77C7",fill_opacity=0.1,height=4,width=3)
        # self.play(Create(ret))
        # self.play(Create(tarefa))
        # f = VGroup(tarefa, ret)
        # self.wait()

        texto = Text(" Bloco\n    de\ncódigo", font_size=70).scale(0.4)
        ret = SurroundingRectangle(texto, corner_radius=0.1, color=PURPLE, fill_opacity=0.1, stroke_width=2, buff=0.2)
        tarefa = Text("   Tarefa\nespecífica", font_size=70, color=PURPLE).scale(0.5)
        nome = Text("aprender()", font_size=70, color=PURPLE).next_to(ret, UP).scale(0.3)

        cod = VGroup(texto, ret)
        codgrupo = VGroup(cod, nome).arrange(UP, buff=0.1).scale(1.2)
        codtarefa = VGroup(codgrupo, tarefa).arrange(RIGHT, buff=3)

        flecha = Arrow(start=codgrupo.get_right(), end=tarefa.get_left())

        self.play(FadeIn(codgrupo))
        self.play(GrowArrow(flecha))
        self.play(FadeIn(tarefa))
        self.wait()
        self.play(FadeOut(*self.mobjects))

        codstring = '''int main(){
    aprender();
    aprender();
    aprender();
    return 0;        
}'''
        cod = codigoComando(codstring).scale(1.2)

        self.play(Write(cod[1][0]), run_time=0.5)
        self.play(FadeIn(cod[1][1]), run_time=0.5)
        self.play(FadeIn(cod[1][2]), run_time=0.5)
        self.play(FadeIn(cod[1][3]), run_time=0.5)
        self.play(Write(cod[1][4]), Write(cod[1][5]), run_time=0.5)
        self.wait()
        self.play(FadeOut(*self.mobjects))


class TiposFuncoes(MovingCameraScene):
    def construct(self):
        helloworldstring = '''#include <stdio.h>

int main(){
    printf("Olá, mundo!");
    aprender();
    return 0;
}'''

        helloworldcode = codigoComando(helloworldstring)
        tela = FullScreenRectangle(color=BLACK)

        main = SurroundingRectangle(helloworldcode[1][2], buff=0.05)
        main2 = SurroundingRectangle(helloworldcode[1][5:7], buff=0.05)
        area1 = Union(main, main2)
        destaque1 = Difference(tela, area1).set_stroke(width=0)
        destaque1.set_fill(color=BLACK, opacity=0.7)

        aprender = SurroundingRectangle(helloworldcode[1][4], buff=0.05)
        destaque2 = Difference(tela, aprender).set_stroke(width=0)
        destaque2.set_fill(color=BLACK, opacity=0.7)

        importamos = SurroundingRectangle(helloworldcode[1][0], buff=0.05)
        importamos2 = SurroundingRectangle(helloworldcode[1][3], buff=0.05)
        area2 = Union(importamos, importamos2)
        destaque3 = Difference(tela, area2).set_stroke(width=0)
        destaque3.set_fill(color=BLACK, opacity=0.7)
        
        self.play(FadeIn(helloworldcode))
        self.wait(1.8)
        self.play(FadeIn(destaque1))
        self.wait(1)

        self.play(ReplacementTransform(destaque1, destaque2))
        self.wait(1)

        self.play(ReplacementTransform(destaque2, destaque3))
        self.wait(1)

        self.play(FadeOut(destaque3))
        #self.wait(1)

        entrypoint = Text("Entry point", font_size=70, color=GREEN, weight=BOLD).scale(1.6)
        self.play(helloworldcode[1:].animate.set_opacity(0.4))
        self.play(Write(entrypoint))
        self.wait(5)

        entrypoint1 = Text("Entry point", font_size=70, color=GREEN, weight=BOLD).scale(0.4).next_to(helloworldcode[1][2], LEFT, buff=1.3)
        self.play(ReplacementTransform(entrypoint, entrypoint1), helloworldcode[1:].animate.set_opacity(1))
       
        seta = Arrow(start= entrypoint1.get_right(), end=helloworldcode[1][2].get_left(), color=GREEN)
        self.play(GrowArrow(seta))
        self.wait(5)

        self.play(self.camera.frame.animate.move_to(helloworldcode[1][2]).scale(0.5),
                  helloworldcode[1][0:2].animate.set_opacity(0.4),
                  helloworldcode[1][3:6].animate.set_opacity(0.4),
                  helloworldcode[1][2][9].animate.set_opacity(0.4),
                  helloworldcode[1][6].animate.set_opacity(0.4),
                  seta.animate.set_opacity(0.4),
                  entrypoint1.animate.set_opacity(0.4)
                  )
        self.wait()
        self.play(Circumscribe(helloworldcode[1][2][0:3], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)
        self.wait(2)
        self.play(Circumscribe(helloworldcode[1][2][3:7], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)
        self.play(Circumscribe(helloworldcode[1][2][7:9], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)
        self.play(self.camera.frame.animate.move_to(helloworldcode[1]),
                  #helloworldcode[1:].animate.set_opacity(1),
                  helloworldcode[1][2][9].animate.set_opacity(1),
                  helloworldcode[1][6].animate.set_opacity(1),
                  Circumscribe(helloworldcode[1][6], buff=0.05, fade_out=True, run_time=1.5, color=WHITE),
                  Circumscribe(helloworldcode[1][2][9], buff=0.05, fade_out=True, run_time=1.5, color=WHITE)
                  )
        self.wait(5)
        self.play(helloworldcode[1][3:6].animate.set_opacity(1),
                  Circumscribe(helloworldcode[1][3][20], buff=0.05, fade_out=True, run_time=1.5, color=WHITE),
                  Circumscribe(helloworldcode[1][4][10], buff=0.05, fade_out=True, run_time=1.5, color=WHITE),
                  Circumscribe(helloworldcode[1][5][7], buff=0.05, fade_out=True, run_time=1.5, color=WHITE),
                  )
        sublinhado = Underline(helloworldcode[1][5][0:7], color=WHITE)
        self.play(Create(sublinhado))
        self.play(FadeOut(sublinhado))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        self.play(self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN))


class Curiosidade(MovingCameraScene):
    def construct(self):
        titulo = Text("Curiosidade", font_size=70, color=PURPLE)
        curiosidade = Text("C é whitespace-insensitive", font_size=70)
        texto = Group(titulo, curiosidade).arrange(DOWN, buff=0.2).scale(0.7)

        codstring1 = '''main () {}'''
        cod1 = codigoComando(codstring1, show_background=True)

        codstring2 = '''        main ()
{                       }'''
        cod2 = codigoComando(codstring2, show_background=True)

        codstring3 = '''main
(
)
{
}'''
        cod3 = codigoComando(codstring3, show_background=True)

        codstring4 = '''main
() {}'''
        cod4 = codigoComando(codstring4, show_background=True)

        cod1.move_to(UP * 2 + LEFT * 3.5)
        cod2.move_to(UP * 1.8 + RIGHT * 3) 
        cod3.move_to(DOWN * 1.5 + LEFT * 3.5)
        cod4.move_to(DOWN * 1.8 + RIGHT * 2.5)

        self.play(FadeIn(titulo))
        self.play(Write(curiosidade))
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))
        self.play(FadeIn(cod1))
        self.play(FadeIn(cod2))
        self.play(FadeIn(cod3))
        self.play(FadeIn(cod4))
        fundo = VGroup(*self.mobjects)
        #self.play(fundo.animate.set_opacity(0.4))
        self.play(FadeOut(fundo))
        organizar = Text("Mantenha seu código\n         organizado!", font_size=70).scale(0.9)
        self.play(Write(organizar))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))


#PARTE2

#--------PARTE3---------

class Main(Scene):
    def construct(self):
        mainstring1 = '''main(){
    // printf() e scanf() omitidos para melhor visualização
        
    double media1 = calcularMedia(a1, b1)

    double media2 = calcularMedia(a2, b2)

    double media3 = calcularMedia(a3, b3)

    double media4 = calcularMedia(a4, b4)

    double media5 = calcularMedia(a5, b5)
}'''
        codmain = codigoComando(mainstring1).move_to(ORIGIN).scale(0.8)

        self.play(Write(codmain[1][0]), FadeIn(codmain[1][1]), run_time=0.5)
        self.play(FadeIn(codmain[1][3]), run_time=0.8)
        self.play(FadeIn(codmain[1][5]), run_time=0.8)
        self.play(FadeIn(codmain[1][7]), run_time=0.8)
        self.play(FadeIn(codmain[1][9]), run_time=0.8)
        self.play(FadeIn(codmain[1][11]), run_time=0.8)
        self.play(Write(codmain[1][12]), run_time=0.5)
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))


class Paradigma(MovingCameraScene):
    def construct(self):
        explicacao = Text("Baseia-se em procedimentos,\nque são executados numa sequência.", font_size=70)
        paradigma = Text("Linguagem procedural", font_size=70, color=PURPLE)
        definicao = VGroup(paradigma, explicacao).arrange(DOWN, aligned_edge=LEFT).scale(0.6).move_to(ORIGIN)
        linha = Line(start=definicao.get_top(), end=definicao.get_bottom(), color=GRAY).next_to(definicao, LEFT, buff=0.2)

        explicacao1 = Text("Baseia-se em procedimentos,\nque são executados numa sequência.", font_size=70)
        paradigma1 = Text("Linguagem procedural", font_size=70, color=PURPLE)
        definicao1 = VGroup(paradigma1, explicacao1).arrange(DOWN, aligned_edge=LEFT).scale(0.6).next_to(linha, LEFT, buff=0)

        square = Rectangle(
            width=definicao1.width + 0.2,
            height=definicao1.height + 0.2,
            color="#1E1E1E"
        ).set_fill("#1E1E1E", opacity=1).move_to(definicao1)

        self.add(definicao1, square)
        self.play(Create(linha))
        self.play(ReplacementTransform(definicao1, definicao), run_time=1, rate_func=rate_functions.smooth)
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

class Importar(MovingCameraScene):
    def construct(self):
        # prtf = Text("printf", font_size=70, weight=BOLD, color=PURPLE).scale(0.7).shift(LEFT*2.5)
        # func = Text("Função", font_size=70).scale(0.4).next_to(prtf, DOWN, buff=0.2)
        # stdio = Text("stdio", font_size=70, weight=BOLD, color=PURPLE).scale(0.7).shift(RIGHT*2.5)
        # biblioteca = Text("Biblioteca\n   padrão", font_size=70).scale(0.4).next_to(stdio, DOWN, buff=0.3)

        # seta = Arrow(start= prtf.get_right(), end=stdio.get_left(), color=WHITE)

        # self.play(Write(prtf))
        # self.play(FadeIn(func))
        # self.play(GrowArrow(seta))
        # self.play(Write(stdio))
        # self.play(FadeIn(biblioteca))
        # self.wait()
        # self.play(FadeOut(*self.mobjects))

        prtf = Text("printf", font_size=70, weight=BOLD).scale(0.7).shift(LEFT*2.5)
        caixa = ImageMobject("MANIM_RECURSOS/caixa.png").scale(0.45).shift(RIGHT*2.5)
        stdio = Text("stdio.h", font_size=70, weight=BOLD).scale(0.5).next_to(caixa, DOWN, buff=0.1)
        seta = Arrow(start= prtf.get_right(), end=caixa.get_left(), color=WHITE)

        caixagrupo = Group(caixa, stdio)

        self.play(Write(prtf))
        self.play(GrowArrow(seta))
        self.play(FadeIn(caixagrupo))
        self.wait()
        self.play(FadeOut(*self.mobjects))



class Linha1(MovingCameraScene):
    def construct(self):
        helloworldstring = '''#include <stdio.h>

int main(){
    printf("Olá, mundo!");
    return 0;
}'''

        helloworldcode = codigoComando(helloworldstring)
        
        self.play(FadeIn(helloworldcode))
        self.play(self.camera.frame.animate.move_to(helloworldcode[1][0]).scale(0.5))
        self.play(helloworldcode[1][0].animate.set_opacity(0))
        self.play(self.camera.frame.animate.move_to(helloworldcode[1][3]))
        self.wait(2.5)
        #opção 1
        rect = SurroundingRectangle(helloworldcode[1][3], color=WHITE, buff=0.05)
        self.play(ShowPassingFlash(rect, time_width=0.5, run_time=1.5))
        # #opção 2
        # underline = Underline(helloworldcode[1][3], color=RED, buff=0.05)
        # self.play(ShowPassingFlash(underline, time_width=0.4, run_time=1.5))
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))
        self.play(self.camera.frame.animate.set(width=config.frame_width).move_to(ORIGIN))

class Biblioteca(MovingCameraScene):
    def construct(self):
        arq = ImageMobject("MANIM_RECURSOS/arquivo.png")
        bib = Text("biblioteca.h", font_size=70).next_to(arq, DOWN, buff=0.2).scale(0.8)
        arqbib = Group(arq, bib).scale(0.4)

        func = Text("Funções\n    úteis", font_size=70).next_to(arqbib, RIGHT, buff=1.5).scale(0.5)
        grupo = ImageMobject("MANIM_RECURSOS/pessoas.png").next_to(func, RIGHT, buff=1.5).scale(0.55)

        tudo = Group(arqbib, func, grupo).move_to(ORIGIN)
        flecha1 = Arrow(start=arqbib.get_right(), end=func.get_left(), color=PURPLE)
        flecha2 = Arrow(start=func.get_right(), end=grupo.get_left(), color=PURPLE)

        self.play(FadeIn(arqbib))
        self.play(GrowArrow(flecha1))
        self.play(FadeIn(func))
        self.play(GrowArrow(flecha2))
        self.play(FadeIn(grupo))
        self.wait()

        grupofadeout = Group(flecha1, flecha2, func, grupo)
        grupofadeout.set_z_index(arqbib.z_index - 1)

        inc = Text("#include <biblioteca.h>", font_size=70, color=GREEN).scale(0.4)  
        finalgrupo = Group(arqbib.copy(), inc).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        target = finalgrupo[0].get_center() 
        
        self.play(FadeOut(grupofadeout), arqbib.animate.scale(1.8).move_to(target))
        inc.next_to(arqbib, DOWN, buff=0.4)
        #self.play(arqbib.animate.shift(LEFT*2))
        self.play(AddTextLetterByLetter(inc),run_time=1, rate_func=linear)
        self.wait()
        self.play(FadeOut(*self.mobjects))

        exbib1 = Text("math.h", font_size=70, color=PURPLE_A, weight=BOLD).scale(0.4)  
        exfuncs11 = Text("sqrt()", font_size=70).scale(0.4)
        exfuncs12 = Text("exp()", font_size=70).scale(0.4)
        exfuncs13 = Text("log()", font_size=70).scale(0.4)
        exfuncs14 = Text("...", font_size=70).scale(0.4)
        funcoes = VGroup(exfuncs11, exfuncs12, exfuncs13, exfuncs14).arrange(DOWN, buff=0.1, aligned_edge=LEFT)  
        ret1 = SurroundingRectangle(funcoes, color=WHITE, buff=0.2, fill_opacity=0)
        grupoex1 = VGroup(funcoes, ret1)
        grupo1 = VGroup(exbib1, grupoex1).arrange(DOWN, buff=0.2, aligned_edge=LEFT)  
        #self.play(FadeIn(grupo1))
        self.wait()

        exbib2 = Text("stdlib.h", font_size=70, color=PURPLE_A, weight=BOLD).scale(0.4)  
        exfuncs21 = Text("rand()", font_size=70).scale(0.4)
        exfuncs22 = Text("exit()", font_size=70).scale(0.4)
        exfuncs23 = Text("atof()", font_size=70).scale(0.4)
        exfuncs24 = Text("...", font_size=70).scale(0.4)
        funcoes2 = VGroup(exfuncs21, exfuncs22, exfuncs23, exfuncs24).arrange(DOWN, buff=0.1, aligned_edge=LEFT)  
        ret2 = SurroundingRectangle(funcoes2, color=WHITE, buff=0.2, fill_opacity=0)
        grupoex2 = VGroup(funcoes2, ret2)
        grupo2 = VGroup(exbib2, grupoex2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)   

        exbib3 = Text("string.h", font_size=70, color=PURPLE_A, weight=BOLD).scale(0.4)  
        exfuncs31 = Text("strlen()", font_size=70).scale(0.4)
        exfuncs32 = Text("strlwr()", font_size=70).scale(0.4)
        exfuncs33 = Text("strupr()", font_size=70).scale(0.4)
        exfuncs34 = Text("...", font_size=70).scale(0.4)
        funcoes3 = VGroup(exfuncs31, exfuncs32, exfuncs33, exfuncs34).arrange(DOWN, buff=0.1, aligned_edge=LEFT)  
        ret3 = SurroundingRectangle(funcoes3, color=WHITE, buff=0.2, fill_opacity=0)
        grupoex3 = VGroup(funcoes3, ret3)
        grupo3 = VGroup(exbib3, grupoex3).arrange(DOWN, buff=0.2, aligned_edge=LEFT)  

        todasbib = VGroup(grupo1, grupo2, grupo3).arrange(RIGHT, buff=1.5, aligned_edge=DOWN).scale(1.2)
        self.play(FadeIn(grupo1))
        self.play(FadeIn(grupo2))
        self.play(FadeIn(grupo3))

        tela = FullScreenRectangle(color=BLACK).set_fill(opacity=0.7)
        incluir = Text("#include <nome>", font_size=70, color=GREEN, t2s={"nome": ITALIC})
        self.play(FadeIn(tela))
        self.play(Write(incluir))
        self.wait()
        self.play(FadeOut(*self.mobjects))

class Aprender(Scene):
    def construct(self):
        cerebro = ImageMobject("MANIM_RECURSOS/cerebro.png").scale(0.5)
        estrutura = Text("Estrutura de Programa em C", font_size=70, t2c={'Programa em C': PURPLE_A, "Estrutura": BLUE_C}).scale(0.7)

        self.play(GrowFromCenter(cerebro))
        self.play(Wiggle(cerebro))
        self.play(cerebro.animate.shift(LEFT*4.5))
        estrutura.next_to(cerebro, RIGHT, buff=0.4)
        self.play(Write(estrutura))
        self.play(FadeOut(*self.mobjects))

#--------CENAFINAL---------
class Final(MovingCameraScene):
    def construct(self):
        final_text1 = Text("Próxima aula:",font_size=60)
        final_text2 = Text("Variáveis e tipos de dados",font_size=75, t2c={'Variáveis': PURPLE})
        final = VGroup(final_text1, final_text2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(.7)

        logo = ImageMobject("MANIM_RECURSOS/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        # O cursor
        cursorVinheta=ImageMobject("MANIM_RECURSOS/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)

        self.play(Write(final))
        self.wait()

        self.play(
            logoOrigin.animate.become(logo),
            run_time=2
        )

        # Cursor aparece e se move
        self.play(cursorVinheta.animate.move_to(ORIGIN+RIGHT*0.25+DOWN*0.45))
        self.play(cursorVinheta.animate.scale(0.8),run_time=0.1,rate_func=linear)  # Clica
        self.play(cursorVinheta.animate.scale(1.2),run_time=0.1,rate_func=linear)  #
        
        # Vinheta Puxada
        self.play(
            GrowFromCenter(Rectangle(color="#0A0A0A",fill_opacity=1,width=20, height=10),run_time=0.5)
        )

