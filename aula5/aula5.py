from manim import *

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope")
MarkupText.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

codeCompras = '''#include <stdio.h>

float calcularTotal(int qtd, float uni)
{
    float t = qtd * uni;
    return t;
}

int main() {
    int quantidade;
    float precoUnitario, total; 
    
    quantidade = 3;
    //char quantidade = '3'
    precoUnitario = 10.50;

    total = calcularTotal(quantidade, precoUnitario);

    printf("Quantidade: %d \\n Preço unitário: %f\\n", 
    quantidade, precoUnitario);

    printf("Total a pagar: R$ %.2f\\n", total);
    
    return 0;
}'''

class Aula5(Scene):
    def construct(self):
        #cenas
        segundoConjuntoRegras.construct(self)
        tipoInt.construct(self)
        tipoFloat.construct(self)
        tipoChar.construct(self)
        tipoString.construct(self)
        globalLocal.construct(self)
        porExemplo.construct(self)
        cuidado.construct(self)
        calculandoCorretamente.construct(self)


class segundoConjuntoRegras(Scene):
    def construct(self):
        titulo = Text("Tipos de variável", t2c = {"Tipos": PURPLE}, font_size = 80).scale(0.8)
        titulo.move_to(ORIGIN)

        rendered_codeCompras = Code(
            code_string=codeCompras, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.6).move_to(ORIGIN)

        blocoCalcular = rendered_codeCompras.code_lines[0:7]
        blocoMain = rendered_codeCompras.code_lines[8:25]

        self.play(Write(titulo))
        self.wait(1.2)
        self.play(FadeOut(titulo))

        self.play(FadeIn(rendered_codeCompras))
        rendered_codeCompras.save_state()
        self.play(rendered_codeCompras.animate.scale(1.4), run_time = 2)
        self.play(rendered_codeCompras.animate.shift(DOWN * 1.2))

        sublinhado1 = Underline(VGroup(*rendered_codeCompras.code_lines[2][19:34]), stroke_width = 1.6)
        sublinhado2 = Underline(VGroup(*rendered_codeCompras.code_lines[9]), stroke_width = 1.6)
        sublinhado3 = Underline(VGroup(*rendered_codeCompras.code_lines[10]), stroke_width = 1.6)
        sublinhadoT = Underline(VGroup(*rendered_codeCompras.code_lines[4]), stroke_width = 1.6)


        # atribuição
        sublinhado4 = rendered_codeCompras.code_lines[12]
        sublinhado5 = rendered_codeCompras.code_lines[14]

        sublinhado1.shift(UP * 0.05)
        sublinhado2.shift(UP * 0.05)
        sublinhado3.shift(UP * 0.05)
        sublinhadoT.shift(UP * 0.05)

        self.play(Create(sublinhado2))
        self.play(Create(sublinhado3))
        self.play(Create(sublinhado1))
        self.play(Create(sublinhadoT))

        self.play(Uncreate(sublinhado2), Uncreate(sublinhado3), Uncreate(sublinhado1), Uncreate(sublinhadoT))
        self.wait()

        self.play(
            sublinhado4.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.8
        )
        self.play(
            sublinhado5.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.8
        )
        self.wait()
        self.play(Restore(rendered_codeCompras))
        LinhaTotal = [
            linha.animate.set_opacity(0.2)
            for linha in rendered_codeCompras.code_lines
        ]

        LinhaTotal.append(
            rendered_codeCompras.code_lines[16].animate.set_opacity(1)
        )
        self.play(*LinhaTotal)
        self.wait()
        self.play(rendered_codeCompras.code_lines[16].animate.scale(1.6))
        self.play(Wiggle(rendered_codeCompras.code_lines[16]), n_wiggles=2)
        self.wait(2)

        sublinhado6 = Underline(VGroup(*rendered_codeCompras.code_lines[16][20:44]), stroke_width = 1.6)
        sublinhado6.shift(UP * 0.05)
        self.play(Create(sublinhado6))
        self.wait(2)
        self.play(Uncreate(sublinhado6))

        self.play(Restore(rendered_codeCompras))
        self.play(
            blocoMain.animate.shift(DOWN * 6),
            run_time=1.2,
            rate_func=smooth
        )
        blocoCalcular.save_state()
        self.play(blocoCalcular.animate.move_to(ORIGIN).scale(1.4), rate_func = smooth)
        self.wait(2)

        destacarAumentando = blocoCalcular[5]
        self.play(
            destacarAumentando.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.8
        )
        self.play(Flash(VGroup(*blocoCalcular[5][6])), color = WHITE, line_length=0.1)

        self.play(Restore(blocoCalcular), rate_func = smooth)
        self.play(
            blocoMain.animate.shift(UP * 6),
            run_time=1.2,
            rate_func=smooth
        )

        origemSeta = blocoCalcular[5]
        destinoSeta = VGroup(*rendered_codeCompras.code_lines[16][8:20])

        setaCalcular = CurvedArrow(
            origemSeta.get_bottom() + DOWN * 0.1 + RIGHT * 0.4,
            destinoSeta.get_top() + UP * 0.1,
            angle=-PI/3,
            stroke_width=3,
            tip_length=0.15
        )
        setaCalcular.set_color(PURE_YELLOW)

        self.play(Create(setaCalcular))
        self.wait(2)
        self.play(Uncreate(setaCalcular), run_time = 0.6)
        self.wait(2)

        destacarRetangular = blocoMain[13]
        self.play(Circumscribe(destacarRetangular, buff=0.05, fade_out=True, color=WHITE, stroke_width = 1.4), run_time=1.5)
        self.wait(2)
        
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

        rendered_codeCompras = Code(
            code_string=codeCompras, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.6).move_to(ORIGIN)

        # sublinhadoInt = Underline(VGroup(*rendered_codeCompras.code_lines[9][0:3]), stroke_width = 1.6)
        # sublinhadoInt.shift(UP * 0.05)

        # sublinhadoAtribuiçao = Underline(VGroup(*rendered_codeCompras.code_lines[12][11:12]), stroke_width = 1.6)
        # sublinhadoAtribuiçao.shift(UP * 0.05)

        nomeRect = Rectangle(width=2.5, height=0.6)
        valorRect = Rectangle(width=1, height=0.6)

        bloco = VGroup(
            nomeRect,
            valorRect
        ).arrange(RIGHT, buff=0)
        bloco.set_stroke(BLUE, width=2)
        bloco.set_fill(BLUE, opacity=0.1)

        nomeTxt = Text(
            "quantidade",
            font_size=20
        )

        valorTxt = Text(
            "3",
            font_size=24
        ).move_to(valorRect)

        blocoMemoria = VGroup(
            bloco,
            nomeTxt, 
            valorTxt
        )

        trechoQuantidade = VGroup(*rendered_codeCompras.code_lines[9])
        trechoNumero = VGroup(*rendered_codeCompras.code_lines[12])


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
        
        self.play(FadeIn(rendered_codeCompras))
        # self.play(Create(sublinhadoInt))
        # self.wait()
        
        # self.wait()
        # self.play(Create(sublinhadoAtribuiçao))

        # self.wait(2)
        # self.play(Uncreate(sublinhadoInt))
        # self.play(Uncreate(sublinhadoAtribuiçao))

        self.play(rendered_codeCompras.animate.scale(0.8))
        self.play(rendered_codeCompras.animate.shift(LEFT * 2.5), run_time=1.2, rate_func=smooth)
        bloco.move_to(rendered_codeCompras.get_center()).next_to(rendered_codeCompras, buff = 1)
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

        menorFloat = MathTex(r"-3.4 \times 10^{38}")
        maiorFloat = MathTex(r"3.4 \times 10^{38}")

        menorFloat.next_to(retaNumerica.get_left(), DOWN)
        maiorFloat.next_to(retaNumerica.get_right(), DOWN)

        posicaoFinalTexto = retaNumerica.get_center() + UP * 0.8

        # aparece o codigo de compras para mostrar um exemplo de float
        rendered_codeCompras = Code(
            code_string=codeCompras, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.6).move_to(ORIGIN)

        sublinhadoFloat = Underline(VGroup(*rendered_codeCompras.code_lines[10]), stroke_width = 1.6)
        sublinhadoFloat.shift(UP * 0.05)
        
        # destacarPreco = VGroup(*rendered_codeCompras.code_lines[14])

        valor_codigo = VGroup(*rendered_codeCompras.code_lines[14][14:19])

        decimal = DecimalNumber(0,num_decimal_places = 2, font_size=valor_codigo.height * 160).move_to(valor_codigo.get_center())
        decimal.stretch(1.15, dim=0)
      
        decimal.match_color(valor_codigo)
        decimal.set_color(valor_codigo[0].get_color())
   

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
        self.play(tituloFloat.animate.move_to(posicaoFinalTexto), run_time = 1.8, rate_func = rate_functions.ease_out_bounce)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

        self.play(FadeIn(rendered_codeCompras))
        self.play(Create(sublinhadoFloat))
        self.wait()
        # Esconde o 10.50
        valor_codigo.set_opacity(0)
        self.add(decimal)
        
        self.play(ChangeDecimalToValue(decimal, 10.50), run_time=3)

        # self.wait(2)

        # self.play(
        #     destacarPreco.animate.scale(1.3),
        #     rate_func = there_and_back,
        #     run_time = 0.8
        # )
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )


class tipoChar(Scene):
    def construct(self):
        tituloChar = Text(
            "char",
            font_size=160,
            disable_ligatures=True
        ).scale(0.5)            
        tituloChar.move_to(ORIGIN)   

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
        ).scale(0.6)

        grupoChar = VGroup(
            tituloChar.copy(),
            rendered_codeChar
        ).arrange(RIGHT, buff=1)

        grupoChar.move_to(ORIGIN)

        posFinalTitulo = grupoChar[0].get_center()

        charTerminal = ImageMobject("images/charTerminal.png").scale(0.4)
        charTerminal.next_to(
            grupoChar[1].get_center(),
            DOWN, 
            buff = 1.5
        )

        # cursor do terminal
        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 0.08,
            width = 0.04,
        ).move_to(charTerminal.get_bottom() + UP * 0.49 + RIGHT * 0.76) 
        cursor.set_z_index(100)

        explicacao1 = Text("'3' = 51 (ASCII)", font_size = 20)
        explicacao2 = Text("51 + 4 = 55", font_size = 20)
        
        grupoExplicacao = VGroup(explicacao1, explicacao2).arrange(DOWN, buff = 0.2, aligned_edge = LEFT).next_to(grupoChar[0].get_center(), DOWN, buff = 2)
       
        setaChar = CurvedArrow(
            charTerminal.get_bottom() + DOWN * 0.1,
            grupoExplicacao.get_right()+ RIGHT * 0.1,
            angle=-PI/4,
            color=PURE_YELLOW,
            stroke_width=3,
            tip_length=0.15
        )

        LinhaTotal = [
            linha.animate.set_opacity(0.2)
            for linha in rendered_codeChar.code_lines
        ]

        LinhaTotal.append(
            rendered_codeChar.code_lines[4].animate.set_opacity(1)
        )
        
        naoParaCalculos = Text("Não é bom para cálculos", font_size = 80).scale(0.2)

        boxRetangular = (
            SurroundingRectangle(
                naoParaCalculos,
                corner_radius=0.3,
                buff=0.2
            )
            .set_stroke(BLUE, width=2)
            .set_fill(BLUE, opacity=0.1)
        ).next_to(rendered_codeChar, UP, buff = 0.5)

        naoParaCalculos.move_to(boxRetangular.get_center())

        # vou usar tipoChar para fazer a próxima parte
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

    
        self.play(Write(tituloChar))
        self.play(tituloChar.animate.move_to(posFinalTitulo))
        self.wait()
        self.play(FadeIn(rendered_codeChar))
        self.wait()
        self.play(FadeIn(charTerminal))
        self.play(FadeIn(cursor), Blink(cursor, blinks=2))
        self.wait()
        self.play(Create(setaChar))
        self.play(Write(explicacao1))
        self.wait(0.3)
        self.play(Write(explicacao2))
        self.wait()
        self.play(FadeOut(cursor), FadeOut(charTerminal), FadeOut(setaChar), FadeOut(explicacao1), FadeOut(explicacao2))
        self.wait()
        rendered_codeChar.save_state()
        self.play(*LinhaTotal)
        self.play(Create(boxRetangular), FadeIn(naoParaCalculos))
        self.wait()
        # próxima parte
        self.play(FadeOut(tituloChar), FadeOut(boxRetangular), FadeOut(naoParaCalculos))
        self.play(Restore(rendered_codeChar))
        self.play(rendered_codeChar.animate.move_to(ORIGIN).scale(1.2), rate_func = smooth)
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
        self.wait()
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
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class globalLocal(Scene):
    def construct(self):
        escopo = Text("Escopo", font_size = 120).scale(0.5)
        escopo.move_to(ORIGIN)
        escopo.set_opacity(0.2)

        globalTitulo = Text("Global", font_size = 100).scale(0.5)
        globalTitulo.move_to([0, 3, 0])

        arquivo = Rectangle(
            width = 4,
            height = 4.6,
            stroke_width = 1,
            stroke_color = WHITE
        )
        arquivo.set_fill("#FFFFFF", opacity=0.1)

        arquivo.next_to(globalTitulo, DOWN * 3.5)
        nomeArq = Text("arquivo.c", font_size = 80).scale(0.2)
        nomeArq.move_to(arquivo.get_center() + UP * 2)

        globalCodigo = Code(
            code_string='int globalVar = 10;',
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle",
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
            }
        ).scale(0.55)
        globalCodigo.move_to(arquivo.get_center() + UP * 1.5 + LEFT * 0.7)

        funcao = Rectangle(
            width = 2,
            height = 1,
            stroke_width = 1
        ).next_to(globalCodigo, DOWN)
        funcao.set_stroke("#AA77C7", width=2)
        funcao.set_fill("#8728BE", opacity=0.1)
        textoFuncao = Text("funcao()", font_size = 80).scale(0.2)
        
        textoFuncao.move_to(funcao.get_center())
        textoFuncao.next_to(funcao.get_top(), DOWN * 0.5)

        main = Rectangle(
            width = 2,
            height = 1,
            stroke_width = 1,
            stroke_color = BLUE
        ).next_to(funcao, DOWN)
        main.set_fill(BLUE, opacity=0.1)
        textoMain1 = Text("main()", font_size = 80).scale(0.2)
        localCodigo = Code(
            code_string='int localVar;',
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle",
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
            }
        ).scale(0.55)
        textoMain1.move_to(main.get_center())
        textoMain1.next_to(main.get_top(), DOWN * 0.5)
        localCodigo.move_to(main.get_center() + LEFT * 0.1 + DOWN * 0.15)

        # Tronco principal
        p0 = globalCodigo.get_left() + LEFT * 0.3
        p1 = p0 + DOWN * 2.25

        tronco = Line(
            p0,
            p1,
            color=GREEN,
            stroke_width=4
        )

        p_funcao = funcao.get_left() + LEFT * 0.02
        p_main = main.get_left() + LEFT * 0.02

        # Ramo para funcao()
        ramoFuncao = Arrow(
            start = [p1[0], funcao.get_center()[1], 0],
            end =  p_funcao,
            buff = 0,
            color = GREEN,
            stroke_width = 4,
            tip_length = 0.15
        )

        # Ramo para main()
        ramoMain = Arrow(
            start = [p1[0], main.get_center()[1], 0],
            end = p_main,
            buff = 0,
            color = GREEN,
            stroke_width = 4,
            tip_length = 0.15
        )

        bolinha = Dot(radius=0.05, color=GREEN)
        aura = Circle(
            radius=0.12,
            color=GREEN,
            stroke_opacity=0.3
        ).move_to(bolinha)

        aura.add_updater(lambda m: m.move_to(bolinha))

        bolinha.move_to(p0)

        caminhoCompleto = VMobject()
        caminhoCompleto.set_points_as_corners([
            p0,
            np.array([p0[0], funcao.get_center()[1], 0]),
            p_funcao,

            np.array([p0[0], funcao.get_center()[1], 0]),

            np.array([p0[0], main.get_center()[1], 0]),
            p_main
        ])

        podeManipular = Text("Pode ser manipulada por:", font_size = 80).scale(0.2)
        podeManipular.next_to(tronco, LEFT)

        localTitulo = Text("Local", font_size = 100).scale(0.5)
        localTitulo.move_to([0, 3, 0])

        p0_local = localCodigo.get_left() + LEFT * 0.52

        p1_local = np.array([
            p0_local[0],
            funcao.get_center()[1],
            0
        ])

        p_funcao = funcao.get_left() + LEFT * 0.02

        troncoLocal = Line(
            p0_local,
            p1_local,
            color=GREEN,
            stroke_width=4
        )

        ramoLocal = Arrow(
            start=p1_local,
            end=p_funcao,
            buff=0,
            color=GREEN,
            stroke_width=4,
            tip_length=0.15
        )

        bolinhaLocal = Dot(
            radius=0.05,
            color=GREEN
        )

        auraLocal = Circle(
            radius=0.12,
            color=GREEN,
            stroke_opacity=0.3
        )

        auraLocal.add_updater(
            lambda m: m.move_to(bolinhaLocal)
        )

        bolinhaLocal.move_to(p0_local)

        pontoBloqueio = troncoLocal.point_from_proportion(0.5)

        restrita1 = Text("Restrita ao local em", font_size = 80).scale(0.2)
        restrita2 = Text("que foi criada", font_size = 80).scale(0.2)
        gropoRestrito = VGroup(restrita1, restrita2).arrange(DOWN, buff = 0.2, aligned_edge = LEFT)
        gropoRestrito.next_to(pontoBloqueio, LEFT)

        restrito = ImageMobject("images/restrito.png").scale(0.2).next_to(gropoRestrito, LEFT, buff = 0.3)


        self.play(GrowFromCenter(escopo), run_time = 1.5)
        self.wait()
        self.play(escopo.animate.set_opacity(1))
        self.play(ShrinkToCenter(escopo))
        self.play(Write(globalTitulo))
        self.play(FadeIn(arquivo), FadeIn(nomeArq))
        self.wait()
        self.play(FadeIn(globalCodigo), FadeIn(funcao), FadeIn(textoFuncao), FadeIn(main), FadeIn(textoMain1), FadeIn(localCodigo))
        self.wait()

        self.play(
            Create(tronco)
        )
        self.play(FadeIn(podeManipular))

        self.play(
            Create(ramoFuncao),
            Create(ramoMain)
        )
        self.add(bolinha, aura)
        self.play(
            MoveAlongPath(bolinha, caminhoCompleto),
            run_time=3,
            rate_func=linear
        )
        self.play(FadeOut(bolinha), FadeOut(aura))
        self.play(FadeOut(tronco), FadeOut(ramoMain), FadeOut(ramoFuncao), FadeOut(podeManipular))
        
        self.play(Transform(globalTitulo, localTitulo))

        self.play(Create(troncoLocal))
        self.play(Create(ramoLocal))
        self.add(bolinhaLocal, auraLocal)

        self.play(
            MoveAlongPath(
                bolinhaLocal,
                Line(p0_local, pontoBloqueio)
            ),
            run_time=1
        )

        self.play(
            bolinhaLocal.animate.set_color(RED),
            auraLocal.animate.set_color(RED)
        )

        self.play(
            Wiggle(bolinhaLocal),
            run_time=0.4
        )

        self.play(
            FadeIn(restrito),
            FadeIn(gropoRestrito)
        )
        
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class porExemplo(Scene):
    def construct(self):
        rendered_codeCompras = Code(
            code_string=codeCompras, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.6).move_to(ORIGIN)

        sublinhado1 = Underline(VGroup(*rendered_codeCompras.code_lines[16][20:30]), stroke_width = 1.6)
        sublinhado1.shift(UP * 0.05)
        
        sublinhado2 = Underline(VGroup(*rendered_codeCompras.code_lines[4][7:10]), stroke_width = 1.6)
        sublinhado2.shift(UP * 0.05)

        box = Rectangle(
            width=0.65,
            height=0.65
        ).set_stroke("#AA77C7", width=2).set_fill("#8728BE", opacity=0.1)
        quantidade = Text("quantidade", font_size = 80).scale(0.2)
        valor = Text("3", font_size = 80).scale(0.2)

        box.next_to(rendered_codeCompras, RIGHT).shift(UP * 1.6)
        box.shift(LEFT * 1.5)
        quantidade.next_to(box, UP, buff = 0.2)
        valor.move_to(box.get_center())


        box2 = Rectangle(
            width=0.65,
            height=0.65
        ).set_stroke("#AA77C7", width=2).set_fill("#8728BE", opacity=0.1)
        qtd = Text("qtd", font_size = 80).scale(0.2)
        valorQtd = Text("3", font_size = 80).scale(0.2)

        box2.next_to(box, RIGHT, buff = 1.5)
        qtd.next_to(box2, UP, buff = 0.2)
        valorQtd.move_to(box2.get_center())

        setaCopia = Arrow(
            start = box.get_center(),
            end =  box2.get_center(),
            buff = 0.45,
            color = GREEN,
            stroke_width = 4,
            tip_length = 0.15
        )

        copia = Text("copia", font_size = 80).scale(0.15)
        copia.next_to(setaCopia, DOWN * 0.4)


        # para precoUnitario
        box3 = Rectangle(
            width=0.65,
            height=0.65
        ).set_stroke("#AA77C7", width=2).set_fill("#8728BE", opacity=0.1)
        preco = Text("precoUnitario", font_size = 80).scale(0.2)
        valorPreco = Text("10.50", font_size = 80).scale(0.2)

        box3.next_to(box, DOWN, buff = 1)
        preco.next_to(box3, UP, buff = 0.2)
        valorPreco.move_to(box3.get_center())

        box4 = Rectangle(
            width=0.65,
            height=0.65
        ).set_stroke("#AA77C7", width=2).set_fill("#8728BE", opacity=0.1)
        uni = Text("uni", font_size = 80).scale(0.2)
        valorUni = Text("10.50", font_size = 80).scale(0.2)

        box4.next_to(box3, RIGHT, buff = 1.5)
        uni.next_to(box4, UP, buff = 0.2)
        valorUni.move_to(box4.get_center())

        setaCopia2 = Arrow(
            start = box3.get_center(),
            end =  box4.get_center(),
            buff = 0.45,
            color = GREEN,
            stroke_width = 4,
            tip_length = 0.15
        )

        copia2 = Text("copia", font_size = 80).scale(0.15)
        copia2.next_to(setaCopia2, DOWN * 0.4)

        #diferente
        diferente = MathTex(r"quantidade \neq qtd", font_size = 80).scale(0.8)
        diferentePreco = MathTex(r"precoUnitario \neq uni", font_size = 80).scale(0.8).next_to(diferente, DOWN, buff = 1)

        grupoDif = VGroup(diferente, diferentePreco).move_to(ORIGIN)


        self.play(FadeIn(rendered_codeCompras))
        self.play(Indicate(VGroup(*rendered_codeCompras.code_lines[9])))
        self.play(Indicate(VGroup(*rendered_codeCompras.code_lines[12])))
        self.play(Create(box), FadeIn(quantidade), FadeIn(valor))
        self.play(Indicate(VGroup(*rendered_codeCompras.code_lines[16])))
        
        self.play(Create(sublinhado1))
        self.play(Create(setaCopia), FadeIn(copia))
        self.play(Create(sublinhado2))
        self.play(Create(box2), FadeIn(qtd), FadeIn(valorQtd))
        self.play(FadeOut(sublinhado1), FadeOut(sublinhado2))

        self.play(Create(box3), FadeIn(preco), FadeIn(valorPreco))
        self.play(Create(setaCopia2), FadeIn(copia2))
        self.play(Create(box4), FadeIn(uni), FadeIn(valorUni))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.play(Write(diferente), Write(diferentePreco))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class cuidado(Scene):
    def construct(self):
        sinal = ImageMobject("images/cuidado.png").scale(0.4)
        sinal.move_to(ORIGIN)

        self.play(FadeIn(sinal))
        self.play(Wiggle(sinal))
        self.play(sinal.animate.shift(LEFT * 4.8))

        aviso1 = Text("Cuidado: variáveis globais são usadas em contextos", font_size = 80).scale(0.35)
        aviso2 = Text("muito específicos, use-as com moderação.", font_size = 80).scale(0.35)
        grupoAviso = VGroup(aviso1, aviso2).arrange(DOWN, buff = 0.2, aligned_edge = LEFT)

        grupoAviso.move_to(sinal.get_center())

        mascara = Rectangle(
            width=10,
            height=2,
            fill_color="#1E1E1E",  
            fill_opacity=1,
            stroke_width=0
        )

        # cobre toda a região à esquerda do sinal
        mascara.move_to(sinal.get_center() + LEFT * 5.2)

        mascara.set_z_index(8)
        sinal.set_z_index(10)
        grupoAviso.set_z_index(1)

        self.play(FadeIn(mascara))
        self.play(
            grupoAviso.animate.shift(RIGHT * 5.6),
            run_time=2
        )
        
        boxAviso = (
            SurroundingRectangle(
                grupoAviso,
                corner_radius=0.3,
                buff=0.2
            )
            .set_stroke("#AA77C7", width=2)
            .set_fill("#8728BE", opacity=0.1)
        )
        
        self.play(Create(boxAviso))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class calculandoCorretamente(Scene):
    def construct(self):
        rendered_codeCompras = Code(
            code_string=codeCompras, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.6).move_to(ORIGIN)

        LinhaTotal = [
            linha.animate.set_opacity(0.2)
            for linha in rendered_codeCompras.code_lines
        ]

        LinhaTotal.append(
            rendered_codeCompras.code_lines[16].animate.set_opacity(1)
        )

        interrogacao = Text("?", font_size = 130, color = BLUE)

        destacarPrintf = rendered_codeCompras.code_lines[21]


        self.play(FadeIn(rendered_codeCompras))
        rendered_codeCompras.save_state()

        self.play(*LinhaTotal)
        self.play(rendered_codeCompras.code_lines[16].animate.scale(1.6))
        interrogacao.next_to(rendered_codeCompras.code_lines[16], UP * 4)
        self.play(FadeIn(interrogacao))
        self.play(ShrinkToCenter(interrogacao))
        self.play(Restore(rendered_codeCompras))
        self.play(Circumscribe(destacarPrintf, buff=0.05, fade_out=True, color=WHITE, stroke_width = 1.4), run_time=2)
        self.wait()

        printfFormatacao = rendered_codeCompras.code_lines[18]
        printfFormatacao2 = rendered_codeCompras.code_lines[19]
        LinhaPrintf = [
            linha.animate.set_opacity(0)
            for linha in rendered_codeCompras.code_lines
        ]

        LinhaPrintf.extend([
            rendered_codeCompras.code_lines[18].animate.set_opacity(1),
            rendered_codeCompras.code_lines[19].animate.set_opacity(1)
        ])
        grupoPrintf = VGroup(printfFormatacao, printfFormatacao2)

        self.play(*LinhaPrintf)

        self.play(grupoPrintf.animate.scale(1.2).move_to([0, 2.5, 0]))
        sublinhadoPrintf = Underline(VGroup(*rendered_codeCompras.code_lines[18][8:41]), stroke_width = 1.6)
        sublinhadoPrintf.shift(UP * 0.05)

        porcentagem = Text("%", font_size = 80, color = BLUE)
        tipo = Text("tipo", font_size = 80, color = PURPLE)
        porcTipo = VGroup(porcentagem, tipo).arrange(RIGHT, buff = 0.15).move_to(ORIGIN)

        self.play(Create(sublinhadoPrintf))
        self.play(GrowFromCenter(porcentagem))
        self.play( Write(tipo))
        self.wait()
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

