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
		
		Contagem.construct(self)
    	Main.construct(self)
        Paradigma.construct(self)
        Bibliotecas.construct(self)
        Linha1.construct(self)
        Unistd.construct(self)
        Biblioteca.construct(self)
        Recapitulando.construct(self)
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

class Contagem(Scene):
    def construct(self):
        contString = r'''#include <stdio.h>
#include <unistd.h>

int main(){
    printf("Contagem regressiva 1:\n");
    printf("3\n");
    sleep(1);
    printf("2\n");
    sleep(1);
    printf("1\n");
    sleep(1);

    printf("Contagem regressiva 2:\n");
    printf("3\n");
    sleep(1);
    printf("2\n");
    sleep(1);
    printf("1\n");
    sleep(1);

    printf("Contagem regressiva 3:\n");
    printf("3\n");
    sleep(1);
    printf("2\n");
    sleep(1);
    printf("1\n");
    sleep(1);
    return 0;
}'''
        contCod = codigoComando(contString).move_to(ORIGIN).scale(0.65)

        self.play(FadeIn(contCod[1][0:5]))
        self.wait(3)
        self.play(Write(contCod[1][5]))
        self.wait()
        self.play(Write(contCod[1][6]))
        self.wait(2.5)

        contorno = SurroundingRectangle(contCod[1][6], color=WHITE, buff=0.05, stroke_width=3)
        self.play(Create(contorno))
        #self.play(Circumscribe(contCod[1][6], buff=0.05,  color=WHITE), run_time=1.5)

        # --- Explicação da função sleep ---
        importada = Text("Função importada", font_size=35, color=WHITE, weight=BOLD).scale(0.6).next_to(contCod[1][6], RIGHT*4)
        seta = Arrow(start= contorno.get_right(), end=importada.get_left(), color=WHITE)
        self.play(GrowArrow(seta))
        self.play(Write(importada))
        self.wait(1.5)
        self.play(FadeOut(importada, seta, contorno))

        sublinhado = Underline(contCod[1][6][5:8], color=WHITE)
        self.play(Create(sublinhado))

        pausa = Text("Pausa por 1 segundo", font_size=35, color=WHITE, weight=BOLD).scale(0.5).next_to(contCod[1][6], RIGHT)
        self.play(Write(pausa))
        self.wait(4)
        self.play(FadeOut(sublinhado, pausa))
        # ---

        self.play(Write(contCod[1][7]))
        self.wait()
        self.play(Write(contCod[1][8]))
        self.wait(1.5)
        self.play(Write(contCod[1][9]))
        self.wait()
        self.play(Write(contCod[1][10]))
        self.wait(1.5)

        self.play(FadeIn(contCod[1][11:19]), run_time=0.7)
        self.play(FadeIn(contCod[1][19:27]), run_time=0.7)

        self.play(Write(contCod[1][27:30]))
        self.wait()

        # --- Zoom das partes repetidas do código ---
        self.play(contCod[1][5:12].animate.scale(1.1), contCod[1][0:5].animate.set_opacity(0.4), contCod[1][12:30].animate.set_opacity(0.4), run_time=0.7)
        self.play(contCod[1][5:12].animate.scale(0.9), contCod[1][0:5].animate.set_opacity(1), contCod[1][12:30].animate.set_opacity(1), run_time=0.7)
        self.wait(0.15)

        self.play(contCod[1][13:20].animate.scale(1.1), contCod[1][0:13].animate.set_opacity(0.4), contCod[1][20:30].animate.set_opacity(0.4), run_time=0.7)
        self.play(contCod[1][13:20].animate.scale(0.9), contCod[1][0:13].animate.set_opacity(1), contCod[1][20:30].animate.set_opacity(1), run_time=0.7)
        self.wait(0.15)

        self.play(contCod[1][21:27].animate.scale(1.1), contCod[1][0:21].animate.set_opacity(0.4), contCod[1][27:30].animate.set_opacity(0.4), run_time=0.7)
        self.play(contCod[1][21:27].animate.scale(0.9), contCod[1][0:21].animate.set_opacity(1), contCod[1][27:30].animate.set_opacity(1), run_time=0.7)
        self.wait(0.15)
        # ---

        self.wait(2)
        funcString = r'''#include <stdio.h>
#include <unistd.h>

void contagemRegressiva(){
    printf("3\n");
    sleep(1);
    printf("2\n");
    sleep(1);
    printf("1\n");
    sleep(1);
    return;
}

int main(){
    printf("Contagem regressiva 1:\n");
    contagemRegressiva();
    printf("Contagem regressiva 2:\n");
    contagemRegressiva();
    printf("Contagem regressiva 3:\n");
    contagemRegressiva();
    return 0;
}
'''

        funcCod = codigoComando(funcString).move_to(ORIGIN).scale(0.65)
        self.play(TransformMatchingShapes(contCod, funcCod))
        self.wait(2)
        #self.play(Write(funcCod))

        self.play(Circumscribe(funcCod[1][2:12], buff=0.05, fade_out=True, color=WHITE, stroke_width=3), run_time=1.5)

        sublinhado1 = Underline(funcCod[1][19], color=WHITE, buff=0, stroke_width=3)
        sublinhado2 = Underline(funcCod[1][15], color=WHITE, buff=0, stroke_width=3)
        sublinhado3 = Underline(funcCod[1][17], color=WHITE, buff=0, stroke_width=3)
        self.play(Create(sublinhado1), Create(sublinhado2), Create(sublinhado3))
        self.play(FadeOut(sublinhado1, sublinhado2, sublinhado3))

        cod = funcCod.copy().to_edge(LEFT, buff=1)
        self.play(Transform(funcCod, cod))
        
        for i in range(13, 16): 
            if i == 13:
                h = get_highlight(funcCod, i)
                self.play(FadeIn(h), run_time=0.5)
                self.wait()
            elif i == 15:
                s = h
                h = get_highlight(funcCod, i, PURPLE)
                self.play(ReplacementTransform(s, h), run_time=0.5)
                self.wait()
            else:
                s = h
                h = get_highlight(funcCod, i)
                self.play(ReplacementTransform(s, h), run_time=0.5)
                self.wait()

        # função contagem regressiva executando
        for i in range(3, 12): 
            if i == 3:
                a = get_highlight(funcCod, i, PURPLE)
                self.play(FadeIn(a), run_time=0.5)
                self.wait()
            elif i == 11:
                self.play(FadeOut(a), run_time=0.5)
                self.wait()
            else:
                s = a
                a = get_highlight(funcCod, i, PURPLE)
                self.play(ReplacementTransform(s, a), run_time=0.5)
                self.wait()

        for i in range(16, 18): 
            if i == 17:
                s = h
                h = get_highlight(funcCod, i, PURPLE)
                self.play(ReplacementTransform(s, h), run_time=0.5)
                self.wait()
            # # elif i == 18:
            # #     self.play(FadeOut(h), run_time=0.5)
            else:
                s = h
                h = get_highlight(funcCod, i)
                self.play(ReplacementTransform(s, h), run_time=0.5)
                self.wait()

        # função contagem regressiva executando
        for i in range(3, 12): 
            if i == 3:
                b = get_highlight(funcCod, i, PURPLE)
                self.play(FadeIn(b), run_time=0.5)
                self.wait()
            elif i == 11:
                self.play(FadeOut(b), run_time=0.5)
                self.wait()
            else:
                s = b
                b = get_highlight(funcCod, i, PURPLE)
                self.play(ReplacementTransform(s, b), run_time=0.5)
                self.wait()

        for i in range(18, 20): 
            if i == 19:
                s = h
                h = get_highlight(funcCod, i, PURPLE)
                self.play(ReplacementTransform(s, h), run_time=0.5)
                self.wait()
            #     h = get_highlight(funcCod, i)
            #     self.play(FadeIn(h), run_time=0.5)
            # # elif i == 20:
            # #     self.play(FadeOut(h), run_time=0.5)
            else:
                s = h
                h = get_highlight(funcCod, i)
                self.play(ReplacementTransform(s, h), run_time=0.5)
                self.wait()

        # função contagem regressiva executando
        for i in range(3, 12): 
            if i == 3:
                c = get_highlight(funcCod, i, PURPLE)
                self.play(FadeIn(c), run_time=0.5)
                self.wait()
            elif i == 11:
                self.play(FadeOut(c), run_time=0.5)
                self.wait()
            else:
                s = c
                c = get_highlight(funcCod, i, PURPLE)
                self.play(ReplacementTransform(s, c), run_time=0.5)
                self.wait()

        s = h
        h = get_highlight(funcCod, 20)
        self.play(ReplacementTransform(s, h), run_time=0.5)
        self.wait()
        self.play(FadeOut(h))
        self.wait()

        self.play(funcCod[1:].animate.set_opacity(0.2))
        textModularizar = Text("Modularizar",color="#AA77C7")
        textSeparar = Text("Separar").next_to(textModularizar,DOWN)
        textOrganizar = Text("Organizar").next_to(textSeparar,DOWN)

        group3Palavras = VGroup(textModularizar,textSeparar,textOrganizar).move_to(ORIGIN).scale(2)

        self.play(Write(textModularizar))
        self.play(Write(textSeparar))
        self.play(Write(textOrganizar))

        self.wait()

        self.play(Unwrite(group3Palavras),FadeOut(funcCod))
        self.wait()


        # self.wait(2.5)
        # self.play(FadeOut(*self.mobjects))

# class Modularizar(Scene):
#     def construct(self):
#         textModularizar = Text("Modularizar",color="#AA77C7")
#         textSeparar = Text("Separar").next_to(textModularizar,DOWN)
#         textOrganizar = Text("Organizar").next_to(textSeparar,DOWN)

#         group3Palavras = VGroup(textModularizar,textSeparar,textOrganizar).move_to(ORIGIN).scale(2)

#         self.play(Write(textModularizar))
#         self.play(Write(textSeparar))
#         self.play(Write(textOrganizar))

#         self.wait()

#         self.play(Unwrite(group3Palavras))
#         self.wait()

class Main(Scene):
    def construct(self):
        mainstring1 = r'''int main(){
    printf("Contagem regressiva 1:\n");
    contagemRegressiva();
    printf("Contagem regressiva 2:\n");
    contagemRegressiva();
    printf("Contagem regressiva 3:\n");
    contagemRegressiva();
    return 0;
}'''
        codmain = codigoComando(mainstring1).move_to(ORIGIN).scale(0.8)

        #self.play(Write(codmain[1][0]), Write(codmain[1][7]), Write(codmain[1][8]), run_time=0.5)
        self.play(Write(codmain[1][0]), run_time=0.5)
        self.play(Write(codmain[1][7]), run_time=0.2)
        self.play(Write(codmain[1][8]), run_time=0.2)

        self.play(Write(codmain[1][1]), Write(codmain[1][3]), Write(codmain[1][5]))
        self.wait(2)
        self.play(Write(codmain[1][2]), Write(codmain[1][4]), Write(codmain[1][6]))

        # self.play(FadeIn(codmain[1][1]), run_time=0.8)
        # self.play(FadeIn(codmain[1][3]), run_time=0.8)
        # self.play(FadeIn(codmain[1][5]), run_time=0.8)
        # self.play(FadeIn(codmain[1][2]), run_time=0.8)
        # self.play(FadeIn(codmain[1][4]), run_time=0.8)
        # self.play(FadeIn(codmain[1][6]), run_time=0.8)
                  
        #self.play(Write(codmain[1][7]), Write(codmain[1][8]), run_time=0.5)
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

class Bibliotecas(Scene):
    def construct(self):
        funcString = r'''#include <stdio.h>
#include <unistd.h>
        
void contagemRegressiva(){
    printf("3\n");
    sleep(1);
    printf("2\n");
    sleep(1);
    printf("1\n");
    sleep(1);
    return;
}

int main(){
    printf("Contagem regressiva 1:\n");
    contagemRegressiva();
    printf("Contagem regressiva 2:\n");
    contagemRegressiva();
    printf("Contagem regressiva 3:\n");
    contagemRegressiva();
    return 0;
}
'''
        
        funcCod = codigoComando(funcString).move_to(ORIGIN).scale(0.65)
        self.play(FadeIn(funcCod))

        self.play(Circumscribe(funcCod[1][0], buff=0.05, fade_out=True, color=WHITE, stroke_width=3), 
                  Circumscribe(funcCod[1][4][0:6], buff=0.05, fade_out=True, color=WHITE, stroke_width=3), 
                  Circumscribe(funcCod[1][6][0:6], buff=0.05, fade_out=True, color=WHITE, stroke_width=3), 
                  Circumscribe(funcCod[1][8][0:6], buff=0.05, fade_out=True, color=WHITE, stroke_width=3), 
                  Circumscribe(funcCod[1][14][0:6], buff=0.05, fade_out=True, color=WHITE, stroke_width=3),
                  Circumscribe(funcCod[1][16][0:6], buff=0.05, fade_out=True, color=WHITE, stroke_width=3),
                  Circumscribe(funcCod[1][18][0:6], buff=0.05, fade_out=True, color=WHITE, stroke_width=3),
                  run_time=2)

        self.wait()

        self.play(Circumscribe(funcCod[1][1], buff=0.05, fade_out=True, color=WHITE, stroke_width=3), 
                  Circumscribe(funcCod[1][5][0:5], buff=0.05, fade_out=True, color=WHITE, stroke_width=3),
                  Circumscribe(funcCod[1][7][0:5], buff=0.05, fade_out=True, color=WHITE, stroke_width=3),
                  Circumscribe(funcCod[1][9][0:5], buff=0.05, fade_out=True, color=WHITE, stroke_width=3),
                  run_time=2)

        self.wait(2.5)
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

class Unistd(MovingCameraScene):
    def construct(self):
        funcString = r'''#include <stdio.h>
#include <unistd.h>
        
void contagemRegressiva(){
    printf("3\n");
    sleep(1);
    printf("2\n");
    sleep(1);
    printf("1\n");
    sleep(1);
    return;
}

int main(){
    printf("Contagem regressiva 1:\n");
    contagemRegressiva();
    printf("Contagem regressiva 2:\n");
    contagemRegressiva();
    printf("Contagem regressiva 3:\n");
    contagemRegressiva();
    return 0;
}
'''

        funcCode = codigoComando(funcString).move_to(ORIGIN).scale(0.65)
        
        self.play(FadeIn(funcCode))
        self.play(self.camera.frame.animate.move_to(funcCode[1][1]).scale(0.6))
        self.play(funcCode[1][1].animate.set_opacity(0))
        self.play(self.camera.frame.animate.move_to(funcCode[1][7]))
        self.wait(2.5)
        #opção 1
        rect = SurroundingRectangle(funcCode[1][5], color=WHITE, buff=0.05)
        rect2 = SurroundingRectangle(funcCode[1][7], color=WHITE, buff=0.05)
        rect3 = SurroundingRectangle(funcCode[1][9], color=WHITE, buff=0.05)
        self.play(
                  ShowPassingFlash(rect, time_width=0.5, run_time=1.5),
                  ShowPassingFlash(rect2, time_width=0.5, run_time=1.5),
                  ShowPassingFlash(rect3, time_width=0.5, run_time=1.5),)

        # self.play(
        #         Circumscribe(funcCode[1][5][0:5], buff=0.05, color=WHITE, stroke_width=3),
        #         Circumscribe(funcCode[1][7][0:5], buff=0.05, color=WHITE, stroke_width=3),
        #         Circumscribe(funcCode[1][9][0:5], buff=0.05, color=WHITE, stroke_width=3),
        #         run_time=2
        #         )
        # #opção 2
        # underline = Underline(helloworldcode[1][3], color=RED, buff=0.05)
        # self.play(ShowPassingFlash(underline, time_width=0.4, run_time=1.5))
        self.wait()
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

class Recapitulando(Scene):
    def construct(self):
        titulo = Text("Recapitulando...", color=PURPLE, font_size=35, weight=BOLD)
        topico1 = Text("2.  É necessário que exista uma função main", font_size=33)
        topico2 = Text("3.  Podemos chamar outras funções importadas ou\ndeclaradas no código", font_size=33)
        topico3 = Text("4.  Dividimos o código em subrotinas para que\nfique menor e mais organizado", font_size=33)
        topico4 = Text("1.  Um código em C tem uma ou mais funções", font_size=33)

        topicos = VGroup(topico4, topico1, topico2, topico3).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        tudo = VGroup(titulo, topicos).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(ORIGIN)

        self.play(Write(titulo))
        self.wait()
        self.play(Write(topico4))
        self.wait()
        self.play(Write(topico1))
        self.wait()
        self.play(Write(topico2), run_time=2.5)
        self.wait()
        self.play(Write(topico3), run_time=2.5)

        self.wait()
        self.play(Unwrite(tudo))

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
