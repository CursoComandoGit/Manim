from manim import *

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope")
MarkupText.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

codigoSoma = '''#include <stdio.h>

int main(){
    int valor1;
    float valor2, soma;

    valor1 = 6;
    valor2 = 4.5;
    soma = valor1 + valor2;

    printf("A soma do valor 1 e 2 é igual a %f", soma);
    return 0;
}
'''

class Aula5(Scene):
    def construct(self):
        #cenas

        segundoConjuntoRegras.construct(self)
        soma.construct(self)
        tiposPrimitivos.construct(self)
        tipoInt.construct(self)
        tipoFloat.construct(self)
        contaCaractereValor2.construct(self)
        intChar.construct(self)
        tipoChar.construct(self)
        tipoString.construct(self)


class segundoConjuntoRegras(Scene):
    def construct(self):
        titulo = Text("Tipos de variáveis", t2c = {"Tipos": PURPLE}, font_size = 80).scale(0.8)
        titulo.move_to(ORIGIN)

        self.play(Write(titulo))
        self.wait(1.2)
        self.play(FadeOut(titulo))



class soma(Scene):
    def construct(self):

        rendered_codigoSoma = Code(
            code_string=codigoSoma, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)


        self.play(Create(rendered_codigoSoma), run_time = 3)
        self.play(rendered_codigoSoma.animate.shift(LEFT * 1.2))

        declaracao1 = Underline(VGroup(*rendered_codigoSoma.code_lines[3]), stroke_width = 1.6)
        declaracao1.shift(UP * 0.05)

        declaracao2 = Underline(VGroup(*rendered_codigoSoma.code_lines[4]), stroke_width = 1.6)
        declaracao2.shift(UP * 0.05)

        retanguloInt = RoundedRectangle(
            corner_radius=0.2,
            color=BLUE_D,
            width=1.5,
            height=1.2
        ).shift(UP * 1)

        tipoInt = Text(
            "Int",
            font_size=32,
            color=BLUE_D
        )

        valor1 = Text(
            "valor1",
            font_size=120
        ).scale(0.12)

        tipoInt.next_to(
            retanguloInt,
            UP,
            buff=0.15
        )

        valor1.move_to(
            retanguloInt.get_top() + DOWN * 0.25
        )


        retanguloFloat = RoundedRectangle(
            corner_radius=0.2,
            color=RED_E,
            width=1.5,
            height=1.2
        ).shift(UP * 1).next_to(retanguloInt, RIGHT * 3)

        tipoFloat = Text(
            "Float",
            font_size=32,
            color=RED_E,
            disable_ligatures=True
        )

        valor2 = Text(
            "valor2",
            font_size=120
        ).scale(0.12)

        tipoFloat.next_to(
            retanguloFloat,
            UP,
            buff=0.15
        )

        valor2.move_to(
            retanguloFloat.get_top() + DOWN * 0.25
        )
        

        linhaValor1 = rendered_codigoSoma.code_lines[6]
        linha_copia1 = linhaValor1.copy()

        valor6 = Text(
            "6",
            font_size=32
        )

        valor6.move_to(
            retanguloInt.get_center() + DOWN * 0.15
        )

        linhaValor2 = rendered_codigoSoma.code_lines[7]
        linha_copia2 = linhaValor2.copy()


        valor4eMeio = Text(
            "4.5",
            font_size=32
        )

        valor4eMeio.move_to(
            retanguloFloat.get_center() + DOWN * 0.15
        )

        grupoInt = VGroup(tipoInt, retanguloInt, valor1, linha_copia1)
        grupoFloat = VGroup(tipoFloat, retanguloFloat, valor2, linha_copia2)
        
        gruposDeclaracao = VGroup(grupoInt, grupoFloat)


        self.play(Create(declaracao1), Write(tipoInt))
        self.play(Create(retanguloInt), FadeIn(valor1))

        self.play(Create(declaracao2), Write(tipoFloat))
        self.play(Create(retanguloFloat), FadeIn(valor2))

        self.play(Uncreate(declaracao1), Uncreate(declaracao2))

        self.add(linha_copia1)
        self.add(linha_copia2)

        self.play(
            Transform(
                linha_copia1,
                valor6
            ),
            run_time=1.5,
            rate_func=smooth
        )
        self.play(
            Transform(
                linha_copia2,
                valor4eMeio
            ),
            run_time=1.5,
            rate_func=smooth
        )

        


        self.play(gruposDeclaracao.animate.scale(0.65).shift(LEFT * 1.2))

        #retangulo soma

        indicarSoma = rendered_codigoSoma.code_lines[8]

        retanguloSoma = RoundedRectangle(
            corner_radius=0.2,
            color=RED_E,
            width=1.5,
            height=1.2
        )

        tipoSoma = Text(
            "Float",
            font_size=32,
            color=RED_E,
            disable_ligatures=True
        )

        valorSoma = Text(
            "soma",
            font_size=120
        ).scale(0.12)

        tipoSoma.next_to(
            retanguloSoma,
            UP,
            buff=0.15
        )

        valorSoma.move_to(
            retanguloSoma.get_top() + DOWN * 0.25
        )
        grupoSoma = VGroup(tipoSoma, retanguloSoma, valorSoma)
        grupoSoma.scale(0.65)

        grupoSoma.next_to(
            gruposDeclaracao,
            RIGHT * 2
        )

        
        self.play(Indicate(indicarSoma))
        self.play(Write(tipoSoma), Create(retanguloSoma), FadeIn(valorSoma))


        seis = linha_copia1.copy()
        quatroMeio = linha_copia2.copy()

        pontoMeio = retanguloSoma.get_top() + UP * 1
        seis_destino = seis.copy()
        quatroMeio_destino = quatroMeio.copy()

        seis_destino.move_to(pontoMeio)
        quatroMeio_destino.move_to(pontoMeio)

        self.play(
            TransformFromCopy(linha_copia1, seis_destino),
            TransformFromCopy(linha_copia2, quatroMeio_destino),
            run_time=1.2,
            rate_func=smooth
        )

        resultado = Text(
            "10.5",
            font_size=22
        )

        resultado.move_to(pontoMeio)

        printfSoma = rendered_codigoSoma.code_lines[10]

        self.play(
            Transform(seis_destino, resultado),
            FadeOut(quatroMeio_destino),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            seis_destino.animate.move_to(
                retanguloSoma.get_center() + DOWN * 0.10
            ),
            run_time=1.2,
            rate_func=smooth
        )

        self.play(Circumscribe(printfSoma, buff=0.05, fade_out=True, stroke_width = 1.4), run_time=2)
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class tiposPrimitivos(Scene):
    def construct(self):
        tipos = [
            ("int", BLUE_D, "42"),
            ("float", RED_E , "3.14"),
            ("char", GREEN_C, "'A'"),
            ("double", LIGHT_PINK, "3.141592"),
            ("void", TEAL, "∅"),
        ]

        def criar_card(nome, cor, exemplo):
            caixa = RoundedRectangle(
                width=2.2, height=2.4, corner_radius=0.2, color=cor, fill_color=cor, fill_opacity=0.15, stroke_width=3
            )
            rotulo_nome = Text(nome, font_size=30, color=cor, weight=BOLD, disable_ligatures=True)
            rotulo_exemplo = Text(exemplo, font_size=26)
            conteudo = VGroup(rotulo_nome, rotulo_exemplo).arrange(DOWN, buff=0.5)
            conteudo.move_to(caixa.get_center())
            return VGroup(caixa, conteudo)
        
        cards = VGroup(*[criar_card(n, c, e) for n, c, e in tipos])
        cards.arrange(RIGHT, buff=0.5).move_to(ORIGIN)

        for card in cards:
            card.shift(DOWN * 5) #posição inicial na tela

        for card in cards:
            self.play(card.animate.shift(UP * 5), run_time = 0.5)
            self.wait(0.2)

        self.wait(1)

        direcoes = [
            UL,     #int 
            LEFT,   #float
            DOWN,   #char
            RIGHT,  #double
            UR      #void
        ]

        animacao = [
            card.animate.shift(direcao * 8).rotate(PI / 6 * (1 if i % 2 == 0 else -1))
            for i, (card, direcao) in enumerate(zip(cards, direcoes))
        ]

        self.play(*animacao, run_time = 1.5, rate_func=rate_functions.ease_in_cubic)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        
class tipoInt(Scene):
    def construct(self):
        tituloInt = Text("int", font_size = 160).scale(0.5)
        tituloInt.move_to(ORIGIN)

        inteiros = MathTex(r"\mathbb{Z} = \{..., -3, -2, -1, 0, 1, 2, 3, ...\}")

        boxRetangular = (
            SurroundingRectangle(
                inteiros,
                corner_radius=0.3,
                buff=0.2
            )
            .set_stroke("#AA77C7", width=2)
            .set_fill("#8728BE", opacity=0.1)
        )

        naoInteiro = MathTex("3,14")
        naoInteiro.next_to(inteiros, DOWN, buff = 1)

        rendered_codigoSoma = Code(
            code_string=codigoSoma, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)

        nomeRect = Rectangle(width=2.5, height=0.6)
        valorRect = Rectangle(width=1, height=0.6)

        bloco = VGroup(
            nomeRect,
            valorRect
        ).arrange(RIGHT, buff=0)
        bloco.set_stroke(BLUE_D, width=2)
        bloco.set_fill(BLUE_D, opacity=0.1)

        nomeTxt = Text(
            "valor1",
            font_size=20,
            disable_ligatures=True
        )

        valorTxt = Text(
            "6",
            font_size=24
        ).move_to(valorRect)

        blocoMemoria = VGroup(
            bloco,
            nomeTxt, 
            valorTxt
        )

        trechoQuantidade = VGroup(*rendered_codigoSoma.code_lines[3])
        trechoNumero = VGroup(*rendered_codigoSoma.code_lines[6])


        self.play(Write(tituloInt))
        self.play(tituloInt.animate.move_to([0,2.5,0]))

        self.play(Write(boxRetangular))
        self.play(Write(inteiros))
        self.play(ApplyWave(inteiros))
        self.play(FadeIn(naoInteiro))
        self.play(Write(Cross(naoInteiro, stroke_width = 2.6)))
        self.wait(2)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        
        self.play(FadeIn(rendered_codigoSoma))

        self.play(rendered_codigoSoma.animate.scale(0.8))
        self.play(rendered_codigoSoma.animate.shift(LEFT * 2.5), run_time=1.2, rate_func=smooth)
        bloco.move_to(rendered_codigoSoma.get_center()).next_to(rendered_codigoSoma, buff = 1)
        nomeTxt.move_to(nomeRect)
        valorTxt.move_to(valorRect)

        self.play(Create(bloco))

        self.play(
            TransformFromCopy(
                trechoQuantidade,
                nomeTxt
            )
        )

        self.play(
            TransformFromCopy(
                trechoNumero,
                valorTxt
            )
        )

        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


class tipoFloat(Scene):
    def construct(self):
        tituloFloat = Text(
            "float",
            font_size=160,
            disable_ligatures=True
        ).scale(0.5)            
        tituloFloat.move_to(ORIGIN)    

        retaNumerica = DoubleArrow(
            LEFT * 5,
            RIGHT * 5,
            buff = 0,
            tip_length=0.2,
            stroke_width=4, 
            color = PURE_YELLOW
        )

        marcaCentro = Line(
            UP * 0.15,
            DOWN * 0.15,
            stroke_width=3,
            color = PURE_YELLOW
        )

        marcaCentro.move_to(retaNumerica.get_center())

        zero = MathTex("0", font_size=24)

        zero.next_to(
            marcaCentro,
            DOWN,
            buff = 0.15
        )

        grupoReta = Group(retaNumerica, marcaCentro)

        # Valor de 0 a 3.4
        tracker = ValueTracker(0)

        menorFloat = always_redraw(
            lambda: MathTex(
                rf"-{tracker.get_value():.1f}\times10^{{38}}",
                font_size=40,
                color=BLUE
            ).next_to(retaNumerica.get_left(), DOWN, buff=0.2)
        )

        maiorFloat = always_redraw(
            lambda: MathTex(
                rf"{tracker.get_value():.1f}\times10^{{38}}",
                font_size=40,
                color=BLUE
            ).next_to(retaNumerica.get_right(), DOWN, buff=0.2)
        )

        posicaoFinalTexto = retaNumerica.get_center() + UP * 0.8

        # aparece o codigo para mostrar um exemplo de float
        rendered_codigoSoma = Code(
            code_string=codigoSoma, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)

        sublinhadoFloat = Underline(VGroup(*rendered_codigoSoma.code_lines[4]), stroke_width = 1.6)
        sublinhadoFloat.shift(UP * 0.05)
        
        destacarPreco = VGroup(*rendered_codigoSoma.code_lines[7])

        self.play(Write(tituloFloat))
        self.play(tituloFloat.animate.move_to([0,2.5,0]))
        self.wait()

        self.play(
            GrowFromCenter(grupoReta),
            run_time=1.2,
            rate_func=smooth
        )
        self.play(
            FadeIn(menorFloat),
            FadeIn(zero),
            FadeIn(maiorFloat)
        )
        
        self.play(
            tracker.animate.set_value(3.4),
            run_time=3,
            rate_func=linear
        )

        self.play(tituloFloat.animate.move_to(posicaoFinalTexto), run_time = 1.8, rate_func = rate_functions.ease_out_bounce)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.play(FadeIn(rendered_codigoSoma))
        self.play(Create(sublinhadoFloat))

        self.wait(2)

        self.play(Indicate(destacarPreco))

        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


class contaCaractereValor2(Scene):
    def construct(self):
        # expressão
        num1 = Text("1", font_size=60)
        mais = Text("+", font_size=60)
        char1 = Text("'1'", font_size=60)
        igual = Text("=", font_size=60)
        inter = Text("?", font_size=60)

        soma = VGroup(num1, mais, char1, igual, inter).arrange(RIGHT, buff=0.25)

        um = char1[1]

        num49 = Text("49", font_size=40, color=PURE_YELLOW)

        soma.move_to(ORIGIN)
        num49.next_to(um, DOWN, buff=1.3)
        num49.shift(RIGHT * 0.06)

        seta = Arrow(
            start=um.get_bottom() + RIGHT * 0.06,
            end=num49.get_top(),
            buff=0.1,
            color=PURE_YELLOW
        )
        

        self.play(Write(soma))
        self.wait(0.5)

        self.play(GrowArrow(seta))
        self.play(Write(num49))
        self.wait()
        self.play(FadeOut(seta), FadeOut(num49))

        self.play(soma.animate.shift(LEFT * 4.1), run_time=1)


        caixa = RoundedRectangle(
            corner_radius=0.2,
            color=GREEN_C,
            fill_color=GREEN_C,
            fill_opacity=0.2,
            width=1.5,
            height=1.5
        ).next_to(soma, RIGHT, buff=2.5)

        nomeVar = Text("valor2", font_size=90, disable_ligatures=True).scale(0.3).next_to(caixa, UP, buff=0.2)
        conteudoChar = Text("'1'", font_size=120).scale(0.4).move_to(caixa)
        conteudoNum = Text("49", font_size=120, color=PURE_YELLOW).scale(0.4).move_to(caixa)

        codigo1 = Text("char var = '1';", font_size=120).scale(0.25)
        codigo1.next_to(caixa, RIGHT, buff=1.8)

        grupoCaixa = VGroup(
            VGroup(caixa, nomeVar, conteudoChar),
            codigo1
        )

        
        codigo1.shift(UP * 0.45)

        conteudoNum.move_to(conteudoChar)

        codigo2 = Text("char var = 49;", font_size=120).scale(0.25)
        codigo2.move_to(codigo1)

        codigo3 = Text("char var = 'a';", font_size=120).scale(0.25)
        codigo3.next_to(codigo1, DOWN, buff=0.5)

        codigo4 = Text("char var = 97;", font_size=120).scale(0.25)
        codigo4.move_to(codigo3)


        self.play(Create(caixa), Write(nomeVar), Write(conteudoChar))
        self.wait()
        self.play(Transform(conteudoChar, conteudoNum))


        self.play(Write(codigo1))
        
        self.play(TransformMatchingShapes(codigo1, codigo2))

        self.play(Write(codigo3))
        
        self.play(TransformMatchingShapes(codigo3, codigo4))

        self.play(FadeOut(codigo2), FadeOut(codigo4), FadeOut(caixa), FadeOut(nomeVar), FadeOut(conteudoChar))

        self.play(soma.animate.shift(RIGHT * 4.1).scale(1.2), run_time=1)
        self.wait()

        numero1 = Text("1", font_size=60)
        adicao = Text("+", font_size=60)
        quarentaNove = Text("49", font_size=60)
        simbIgual = Text("=", font_size=60)
        cinq = Text("50", font_size=60)

        soma2 = VGroup(numero1, adicao, quarentaNove, simbIgual, cinq).arrange(RIGHT, buff=0.25).scale(1.2)

        self.play(TransformMatchingShapes(soma, soma2))
        self.wait()
        self.play(cinq.animate.scale(1.5).set_color(PURE_YELLOW))

        exclamacao = Text("!", font_size=60, color=PURE_YELLOW).scale(1.5)
        exclamacao.match_height(cinq)
        exclamacao.next_to(cinq, RIGHT, buff=0.2)

        self.play(FadeIn(exclamacao))
        self.wait()

        joker = ImageMobject("images/joker.png").scale(0.25).next_to(soma, DOWN * 1.8 + LEFT * 0.9, buff = 0.3)
        piada = Text(
            "Não é um fatorial ok engraçadinho?",
            font_size=90
        ).scale(0.25)

        mascara = Rectangle(
            width=10,
            height=2,
            fill_color="#1E1E1E",  
            fill_opacity=1,
            stroke_width=0
        )

        mascara.move_to(joker.get_center() + LEFT * 4.5)

        mascara.set_z_index(8)
        joker.set_z_index(10)
        piada.set_z_index(1)
        

        piada.move_to(joker.get_center() + LEFT)
        self.play(FadeIn(joker), FadeIn(mascara))

        self.play(
            piada.animate.shift(RIGHT * 4.5),
            run_time=2
        )
        self.wait(1)
 
        self.play(FadeOut(exclamacao), FadeOut(piada), FadeOut(joker))
        self.play(cinq.animate.scale(1 / 1.5).set_color(WHITE))
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
 

class intChar(Scene):
    def construct(self):
        codeChar = '''#include <stdio.h>

int main()
{
    int letra = 67;
    
    printf("%c", letra);
    return 0;
}'''

        rendered_codeChar = Code(
            code_string=codeChar, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.9)

        terminal = ImageMobject("images/terminal.png").scale(0.6)
        terminal.next_to(
            rendered_codeChar.get_center(),
            DOWN, 
            buff = 1.5
        )


        grupo = Group(rendered_codeChar, terminal).arrange(RIGHT, buff=1).move_to(ORIGIN)

        # cursor do terminal
        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 0.1,
            width = 0.04,
        ).move_to(terminal.get_bottom() + UP * 0.69 + RIGHT * 1.1) 
        cursor.set_z_index(100)

        terminalTitulo = Text("Terminal", font_size=40, color="#AA77C7").next_to(terminal, UP, buff=0.2)

        num67 = Text("67", font_size=90).scale(0.25).move_to(terminal.get_top() + DOWN * 0.3 + LEFT * 2)
        caractereC = Text("C", font_size=90).scale(0.25).move_to(num67)

        caixaInt = RoundedRectangle(
            corner_radius=0.2,
            color=BLUE_D,
            fill_color=BLUE_D,
            fill_opacity=0.2,
            width=2.2,
            height=2.4
        ).move_to(ORIGIN)

        nomeInt = Text("int", font_size=90, disable_ligatures=True, color=BLUE_D).scale(0.4).next_to(caixaInt, UP, buff=0.2)
        conteudoInt = Text("42", font_size=120).scale(0.4).move_to(caixaInt)

        conteudoByteInt = Text(
            "4 bytes",
            font_size=80
        ).scale(0.4).move_to(caixaInt)

        
        caixaChar = RoundedRectangle(
            corner_radius=0.2,
            color=GREEN_C,
            fill_color=GREEN_C,
            fill_opacity=0.2,
            width=2.2,
            height=2.4
        ).move_to(ORIGIN)

        nome = Text("char", font_size=90, disable_ligatures=True, color=GREEN_C).scale(0.4).next_to(caixaChar, UP, buff=0.2)
        conteudoChar = Text("'A'", font_size=120).scale(0.4).move_to(caixaChar)

        conteudoByte = Text(
            "1 byte",
            font_size=80
        ).scale(0.4).move_to(caixaChar)

        grupoChar = VGroup(caixaChar, nome, conteudoChar)
        grupoInt = VGroup(caixaInt, nomeInt, conteudoInt)

        grupoCaixas = VGroup(grupoInt, grupoChar).arrange(RIGHT, buff=1.5).move_to(ORIGIN)
        grupoCaixas.shift(UP * 5)
                
        self.play(
            LaggedStart(
                *[Write(linha) for linha in rendered_codeChar.code_lines],
                lag_ratio=0.1
            )
        )
        self.play(Write(terminalTitulo))
        self.play(FadeIn(terminal))
        self.play(FadeIn(num67))
        self.play(Transform(num67, caractereC))
        self.play(FadeIn(cursor), Blink(cursor, blinks=2))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.play(grupoInt.animate.shift(DOWN * 5), run_time = 0.6)
        self.play(grupoChar.animate.shift(DOWN * 5), run_time = 0.6)
        pergunta = Text("Então por que existem dois tipos?", font_size=90).scale(0.4).next_to(grupoCaixas, UP, buff=1)


        self.wait()
        self.play(Write(pergunta))

        # frente da carta int
        cartaFrenteInt = VGroup(
            caixaInt,
            conteudoInt
        )

        # começa o flip
        self.play(
            Rotate(
                cartaFrenteInt,
                angle=PI / 2,
                axis=UP
            ),
            run_time=0.25
        )

        self.remove(conteudoInt)

        conteudoByteInt.move_to(caixaInt)
        conteudoByteInt.set_opacity(0)

        cartaVersoInt = VGroup(
            caixaInt,
            conteudoByteInt
        )

        self.add(cartaVersoInt)

        # começa a segunda metade
        self.play(
            Rotate(
                cartaVersoInt,
                angle=PI / 2 * 0.2,
                axis=UP
            ),
            run_time=0.1
        )

        self.play(
            Rotate(
                cartaVersoInt,
                angle=PI / 2 * 0.8,
                axis=UP
            ),
            conteudoByteInt.animate.set_opacity(1),
            run_time=0.2
        )

        self.wait()


        # frente da carta char
        cartaFrente = VGroup(
            caixaChar,
            conteudoChar
        )

        # começa o flip
        self.play(
            Rotate(
                cartaFrente,
                angle=PI / 2,
                axis=UP
            ),
            run_time=0.25
        )

        self.remove(conteudoChar)

        conteudoByte.move_to(caixaChar)
        conteudoByte.set_opacity(0)

        cartaVerso = VGroup(
            caixaChar,
            conteudoByte
        )

        self.add(cartaVerso)

        # começa a segunda metade
        self.play(
            Rotate(
                cartaVerso,
                angle=PI / 2 * 0.2,
                axis=UP
            ),
            run_time=0.1
        )

        self.play(
            Rotate(
                cartaVerso,
                angle=PI / 2 * 0.8,
                axis=UP
            ),
            conteudoByte.animate.set_opacity(1),
            run_time=0.2
        )

        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


class tipoChar(Scene):
    def construct(self):

        codeChar = '''#include <stdio.h>

int main()
{
    char quantidade = '3';
    quantidade = quantidade + 4;
    
    printf("Quantidade = %d", quantidade);

    return 0;
}'''

        rendered_codeChar = Code(
            code_string=codeChar, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.6).move_to(ORIGIN)

        
        trechoAspasSimples1 = rendered_codeChar.code_lines[4][15]
        trechoAspasSimples2 = rendered_codeChar.code_lines[4][17]

        trechoAspasDuplas1 = rendered_codeChar.code_lines[7][7]
        trechoAspasDuplas2 = rendered_codeChar.code_lines[7][21]

        linhasParaSumir = VGroup(
            *[
                linha
                for i, linha in enumerate(rendered_codeChar.code_lines)
                if i != 7
            ]
        )

        linhaPrintf = VGroup(*rendered_codeChar.code_lines[7])
        cadeia = VGroup(*linhaPrintf[7:22])


        # representando a cadeia de caracteres na memória
        caracteres = [
            "Q","u","a","n","t","i","d","a",
            "d","e"," ","="," ","%","d","\\0"
        ]

        memoria = VGroup()

        for i, c in enumerate(caracteres):
            caixa = Rectangle(
                width=0.55,
                height=0.55
            ).set_stroke("#AA77C7", width=2).set_fill("#8728BE", opacity=0.1)

            if c == "\\0":
                texto = MathTex(
                    r"\backslash 0",
                    color=RED
                ).scale(0.5)

                caixa.set_stroke(RED, width=2)
                caixa.set_fill(RED, opacity=0.1)
            else:
                texto = Text(
                    c,
                    font_size=24
                )

           
            texto.move_to(caixa.get_center())

            indice = Text(
                str(i),
                font_size=16,
                color=BLUE
            )

            indice.next_to(caixa, DOWN, buff=0.08)

            celula = VGroup(caixa, texto, indice)

            memoria.add(celula)

        memoria.arrange(RIGHT, buff=0)
        memoria.move_to(ORIGIN)

    
        self.play(FadeIn(rendered_codeChar))
        self.wait()
        
        self.play(rendered_codeChar.animate.scale(1.2), rate_func = smooth)
        self.play(
            Flash(
                trechoAspasSimples1,
                color=PURE_YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            ),
            Flash(
                trechoAspasSimples2,
                color=PURE_YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            )
        )
        self.wait()

        self.play(
            Flash(
                trechoAspasDuplas1,
                color=PURE_YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            ),
            Flash(
                trechoAspasDuplas2,
                color=PURE_YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            )
        )
        self.wait()

        self.play(
            FadeOut(linhasParaSumir), linhaPrintf.animate.move_to([0, 2.5, 0]).scale(1.6)
        )

        self.play(Indicate(cadeia))
        
        self.play(TransformFromCopy(cadeia, memoria))
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class tipoString(Scene):
    def construct(self):
        palavra = Text(
            "TIPOS",
            font_size=80,
            disable_ligatures=True
        )

        codigo = Code(
            code_string='char palavra[] = "TIPOS";',
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle",
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
            }
        ).scale(1.4)

        codigo.move_to(palavra)

        definicao = Text("String = conjunto de char's", font_size = 80).scale(0.2)

        boxRetangular = (
            SurroundingRectangle(
                definicao,
                corner_radius=0.3,
                buff=0.2
            )
            .set_stroke(BLUE, width=2)
            .set_fill(BLUE, opacity=0.1)
        ).next_to(codigo, DOWN, buff = 0.5)

        definicao.move_to(boxRetangular.get_center())

        cadeado = ImageMobject("images/cadeado.png").scale(0.25).next_to(boxRetangular, UP * 6 + LEFT * 2.8, buff = 0.3)
        emBreve = Text("Esse contéudo será desbloqueado nas próximas aulas", font_size = 80).scale(0.2)

        emBreve.move_to(cadeado.get_center())

        mascara = Rectangle(
            width=10,
            height=2,
            fill_color="#1E1E1E",  
            fill_opacity=1,
            stroke_width=0
        )

        # cobre toda a região à esquerda do cadeado
        mascara.move_to(cadeado.get_center() + LEFT * 5)


        mascara.set_z_index(8)
        cadeado.set_z_index(10)
        emBreve.set_z_index(1)

        self.play(
            AddTextLetterByLetter(palavra),
            run_time=1.5
        )

        self.play(
            FadeTransform(palavra, codigo),
            run_time=1
        )

        self.play(Create(boxRetangular), FadeIn(definicao))

        self.play(FadeIn(cadeado), FadeIn(mascara))

        self.play(
            emBreve.animate.shift(RIGHT * 3.4),
            run_time=2
        )
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )