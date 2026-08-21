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
