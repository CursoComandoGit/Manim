from manim import *
import random
import numpy as np
import struct

config.background_color = "#1E1E1E"
MarkupText.set_default(font = "Manrope")
Text.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

COR_SINAL = "#AA77C7"

def criar_texto(texto, cor=WHITE, tamanho=0.4):
    t = Text(texto, font="Monospace", font_size=100, color=cor).scale(tamanho)
    return t

def colchete_deitado(mob, cor=WHITE, altura=0.2):
    largura = mob.get_width()
    pontos = [
        [-largura / 2, altura, 0],
        [-largura / 2, 0, 0],
        [largura / 2, 0, 0],
        [largura / 2, altura, 0],
    ]
    colchete = VMobject(color=cor, stroke_width=3)
    colchete.set_points_as_corners(pontos)
    colchete.next_to(mob, DOWN, buff=0.15)
    return colchete

def formatar_potencia(base_str, expoente_str, cor=WHITE, tamanho=0.4):
    base = criar_texto(base_str, cor=cor, tamanho=tamanho)
    exp = criar_texto(expoente_str, cor=cor, tamanho=tamanho * 0.7)
    exp.next_to(base, UR, buff=0.03).shift(RIGHT * 0.05 + DOWN * 0.1)
    return VGroup(base, exp)

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

def sobrescrito(n):
    mapa = {"0":"⁰","1":"¹","2":"²","3":"³","4":"⁴",
            "5":"⁵","6":"⁶","7":"⁷","8":"⁸","9":"⁹"}
    return "".join(mapa[d] for d in str(n))

def criaCapitulo(cena : Scene, titulo : Text, descricao = Text(""), numero = 1, comFade = False):
    if cena.mobjects:
        cena.play(*[obj.animate.set_opacity(0) for obj in cena.mobjects])
    ntext = Text(
        f"Capítulo {numero}",
        color=WHITE,
        font="Segoe UI",
        weight=THIN,
        font_size=80
    ).scale(0.5)

    grupoCompleto = VGroup(ntext, titulo, descricao)

    grupoCompleto.arrange(DOWN, buff=0.75)
    grupoCompleto[-1].move_to(grupoCompleto[-2].get_bottom()+[0,-0.25,0], aligned_edge=UP)

    grupoCompleto.center()

    if comFade:
        anim = LaggedStart(
            FadeIn(ntext, shift=UP * 0.3),
            FadeIn(titulo, shift=UP * 0.3),
            FadeIn(descricao, shift=UP * 0.3),
            lag_ratio=0.5
        )

        animR = LaggedStart(
            FadeOut(descricao, shift=DOWN * 0.3),
            FadeOut(titulo, shift=DOWN * 0.3),
            FadeOut(ntext, shift=DOWN * 0.3),
            lag_ratio=0.25
        )
    else:
        anim = Write(descricao)
        
        animR = AnimationGroup(FadeOut(descricao), FadeOut(titulo), FadeOut(ntext))

    if not comFade:
        cena.add(ntext)
        cena.wait(0.6)
        cena.add(titulo)
        cena.wait(0.3)
    cena.play(anim, rate_func=rate_functions.ease_in_out_back, run_time=1)
    cena.wait(1)
    cena.play(animR)
    cena.remove(grupoCompleto)
    cena.play(*[obj.animate.set_opacity(1) for obj in cena.mobjects])
    
    cena.wait()

class AulaCompleta(MovingCameraScene):
    def construct(self):
        Inicio.construct(self)
        Intro.construct(self)
        Ram.construct(self)
        Variaveis.construct(self)
        Numero.construct(self)
        Background.construct(self)
        Capitulo.construct(self)
        Computador.construct(self)
        Tamanho.construct(self)
        Negativos.construct(self)
        Float.construct(self)

        Char.construct(self)
        Xerox.construct(self)
        Void.construct(self)
        Modificadores.construct(self)
        Signed.construct(self)
        Unsigned.construct(self)
        Tamanho2.construct(self)
        Longfloat.construct(self)
        Testar.construct(self)
        Final.construct(self)

class Inicio(Scene):
    def construct(self):
        helloworldstring = '''#include <stdio.h>
        
        int main(){
            printf("Olá, mundo!");
            return 0;
        }'''
        
        helloworldcode = codigoComando(helloworldstring, True).scale(0.65)

        computador = SVGMobject("assets/computador.svg")

        grupo = VGroup(helloworldcode, computador).arrange(RIGHT, buff=2.5).move_to(ORIGIN)

        seta = Arrow(start=helloworldcode.get_right(), end=computador.get_left())


        self.play(FadeIn(helloworldcode))
        self.wait()
        self.play(FadeIn(computador))
        self.wait()
        self.play(GrowArrow(seta))
        self.wait()
        self.play(FadeOut(seta), FadeOut(computador))

        helloworldcode2 = helloworldcode.copy()

        programador = SVGMobject("assets/programador")
        
        entender = VGroup(programador, helloworldcode2).arrange(RIGHT, buff=1.5).move_to(ORIGIN)
        interrogacao = Text("?", font_size=70).scale(1.5).move_to(helloworldcode2)
        

        self.play(helloworldcode.animate.move_to(helloworldcode2))
        self.play(FadeIn(programador))
        self.play(Write(interrogacao))


        self.play(FadeOut(*self.mobjects))

#INTRO aqui
class Intro(Scene):
    def construct(self):
        logo_svg = SVGMobject("assets/comando.svg").scale(1.5).move_to(ORIGIN)
                
        self.play(Write(logo_svg))

        self.play(logo_svg.animate.shift(UP*0.6))        
        comando = MarkupText('<b>comando.c</b>', font="Major Mono Display").next_to(logo_svg, DOWN, buff=0.2).scale(0.6)
        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 1.1,
            width = 0.5
        ).move_to(comando[0]).scale(0.3)

        self.play(TypeWithCursor(comando, cursor))
        self.play(Blink(cursor, blinks=1))
        self.remove(cursor)
        self.wait()
        self.play(FadeOut(*self.mobjects))

class Ram(MovingCameraScene):
    def construct(self):
        ram = Text("Random Access Memory", font_size=70, t2c={'R':PURPLE, 'A':PURPLE, 'M':PURPLE}).move_to(ORIGIN).scale(0.9)
        
        memoria = Text("RAM", font_size=70, color=PURPLE).scale(0.9)
        ret = SurroundingRectangle(memoria, color=WHITE, buff=0.2)

        a = Line(UP*0.1, DOWN*0.1)
        b = a.copy()
        c = a.copy()
        d = a.copy()
        e = a.copy()

        riscos = VGroup(a, b, c, d, e).arrange(RIGHT, buff=0.3).next_to(ret, UP, buff=0)
        riscos2 = riscos.copy().next_to(ret, DOWN, buff=0)

        self.play(Write(ram))
        self.play(TransformMatchingShapes(ram, memoria))
        rgrupo = VGroup(ret, riscos2, riscos)
        self.play(Write(rgrupo))
        self.wait()

        bits = [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0]
        caixas = VGroup()

        ponto1 = Dot().scale(0.7)
        ponto2 = ponto1.copy()
        ponto3 = ponto1.copy()
        lpontos = VGroup(ponto1, ponto2, ponto3).arrange(RIGHT, buff=0.2)
        rpontos = lpontos.copy()

        for bit in bits:
            numero = Text(str(bit), font_size=48, color=WHITE)
            quadrado = Square(side_length=1)
            quadrado.set_stroke(color=WHITE, width=3)
            quadrado.set_fill(opacity=0)

            numero.move_to(quadrado.get_center())
            celula = VGroup(quadrado, numero)
            caixas.add(celula)

        caixas.arrange(RIGHT, buff=0).move_to(ORIGIN).scale(0.9)
        lpontos.next_to(caixas, LEFT, buff=0.2)
        rpontos.next_to(caixas, RIGHT, buff=0.2)

        self.play(Unwrite(memoria), FadeOut(rgrupo))
        self.wait(0.5)
        self.play(FadeIn(caixas), FadeIn(lpontos), FadeIn(rpontos))

        self.play(self.camera.frame.animate.scale(0.6), FadeOut(rpontos, lpontos))


        for x in range(0,3):
            numero = Text("0", font_size=48, color=WHITE)
            quadrado = Square(side_length=1)
            quadrado.set_stroke(color=WHITE, width=3)
            quadrado.set_fill(opacity=0)

            numero.move_to(quadrado.get_center())
            celula = VGroup(quadrado, numero).scale(0.9)
            if len(caixas) > 0:
                celula.next_to(caixas[-1], RIGHT, buff=0) 
            caixas.add(celula)
        self.wait(0.5)

        self.play(self.camera.frame.animate.move_to(caixas[-1]))

        primeiras_seis = caixas[:6]
        for celula in primeiras_seis:
            caixas.remove(celula) 

        msign = Text("Menos significativo", font_size=70, color=PURPLE, weight=BOLD).scale(0.2)
        setamenos = Arrow(start=caixas[-4].get_left(), end=caixas[-2].get_right(), color=PURPLE, stroke_width=3, tip_length=0.2)
        gruposeta = VGroup(setamenos, msign).arrange(UP, buff=0).next_to(caixas[-3], UP, buff=0.6)
        msign.shift(LEFT*0.1)

        self.play(Write(gruposeta))

        xis = VGroup()
        potencias = VGroup()
        n = len(caixas)

        for i, celula in enumerate(caixas):
            x = Text("×", font_size=36, color=WHITE).scale(0.6)
            x.next_to(celula, DOWN, buff=0.15)
            xis.add(x)

            expoente = n - 1 - i
            potencia = Text(f"2{sobrescrito(expoente)}", font_size=48, color=WHITE).scale(0.6)
            potencia.next_to(x, DOWN, buff=0.15)
            potencias.add(potencia)

        sinais_mais = VGroup()

        for i in range(len(potencias) - 1):
            mais = Text("+", font_size=48, color=WHITE).scale(0.6)
            # posiciona no meio do caminho entre uma potência e a próxima
            ponto_medio = (potencias[i].get_right() + potencias[i+1].get_left()) / 2
            mais.move_to(ponto_medio)
            sinais_mais.add(mais)


        self.play(FadeIn(xis), FadeIn(potencias), FadeIn(sinais_mais))
        self.wait()


        for i in range(7, 5, -1):

            self.play(caixas[i][1].animate.set_color(PURPLE), run_time=0.5)
            valor1 = Text("= 0", font_size=48, color=PURPLE).scale(0.5).next_to(potencias[i-8], DOWN, buff=0.1)
            self.play(Write(valor1), potencias[i-8].animate.set_color(PURPLE), xis[i-8].animate.set_color(PURPLE))
            self.wait()
            self.play(FadeOut(valor1))

            self.wait()
            novo_numero = Text("1", font_size=48, color=PURPLE).scale(0.9)
            novo_numero.move_to(caixas[i][0].get_center())
            self.play(ReplacementTransform(caixas[i][1], novo_numero))
            self.wait()

            self.play(caixas[i][1].animate.set_color(PURPLE), run_time=0.5)
            if i == 7:
                valor1 = Text("= 1", font_size=48, color=PURPLE).scale(0.5).next_to(potencias[i-8], DOWN, buff=0.1)
            else:
                valor1 = Text("= 2", font_size=48, color=PURPLE).scale(0.5).next_to(potencias[i-8], DOWN, buff=0.1)
            self.play(Write(valor1))
            self.wait()
            self.play(FadeOut(valor1), potencias[i-8].animate.set_color(WHITE), xis[i-8].animate.set_color(WHITE), caixas[i][1].animate.set_color(WHITE))
        
        chave = Brace(potencias[-2:], direction=DOWN, color=PURPLE, buff=0.1)
        texto = Text("= 3", font_size=24, color=PURPLE)
        texto.next_to(chave, DOWN, buff=0.1)

        numeros_roxos = VGroup(*[celula[1] for celula in caixas[6:8]])
        self.play(FadeIn(chave), Write(texto), potencias[-2:].animate.set_color(PURPLE), xis[6:8].animate.set_color(PURPLE), numeros_roxos.animate.set_color(PURPLE), sinais_mais[-1].animate.set_color(PURPLE))
        self.wait()

        self.play(FadeOut(chave), FadeOut(texto), potencias[6:8].animate.set_color(WHITE), xis[6:8].animate.set_color(WHITE), numeros_roxos.animate.set_color(WHITE), sinais_mais[-1].animate.set_color(WHITE))



        self.play(self.camera.frame.animate.move_to(caixas).set_width(config.frame_width), FadeOut(gruposeta))
        self.wait()

        bitsbytes = Text("8 bits = 1  byte", font_size=70, color=PURPLE).scale(0.6).next_to(caixas, UP, buff=0.5)
        self.play(Write(bitsbytes))
        self.wait()
        self.play(FadeOut(bitsbytes))

        sign = Text("Mais significativo", font_size=70, color=PURPLE, weight=BOLD).scale(0.2)
        setamais = Arrow(start=caixas[3].get_right(), end=caixas[1].get_left(), color=PURPLE, stroke_width=3, tip_length=0.2)
        gruposetam = VGroup(setamais, sign).arrange(UP, buff=0).next_to(caixas[2], UP, buff=0.6)
        sign.shift(RIGHT*0.1)

        self.play(self.camera.frame.animate.scale(0.6).move_to(caixas[0]))
        self.play(Write(gruposetam))
        self.wait()
        self.play(potencias[0].animate.set_color(PURPLE), run_time=0.5)
        self.wait()
        num = Text("128", font_size=48, color=PURPLE).scale(0.6).move_to(potencias[0])
        self.play(Transform(potencias[0], num))
        self.wait()

        num = Text(f"2{sobrescrito(7)}", font_size=48, color=WHITE).scale(0.6).move_to(potencias[0])
        self.play(Transform(potencias[0], num), self.camera.frame.animate.move_to(caixas).set_width(config.frame_width), FadeOut(gruposetam))
        animacoes = []
        for celula in caixas:
            numero_antigo = celula[1]
            
            if numero_antigo.text == "0":   
                quadrado = celula[0]
                
                novo_numero = Text("1", font_size=48, color=WHITE).scale(0.9)
                novo_numero.move_to(quadrado.get_center())
                
                animacoes.append(Transform(numero_antigo, novo_numero))

        self.play(*animacoes)

        resultado = Text("= 255", font_size=48, color=PURPLE, weight=BOLD).scale(0.6).next_to(potencias, RIGHT, buff=0.2)
        self.play(Write(resultado))
        self.wait()

        self.play(FadeOut(resultado))


        animacoes = []
        for celula in caixas:
            numero_antigo = celula[1]
            quadrado = celula[0]
                            
            novo_numero = Text("0", font_size=48, color=WHITE).scale(0.9)
            novo_numero.move_to(quadrado.get_center())
            animacoes.append(Transform(numero_antigo, novo_numero))

        self.play(*animacoes)
        
        estado = [0] * 8

        resultado = Text("= 0", font_size=48, color=WHITE, weight=BOLD).next_to(potencias, DOWN, buff=0.6)
        self.play(Write(resultado))
        self.wait(0.5)

        for n in range(1, 7):
            novo_estado = [int(b) for b in format(n, "08b")]
            anims = []

            for i, (antigo, novo) in enumerate(zip(estado, novo_estado)):
                if antigo != novo:  
                    digito = Text(str(novo), font_size=48, color=WHITE).scale(0.9)
                    digito.move_to(caixas[i][0].get_center())
                    anims.append(Transform(caixas[i][1], digito))

            novo_resultado = Text(f"= {n}", font_size=48, color=WHITE, weight=BOLD).next_to(potencias, DOWN, buff=0.6)
            anims.append(Transform(resultado, novo_resultado))

            self.play(*anims)
            self.wait(0.5)
            estado = novo_estado

        ani = []
        for i, celula in enumerate(caixas):
            if estado[i] == 0:   
                digito = Text("1", font_size=48, color=WHITE).scale(0.9)
                digito.move_to(celula[0].get_center())
                ani.append(Transform(celula[1], digito))

        novo_resultado = Text("= 255", font_size=48, color=WHITE, weight=BOLD).next_to(potencias, DOWN, buff=0.6)
        self.play(*ani, Transform(resultado, novo_resultado))
        self.wait()

        self.play(FadeOut(sinais_mais), FadeOut(potencias), FadeOut(resultado), FadeOut(xis))

        bts = [0, 1, 1, 0, 0, 0, 1, 1]
        caixas2 = VGroup()

        for bt in bts:
            num = Text(str(bt), font_size=48, color=WHITE)
            quad = Square(side_length=1).set_stroke(color=WHITE, width=3).set_fill(opacity=0)

            num.move_to(quad.get_center())
            cel = VGroup(quad, num)
            caixas2.add(cel)

        caixas2.arrange(RIGHT, buff=0).scale(0.8)

        decimal = [9, 9]
        dec = VGroup()

        for decms in decimal:
            n = Text(str(decms), font_size=48, color=WHITE)
            q = Square(side_length=1).set_stroke(color=WHITE, width=3).set_fill(opacity=0)

            n.move_to(q.get_center())
            c = VGroup(q, n)
            dec.add(c)

        dec.arrange(RIGHT, buff=0).scale(0.8)

        igual = Text("=", font_size=48, color=WHITE)
        bindec = VGroup(caixas2, igual, dec).arrange(RIGHT, buff=0.5).move_to(self.camera.frame.get_center())
        self.play(ReplacementTransform(caixas, caixas2))
        self.play(Write(igual), Write(dec))

        base2 = Text("Base 2", font_size=48, color=PURPLE).scale(0.8).next_to(caixas2, UP, buff=0.7)
        base10 = Text("Base 10", font_size=48, color=PURPLE).scale(0.8).next_to(dec, UP, buff=0.7)
        self.play(FadeIn(base2), FadeIn(base10))


        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.set_width(config.frame_width)

class Variaveis(Scene):
    def construct(self):
        dev = SVGMobject("assets/programador")
        pc = SVGMobject("assets/computador")
        ram = SVGMobject("assets/memoria")

        grupo = VGroup(dev, pc, ram).arrange(RIGHT, buff=2).move_to(ORIGIN)

        seta1 = Arrow(start=dev.get_right(), end=pc.get_left())
        seta2 = Arrow(start=pc.get_right(), end=ram.get_left())

        self.play(FadeIn(dev))
        self.play(GrowArrow(seta1))
        self.play(FadeIn(pc))
        self.play(GrowArrow(seta2))
        self.play(FadeIn(ram))
        self.wait()
        self.play(FadeOut(*self.mobjects))

class Numero(Scene):
    def construct(self):
        num = Text("11000000 10100000 00000000 00000000", font_size=70).move_to(ORIGIN).scale(0.7)
        inteiro = Text("int: -1.063.256.064", font_size=70, t2c={'int:':PURPLE}).scale(0.7)
        flutuante = Text("float: -5.0", font_size=70, t2c={'float:':PURPLE}).scale(0.7)

        self.play(Write(num))

        copia = num.copy()
        g = VGroup(inteiro, flutuante).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        grupo = VGroup(copia, g).arrange(DOWN, buff=0.6).move_to(ORIGIN)

        self.play(num.animate.move_to(copia))
        self.wait()
        self.play(Write(inteiro))
        self.wait()
        self.play(Write(flutuante))
        self.wait()

        interrogacao = Text("?", font_size=70, color=WHITE).next_to(num, UP, buff=0.5)
        self.play(Write(interrogacao))
        self.wait()

        self.play(FadeOut(*self.mobjects))

class Background(Scene):
    def construct(self):
        num_lines = 50
        binary_string = "\n".join(
            "".join(random.choice("01") for _ in range(18))
            for _ in range(num_lines)
        )

        block1 = Text(binary_string, font="DejaVu Sans Mono", line_spacing=1).scale(0.6)
        block2 = block1.copy()

        gap = 0.2
        block1.move_to(ORIGIN)
        block2.next_to(block1, DOWN, buff=gap)

        scrolling_group = VGroup(block1, block2)
        scrolling_group.set_opacity(0)             
        self.add(scrolling_group)

        scroll_speed = 2.0
        loop_distance = block1.height + gap
        start_y = scrolling_group.get_y()

        max_opacity = 1.0                           
        opacity = ValueTracker(0)

        def background_scroll(mob, dt):
            mob.shift(UP * scroll_speed * dt)
            if mob.get_y() - start_y >= loop_distance:
                mob.shift(DOWN * loop_distance)
            mob.set_opacity(opacity.get_value() * max_opacity)

        scrolling_group.add_updater(background_scroll)

        self.play(opacity.animate.set_value(1), run_time=2)  
        self.wait()            
        self.play(opacity.animate.set_value(0), run_time=2)
        self.play(FadeOut(*self.mobjects))     

class Capitulo(Scene):
    def construct(self):
        titulo = Text("Escovando bits", weight=BOLD, t2c={"bits":"#AA77C7"}, font_size = 100).scale(0.6)
        descr = Text("Como variáveis são guardadas", weight=BOLD, font_size = 100).scale(0.3)
        criaCapitulo(self, titulo, descr, 1)    
        self.play(FadeOut(*self.mobjects))                     

class Computador(Scene):
    def construct(self):
        comp = SVGMobject("assets/computador").scale(1.5)

        texto = Text("64 bits", font_size=70, weight=BOLD).scale(0.8)

        grupo = VGroup(comp, texto).arrange(UP, buff=0.2).move_to(ORIGIN)

        self.play(FadeIn(comp), Write(texto))

        self.wait()
        self.play(FadeOut(grupo))

        linux = SVGMobject("assets/linux").scale(1.2)
        mac = SVGMobject("assets/mac")
        so = VGroup(linux, mac).arrange(RIGHT, buff=2.5).move_to(ORIGIN)
        self.play(FadeIn(so))

        self.wait()
        
        self.play(FadeOut(*self.mobjects))

class Tamanho(Scene):
    def construct(self):
        bytes = Text("int = 4 bytes", font_size=70).move_to(ORIGIN).scale(0.6)
        bits = Text("int = 32 bits", font_size=70).move_to(ORIGIN).scale(0.6)
        inicio = Text("-2³¹", font_size=70, color=PURPLE).scale(0.4)
        fim = Text("2³¹", font_size=70, color=PURPLE).scale(0.4)
        #dist = Text("Uma distância bem grande mesmo.", font_size=70).scale(0.4)

        i = Line(UP*0.1, DOWN*0.1, color=PURPLE)
        j = i.copy()

        linha = Line(LEFT, RIGHT*8, color=PURPLE)

        regua = VGroup(i, linha, j).arrange(RIGHT, buff=0).move_to(ORIGIN)
        inicio.next_to(i, DOWN, buff=0.2).shift(RIGHT*0.07)
        fim.next_to(j, DOWN, buff=0.2).shift(RIGHT*0.16)
        tam = VGroup(regua, inicio, fim)

        self.play(Write(bytes))
        self.wait()
        self.play(ReplacementTransform(bytes, bits))
        self.wait()
        b = bits.copy()
        grupo = VGroup(b, tam).arrange(DOWN, buff=0.6)
        #grupo2 = VGroup(grupo).arrange(DOWN, buff=0.8).move_to(ORIGIN)
        self.play(bits.animate.move_to(b))
        self.play(Write(tam))
        self.wait()
        #self.play(Write(dist))

        self.wait() 
        self.play(FadeOut(*self.mobjects))

class Negativos(Scene):
    def construct(self):
        pergunta = Text("Como conseguimos representar\n             números negativos?", font_size=70, color=WHITE).scale(0.6)
        resposta = Text("Complemento de dois", font_size=70, color=PURPLE).scale(0.6).next_to(pergunta, DOWN, buff=0.5)
        grupo = VGroup(pergunta, resposta).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(Write(pergunta))
        self.wait()
        self.play(FadeIn(resposta))
        self.wait() 

        self.play(FadeOut(grupo))

        significativo = Text("Bit mais significativo = ", font_size=70, color=WHITE).scale(0.6)
        zero = Text("0", font_size=70, color=WHITE).scale(0.6)
        
        gbit = VGroup(significativo, zero).arrange(RIGHT, buff=0.2)
        um = Text("1", font_size=70, color=WHITE).scale(0.6)
        zero.shift(UP*0.05)

        numero = Text("Número é ", font_size=70, color=WHITE).scale(0.6)
        positivo = Text("positivo", font_size=70, color=PURPLE).scale(0.6)
        
        npn = VGroup(numero, positivo).arrange(RIGHT, buff=0.2)
        positivo.shift(DOWN*0.06)
        negativo = Text("negativo", font_size=70, color=PURPLE).scale(0.6)

        tudo = VGroup(gbit, npn).arrange(DOWN, buff=0.2).move_to(ORIGIN)
        negativo.move_to(positivo).shift(RIGHT*0.1)
        um.move_to(zero)
        self.play(Write(gbit))
        self.play(Write(npn))
        self.wait()
        self.play(ReplacementTransform(zero, um))
        self.play(ReplacementTransform(positivo, negativo))
        self.wait()

        self.play(FadeOut(um), FadeOut(negativo), FadeOut(numero), FadeOut(significativo))

        dez = Text("1010 =", font_size=70, color=WHITE)
        d = Text("10", font_size=70, color=WHITE).next_to(dez, RIGHT, buff=0.2)
        z = Text("0", font_size=70, color=WHITE).next_to(dez, LEFT, buff=0.2)
        md = Text("-10", font_size=70, color=WHITE).next_to(dez, RIGHT, buff=0.2)
        u= Text("1", font_size=70, color=WHITE).move_to(z)

        self.play(FadeIn(dez), FadeIn(z), FadeIn(d))
        self.wait()
        self.play(ReplacementTransform(d, md), ReplacementTransform(z, u))
        g = VGroup(u, md, dez)
        x = Cross(g, color=RED, stroke_width=3)
        self.play(Write(x))
        self.wait()

        self.play(FadeOut(*self.mobjects))

class Float(Scene):
    def construct(self):
        bytes = Text("float = 4 bytes = 32 bits", font_size=70).scale(0.6)
        sem = Text("Sinal      Expoente     Mantissa", font_size=70, t2c={'Sinal': DARK_BLUE, 'Expoente': PURPLE, 'Mantissa': BLUE}).scale(0.6)
        bits = Text("1 10010011 01110000010100110100100", font_size=70).scale(0.5)

        g = VGroup(bits, sem).arrange(DOWN, buff=0.5)
        grupo = VGroup(bytes, g).arrange(DOWN, buff=0.7).move_to(ORIGIN)
        self.play(Write(bytes))
        self.play(Write(bits))
        self.wait()
        self.play(Write(sem[0:5]), bits[0].animate.set_color(DARK_BLUE))
        self.wait()
        self.play(Write(sem[5:13]), bits[1:9].animate.set_color(PURPLE))
        self.wait()
        self.play(Write(sem[13:21]), bits[9:32].animate.set_color(BLUE))
        self.wait()
        self.play(FadeOut(*self.mobjects))
        pergunta = Text("Por que expoente\n     e mantissa?", font_size=70).scale(0.9)
        self.play(Write(pergunta))
        self.wait()
        self.play(FadeOut(pergunta))

        num = MarkupText("0,1875", font_size=70)
        bin = MarkupText("0,0011", font_size=70)
        igual = MarkupText("=", font_size=70)
        notacao = MarkupText(
            "1,1 × 2<sup>−3</sup>",
            font_size=70,
        )

        self.play(Write(num))
        num2 = num.copy()

        g1 = VGroup(num2, igual, bin).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        self.play(num.animate.move_to(num2))
        self.play(Write(igual), Write(bin))
        self.wait()

        bin2 = bin.copy().move_to(ORIGIN)
        self.play(FadeOut(num, igual))
        self.play(bin.animate.move_to(bin2))
        self.wait()

        g2 = VGroup(bin2, igual, notacao).arrange(RIGHT, buff=0.2).move_to(ORIGIN)
        self.play(bin.animate.move_to(bin2))
        self.play(Write(igual), Write(notacao))
        self.wait()

        notacao2 = notacao.copy().move_to(ORIGIN)
        self.play(FadeOut(bin, igual))
        self.play(notacao.animate.move_to(notacao2))

        b = MarkupText("0 01111100* 10000000000000000000000", font_size=70).scale(0.7)
        note = MarkupText("*Omitido por fins didáticos: para evitar números\n          negativos, somamos 127 ao expoente", font_size=70).scale(0.3).to_edge(DOWN, buff=0.2)

        g3 = VGroup(notacao2, b).arrange(DOWN, buff=0.5).move_to(UP*0.4)
        self.play(notacao.animate.move_to(notacao2))
        self.play(FadeIn(b[0]))
        self.wait()
        
        self.play(FadeIn(b[10:33]))
        self.wait()

        self.play(FadeIn(b[1:10]))
        self.play(FadeIn(note))
        self.wait()
        self.play(FadeOut(*self.mobjects))


#PARTE 2
class Modificadores(Scene):
    def construct(self):
        modificadores = Text("Modificadores de tipo",font_size=100).scale(0.6)
        self.play(FadeIn(modificadores))
        self.play(modificadores.animate.move_to([0,2,0]))

        COR_MOD1 = "#AA77C7"
        COR_MOD2 = "#58C4DD"
        COR_MOD3 = "#236B8E"

        def criar_palavra(texto, cor=WHITE):
            completo = Text(f"H{texto}g", font="Monospace", font_size=100, color=cor).scale(0.4)
            completo[0].set_opacity(0)
            completo[-1].set_opacity(0)
            return completo

        nome_var = criar_palavra("var")
        mod_sinal = criar_palavra("unsigned", COR_MOD1)
        mod_tamanho = criar_palavra("long", COR_MOD2)
        mod_tipo = criar_palavra("int", COR_MOD3)

        modificadores = [mod_sinal, mod_tamanho, mod_tipo]

        # ------------------------------------------------------------------
        # Slots de largura IGUAL (baseada na palavra mais larga, "unsigned"),
        # assim nenhuma combinação de troca gera overlap. Cada palavra é
        # CENTRALIZADA dentro do seu slot (não alinhada pela esquerda), o que
        # deixa o espaço em branco simétrico dos dois lados — visualmente mais
        # parelho do que alinhar pela borda.
        # ------------------------------------------------------------------
        LARGURA_SLOT = max(m.get_width() for m in modificadores) + 0.5
        centros_x_iniciais = [0, LARGURA_SLOT, 2 * LARGURA_SLOT]

        for palavra, cx in zip(modificadores, centros_x_iniciais):
            palavra.move_to(ORIGIN)
            palavra.align_to(ORIGIN, DOWN)          # baseline unificada (truque do H/g)
            y = palavra.get_center()[1]
            palavra.move_to([cx, y, 0])             # centraliza no slot, mantendo a baseline

        grupo_modificadores = VGroup(*modificadores)
        nome_var.next_to(grupo_modificadores, RIGHT, buff=0.4, aligned_edge=DOWN)

        declaracao = VGroup(grupo_modificadores, nome_var)
        declaracao.move_to(ORIGIN)

        # --- Centros reais dos slots, capturados DEPOIS do layout final ---
        centros_x = [m.get_center()[0] for m in modificadores]
        baseline_y = modificadores[0].get_center()[1]

        # --- Colchete deitado cobrindo os modificadores (sem cor) ---
        def colchete_deitado(mob, cor=WHITE, altura=0.2):
            largura = mob.get_width()
            pontos = [
                [-largura / 2, altura, 0],
                [-largura / 2, 0, 0],
                [largura / 2, 0, 0],
                [largura / 2, altura, 0],
            ]
            colchete = VMobject(color=cor, stroke_width=3)
            colchete.set_points_as_corners(pontos)
            colchete.next_to(mob, DOWN, buff=0.15)
            return colchete

        colchete_opcional = colchete_deitado(grupo_modificadores)

        label_opcional = Text("opcional", font="Monospace", font_size=100).scale(0.28)
        label_opcional.next_to(colchete_opcional, DOWN, buff=0.2)

        # --- Animação ---
        self.play(FadeIn(nome_var))
        self.wait()

        self.play(Write(mod_sinal), Write(mod_tamanho), Write(mod_tipo))
        self.wait()

        self.play(Create(colchete_opcional), FadeIn(label_opcional))
        self.wait()

        DESLOCAMENTO_FINAL = 0.6  # aumente/diminua para ajustar o quanto "pra trás"

        self.play(
            mod_sinal.animate.move_to([centros_x[1] - DESLOCAMENTO_FINAL, baseline_y, 0]),
            mod_tamanho.animate.move_to([centros_x[2] - DESLOCAMENTO_FINAL, baseline_y, 0]),
            mod_tipo.animate.move_to([centros_x[0] - DESLOCAMENTO_FINAL, baseline_y, 0]),
        )
        self.wait()
        self.play(FadeOut(*self.mobjects))

class Signed(Scene):
    def construct(self):
        titulo = criar_texto("signed", cor=WHITE, tamanho=0.6)
        titulo.to_edge(UP, buff=1.0)

        numeros = [10, -32, 100, -7, 67, -42]

        valor_atual = numeros[0]
        bits_completo = format(valor_atual & 0xFF, "08b")

        bit_sinal = criar_texto(bits_completo[0], cor=COR_SINAL)
        bits_resto = criar_texto(bits_completo[1:], cor=WHITE)
        binario = VGroup(bit_sinal, bits_resto).arrange(RIGHT, buff=0.1)
        binario.move_to(UP * 0.8)

        numero_decimal = criar_texto(f"{valor_atual}", cor=WHITE)
        numero_decimal.next_to(binario, DOWN, buff=0.9)
        seta = Arrow(binario.get_bottom(), numero_decimal.get_top(), buff=0.15, color=GRAY, stroke_width=3)

        self.play(Write(titulo))
        self.wait()

        self.play(Write(bit_sinal), Write(bits_resto))
        self.wait()

        self.play(GrowArrow(seta), Write(numero_decimal))
        self.wait()

        self.play(bit_sinal.animate.shift(LEFT * 0.4))
        self.wait(0.3)

        colchete_sinal = colchete_deitado(bit_sinal, cor=COR_SINAL)
        label_sinal = criar_texto("sinal", cor=COR_SINAL, tamanho=0.28)
        label_sinal.next_to(colchete_sinal, DOWN, buff=0.2)

        self.play(Create(colchete_sinal), FadeIn(label_sinal))
        self.wait()


        for valor in numeros[1:]:
            bits_completo = format(valor & 0xFF, "08b")

            novo_bit_sinal = criar_texto(bits_completo[0], cor=COR_SINAL).move_to(bit_sinal)
            novo_bits_resto = criar_texto(bits_completo[1:], cor=WHITE).move_to(bits_resto)
            novo_numero = criar_texto(f"{valor}", cor=WHITE).move_to(numero_decimal, aligned_edge=LEFT)

            self.play(
                Transform(bit_sinal, novo_bit_sinal),
                Transform(bits_resto, novo_bits_resto),
                Transform(numero_decimal, novo_numero),
            )
            self.wait()

        self.wait()
        self.play(FadeOut(*self.mobjects))

class Unsigned(Scene):
    def construct(self):
        padrao = Text("Padrão ou Default", t2c={"Padrão": "#AA77C7", "Default": "#AA77C7"})

        self.play(Write(padrao))
        self.wait()
        self.play(Unwrite(padrao))


        titulo = criar_texto("unsigned", cor=WHITE, tamanho=0.6)
        titulo.to_edge(UP, buff=1.0)

        valor_magnitude = 10
        bits_magnitude = format(valor_magnitude, "07b")  # "0001010"

        bit_msb = criar_texto("0", cor=COR_SINAL)
        bits_resto = criar_texto(bits_magnitude, cor=WHITE)

        binario = VGroup(bit_msb, bits_resto).arrange(RIGHT, buff=0.1)
        binario.move_to(UP * 0.8)

        numero_decimal = criar_texto(f"{valor_magnitude}", cor=WHITE)
        numero_decimal.next_to(binario, DOWN, buff=0.9)

        seta = Arrow(binario.get_bottom(), numero_decimal.get_top(), buff=0.15, color=GRAY, stroke_width=3)

        self.play(Write(titulo))
        self.wait()

        self.play(Write(bit_msb), Write(bits_resto))
        self.wait()

        self.play(GrowArrow(seta), Write(numero_decimal))
        self.wait()

        self.play(bit_msb.animate.shift(LEFT * 0.4))
        self.wait(0.3)

        colchete_msb = colchete_deitado(bit_msb, cor=COR_SINAL)
        label_msb = criar_texto("valor", cor=COR_SINAL, tamanho=0.24)
        label_msb.next_to(colchete_msb, DOWN, buff=0.2)

        self.play(Create(colchete_msb), FadeIn(label_msb))
        self.wait()

        # Agora, ao ligar o bit mais significativo, o número só CRESCE — não vira negativo
        bit_um = criar_texto("1", cor=COR_SINAL).move_to(bit_msb)
        numero_maior = criar_texto("138", cor=WHITE).move_to(numero_decimal, aligned_edge=LEFT)

        aviso_sem_negativo = criar_texto("nunca fica negativo!", cor=GRAY, tamanho=0.24)
        aviso_sem_negativo.next_to(numero_decimal, RIGHT, buff=0.6)

        self.play(
            Transform(bit_msb, bit_um),
            Transform(numero_decimal, numero_maior),
        )
        self.play(FadeIn(aviso_sem_negativo, shift=RIGHT * 0.2))
        self.wait()

        bit_zero = criar_texto("0", cor=COR_SINAL).move_to(bit_msb)
        numero_original = criar_texto(f"{valor_magnitude}", cor=WHITE).move_to(numero_decimal, aligned_edge=LEFT)

        self.play(
            Transform(bit_msb, bit_zero),
            Transform(numero_decimal, numero_original),
            FadeOut(aviso_sem_negativo),
        )
        self.wait()

        # Limpa a tela pra segunda parte
        self.play(*[FadeOut(m) for m in [titulo, binario, seta, numero_decimal, colchete_msb, label_msb]])
        self.wait(0.3)

        # Barra centralizada


        LARGURA_BASE = 3.0
        LARGURA_FINAL = LARGURA_BASE * 2
        ALTURA_BARRA = 0.6
        borda_esquerda_final = -LARGURA_FINAL / 2
        centro_x_inicial = borda_esquerda_final + LARGURA_BASE / 2

        # --- Linha do topo com a limitação (intervalo signed) ---
        label_min_signed = formatar_potencia("-2", "31", cor=GRAY)
        label_ate = criar_texto("até", cor=WHITE, tamanho=0.35)
        label_max_signed = VGroup(
            formatar_potencia("2", "31", cor=COR_SINAL),
            criar_texto("- 1", cor=COR_SINAL),
        ).arrange(RIGHT, buff=0.15)

        linha_limite = VGroup(label_min_signed, label_ate, label_max_signed).arrange(RIGHT, buff=0.6)
        linha_limite.move_to([0, 2, 0])

        barra = Rectangle(width=LARGURA_BASE, height=ALTURA_BARRA, color=COR_SINAL, fill_color=COR_SINAL, fill_opacity=0.6)
        barra.move_to([centro_x_inicial, -0.5, 0])

        valor_texto_31 = criar_texto("2.147.483.647", cor=COR_SINAL, tamanho=0.32)
        valor_texto_31.next_to(barra, DOWN, buff=0.3).align_to(barra, LEFT)

        marca_antiga = DashedLine(
                    barra.get_corner(UR) + UP * 0.15,
                    barra.get_corner(DR) + DOWN * 0.15,
                    color=GRAY,
                    stroke_width=3,
                )

        self.play(Write(label_min_signed), Write(label_ate), Write(label_max_signed), GrowFromCenter(barra), Write(valor_texto_31), Create(marca_antiga))
        self.wait()



        self.wait()

        

        label_min_unsigned = criar_texto("0", cor=GRAY).move_to(label_min_signed).align_to(label_min_signed, DOWN)
        label_max_unsigned = VGroup(
            formatar_potencia("2", "32", cor=COR_SINAL),
            criar_texto("- 1", cor=COR_SINAL),
        ).arrange(RIGHT, buff=0.15).move_to(label_max_signed).align_to(label_max_signed, DOWN)

        valor_texto_32 = criar_texto("4.294.967.295", cor=COR_SINAL, tamanho=0.32)
        valor_texto_32.next_to(barra, DOWN, buff=0.3).align_to(barra, LEFT)
        
        self.play(
            barra.animate.stretch_to_fit_width(LARGURA_FINAL, about_edge=LEFT),
            Transform(label_min_signed, label_min_unsigned),
            Transform(label_max_signed, label_max_unsigned),
            Transform(valor_texto_31, valor_texto_32),
            run_time=2,
        )
        self.wait()

        self.play(FadeOut(*self.mobjects))

class Tamanho2(Scene):
    def construct(self):
        def criar_bytes(qtd, cor=WHITE, lado=0.5, buff=0.15):
            quadrados = VGroup(*[
                Square(side_length=lado, color=cor, fill_color=cor, fill_opacity=0.25, stroke_width=2)
                for _ in range(qtd)
            ])
            quadrados.arrange(RIGHT, buff=buff)
            return quadrados

        # Titulo
        titulo = Text("Modificador de tamanho", font_size=100).scale(0.6)
        titulo.to_edge(UP, buff=0.8)

        # Topico
        bolinha_short = Dot(color="#AA77C7", radius=0.06)
        palavra_short = Text("short", font_size=100, color="#AA77C7").scale(0.5)
        topico_short = VGroup(bolinha_short, palavra_short).arrange(RIGHT, buff=0.2)

        bolinha_long = Dot(color="#AA77C7", radius=0.06)
        palavra_long = Text("long", font_size=100, color="#AA77C7").scale(0.5)
        topico_long = VGroup(bolinha_long, palavra_long).arrange(RIGHT, buff=0.2)

        topicos = VGroup(topico_short, topico_long).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        topicos.move_to(ORIGIN)

        self.play(Write(titulo))
        self.play(Write(topico_short),Write(topico_long))
        self.wait()

        self.play(FadeOut(topicos))
        self.wait()

        # int var
        declaracao = Text("int var", font_size=100, t2c={"int":"#AA77C7"}).scale(0.5)
        declaracao.move_to([0,0.5,0])

        bytes_int = criar_bytes(4, cor="#58C4DD")
        bytes_int.next_to(declaracao, DOWN, buff=0.6)

        label_bytes_int = Text("4 bytes", font_size=100, color="#58C4DD").scale(0.3)
        label_bytes_int.next_to(bytes_int, DOWN, buff=0.3)

        self.play(FadeIn(declaracao), FadeIn(bytes_int), FadeIn(label_bytes_int))
        self.wait()

        # short int var
        declaracao_short = Text("short int var", font_size=100, t2c={"short int":"#AA77C7"}).scale(0.5)
        declaracao_short.move_to(declaracao, aligned_edge=DOWN)

        bytes_short = criar_bytes(2, cor="#58C4DD")
        bytes_short.next_to(declaracao_short, DOWN, buff=0.6)

        label_bytes_short = Text("2 bytes", font_size=100, color="#58C4DD").scale(0.3)
        label_bytes_short.next_to(bytes_short, DOWN, buff=0.3)

        # long int var
        declaracao_long = Text("long int var", font_size=100, t2c={"long int":"#AA77C7"}).scale(0.5)
        declaracao_long.move_to(declaracao, aligned_edge=DOWN)

        bytes_long = criar_bytes(8, cor="#58C4DD")
        bytes_long.next_to(declaracao_short, DOWN, buff=0.6)

        label_bytes_long = Text("8 bytes", font_size=100, color="#58C4DD").scale(0.3)
        label_bytes_long.next_to(bytes_long, DOWN, buff=0.3)

        # float var
        declaracao_float = Text("float var", font_size=100, t2c={"float":"#AA77C7"}).scale(0.5)
        declaracao_float.move_to(declaracao, aligned_edge=DOWN)

        bytes_float = criar_bytes(4, cor="#58C4DD")
        bytes_float.next_to(declaracao_short, DOWN, buff=0.6)

        label_bytes_float = Text("4 bytes", font_size=100, color="#58C4DD").scale(0.3)
        label_bytes_float.next_to(bytes_float, DOWN, buff=0.3)

        self.play(
            Transform(declaracao, declaracao_short),
            Transform(bytes_int,bytes_short),
            Transform(label_bytes_int,label_bytes_short)
        )
        self.wait()
        self.play(
            Transform(declaracao, declaracao_long),
            Transform(bytes_int,bytes_long),
            Transform(label_bytes_int,label_bytes_long)
        )
        self.wait()
        self.play(
            FadeOut(titulo),
            Transform(declaracao, declaracao_float),
            Transform(bytes_int,bytes_float),
            Transform(label_bytes_int,label_bytes_float)
        )
        self.wait()

        self.play(FadeOut(*self.mobjects))

class Longfloat(Scene):
    def construct(self):
        pergunta = Text("long float?", font_size=100, t2c={"long float":"#AA77C7"}).scale(0.8)
        pergunta.move_to(ORIGIN)

        self.play(Write(pergunta))
        self.wait()

        risco = Line(pergunta.get_left(), pergunta.get_right(), color=RED, stroke_width=10)
        self.play(Create(risco))
        self.wait()

        # risco
        self.play(FadeOut(pergunta), FadeOut(risco))
        self.wait()

        # Double
        double_texto = Text("double", font_size=100, color="#AA77C7").scale(0.8)

        self.play(FadeIn(double_texto))
        self.wait()
        self.play(FadeOut(double_texto))

        # Casas
        linha_float = Text("float -> 6 a 7 casas decimais*", font_size=100, t2c={"float":"#AA77C7", "6":"#58C4DD", "7": "#58C4DD","*":"#AA77C7"}).scale(0.4).move_to([0,0.5,0])
        linha_double = Text("double -> até 15 casas decimais*", font_size=100, t2c={"double":"#AA77C7", "15":"#58C4DD","*":"#AA77C7"}).scale(0.4)
        asterisco = Text("*Dígitos significativos no total (contando antes e depois da vírgula).", font_size=100, color="#AA77C7").scale(0.2)

        linhas = VGroup(linha_float, linha_double,asterisco).arrange(DOWN, buff=0.5)

        self.play(Write(linha_float))
        self.wait()
        self.play(Write(linha_double))
        self.wait()
        self.play(FadeIn(asterisco))
        self.wait()

        self.play(Unwrite(linha_float), Unwrite(linha_double), FadeOut(asterisco))
        self.wait()

class Void(Scene):
    def construct(self):
        void = Text("void",color="#AA77C7",font_size=100)

        self.play(FadeIn(void))
        self.wait()
        self.play(FadeOut(void))

        # Proximo
        funcao = Text("void funcao(){}", t2c={"void": "#58C4DD", "funcao": GREEN_C}, font_size=100).scale(0.6)
        texto = Text("Executa, e não retorna nada", font_size=100, color=GRAY).scale(0.35)

        grupo = VGroup(funcao, texto).arrange(DOWN, buff=0.3)

        self.play(Write(funcao))
        self.play(FadeIn(texto, shift=UP * 0.2))
        self.wait()
        self.play(FadeOut(*self.mobjects))

class Char(Scene):
    def construct(self):
            # char
            char_texto = Text("char", font_size=100, color="#AA77C7").scale(0.5)
            byte_texto = Text("1 byte", font_size=100).scale(0.5)
            intervalo_texto = Text("0 a 255", font_size=100, t2c={"0":"#AA77C7", "255":"#AA77C7"}).scale(0.5)

            grupo = VGroup(char_texto, byte_texto, intervalo_texto).arrange(RIGHT, buff=1.2)

            seta1 = Arrow(char_texto.get_right(), byte_texto.get_left(), buff=0.15)
            seta2 = Arrow(byte_texto.get_right(), intervalo_texto.get_left(), buff=0.15)

            self.play(Write(char_texto))
            self.play(GrowArrow(seta1), Write(byte_texto))
            self.play(GrowArrow(seta2), Write(intervalo_texto))
            self.wait()
            self.play(FadeOut(*self.mobjects))

            # Tabela Ascii
            tabela_ascii = Text("Tabela ASCII = 127 valores", font_size=100,t2c={"ASCII":"#AA77C7","127":"#58C4DD"}).scale(0.5)
            tabela_ascii.move_to(ORIGIN)

            self.play(FadeIn(tabela_ascii))
            self.wait()

            # Afasta e dim
            self.play(tabela_ascii.animate.set_opacity(0.4))

            self.wait()
            self.play(FadeOut(*self.mobjects))

class Xerox(MovingCameraScene):
    def construct(self):
        xerox = SVGMobject("./svg/xerox.svg")
        texto = Text("1986 - 1987",font_size=100,color=GRAY).scale(0.4)

        grupo = VGroup(xerox, texto).arrange(DOWN, buff=0.5)

        self.play(FadeIn(grupo))
        self.wait()

        mundo = SVGMobject("./svg/world.svg")
        unicode = Text("Unicode",color="#AA77C7",font_size=100).scale(0.7)
        char = Text("1-4 bytes por char",t2c={"bytes":"#236B8E","char": "#58C4DD"})

        grupo_unicode = VGroup(mundo, unicode, char).arrange(DOWN, buff=0.5)

        # Move o grupo pela diferença entre onde "unicode" está e y=0,
        # em vez de centralizar a bounding box inteira (que fica enviesada
        # pelo tamanho do mundo/char).
        grupo_unicode.shift(DOWN * unicode.get_center()[1])

        grupo_unicode.next_to(self.camera.frame, RIGHT, buff=3.5)
        grupo_unicode.shift(UP * (0 - unicode.get_center()[1]))  # garante y=0 após o next_to horizontal

        posicao_camera_original = self.camera.frame.get_center()

        self.add(unicode)

        self.play(self.camera.frame.animate.move_to(unicode))
        self.wait()
        self.play(FadeIn(mundo))
        self.wait()
        self.play(FadeIn(char))
        self.wait()

        self.play(FadeOut(*self.mobjects))
        self.play(self.camera.frame.animate.move_to(posicao_camera_original))

class Testar(MovingCameraScene):
    def construct(self):
        testar = Text("Testar!",t2c={"Testar":"#AA77C7"},font_size=100)
        self.add(testar)
        self.wait()
        self.play(FadeOut(testar))

        unsigned_char = Text("unsigned char var",t2c={"unsigned char":"#AA77C7"})
        short_long_int = Text("short long int var",t2c={"short long int":"#AA77C7"})
        reticencias = Text("...",color="#AA77C7")

        grupo_tipos = VGroup(unsigned_char, short_long_int, reticencias).arrange(DOWN, buff=0.5)

        codigo = Text(
            'printf("%u", numero);',
            t2c={"%u": "#58C4DD", "printf": GREEN_C},
            font_size=100,
        ).scale(0.5)

        self.play(FadeIn(unsigned_char))
        self.play(FadeIn(short_long_int))
        self.play(FadeIn(reticencias))

        self.play(FadeOut(grupo_tipos))

        self.play(Write(codigo))
        self.wait()
        self.play(Unwrite(codigo))

class Final(MovingCameraScene):
    def construct(self):
        logo = ImageMobject("png/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        # O cursor
        cursorVinheta=ImageMobject("png/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)


        # --- CENA 30 ---- "Proxima aula"
        final_text1 = Text("Próxima aula:",font_size=60)
        final_text2 = Text("Compilador e erros",font_size=75, t2c={"erros":"#AA77C7"})
        final = VGroup(final_text1, final_text2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(.7)

        self.play(Write(final))
        self.wait()


        # Aplausos, Cortinas, Pão e Circo
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

        # creditos
