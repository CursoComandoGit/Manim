from manim import *

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope")
MarkupText.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

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

class aulaCompleta(MovingCameraScene):
    def construct(self):
        # ----------- Cenas -----------
        Inicio.construct(self)
        #--------PARTE1---------
        HelloWorld.construct(self)
        #GRAVAÇÃO DE TELA
        Funcao.construct(self)
        TiposFuncoes.construct(self)
        Curiosidade.construct(self)
        #PARTE2
        animacaoAntigaWindows.construct(self)
        alunoPassou.construct(self)
        simMas.construct(self)
        codigo5vezes.construct(self)
        #--------PARTE3---------
        Main.construct(self)
        Paradigma.construct(self)
        Importar.construct(self)
        Linha1.construct(self)
        Biblioteca.construct(self)
        Aprender.construct(self)
        Final.construct(self)

class Inicio(MovingCameraScene):
    def construct(self):
        # ----------- Objetos -----------
        codeExemplo = r'''#include <assert.h>
#include <ctype.h>
#include <limits.h>
#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* readline();
char* ltrim(char*);
char* rtrim(char*);
char** split_string(char*);

int parse_int(char*);
float comp(const void *a, const void *b);
int** mergeHighDefinitionIntervals(int intervals_rows, int intervals_columns, int** intervals, int* result_rows, int* result_columns);

int main()
{
    int intervals_rows = parse_int(ltrim(rtrim(readline())));
    int intervals_columns = parse_int(ltrim(rtrim(readline())));
    int** intervals = malloc(intervals_rows * sizeof(int*));

    for (int i = 0; i < intervals_rows; i++) {
        *(intervals + i) = malloc(intervals_columns * (sizeof(int)));

        char** intervals_item_temp = split_string(rtrim(readline()));

        for (int j = 0; j < intervals_columns; j++) {
            int intervals_item = parse_int(*(intervals_item_temp + j));
            *(*(intervals + i) + j) = intervals_item;
        }
    }

    int result_rows;
    int result_columns;
    int** result = mergeHighDefinitionIntervals(intervals_rows, intervals_columns, intervals, &result_rows, &result_columns);

    for (int i = 0; i < result_rows; i++) {
        for (int j = 0; j < result_columns; j++) {
            printf("%d", *(*(result + i) + j));

            if (j != result_columns - 1) {
                printf(" ");
            }
        }

        if (i != result_rows - 1) {
            printf("\n");
        }
    }
    printf("\n");

    return 0;
}'''
        codeRenderExemplo = Code(
            code_string=codeExemplo.replace("\xa0", " "), 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity" : 0,
                "stroke_opacity": 0,    
                "color" : "#1E1E1E"
                }
        ).scale(0.3)
        
        groupPausa = VGroup(
            Rectangle(width=0.4, height=1.2, fill_color="#AAAAAA", fill_opacity=1, stroke_opacity=0),
            Rectangle(width=0.4, height=1.2, fill_color="#AAAAAA", fill_opacity=1, stroke_opacity=0).shift(RIGHT * 0.7)
        ).move_to(ORIGIN)

        textFuncoes = Text("O que são funções?",t2c={"funções":"#AA77C7"}).scale(2)

        imagePrimeiroP = ImageMobject("assets/cfile.png")
        textPrimeiroP = Text("meu_primeiro.c").next_to(imagePrimeiroP,DOWN)

        groupPrimeiroP = Group(imagePrimeiroP,textPrimeiroP).move_to(ORIGIN)



        # ----------- Animações -----------
        self.play(Write(codeRenderExemplo))
        self.wait()

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.set(width=codeRenderExemplo.code_lines[0:9].width * 3.8).move_to(codeRenderExemplo.code_lines[0:9].get_center() + RIGHT*1.4))
        #self.play(self.camera.frame.animate.shift(RIGHT))
        self.wait()

        self.play(self.camera.frame.animate.shift(DOWN*2.5),run_time=4)
        
        self.play(Restore(self.camera.frame))
        self.play(Create(groupPausa),codeRenderExemplo[1:].animate.set_opacity(0.5))
        self.wait()

        self.play(FadeOut(groupPausa, codeRenderExemplo))
        self.wait()

        self.play(Write(textFuncoes))
        self.wait()
        self.play(FadeOut(textFuncoes))
        self.play(FadeIn(groupPrimeiroP))
        self.wait()
        self.play(FadeOut(groupPrimeiroP))
        self.wait()

#--------PARTE1---------
class HelloWorld(MovingCameraScene):
    def construct(self):
        helloworldstring = '''#include <stdio.h>

int main(){
    printf("Olá, mundo!");
    return 0;
}'''

        helloworldcode = codigoComando(helloworldstring)
        self.play(FadeIn(helloworldcode))
        self.wait()
        self.play(helloworldcode[1][1:].animate.set_opacity(0.4))

        self.wait()
        self.play(helloworldcode[1:].animate.set_opacity(1))
        self.wait()
        
        self.play(helloworldcode[1][0].animate.set_opacity(0.4),
                  helloworldcode[1][3].animate.set_opacity(0.4))
        
        sublinhado = Underline(helloworldcode[1][2][3:9], color=WHITE)
        self.play(Create(sublinhado))
        self.play(FadeOut(sublinhado))

        sublinhado2 = Underline(helloworldcode[1][4][0:7], color=WHITE)
        self.play(Create(sublinhado2))
        self.play(FadeOut(sublinhado2))

        self.wait()
        self.play(helloworldcode[1:].animate.set_opacity(1))
        self.wait()

        # Versão antiga
        #self.play(FadeIn(helloworldcode[0]), Write(helloworldcode[1][0]), run_time=1)
        #self.wait(2.5)
        #self.play(Write(helloworldcode[1][2]), Write(helloworldcode[1][4:6]), run_time=1)

        #sublinhado = Underline(helloworldcode[1][2][3:9], color=WHITE)
        #self.play(Create(sublinhado))
        #self.play(FadeOut(sublinhado))

        #sublinhado2 = Underline(helloworldcode[1][4][0:7], color=WHITE)
        #self.play(Create(sublinhado2))
        #self.play(FadeOut(sublinhado2))

        # self.play(Circumscribe(helloworldcode[1][2][0:9], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)
        # self.play(Circumscribe(helloworldcode[1][4], buff=0.05, fade_out=True, color=WHITE), run_time=1.5)

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
class animacaoAntigaWindows(Scene):
    def construct(self):
        # ----------- Objetos -----------

        # NumberPlane() que faz uma grid de quadrados, vai servir só de debug para me guiar
        numberPlane = NumberPlane()

        # Repetição de tarefas
        #Entrada
        svgEntrada = SVGMobject("assets/file.svg").move_to([-3.3,0,0])
        textEntrada = Text("Entrada",color="#58C4DD").next_to(svgEntrada,DOWN).scale(0.6)

        groupEntrada = VGroup(svgEntrada,textEntrada)

        # Saida
        svgSaida = SVGMobject("assets/file.svg").move_to([3.3,0,0])
        textSaida = Text("Saida",color="#58C4DD").next_to(svgSaida,DOWN).scale(0.6)

        groupSaida = VGroup(svgSaida,textSaida)

        # Linha de ligação entre os SVGs
        arrowLinha = Arrow([-2,0,0],[2,0,0],color='#AA77C7',max_tip_length_to_length_ratio=0)

        # Primeira Tarefa
        dotBolinha1 = Dot(color="#AA77C7").move_to([-1.8,0,0])
        textBolinha1 = Text("Tarefa 1",color="#AA77C7").next_to(dotBolinha1,DOWN).scale(0.4)

        groupBolinha1 = VGroup(dotBolinha1,textBolinha1)
        
        # Segunda Tarefa
        dotBolinha2 = Dot(color="#AA77C7").move_to([-1.8,0,0])
        textBolinha2 = Text("Tarefa 2",color="#AA77C7").next_to(dotBolinha2,DOWN).scale(0.4)

        groupBolinha2= VGroup(dotBolinha2,textBolinha2)
        
        # Terceira Tarefa
        dotBolinha3 = Dot(color="#AA77C7").move_to([-1.8,0,0])
        textBolinha3 = Text("Tarefa 3",color="#AA77C7").next_to(dotBolinha3,DOWN).scale(0.4)

        groupBolinha3 = VGroup(dotBolinha3,textBolinha3)





        # ----------- Animações -----------

        # Animação de fato
        self.play(FadeIn(groupEntrada),FadeIn(groupSaida))
        self.play(Create(arrowLinha))

        # Tarefas sendo passadas
        self.play(Create(groupBolinha1),run_time=0.5)

        self.play(Create(groupBolinha2),run_time=0.2)
        self.play(groupBolinha1.animate(rate_func=rate_functions.ease_in_out_sine).move_to([1.8,-0.3,0]),run_time=0.7)

        self.play(Create(groupBolinha3),run_time=0.2)
        self.play(groupBolinha2.animate(rate_func=rate_functions.ease_in_out_sine).move_to([1.8,-0.3,0]),FadeOut(groupBolinha1),run_time=0.7)

        self.play(groupBolinha3.animate(rate_func=rate_functions.ease_in_out_sine).move_to([1.8,-0.3,0]),FadeOut(groupBolinha2),run_time=0.7)

        self.play(FadeOut(groupBolinha3))

        # Limpa tudo
        self.play(FadeOut(groupEntrada),FadeOut(groupSaida),FadeOut(arrowLinha))
        self.wait()

class alunoPassou(MovingCameraScene):
    def construct(self):
        # ----------- Objetos -----------
        codeMedia = r'''#include <stdio.h>
double calcularMedia(float n1, float n2) {
    float soma = 0;
    
    soma = n1 + n2;
    double media = soma / 2;
    
    return media;
}
int main() {
    float a, b;
    const int C = 6;
    
    printf("Informe a nota 1: ");
    scanf("%f", &a);
    printf("Informe a nota 2:  ");
    scanf("%f", &b);
    
    double media = calcularMedia(a, b);
    
    if(media >= C) {
        printf("\nA media e maior ou igual a %d!", C);
    }
    else {
         printf("\nA media e menor que %d!", C);
    }
       
    return 0;
}
'''

        # Tá no formato novo sugerido, pode ser que mude mais para frente
        codeRenderMedia = Code(
            code_string=codeMedia, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity" : 0,
                "stroke_opacity": 0,    
                "color" : "#1E1E1E"
                }
        ).scale(0.65)

        # Técnicamente uma cena diferente, mas é que uma depende da outra, fica mais fácil trabalhar na mesma classe
        textDemonstrativo = Text("Parte Demonstrativa",t2c={"Demonstrativa":"#AA77C7"}).move_to([0,2,0]).scale(1.5)

        # Técnicamente uma outra cena diferente, mas é que uma depende da outra, fica mais fácil trabalhar na mesma classe
        
        textMaisC = Text("+").scale(1.5)
        svgTeclaCtrlC = ImageMobject("assets/ctrl.png").scale(1.5).next_to(textMaisC,LEFT)
        svgTeclaC = ImageMobject("assets/c.png").scale(1.5).next_to(textMaisC,RIGHT)
        
        groupCtrlc = Group(svgTeclaCtrlC,svgTeclaC,textMaisC).move_to([0,0,0])
        
        textMaisV = Text("+").scale(1.5)
        svgTeclaCtrlV = ImageMobject("assets/ctrl.png").scale(1.5).next_to(textMaisV,LEFT)
        svgTeclaV = ImageMobject("assets/v.png").scale(1.5).next_to(textMaisV,RIGHT)
        
        groupCtrlv = Group(svgTeclaCtrlV,svgTeclaV,textMaisV).move_to([0,-2,0])

        # Literalmente impossível fazer em outra classe, eu vou interagir diretamente com o código
        blocoCalcularMedia = codeRenderMedia.code_lines[0:9]
        blocoMain = codeRenderMedia.code_lines[9:30]

        sublinhado1 = Underline(blocoMain[9][12:25])
        sublinhado2 = Underline(blocoMain[9][26:29])

        # ----------- Animação -----------
        # Uma Cena
        self.play(Write(codeRenderMedia))
        
        self.wait()

        # Segunda uma cena
        # As Classes do Manim são, basicamente, agrupamentos de vários mobjects em vetores. Quando você faz set_opacity, ele muda a opacidade para TODOS os submobjects, inclusive o da stroke (contorno) que antes era 0, e agora se tornou o valor novo

        # A solução: O primeiro submobject (índice 0) da classe Code é o submobject do fundo. 
        # Pulando ele com [1:] (todos os submobjects a partir do índice 1) evita-se a bagunça toda porque nunca tocamos no variável de contorno 
        self.play(codeRenderMedia[1:].animate.set_opacity(0.5))
        self.play(Write(textDemonstrativo))
        self.wait()

        # Terceira uma cena
        self.play(FadeIn(groupCtrlc))
        self.play(FadeIn(groupCtrlv))

        self.wait()

        self.play(FadeOut(groupCtrlc,groupCtrlv,textDemonstrativo),codeRenderMedia[1:].animate.set_opacity(1))
        self.wait()

        # Mais uma cena
        self.play(Indicate(blocoMain))
        self.wait()
        self.play(Indicate(blocoCalcularMedia))

        # Salvar como está agora
        self.camera.frame.save_state() # saving camera state so that we can restore it later

        # Zoom no bloco
        self.play(self.camera.frame.animate.set(width = blocoMain.width*2).move_to(blocoMain))
        
        
        # Circumscribe na Main
        self.play(Circumscribe(codeRenderMedia.code_lines[9], color=WHITE),run_time=1.2)

        # Circumscribe nas notas
        self.play(Circumscribe(codeRenderMedia.code_lines[13:17], color=WHITE),run_time=1.2)

        self.wait()

        # Zoom no calcularMedia
        self.play(self.camera.frame.animate.set(width = codeRenderMedia.code_lines[18].width*2).move_to(codeRenderMedia.code_lines[18]), Wiggle(codeRenderMedia.code_lines[18]))
        self.wait()



        # Move códigos para longe
        self.play(self.camera.frame.animate.set(width = codeRenderMedia.code_lines[18].width*1.3).move_to(codeRenderMedia.code_lines[18]), codeRenderMedia.code_lines[0:17].animate.shift(UP*2), codeRenderMedia.code_lines[19:].animate.shift(DOWN*2))
        self.wait()

        self.play(Circumscribe(blocoMain[9][11],color=WHITE))
        self.wait()
        self.play(Create(sublinhado1))
        self.play(FadeOut(sublinhado1))
        self.wait()
        self.play(Create(sublinhado2))
        self.play(FadeOut(sublinhado2))
        self.wait()

        # Move códigos de volta para perto
        self.play(self.camera.frame.animate.set(width = codeRenderMedia.code_lines[18].width*2).move_to(codeRenderMedia.code_lines[18]), codeRenderMedia.code_lines[0:17].animate.shift(DOWN*2), codeRenderMedia.code_lines[19:].animate.shift(UP*2))
        self.wait()

        # Câmera se desloca para a função calcular media
        self.play(self.camera.frame.animate.set(width = blocoCalcularMedia.width*2).move_to(blocoCalcularMedia))
        self.wait()

        # POsicao da camera
        cam_center = self.camera.frame.get_center()
        cam_width = self.camera.frame.width

        # Centraliaz na calcular media
        self.play(self.camera.frame.animate.set(width = blocoCalcularMedia[1].width*1.3).move_to(blocoCalcularMedia[1]), blocoMain.animate.shift(DOWN*3), blocoCalcularMedia[2:].animate.shift(DOWN*3))
        self.wait()

        sublinhado3 = Underline(blocoCalcularMedia[1][0:6])
        self.play(Create(sublinhado3))
        self.play(FadeOut(sublinhado3))
        self.wait()
        sublinhado4 = Underline(blocoCalcularMedia[1][6:19])
        self.play(Create(sublinhado4))
        self.play(FadeOut(sublinhado4))
        self.wait()
        sublinhado5 = Underline(blocoCalcularMedia[1][20:35])
        self.play(Create(sublinhado5))
        self.play(FadeOut(sublinhado5))
        self.wait()

        # Retorna a focar no bloco todo
        self.play(self.camera.frame.animate.set(width=cam_width).move_to(cam_center),blocoMain.animate.shift(UP*3),blocoCalcularMedia[2:].animate.shift(UP*3))
        self.wait()

        # Variável retorna para onde foi chamada
        self.play(Indicate(blocoCalcularMedia[7]))
        self.wait()


        
        # Zoom na Main
        self.play(self.camera.frame.animate.set(width = codeRenderMedia.code_lines[18].width*2).move_to(codeRenderMedia.code_lines[18]))
        self.wait()

        self.play(Indicate(codeRenderMedia.code_lines[18]))
        self.wait()

        # Finalmente termina tudo, dá clear, e volta a câmera para a posição original
        self.play(self.camera.frame.animate.shift(RIGHT*20))
        self.clear()
        self.play(Restore(self.camera.frame))

class simMas(Scene):
    def construct(self):
        # ----------- Objetos -----------
        textSim = Text("Sim,",color="#AA77C7")
        textMas = Text("mas").next_to(textSim,RIGHT).align_to(textSim)

        groupSimas = VGroup(textSim,textMas).move_to(ORIGIN).scale(2)

        # ----------- Animações -----------
        self.play(Write(textSim))
        self.wait()
        self.play(Write(textMas))
        self.wait()

        self.play(Unwrite(groupSimas))
        self.wait()

class codigo5vezes(Scene):
    def construct(self):
        # ----------- Objetos -----------
        code5vezes=r'''// printf() e scanf() omitidos para melhorar visualização

    float soma1;
    
    soma1 = n1 + n2;
    double media1 = soma1 / 2;

    float soma2;
    
    soma2 = n3 + n4;
    double media2 = soma2 / 2;
    
    float soma3;

    soma3 = n5 + n6;
    double media3 = soma3 / 2;
    
    float soma4;
    
    soma4 = n7 + n8;
    double media4 = soma4 / 2;
    
    float soma5;

    soma5 = n9 + n10;
    double media5 = soma5 / 2;'''
        
        codeRender5vezes = Code(code_string=code5vezes, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity" : 0,
                "stroke_opacity": 0,    
                "color" : "#1E1E1E"
                }
        ).scale(0.7).move_to([0,-20,0])

        codeLimpo = r'''#include <stdio.h>
double calcularMedia(float n1, float n2) {
    float soma = 0;
    
    soma = n1 + n2;
    double media = soma / 2;
    
    return media;
}
int main() {
    // printf() e scanf() omitidos para melhorar visualização

    double media1 = calcularMedia(a1,b1)

    double media2 = calcularMedia(a2,b2)

    double media3 = calcularMedia(a3,b3)

    double media4 = calcularMedia(a4,b4)

    double media5 = calcularMedia(a5,b5)
}'''
        codeRenderLimpo = Code(code_string=codeLimpo, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity" : 0,
                "stroke_opacity": 0,    
                "color" : "#1E1E1E"
                }
        ).scale(0.7)

        textModularizar = Text("Modularizar",color="#AA77C7")
        textSeparar = Text("Separar").next_to(textModularizar,DOWN)
        textOrganizar = Text("Organizar").next_to(textSeparar,DOWN)

        group3Palavras = VGroup(textModularizar,textSeparar,textOrganizar).move_to(ORIGIN).scale(2)
        # ----------- Animações -----------
        self.play(codeRender5vezes.animate.move_to(ORIGIN),run_time=2)
        self.wait()

        self.play(ReplacementTransform(codeRender5vezes,codeRenderLimpo))
        self.wait()
        self.play(Flash([3,2,0]))
        self.wait()

        self.play(codeRenderLimpo[1:].animate.set_opacity(0.2))
        self.play(Write(textModularizar))
        self.play(Write(textSeparar))
        self.play(Write(textOrganizar))
        self.wait()

        self.play(Unwrite(group3Palavras),Unwrite(codeRenderLimpo))
        self.wait()


#--------PARTE3---------

class Main(Scene):
    def construct(self):
        mainstring1 = '''int main(){
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
        caixa = ImageMobject("assets/caixa.png").scale(0.45).shift(RIGHT*2.5)
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
        arq = ImageMobject("assets/arquivo.png")
        bib = Text("biblioteca.h", font_size=70).next_to(arq, DOWN, buff=0.2).scale(0.8)
        arqbib = Group(arq, bib).scale(0.4)

        func = Text("Funções\n    úteis", font_size=70).next_to(arqbib, RIGHT, buff=1.5).scale(0.5)
        grupo = ImageMobject("assets/pessoas.png").next_to(func, RIGHT, buff=1.5).scale(0.55)

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
        cerebro = ImageMobject("assets/cerebro.png").scale(0.5)
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
        # ----------- Objetos -----------
        final_text1 = Text("Próxima aula:",font_size=60)
        final_text2 = Text("Variáveis e tipos de dados",font_size=75, t2c={'Variáveis': PURPLE})
        final = VGroup(final_text1, final_text2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(.7)

        logo = ImageMobject("assets/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        # O cursor
        cursorVinheta=ImageMobject("assets/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)

        # ----------- Animações -----------

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