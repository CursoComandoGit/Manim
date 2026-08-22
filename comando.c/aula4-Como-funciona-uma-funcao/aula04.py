from manim import *
import re
from customTerminal import CustomTerminal

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope")
MarkupText.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

# ---------------- CONFIG GERAL DOS BLOQUINHOS PARA FICAR BONITO E BEM ORGANIZADO ----------------
UNIT_W = 0.55      # largura de "1 unidade" no grid horizontal
UNIT_H = 0.65      # altura de "1 unidade" no grid vertical
GAP    = 0.15      # espaço entre blocos (mesma linha) e entre linhas
CORNER = 0.15       # raio dos cantos arredondados
STROKE_W = 3

DEFAULT_STYLE = dict(stroke_color=GRAY_B, stroke_width=STROKE_W, fill_opacity=0)

# Tamanhos prontos (em unidades) -> mexa aqui pra mudar "grande/pequeno" globalmente
SQ_SMALL   = (1, 1)     # quadrado pequeno
RECT_SMALL = (2, 0.8)
RECT_MED   = (3.2, 1)
RECT_LARGE = (6, 1)     # o retângulo grande do topo
RECT_FULL  = (7.2, 1)   # linha "cheia" (sem quadrado do lado), largura = SQ+gap+RECT_LARGE

def block(size, **style):
    w, h = size
    cfg = {**DEFAULT_STYLE, **style}
    return RoundedRectangle(width=w * UNIT_W, height=h * UNIT_H, corner_radius=CORNER, **cfg)


def row(*blocks):
    r = VGroup(*blocks)
    r.arrange(RIGHT, buff=GAP, aligned_edge=UP)
    return r


def structure(*rows):
    s = VGroup(*rows)
    s.arrange(DOWN, buff=GAP, aligned_edge=LEFT)
    return s

# ---------------- CONFIG GERAL DOS BLOQUINHOS PARA FICAR BONITO E BEM ORGANIZADO ----------------

def fix_cap(mob):
    for m in mob.family_members_with_points():
        m.set_cap_style(CapStyleType.BUTT)
    return mob

def TX(texto, **kwargs):
    return fix_cap(Text(texto, **kwargs))


def T(texto, **kwargs):
    return fix_cap(Tex(texto, **kwargs))

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

def indices_por_numero(code_string):
    resultado = {}
    for i, linha in enumerate(code_string.splitlines()):
        m = re.search(r'instrução (\d+)', linha)
        if m:
            resultado[int(m.group(1))] = i
    return resultado

def get_highlight(code_obj : Code, line_index : int, color=WHITE, opacity=0.3, fill_screen = True, highlight_text_only = False) -> Rectangle:
    total_lines = len(code_obj.code_lines)
    
    anchorY = code_obj.code_lines[0].get_y()
    
    centerY = code_obj.background.get_y()
    
    mid_index = (total_lines - 1) / 2.0
    
    if mid_index != 0:
        true_step = (anchorY - centerY) / mid_index
    else:
        true_step = code_obj.code_lines.height
    
    highlight = Rectangle(
        #mesma da linha específica
        width=50 if fill_screen else (code_obj.background.width - 0.2 if not highlight_text_only else code_obj.code_lines[line_index].width + 0.05),
        height=true_step,
        color=color,
        fill_opacity=opacity,
        stroke_width=0
    )
    #Movendo rect para linha específica e ajustando fator de escala
    actual_y = anchorY - (line_index * true_step)
    
    highlight.set_y(actual_y)
    highlight.set_x(code_obj.code_lines[line_index].get_x())
    highlight.set_z_index(0.5) 
    
    return highlight

class AulaCompleta(MovingCameraScene):
    def construct(self):
        # ----------- Cenas -----------
        Inicio.construct(self)
        Maquina.construct(self)
        ExemplosFuncao.construct(self)
        intMain.construct(self)
        Capitulo1.construct(self)
        Curiosidade.construct(self)
        Capitulo1ponto1.construct(self)
        printf.construct(self)
        Capitulo2.construct(self)
        


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

        # ---- Layout constants ----
        line_start_x = -5.0
        line_end_x = 5.0
        y = -1.0
 
        line = Line([line_start_x, y, 0], [line_end_x, y, 0], color=WHITE)

        
        # 3 quadradinhos igualzinho o Rainier pediu
        sq_side = 1
        square1 = Square(side_length=sq_side, color='#58C4DD', fill_color='#58C4DD', fill_opacity=1)
        square1.set_z_index(1)
        labelSquare1 = Text("1", font_size=55, color=WHITE)
        labelSquare1.set_z_index(2)
        labelSquare1.move_to(square1.get_center())
        groupSquare1 = VGroup(square1, labelSquare1)

        square2 = Square(side_length=sq_side, color='#58C4DD', fill_color='#58C4DD', fill_opacity=1)
        square2.set_z_index(1)
        labelSquare2 = Text("2", font_size=55, color=WHITE)
        labelSquare2.set_z_index(2)
        labelSquare2.move_to(square2.get_center())
        groupSquare2 = VGroup(square2, labelSquare2)

        square3 = Square(side_length=sq_side, color='#58C4DD', fill_color='#58C4DD', fill_opacity=1)
        square3.set_z_index(1)
        labelSquare3 = Text("3", font_size=55)
        labelSquare3.set_z_index(3)
        labelSquare3.move_to(square3.get_center())
        groupSquare3 = VGroup(square3, labelSquare3)
 

        # O retangulo da função
        rect_w, rect_h = 4.0, 2.0
        rect = Rectangle(width=rect_w, height=rect_h, color="#236B8E", fill_color='#236B8E', fill_opacity=1)
        rect.move_to([0, y+1, 0])
        rect.set_z_index(4)
        label = Text("soma(x, y)", font_size=55, color=WHITE)
        label.move_to(rect.get_center())
        label.set_z_index(5)


        # entry position for square1: just left of the line start
        entry_x = line_start_x
        groupSquare1.move_to([entry_x+0.5, y+0.5, 0])
        groupSquare2.move_to([entry_x+2, y+0.5, 0])
        groupSquare3.move_to([line_end_x-0.5, y+0.5, 0])
 
        # left arrow, pointing right, sitting right before the line start
        left_arrow = Arrow(
            start=[line_start_x - 1.6, y+1, 0],
            end=[line_start_x - 0.7, y+1, 0],
            color=WHITE,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.35,
        )
 
        # right arrow, pointing right, sitting right after the line end
        right_arrow = Arrow(
            start=[line_end_x + 0.7, y+1, 0],
            end=[line_end_x + 1.6, y+1, 0],
            color=WHITE,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.35,
        )

        # ESSE É IMPORTANTE
        groupMaquina = VGroup(line, groupSquare1, groupSquare2, groupSquare3, rect, label, left_arrow, right_arrow).scale(0.7)

        # ---- Conjunto 1 ----
        funcao = Text("1. O que são funções?", font_size=100, weight=BOLD, t2c={"funções":"#AA77C7"}).scale(0.6).move_to([0,2,0])
        groupFuncao = VGroup(funcao, groupMaquina)
        groupFuncao.arrange(DOWN, buff=0.6)


        # outra coisa
        terminal = CustomTerminal(
            styleLinux=False,      
            windowsPath="comando@c: ",  
            sizeX=9,
            sizeY=3.5,
            textSize=28,
            title="terminal",
            corBack="#1e1e1e",
            corTop="#2D2D2D",
        )

        terminal.corPath = "#AA77C7"
        terminal.currentPath.set_color("#AA77C7")

        # ---- Linha 1: comando@c: ./a.out ----
        terminal.initialize_line(self, "./a.out", color=WHITE)
        self.wait(0.3)

        # ---- Linha 2: saída do programa ----
        terminal.cursorNewLine()
        terminal.instantInitializeLine("Olá, Mundo!", color=WHITE)
        self.wait(0.3)

        # ---- Linha 3: novo prompt ----
        terminal.cursorNewLine(willGeneratePath=True, newPath="comando@c: ")

        # ---- Conjunto 2 ----
        programa = Text("2. Seu primeiro programa", font_size=100, weight=BOLD, t2c={"programa":"#AA77C7"}).scale(0.6).move_to([0,2,0])
        groupPrograma = VGroup(programa, terminal)
        groupPrograma.arrange(DOWN, buff=0.6)

        # ESSE TAMBÉM
        diagrama = structure(
            row(block(SQ_SMALL), block(RECT_MED)),
            row(block(RECT_SMALL)),
            row(block(RECT_SMALL)),
            row(block(SQ_SMALL), block(RECT_MED)),
            row(block(RECT_SMALL)),
            row(block(RECT_MED)),
        )

        # ---- Conjunto 3 ----
        estrutura = Text("3. Estrutura de código C", font_size=100, weight=BOLD, t2c={"código":"#AA77C7"}).scale(0.6).move_to([0,2,0])
        groupEstrutura = VGroup(estrutura, diagrama)
        groupEstrutura.arrange(DOWN, buff=0.6)

        largura_tela = self.camera.frame.get_width()   # ~14.22 por padrão
        altura_tela = self.camera.frame.get_height()    # ~8

        conjuntos = [groupFuncao, groupPrograma, groupEstrutura]

        # Posiciona cada conjunto em sua própria "região" da tela,
        # uma do lado da outra, cada um alinhado à direita da sua região
        for i, c in enumerate(conjuntos):
            centro_regiao = RIGHT * (i * largura_tela)
            borda_direita_regiao = centro_regiao + RIGHT * (largura_tela / 2 - 1)  # -1 = margem
            c.move_to(borda_direita_regiao)
            # se o conjunto for maior que a tela, ajusta escala pra caber
            if c.height > altura_tela * 0.9:
                c.scale_to_fit_height(altura_tela * 0.9)



        # ----------- Animações -----------
        self.camera.frame.save_state()
        self.play(Write(codeRenderExemplo), run_time=2)
        self.wait()

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.set(width=codeRenderExemplo.code_lines[0:9].width * 3.8).move_to(codeRenderExemplo.code_lines[0:9].get_center() + RIGHT*1.4), run_time=1.5)
        #self.play(self.camera.frame.animate.shift(RIGHT))
        self.wait()

        self.play(self.camera.frame.animate.shift(DOWN*2.5),run_time=4)
        
        self.play(Restore(self.camera.frame))
        self.play(Create(groupPausa),codeRenderExemplo[1:].animate.set_opacity(0.5))
        self.wait()

        self.play(FadeOut(groupPausa, codeRenderExemplo))
        self.wait()

        # Câmera começa focada no primeiro conjunto
        self.camera.frame.move_to(groupFuncao)
        self.play(FadeIn(groupFuncao))
        self.add(groupFuncao, groupPrograma, groupEstrutura)
        self.wait()

        # Pan pra segundo conjunto
        self.play(self.camera.frame.animate.move_to(groupPrograma), run_time=2)

        self.wait()

        # Pan pra terceiro conjunto
        self.play(self.camera.frame.animate.move_to(groupEstrutura), run_time=2)
        self.wait()

        self.play(FadeOut(*self.mobjects))
        self.play(Restore(self.camera.frame))

#--------PARTE1---------
class Maquina(MovingCameraScene):
    def construct(self):

        # ---- Layout constants ----
        line_start_x = -5.0
        line_end_x = 5.0
        y = -1.0
 
        line = Line([line_start_x, y, 0], [line_end_x, y, 0], color=WHITE)

        
        # 3 quadradinhos igualzinho o Rainier pediu
        sq_side = 1
        square1 = Square(side_length=sq_side, color='#58C4DD', fill_color='#58C4DD', fill_opacity=1)
        square1.set_z_index(1)
        labelSquare1 = Text("1", font_size=55, color=WHITE)
        labelSquare1.set_z_index(2)
        labelSquare1.move_to(square1.get_center())
        groupSquare1 = VGroup(square1, labelSquare1)

        square2 = Square(side_length=sq_side, color='#58C4DD', fill_color='#58C4DD', fill_opacity=1)
        square2.set_z_index(1)
        labelSquare2 = Text("2", font_size=55, color=WHITE)
        labelSquare2.set_z_index(2)
        labelSquare2.move_to(square2.get_center())
        groupSquare2 = VGroup(square2, labelSquare2)

        square3 = Square(side_length=sq_side, color='#58C4DD', fill_color='#58C4DD', fill_opacity=1)
        square3.set_z_index(1)
        labelSquare3 = Text("3", font_size=55)
        labelSquare3.set_z_index(3)
        labelSquare3.move_to(square3.get_center())
        groupSquare3 = VGroup(square3, labelSquare3)
 

        # O retangulo da função
        rect_w, rect_h = 4.0, 2.0
        rect = Rectangle(width=rect_w, height=rect_h, color="#236B8E", fill_color='#236B8E', fill_opacity=1)
        rect.move_to([0, y+1, 0])
        rect.set_z_index(4)
        label = Text("soma(x, y)", font_size=55, color=WHITE)
        label.move_to(rect.get_center())
        label.set_z_index(5)


        # entry position for square1: just left of the line start
        entry_x = line_start_x
        groupSquare1.move_to([entry_x+0.5, y+0.5, 0])
        groupSquare2.move_to([entry_x+2, y+0.5, 0])
 
        # left arrow, pointing right, sitting right before the line start
        left_arrow = Arrow(
            start=[line_start_x - 1.6, y+1, 0],
            end=[line_start_x - 0.7, y+1, 0],
            color=WHITE,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.35,
        )
 
        # right arrow, pointing right, sitting right after the line end
        right_arrow = Arrow(
            start=[line_end_x + 0.7, y+1, 0],
            end=[line_end_x + 1.6, y+1, 0],
            color=WHITE,
            buff=0,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.35,
        )
 
        # ---- Static setup ----
        self.play(Create(line), Create(left_arrow), Create(right_arrow))
        self.play(Create(rect), Write(label))
        self.wait(0.3)
 
        # ---- Square 1 appears at entry and travels behind the rectangle ----
        self.play(FadeIn(groupSquare1,shift=RIGHT * 0.3))
        self.play(FadeIn(groupSquare2,shift=RIGHT * 0.3))
        self.play(groupSquare1.animate.move_to([-0.75, y+0.5, 0]), groupSquare2.animate.move_to([0.75, y+0.5, 0]), run_time=2)

        # square1 is now hidden behind the (higher z-index) rectangle
        self.remove(groupSquare1)
        self.remove(groupSquare2)
        self.wait()
 
        # ---- Square 3 emerges from behind the rectangle and exits to the right ----
        groupSquare3.move_to([0, y+0.5, 0])
        self.add(groupSquare3)
        exit_x = line_end_x
        self.play(groupSquare3.animate.move_to([exit_x-0.5, y+0.5, 0]), run_time=2)
        self.play(FadeOut(groupSquare3, shift=RIGHT * 0.3))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(rect).scale(0.5))
        
        soma_part = label[0:4]                      # "soma"
        parens_part = VGroup(label[4], label[8])    # "(" e ")"

        self.play(Indicate(soma_part, scale_factor=1.4))
        self.wait(0.2)
        self.play(Indicate(parens_part, scale_factor=1.6))
        
        self.wait()

        self.play(Restore(self.camera.frame),Uncreate(groupSquare3), Uncreate(line), Uncreate(left_arrow), Uncreate(right_arrow), Uncreate(rect), Unwrite(label))
        self.wait()

class ExemplosFuncao(MovingCameraScene):
    def construct(self):
        exemplo1=Code(code_string="int funcao(){", language="c",add_line_numbers=False, formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        exemplo2=Code(code_string="String funcao(t){", language="c", add_line_numbers=False, formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        exemplo3=Code(code_string="void funcao(void){", language="c", add_line_numbers=False, formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        exemplo4=Code(code_string="funcao(){", language="c", add_line_numbers=False, formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        exemplo5=Code(code_string="funcao(t){", language="c", add_line_numbers=False, formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        
        exemplos = VGroup(exemplo1, exemplo2, exemplo3, exemplo4, exemplo5)
        exemplos.arrange(DOWN, buff=0.3)
        exemplos.move_to(ORIGIN)

        for i in exemplos:
            self.play(Write(i), run_time=0.8)

        self.wait()
        self.play(
            Indicate(exemplo1.code_lines[0][:3]), Indicate(exemplo2.code_lines[0][:6]), Indicate(exemplo3.code_lines[0][:4]) 
            )
        self.wait()
        self.play(
            Uncreate(exemplo1), Uncreate(exemplo2), Uncreate(exemplo3), Uncreate(exemplo4), Uncreate(exemplo5), 
        )
        self.wait()

class intMain(MovingCameraScene):
    def construct(self):
        embaralhado='''int funcaoExemplo()
{   
    escrever("instrução 2");
    escrever("instrução 5");
	escrever("instrução 1");
	escrever("instrução 4");
	escrever("instrução 3");

	return 0;
}'''
        certo='''int funcaoExemplo()
{   
	escrever("instrução 1");
	escrever("instrução 2");
	escrever("instrução 3");
    escrever("instrução 4");
	escrever("instrução 5");

	return 0;
}'''    
        # Codigos
        codigoEmbaralhado=Code(code_string=embaralhado, language="c",formatter_style="material",add_line_numbers=False,background="rectangle", background_config={"fill_opacity" : 0,"stroke_opacity": 0, "color" : "#1E1E1E"}).move_to([0,1,0])
        codigoCerto=Code(code_string=certo, language="c",formatter_style="material",add_line_numbers=False,background="rectangle", background_config={"fill_opacity" : 0,"stroke_opacity": 0, "color" : "#1E1E1E"})


        # O dito do quadrado tampando
        bloco = codigoEmbaralhado.code_lines[2:9]  

        quadrado = Rectangle(
            width=bloco.width + 0.2,    
            height=bloco.height + 0.2,
            fill_color="#58C4DD",       
            fill_opacity=1,
            stroke_opacity=0,
        )
        quadrado.move_to(bloco.get_center())

        idx_emb = indices_por_numero(embaralhado)
        idx_certo = indices_por_numero(certo)


        # animação
        self.play(FadeIn(codigoEmbaralhado, run_time=2), Create(quadrado, run_time=0.5))
        self.wait()
        self.play(FadeOut(quadrado))
        self.wait()
        self.play(codigoEmbaralhado.animate.move_to(ORIGIN))
        animacoes = [
        codigoEmbaralhado.code_lines[idx_emb[n]].animate.move_to(
            codigoCerto.code_lines[idx_certo[n]].get_center()
        )
        for n in idx_emb
        ]
        # ordenação
        self.play(*animacoes, run_time=2)

        self.wait()

        # pinguim ativar e desativar
        self.play(codigoEmbaralhado[1][0:].animate.set_opacity(0.3),run_time=0.5)
        self.play(codigoEmbaralhado.animate.shift(RIGHT*2))
        self.wait()
        self.play(codigoEmbaralhado[1][0:].animate.set_opacity(1))
        self.wait()

        # get_highlight()
        self.play(codigoEmbaralhado.animate.move_to(ORIGIN))
#get_highlight(code_obj : Code, line_index : int, color=WHITE, opacity=0.3, fill_screen = True, highlight_text_only = False) -> Rectangle:
       
        highlight1 = get_highlight(codigoEmbaralhado,2)
        highlight2 = get_highlight(codigoEmbaralhado,3)
        highlight3 = get_highlight(codigoEmbaralhado,4)
        highlight4 = get_highlight(codigoEmbaralhado,5)
        highlight5 = get_highlight(codigoEmbaralhado,6)
        highlight6 = get_highlight(codigoEmbaralhado,8)

        self.play(FadeIn(highlight1))
        self.play(Transform(highlight1,highlight2))
        self.play(Transform(highlight1,highlight3))
        self.play(Transform(highlight1,highlight4))
        self.play(Transform(highlight1,highlight5))
        self.play(Transform(highlight1,highlight6))


        self.play(FadeOut(highlight1))

        self.wait()

        canto_referencia = codigoEmbaralhado.get_corner(UL)+ DOWN 
        self.play(codigoEmbaralhado.animate.shift(UP*3.2),run_time=2)

        # Parte 2 disso aqui porque eu preciso das coordenadas de codigoEmbaralhado
        text='''int main{ 

}'''
        codigo=Code(code_string=text, language="c",formatter_style="material",add_line_numbers=False,background="rectangle", background_config={"fill_opacity" : 0,"stroke_opacity": 0, "color" : "#1E1E1E"})
        codigo.move_to(canto_referencia, aligned_edge=UL)

        comentario = Code(
        code_string="// Começa aqui", language="c", formatter_style="material",
        add_line_numbers=False, background="rectangle",
        background_config={"fill_opacity": 0, "stroke_opacity": 0, "color": "#1E1E1E"},
        )
        comentario.next_to(codigo.code_lines[0], RIGHT, buff=0.3)

        chamada = Code(
        code_string="funcaoExemplo();", language="c", formatter_style="material",
        add_line_numbers=False, background="rectangle",
        background_config={"fill_opacity": 0, "stroke_opacity": 0, "color": "#1E1E1E"},
        )
        y0 = codigo.code_lines[0].get_y()
        y2 = codigo.code_lines[2].get_y()
        step = (y0 - y2) / 2         
        blank_y = y0 - step * 1      

        chamada.align_to(codigo.code_lines[0], LEFT)  
        chamada.shift(RIGHT * 0.4)                  
        chamada.set_y(blank_y)

        linha0 = codigo.code_lines[0]

        int_main = linha0[:7]       
        chave_abre = linha0[7]       
        chave_fecha = codigo.code_lines[2]  

        self.play(FadeIn(codigo))
        self.wait()
        self.play(FadeIn(comentario))
        self.wait()
        self.play(FadeIn(chamada))
        self.wait()

        # parte do indicate

        self.play(Indicate(int_main))
        self.wait()
        bloco_chaves = VGroup(chave_abre, chamada, chave_fecha)
        self.play(Indicate(bloco_chaves))
        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.wait()

# Gravação de tela segundo o roteiro

class Capitulo1(MovingCameraScene):
    def construct(self):
        capitulo = Text(
            "Capítulo 1",
            font_size=34,
            weight=NORMAL,
        )

        linha = Line(LEFT, RIGHT, stroke_width=1.5)
        

        titulo = Text(
            "\u201cSeu primeiro programa\u201d",
            font_size=100,
            weight=BOLD,
            t2c={"\u201c": "#58C4DD", "\u201d": "#58C4DD", "primeiro" : "#AA77C7"},
        ).scale(0.72)

        linha.set_width(titulo.get_width())

        subtitulo = Text(
            "",
            font_size=100,
            weight=BOLD,
            t2c={"programa": "#AA77C7"},
        ).scale(0.26)

        bloco = VGroup(capitulo, linha, titulo, subtitulo).arrange(DOWN, buff=0.3)
        bloco.move_to(ORIGIN)

        posicao_final_titulo = titulo.get_center()

        tampa = Rectangle(
            width=titulo.width + 0.4,
            height=titulo.height + 0.4,
            fill_color="#1E1E1E",
            fill_opacity=1,
            stroke_opacity=0,
        )
        tampa.next_to(linha, UP, buff=0)

        # Orgnizacao
        titulo.set_z_index(0)
        tampa.set_z_index(1)
        linha.set_z_index(2)
        capitulo.set_z_index(2)
        subtitulo.set_z_index(0)

        titulo.move_to(tampa.get_center())


        self.add(tampa)
        self.play(Write(capitulo))
        self.play(Create(linha))
        self.play(titulo.animate.move_to(posicao_final_titulo), run_time=1.3)
        self.play(FadeIn(subtitulo))
        self.wait()

        self.play(FadeOut(subtitulo),titulo.animate.move_to(tampa.get_center()),Unwrite(capitulo))
        self.play(Uncreate(linha),FadeOut(titulo))
        self.remove(tampa)

        
        
class Curiosidade(MovingCameraScene):
    def construct(self):
        titulo = Text("Curiosidade", font_size=70, color=PURPLE)
        curiosidade = Text("C é whitespace-insensitive", font_size=70)
        texto = Group(titulo, curiosidade).arrange(DOWN, buff=0.2).scale(0.7)

        donut = r'''             k;double sin()
         ,cos();main(){float A=
       0,B=0,i,j,z[1760];char b[
     1760];printf("\x1b[2J");for(;;
  ){memset(b,32,1760);memset(z,0,7040)
  ;for(j=0;6.28>j;j+=0.07)for(i=0;6.28
 >i;i+=0.02){float c=sin(i),d=cos(j),e=
 sin(A),f=sin(j),g=cos(A),h=d+2,D=1/(c*
 h*e+f*g+5),l=cos      (i),m=cos(B),n=s\
in(B),t=c*h*g-f*        e;int x=40+30*D*
(l*h*m-t*n),y=            12+15*D*(l*h*n
+t*m),o=x+80*y,          N=8*((f*e-c*d*g
 )*m-c*d*e-f*g-l        *d*n);if(22>y&&
 y>0&&x>0&&80>x&&D>z[o]){z[o]=D;;;b[o]=
 ".,-~:;=!*#$@"[N>0?N:0];}}/*#****!!-*/
  printf("\x1b[H");for(k=0;1761>k;k++)
   putchar(k%80?b[k]:10);A+=0.04;B+=
     0.02;}}/*****####*******!!=;:~
       ~::==!!!**********!!!==::-
         .,~~;;;========;;;:~-.
             ..,--------,*/'''

        identado = r'''#define _XOPEN_SOURCE 600
#define _POSIX_C_SOURCE 200112L
#define _BSD_SOURCE
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <unistd.h>

// mmmmm..... donut!

int main() {
    float A = 0, B = 0;
    float i, j;
    int k;
    float z[1760];
    char b[1760];

    printf("\x1b[2J");

    for (;;) {
        memset(b, 32, 1760);
        memset(z, 0, 7040);

        for (j = 0; j < 6.28; j += 0.07) {
            for (i = 0; i < 6.28; i += 0.02) {
                float c = sin(i);
                float d = cos(j);
                float e = sin(A);
                float f = sin(j);
                float g = cos(A);
                float h = d + 2;
                float D = 1 / (c * h * e + f * g + 5);
                float l = cos(i);
                float m = cos(B);
                float n = sin(B);
                float t = c * h * g - f * e;

                int x = 40 + 30 * D * (l * h * m - t * n);
                int y = 12 + 15 * D * (l * h * n + t * m);
                int o = x + 80 * y;
                int N = 8 * ((f * e - c * d * g) * m - c * d * e - f * g - l * d * n);

                if (22 > y && y > 0 && x > 0 && 80 > x && D > z[o]) {
                    z[o] = D;
                    b[o] = ".,-~:;=!*#$@"[N > 0 ? N : 0];
                }
            }
        }

        printf("\x1b[H");
        for (k = 0; k < 1761; k++) {
            putchar(k % 80 ? b[k] : 10);
        }

        A += 0.04;
        B += 0.02;
        usleep(30000);
    }

    return 0;
}'''

        donutCodigo = Code(code_string=donut, language="c",formatter_style="material",add_line_numbers=False,background="rectangle", background_config={"fill_opacity" : 0,"stroke_opacity": 0, "color" : "#1E1E1E"}).scale(0.8)
        identadoCodigo = Code(code_string=identado, language="c",formatter_style="material",add_line_numbers=False,background="rectangle", background_config={"fill_opacity" : 0,"stroke_opacity": 0, "color" : "#1E1E1E"}).scale(0.6).shift(UP*0.05)


        self.play(FadeIn(titulo))
        self.play(Write(curiosidade))
        self.wait(2.5)
        self.play(FadeOut(*self.mobjects))
        self.play(Write(donutCodigo))
        self.wait()
        self.play(Transform(donutCodigo,identadoCodigo))
        self.wait()

        #self.play(fundo.animate.set_opacity(0.4))
        self.play(FadeOut(donutCodigo))
        organizar = Text("Mantenha seu código\n         organizado!", font_size=70).scale(0.9)
        self.play(Write(organizar))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

# Gravação de tela segundo o roteiro

class Capitulo1ponto1(MovingCameraScene):
    def construct(self):
        capitulo = Text(
            "Capítulo 1.1",
            font_size=34,
        )


        linha = Line(LEFT, RIGHT, stroke_width=1.5)
        

        titulo = Text(
            "\u201cOlá, mundo!\u201d",
            font_size=100,
            weight=BOLD,
            t2c={"\u201c": "#58C4DD", "\u201d": "#58C4DD"},
        ).scale(0.72)

        linha.set_width(titulo.get_width())

        subtitulo = Text(
            "seu primeiro programa (de verdade)",
            font_size=100,
            weight=BOLD,
            t2c={"programa": "#AA77C7"},
        ).scale(0.26)

        bloco = VGroup(capitulo, linha, titulo, subtitulo).arrange(DOWN, buff=0.3)
        bloco.move_to(ORIGIN)

        posicao_final_titulo = titulo.get_center()

        tampa = Rectangle(
            width=titulo.width + 0.4,
            height=titulo.height + 0.4,
            fill_color="#1E1E1E",
            fill_opacity=1,
            stroke_opacity=0,
        )
        tampa.next_to(linha, UP, buff=0)

        # Orgnizacao
        titulo.set_z_index(0)
        tampa.set_z_index(1)
        linha.set_z_index(2)
        capitulo.set_z_index(2)
        subtitulo.set_z_index(0)

        titulo.move_to(tampa.get_center())


        self.add(tampa)
        self.play(Write(capitulo))
        self.play(Create(linha))
        self.play(titulo.animate.move_to(posicao_final_titulo), run_time=1.3)
        self.play(FadeIn(subtitulo))
        self.wait()

        self.play(FadeOut(subtitulo),titulo.animate.move_to(tampa.get_center()),Unwrite(capitulo))
        self.play(Uncreate(linha),FadeOut(titulo))
        self.play(FadeOut(tampa))
        
class printf(MovingCameraScene):
    def construct(self):
        codigo = Code(code_string='printf("printf funcionando!");', add_line_numbers=False, language="c", formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        printf = Code(code_string='printf();', add_line_numbers=False, language="c", formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}).scale(1.5)
        printfErrado = Code(code_string='printf(){', add_line_numbers=False, language="c", formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}).scale(1.5)

        chave = printfErrado.code_lines[0][8]

        x_vermelho = Cross(chave, stroke_color=RED, stroke_width=6)
        x_vermelho.scale(2.5)

        codigo.move_to([0,2,0])

        terminal_bg = RoundedRectangle(
            corner_radius=0.1,
            width=8,
            height=2,
            fill_color="#1e1e1e",
            fill_opacity=1,
            stroke_color=GRAY,
        )
        terminal_bg.next_to(codigo, DOWN, buff=1)

        terminal_texto = Text(
            "printf funcionando!",
            font="Monospace",
            font_size=28,
            color="#AA77C7",
        )
        terminal_texto.move_to(terminal_bg)

        self.play(Create(codigo))
        self.wait(0.5)
        self.play(Create(terminal_bg))
        self.play(Write(terminal_texto))
        self.wait(2)
        self.play(Uncreate(terminal_bg),Unwrite(terminal_texto))

        self.play(Transform(codigo,printf))
        self.wait()
        self.play(Transform(codigo,printfErrado))
        self.wait()
        self.play(Create(x_vermelho))
        self.wait()
        self.play(Uncreate(x_vermelho))
        self.play(Transform(codigo,printf))
        self.wait()
        self.play(FadeOut(codigo))


#PARTE2
class Capitulo2(MovingCameraScene):
    def construct(self):
        capitulo = Text(
            "Capítulo 2",
            font_size=34,
        )


        linha = Line(LEFT, RIGHT, stroke_width=1.5)
        

        titulo = Text(
            "\u201cFunções (na prática)\u201d",
            font_size=100,
            weight=BOLD,
            t2c={"\u201c": "#58C4DD", "\u201d": "#58C4DD", "Funções" : "#AA77C7"},
        ).scale(0.72)

        linha.set_width(titulo.get_width())

        subtitulo = Text(
            "",
            font_size=100,
            weight=BOLD,
            t2c={"programa": "#AA77C7"},
        ).scale(0.26)

        bloco = VGroup(capitulo, linha, titulo, subtitulo).arrange(DOWN, buff=0.3)
        bloco.move_to(ORIGIN)

        posicao_final_titulo = titulo.get_center()

        tampa = Rectangle(
            width=titulo.width + 0.4,
            height=titulo.height + 0.4,
            fill_color="#1E1E1E",
            fill_opacity=1,
            stroke_opacity=0,
        )
        tampa.next_to(linha, UP, buff=0)

        # Orgnizacao
        titulo.set_z_index(0)
        tampa.set_z_index(1)
        linha.set_z_index(2)
        capitulo.set_z_index(2)
        subtitulo.set_z_index(0)

        titulo.move_to(tampa.get_center())


        self.add(tampa)
        self.play(Write(capitulo))
        self.play(Create(linha))
        self.play(titulo.animate.move_to(posicao_final_titulo), run_time=1.3)
        self.play(FadeIn(subtitulo))
        self.wait()

        self.play(FadeOut(subtitulo),titulo.animate.move_to(tampa.get_center()),Unwrite(capitulo))
        self.play(Uncreate(linha),FadeOut(titulo))
        self.play(FadeOut(tampa))

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
        self.wait()
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

    double media1 = calcularMedia(a1,b1);

    double media2 = calcularMedia(a2,b2);

    double media3 = calcularMedia(a3,b3);

    double media4 = calcularMedia(a4,b4);

    double media5 = calcularMedia(a5,b5);
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
        
    double media1 = calcularMedia(a1, b1);

    double media2 = calcularMedia(a2, b2);

    double media3 = calcularMedia(a3, b3);

    double media4 = calcularMedia(a4, b4);

    double media5 = calcularMedia(a5, b5);
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



        # ----------- Animações -----------

        self.play(Write(final))
        self.wait()

class Creditos(Scene):
    def construct(self):
        #creditos
        logo = ImageMobject("assets/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        cursor=ImageMobject("assets/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)
        titulo=Text("Créditos", font_size=80)
        titulo.color="#AA77C7"

   
        diretor = VGroup(T("Diretor", color = "#AA77C7", font_size=60), T("Rainier R. Waki", font_size=50)).arrange(DOWN, buff=0.3)
        tutor = VGroup(T("Tutor", color = "#AA77C7", font_size=60), T("Alyson V. Isaluski", font_size=50)).arrange(DOWN, buff=0.3)
        redator = VGroup(T("Redator", color = "#AA77C7", font_size=60), T("Eduardo M. de Souza", font_size=50)).arrange(DOWN, buff=0.3)
        animadores = VGroup(
            T("Animadores", color = "#AA77C7", font_size=60),
            VGroup(
                T("Natália S. Kikuti", font_size=50),
                T("Gabriel Covalski", font_size=50)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        editora = VGroup(T("Editora", color = "#AA77C7", font_size=60), T("Sophia B. Peraza", font_size=50)).arrange(DOWN, buff=0.3)
        roteirista = VGroup(
            T("Roteiristas", color = "#AA77C7", font_size=60),
            VGroup(
                T("Alyson V. Isaluski", font_size=50),
                T("Kia de P. Marins", font_size=50)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        utfpr = ImageMobject("assets/utfpr.png").scale(0.7)
        
        creditos = VGroup(diretor, tutor, redator, animadores).scale(0.6)
        creditos2= VGroup(editora, roteirista).scale(0.6)

        for bloco in creditos:
            if isinstance(bloco, VGroup):
                bloco.arrange(DOWN, aligned_edge=LEFT)

        for bloco in creditos2:
            if isinstance(bloco, VGroup):
                bloco.arrange(DOWN, aligned_edge=LEFT)

        creditos.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        creditos.to_edge(LEFT, buff=0.5).shift(UP*0.2)

        creditos2.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        creditos2.to_edge(LEFT, buff=0.5).shift(UP*0.2)

        utfpr.scale(0.4)
        utfpr.move_to(DOWN*3.5)
        utfpr.to_edge(LEFT, buff=0.5)

        self.play(
            logoOrigin.animate.become(logo),
            run_time=2
        )

        # Cursor aparece e se move
        self.play(cursor.animate.move_to(ORIGIN+RIGHT*0.25+DOWN*0.45))
        self.play(cursor.animate.scale(0.8), run_time=0.1, rate_func=linear)  # Clica
        self.play(cursor.animate.scale(1.2), run_time=0.1, rate_func=linear)  #

        # Vinheta Puxada
        self.play(
            GrowFromCenter(Rectangle(color="#0A0A0A", fill_opacity=1, width=20, height=10), run_time=0.5)
        )

        # Nomes e Cargos
        self.play(Write(creditos),FadeIn(utfpr))
        self.wait()
        self.play(FadeOut(creditos))
        self.play(Write(creditos2))
        self.wait()
        self.play(FadeOut(creditos2),FadeOut(utfpr))
