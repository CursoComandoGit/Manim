from manim import *
import struct

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope")
MarkupText.set_default(font = "Manrope")
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

class AulaCompleta(MovingCameraScene):
    def construct(self):
        # Nova ordem de animações

        Char.construct(self)
        Xerox.construct(self)
        Void.construct(self)
        Modificadores.construct(self)
        Signed.construct(self)
        Unsigned.construct(self)
        Tamanho.construct(self)
        Longfloat.construct(self)
        Testar.construct(self)
        Final.construct(self)

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

class Tamanho(Scene):
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
