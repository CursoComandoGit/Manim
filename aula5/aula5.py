from manim import *
import random
from objetoFisico import ObjetoFisico
import numpy as np
from customTerminal import CustomTerminal

#Escaneia objeto escolhido. A animação é feita assim que a função é chamada
def scanAnimation(scene, target_mobject, UDbuff = 0, LRbuff = 0, color=GREEN, scan_time=1.0, glow_opacity=0.15):
    top_y = target_mobject.get_top()[1] + UDbuff
    bottom_y = target_mobject.get_bottom()[1] - UDbuff
    left_x = target_mobject.get_left()[0] - LRbuff
    right_x = target_mobject.get_right()[0] + LRbuff
    
    mainLine = Line(
        start=np.array([left_x, top_y, 0]), 
        end=np.array([left_x, bottom_y, 0]), 
        color=color, 
        stroke_width=2
    )
    
    glow_group = VGroup()
    for width_mult, opacity in [(3, 0.4), (6, 0.2), (10, 0.1)]:
        glow_line = mainLine.copy().set_stroke(color=color, width=mainLine.stroke_width * width_mult, opacity=opacity)
        glow_group.add(glow_line)
        
    scanner_beam = VGroup(glow_group, mainLine)
    
    scan_tail = Polygon(
        [left_x, top_y, 0],
        [left_x, top_y, 0],
        [left_x, bottom_y, 0],
        [left_x, bottom_y, 0],
        color=color,
        stroke_width=0,
        fill_opacity=glow_opacity
    )

    #Não gosto de definir updaters dentro de funções mas posso arrumar depois
    def update_tail(tail):
        current_x = scanner_beam.get_center()[0]
        
        if current_x - left_x < 0.01:
            return
            
        tail.become(
            Polygon(
                [left_x, top_y, 0],
                [current_x, top_y, 0],
                [current_x, bottom_y, 0],
                [left_x, bottom_y, 0],
                color=color,
                stroke_width=0,
                fill_opacity=glow_opacity
            )
        )
    
    scan_tail.add_updater(update_tail)

    scene.play(FadeIn(scanner_beam), run_time=0.5)
    scene.add(scan_tail)
    scene.play(
        scanner_beam.animate.shift(RIGHT * (right_x - left_x)),
        run_time=scan_time,
        rate_func=linear
    )
    
    scan_tail.remove_updater(update_tail)
    scene.play(
        scanner_beam.animate.scale(0),
        scan_tail.animate.set_fill(opacity=0),
        run_time=0.5
    )
    scene.remove(scanner_beam, scan_tail)

def criar_card(nome, cor, exemplo):
            caixa = RoundedRectangle(
                width=2.2, height=2.4, corner_radius=0.2, color=cor, fill_color=cor, fill_opacity=0.15, stroke_width=3
            )
            rotulo_nome = Text(nome, font_size=30, color=cor, weight=BOLD, disable_ligatures=True)
            rotulo_exemplo = Text(exemplo, font_size=26)
            conteudo = VGroup(rotulo_nome, rotulo_exemplo).arrange(DOWN, buff=0.5)
            conteudo.move_to(caixa.get_center())
            return VGroup(caixa, conteudo)
def update_int(mob, dt):
    mob.tempo_acumulado += dt
    
    if mob.tempo_acumulado >= 0.5:
        mob.tempo_acumulado -= 0.5
        
        numero_aleatorio = str(random.randint(1, 99))
        novo_rotulo = Text(numero_aleatorio, font_size=26)
        
        novo_rotulo.move_to(mob[1][1].get_center())
        
        mob[1][1].become(novo_rotulo)
def update_float(mob, dt):
    mob.tempo_acumulado += dt
    
    if mob.tempo_acumulado >= 0.5:
        mob.tempo_acumulado -= 0.5
        
        numero_aleatorio = str(round(random.uniform(1, 99), 2))
        novo_rotulo = Text(numero_aleatorio, font_size=26)
        
        novo_rotulo.move_to(mob[1][1].get_center())
        
        mob[1][1].become(novo_rotulo)
def update_char(mob, dt):
    mob.tempo_acumulado += dt
    characteres = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u","v","w","x","y","z"]
    if mob.tempo_acumulado >= 0.5:
        mob.tempo_acumulado -= 0.5
        
        
        novo_rotulo = Text(characteres[random.randint(0, 25)], font_size=26)
        
        novo_rotulo.move_to(mob[1][1].get_center())
        
        mob[1][1].become(novo_rotulo)

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


def alyBemAly(target_point=ORIGIN, num_arrows=15, min_dist=0.5, max_dist=3.0, arrow_length=1.5,
              off_screen_offset=15.0, run_time=1.5, lag_ratio=0.05, leave_after = True, time_until_leave = 1) -> Succession:
    animations = []
    arrows = VGroup()
    for _ in range(num_arrows):
        angulo = np.random.uniform(0, 2 * PI)
        
        direcao = np.array([np.cos(angulo), np.sin(angulo), 0])
        dist = np.random.uniform(min_dist, max_dist)

        final = target_point + dist * direcao
        finalTail = final + arrow_length * direcao

        arrow = Arrow(start=finalTail, end=final, buff=0)
        arrows.add(arrow)
        arrow.shift(off_screen_offset * direcao)

        anim = arrow.animate(run_time=run_time).shift(-off_screen_offset * direcao)
        animations.append(anim)

    if leave_after:
        return Succession(AnimationGroup(*animations, lag_ratio=lag_ratio), Wait(time_until_leave), arrows.animate.set_opacity(0))
    return Succession(AnimationGroup(*animations, lag_ratio=lag_ratio))

Circumscribe.set_default(color=WHITE)
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

class Intro(Scene):
    def construct(self):
        num_lines = 50
        binary_string = "\n".join("".join(random.choice(["0", "1"]) for _ in range(18)) for _ in range(num_lines))
        
        block1 = Text(binary_string, font="DejaVu Sans Mono", line_spacing=1).scale(0.6)
        block2 = block1.copy()
        
        gap = 0.2
        block2.next_to(block1, DOWN, buff=gap)
        
        scrolling_group = VGroup(block1, block2)
        scrolling_group.move_to(ORIGIN)
        
        self.add(scrolling_group)
        
        scroll_speed = 3.0 
        loop_distance = block1.height + gap 
        start_y = scrolling_group.get_y()
        
        scrolling_group.time_passed = 0.0
        
        def background_scroll(mob, dt):
            mob.time_passed += dt
            
            total_movement = scroll_speed * mob.time_passed
            current_offset = total_movement % loop_distance
            
            mob.set_y(start_y + current_offset)
            
        scrolling_group.add_updater(background_scroll)
        audio = ImageMobject("images\\audio").move_to([-4,0,0]).scale(0.5)
        image = ImageMobject("images\\play").move_to([4,0,0]).scale(0.5)

        self.wait(4)
        self.play(GrowFromPoint(audio, ORIGIN))
        self.play(GrowFromPoint(image, ORIGIN))
        self.wait(2)

        self.play(audio.animate.scale(0).move_to(ORIGIN),
                    image.animate.scale(0).move_to(ORIGIN))
        self.remove(audio, image)
        scrolling_group.remove_updater(background_scroll)
        self.wait(0.5)
        self.play(scrolling_group.animate.shift([-4,0,0]))

        self.wait()
        print = Text("printf(\"blablabla\")").move_to([3,1,0]).scale(0.8)
        string = Text("\"blablabla\"").move_to([3,1,0]).scale(0.8)
        numero = Text("27").scale(0.8).move_to([3,-1,0])

        #Novas animações do roteiro
        bitSegment = VGroup(block2[-i] for i in range(5, 35))
        bitSegment2 = VGroup(block2[-i] for i in range(40, 48))
        bitSegment3 = VGroup(block2[-i] for i in range(60, 124))

        self.play(Transform(bitSegment, print))
        self.wait(0.5)
        self.play(Transform(bitSegment, string))
        self.wait(0.5)
        self.play(Transform(bitSegment3, numero))
        self.wait()
        #Bunch of bs appears on the screen
        posicoes = [[2,-1,0], [2,1,0], [2,2.8,0], [2,-2.8,0], [5, -1, 0], [5,1,0], [4.5,3,0], [4.4,-3,0], [1.8,1.8,0], [1.2,-1.6,0]]
        textoCoisas = ["4", "3.141592", "'b'", "a", "\"constante\"", "500", "\"maiscoisa\"", "\"help me\"", "5","\"ssssp\""]
        things = VGroup(Text(textoCoisas[sample]).scale(random.uniform(1,1.15)).move_to(posicoes[sample])
                        for sample in range(0,len(textoCoisas)))
        correspondingBits = VGroup(VGroup(block2[-j] for j in range(125+5*i, 125+5*(i+1))) for i in range(0,len(textoCoisas)))
        self.wait()
        self.play(bitSegment.animate.set_opacity(0.5),
                  bitSegment2.animate.set_opacity(0.5),
                  bitSegment3.animate.set_opacity(0.5), Succession(*[Transform(correspondingBits[i], things[i]) for i in range(0,int(len(textoCoisas)/2))]), run_time=1)
        self.play(Succession(*[Transform(correspondingBits[i], things[i]) for i in range(int(len(textoCoisas)/2), len(textoCoisas))]), run_time=0.5)
        self.wait(2)
        self.remove(bitSegment, bitSegment2, bitSegment3, correspondingBits, things, scrolling_group)
        #nova animação com cards
        self.clear()
        self.wait()
        variavel = Text("variáveis", color=PURPLE)
        self.add(variavel)
        self.wait(2)
        inteiro = criar_card("int", BLUE_D, "10").move_to([-3,-8,0])
        flutuante = criar_card("float", RED_E, "11.2").move_to([0,-8,0])
        charactere = criar_card("char", GREEN_C, 'c').move_to([3,-8,0])
        definicao = Text("são nomes.").move_to([10,0,0])
        self.play(variavel.animate.shift([0,0.5,0]), inteiro.animate.move_to([-3,-1.5,0]), flutuante.animate.move_to([0,-1.5,0]), charactere.animate.move_to([3,-1.5,0]))
        inteiro.tempo_acumulado=0.0
        flutuante.tempo_acumulado=0.0
        charactere.tempo_acumulado=0.0
        inteiro.add_updater(update_int)
        flutuante.add_updater(update_float)
        charactere.add_updater(update_char)

        self.wait(2)
        inteiro.clear_updaters()
        flutuante.clear_updaters()
        charactere.clear_updaters()
        self.play(inteiro.animate.move_to([-3,-9,0]), flutuante.animate.move_to([0,-9,0]), charactere.animate.move_to([3,-9,0]),
                  variavel.animate.center())
        variavel.save_state()
        grupo = VGroup(variavel, definicao)
        self.play(grupo.animate.arrange(direction=RIGHT))
        self.wait()
        self.play(Restore(variavel), FadeOut(definicao))
        self.play(variavel.animate.move_to([3,0,0]))

        #Resume animação antiga
        ram = Text("RAM").move_to([-3,2,0]).scale(0.8)
        box = Rectangle(height=4, width=2.5).move_to([-3,-1,0])

        self.wait()
        self.play(GrowFromCenter(ram), GrowFromCenter(box))
        arrow = CurvedArrow(variavel.get_left(), box.get_right()+[0,0.25,0], color=YELLOW)
        novoValor2 = Text("3").scale(0.8).move_to(arrow.get_end()+[-1,0,0])
        novoValor = Text("6").scale(0.8).move_to(arrow.get_end()+[-1,0,0])
        valor = Text("10110100").scale(0.8).move_to(arrow.get_end()+[-1.2,0,0])
        linhas = VGroup(Line([box.get_right()[0], arrow.get_end()[1] + 0.45, 0], [box.get_left()[0],arrow.get_end()[1] + 0.45,0]),
                        Line([box.get_right()[0],arrow.get_end()[1] - 0.45,0], [box.get_left()[0],arrow.get_end()[1] - 0.45,0]))
        self.wait()
        self.play(Create(arrow), Create(linhas[0]), Create(linhas[1]))
        self.play(GrowFromPoint(valor, arrow.get_end()))
        self.play(Transform(valor, novoValor))
        self.play(Transform(valor, novoValor2))
        self.wait()

        #Definindo uma gaveta
        corpo = Rectangle(BLACK, height=1.6).set_fill(DARK_BROWN, 1)
        corpo2 = Rectangle(BLACK, height=2.6, width=1.15).set_fill(DARK_BROWN, 1).move_to(corpo.get_left(), aligned_edge=RIGHT).shift([0,0.5,0])
        bola = Circle(radius=0.6, color=BLACK).set_fill(YELLOW, 1).move_to(corpo2.get_left(), aligned_edge=RIGHT)
        tag = SVGMobject("svgs\\tag").move_to(bola.get_right(), aligned_edge=UP).shift([-0.5,0.2,0])
        bitsTag = Text("VAR", font="DejaVu Sans Mono", color=GREY).move_to(tag.get_center()).shift([0.175,-0.155,0]).rotate(25).scale(0.7)

        gaveta = VGroup(corpo, corpo2, bola, tag, bitsTag).move_to([10,0,0]).scale(0.8)
        self.add(gaveta)
        self.play(box.animate.shift([-9,0,0]), ram.animate.shift([-9,0,0]), valor.animate.shift([-9,0,0]), linhas.animate.shift([-9,0,0]),
                  arrow.animate.shift([-10,0,0]), variavel.animate.move_to([-2,0,0]),
                  gaveta.animate.move_to([5,0,0]))
        
        bitsGaveta1 = Text("00101", font="DejaVu Sans Mono").scale(1).move_to(corpo.get_top()).shift([0,1,0])

        self.play(Succession(GrowFromPoint(bitsGaveta1, corpo.get_top(), run_time=0.5)))
        self.wait()

        self.play(bitsGaveta1.animate.scale(0).move_to(corpo.get_top()))
        
        self.play(variavel.animate.center(),
                  gaveta.animate.move_to([11,0,0]))
        self.wait()
        self.play(Write(Text("?").scale(3)))

        self.play(FadeOut(*self.mobjects))
        self.clear()

class CriandoAVariavel(Scene):
    def construct(self):
        codigoString = '''#include <stdio.h>

int main() {

    int quantidade;

}
'''

        exemploCodigo = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material",
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        exemploCodigo.save_state()
        exemploCodigo.code_lines[1:].move_to([0,-9,0])
        bib = get_highlight(exemploCodigo, 0)
        self.play(Write(exemploCodigo))
        self.wait()
        self.play(FadeIn(bib))
        self.wait()

        self.play(FadeOut(bib))
        self.wait(0.5)
        self.play(Restore(exemploCodigo))
        self.wait(0.5)
        self.play(Circumscribe(exemploCodigo.code_lines[2][11], color=WHITE), Circumscribe(exemploCodigo.code_lines[6], color=WHITE))
        self.wait(1.25)

        titulo = Text("Declaração de variável", weight=BOLD, t2c={"variável":"#AA77C7"}, font_size = 100).scale(0.6)
        descr = Text("Sintaxe básica", weight=BOLD, font_size = 100).scale(0.3)
        criaCapitulo(self, titulo, descr, 1)

        self.play(Indicate(exemploCodigo.code_lines[4][4:8], color=BLUE))
        self.wait(0.5)
        self.play(Indicate(exemploCodigo.code_lines[4][8:18], color=WHITE))
        self.wait(0.5)
        self.play(Indicate(exemploCodigo.code_lines[4][18:19], color=WHITE))
        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.clear()

class RegrasNome(Scene):
    def construct(self):
        title = Text("Regras para nomes de variável", weight=BOLD, t2c={"nomes":"#AA77C7"}, font_size = 100).scale(0.6)

        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade;
    int QuAntiDaDe;
    char comando_c;

    int 4aula;
    char *Comando%CÊ-;
    int void;
}
'''
        exampleCode = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        
        self.play(FadeIn(exampleCode))
        self.wait(2)

        correct1 = get_highlight(exampleCode, 3)
        correct2 = get_highlight(exampleCode, 4)
        correct3 = get_highlight(exampleCode, 5)
        self.play(FadeIn(correct1))
        self.play(FadeIn(correct2))
        self.play(FadeIn(correct3))
        self.wait()

        #Mostrando exemplo ruim
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade;
    int QuAntiDaDe;
    char comando_c;

    int aula4;
    char *Comando%CÊ-;
    int void;
}
'''
        exampleCode2 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material",
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        
        incorrect = get_highlight(exampleCode, 7)
        self.play(FadeIn(incorrect), FadeOut(correct1, correct2, correct3))
        self.wait()
        self.play(incorrect.animate.set_fill(RED_A), incorrect.animate.set_color(RED_A))
        self.play(incorrect.animate.scale_to_fit_width(0), Transform(exampleCode, exampleCode2))
        self.remove(incorrect)
        self.wait()
        incorrect2 = get_highlight(exampleCode2, 8, color=RED_A)
        incorrect3 = get_highlight(exampleCode2, 9, color=RED_A)
        self.play(FadeIn(incorrect2))
        self.wait()
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade;
    int QuAntiDaDe;
    char comando_c;

    int aula4;
    char ComandoC;
    int void;
}
'''
        exampleCode3 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material",
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        
        #Mostrando último incorreto sintaxe
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade;
    int QuAntiDaDe;
    char comando_c;

    int aula4;
    char ComandoC;
    int contador;
}
'''
        exampleCode4 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        
        self.play(incorrect2.animate.scale_to_fit_width(0),
                  Transform(exampleCode, exampleCode3))
        self.remove(incorrect2, incorrect3)
        self.wait()
        self.play(FadeIn(incorrect3))
        self.wait()
        self.play(incorrect3.animate.scale_to_fit_width(0),
                  Transform(exampleCode, exampleCode4))
        self.wait()
        programmer = SVGMobject("svgs\\lockedIn").move_to([9,0,0]).flip()
        self.add(programmer)

        self.play(exampleCode.animate.move_to([-2,0,0]), programmer.animate.move_to([4,-0.5,0]))
        #Nomes ruins batem no código e vão embora
        a = Text("a").move_to([3,1,0])
        aImovel = Text("a").move_to([3,1,0])
        aObj = ObjetoFisico(a, np.array([-6,2,0]), xBounds=[exampleCode.get_right()[0], 20], damping=0.25)
        self.play(GrowFromPoint(aImovel, programmer.get_top()))
        self.add(aObj)
        self.remove(aImovel)

        aObj.add_updater(aObj.physics_updater)

        var = Text("var").move_to([3,1,0])
        varImovel = Text("var").move_to([3,1,0])
        varObj = ObjetoFisico(var, np.array([-6.5,2,0]), xBounds=[exampleCode.get_right()[0], 20], damping=0.25)
        self.play(GrowFromPoint(varImovel, programmer.get_top()), run_time=2.5)
        
        self.remove(aObj)
        self.add(varObj)
        self.remove(varImovel)

        varObj.add_updater(varObj.physics_updater)

        variavel = Text("variavel").move_to([3,1,0]).scale(0.8)
        variavelImovel = Text("variavel").move_to([3,1,0]).scale(0.8)
        variavelObj = ObjetoFisico(variavel, np.array([-6.2, 1.5,0]), xBounds=[exampleCode.get_right()[0], 20], damping=0.25)
        self.play(GrowFromPoint(variavelImovel, programmer.get_top()), run_time=2.5)
        self.remove(varObj)
        self.add(variavelObj)
        self.remove(variavelImovel)

        variavelObj.add_updater(variavelObj.physics_updater)
        #Nome melhor animação
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade;
    int QuAntiDaDe;
    char comando_c;
    float localResultFromBaseFunction;
    int aula4;
    char ComandoC;
    int contador;
}
'''
        exampleCode5 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to(exampleCode.get_center())
        
        bestName = Code(code_string="localResultFromBaseFunction",
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to(programmer.get_top()+[0,1,0])
        self.play(GrowFromPoint(bestName, programmer.get_top()), run_time=2.5)
        self.remove(variavelObj)
        self.wait()
        self.play(bestName.animate.move_to(exampleCode.get_center()).scale(0), Transform(exampleCode, exampleCode5))
        self.wait()
        questionMark = Text("a7?").scale(1.5).move_to(programmer.get_top()+[0,1,0])
        self.play(GrowFromPoint(questionMark, programmer.get_top()+[0.2,0,0]), run_time=3)

        self.play(FadeOut(*self.mobjects))
        self.clear()

class CaseSensitive(Scene):
    def construct(self):
        nome = Text("nome", color=YELLOW_B, font="DejaVu Sans Mono")
        Nome = Text("Nome", color=YELLOW_B, font="DejaVu Sans Mono")
        noMe = Text("nOmE", color=YELLOW_B, font="DejaVu Sans Mono")
        diferente = MathTex(r"\neq")
        copyDiferente = diferente.copy()
        
        nomes = VGroup(nome, diferente, Nome, copyDiferente, noMe).arrange(buff=1.05).scale(0.75)

        self.play(Write(nomes))
        self.wait()
        titulo = Text("Atribuição de variável", weight=BOLD, t2c={"variável":"#AA77C7"}, font_size = 100).scale(0.6)
        descr = Text("Regras e propriedades", weight=BOLD, font_size = 100).scale(0.3)

        self.play(FadeOut(*self.mobjects))
        self.clear()
        criaCapitulo(self, titulo, descr, 2)

class Atribucao(MovingCameraScene):
    def construct(self):
        codigoString = '''#include <stdio.h>

int main() {
    int quantidade;
    quantidade = 3;

}
'''
        exampleCode = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        self.play(FadeIn(exampleCode))
        self.wait()
        self.play(Indicate(exampleCode.code_lines[4][4:14], color=WHITE))
        self.wait()
        self.play(Circumscribe(exampleCode.code_lines[4][15:17], color=WHITE))
        self.wait()
        self.play(Circumscribe(exampleCode.code_lines[2][11:12], color=WHITE),
                  Circumscribe(exampleCode.code_lines[6][0:1], color=WHITE), run_time=1.2)
        self.wait()
        exampleCode.save_state()
        self.play(exampleCode.code_lines[4][18:19].animate.scale(1.25).shift([0.5,0,0]))
        self.play(alyBemAly(exampleCode.code_lines[4][18:19].get_center(), 8, 0.1, 1, 1, run_time=1))
        self.wait()
        self.play(Restore(exampleCode))
        self.wait(2)
        recebe = Arrow(exampleCode.code_lines[4][17:18].get_left() + [1,0,0], exampleCode.code_lines[4][14:15].get_right())
        exampleCode.save_state()
        self.wait()
        self.play(Transform(exampleCode.code_lines[4][15:17], recebe), exampleCode.code_lines[4][17:19].animate.shift([1,0,0]))
        self.wait()
        self.play(Restore(exampleCode))

        self.play(Swap(exampleCode.code_lines[4][4:14], exampleCode.code_lines[4][17:18]),
                  exampleCode.code_lines[4][15:17].animate.shift([-1,0,0]), exampleCode.code_lines[4][18:19].animate.shift([1,0,0]))
        self.wait()
        self.play(Swap(exampleCode.code_lines[4][4:14], exampleCode.code_lines[4][17:18]),
                  exampleCode.code_lines[4][15:17].animate.shift([1,0,0]), exampleCode.code_lines[4][18:19].animate.shift([-1,0,0]))
        self.play(Swap(exampleCode.code_lines[3], exampleCode.code_lines[4]))
        self.wait()
        self.play(Swap(exampleCode.code_lines[4], exampleCode.code_lines[3]))
        self.wait()
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade = 3;

}
'''
        exampleCode2 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        self.play(Transform(exampleCode, exampleCode2))
        self.wait(2)
        codigoString = '''#include <stdio.h>

int main() {
    int quantidade, valor;
    quantidade = 3;
    valor = 10;

}
'''
        exampleCode3 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        self.play(Transform(exampleCode, exampleCode3))
        self.wait()
        self.play(Circumscribe(exampleCode.code_lines[3][19: 20], color=WHITE))
        self.wait()
        #Um monte de atribuição
        strAtribuicoes = '''
    valor = 15;
    quantidade = 4;
    valor = 1000;
    quantidade = 234;
    valor = 314;
    quantidade = 16;
    quantidade = 27;
    valor = 0;
    quantidade = 2;
    quantidade = 0;
    quantidade = 42;
    valor = 890;
    valor = 12;
    quantidade = 77;
    valor = 405;
    quantidade = 1;
    quantidade = 99;
    valor = 63;
    valor = 2048;
    quantidade = 8;
    valor = 7;
    quantidade = 150;
    valor = 91;
    quantidade = 3;
    quantidade = 10;
    valor = 500;
    quantidade = 128;
    valor = 33;
    valor = 1024;
    quantidade = 6;
    valor = 15;
    quantidade = 4;
    valor = 1000;
    quantidade = 234;
    valor = 314;
    quantidade = 16;
    quantidade = 27;
    valor = 0;
    quantidade = 2;
    quantidade = 0;
    quantidade = 42;
    valor = 890;
    valor = 12;
    quantidade = 77;
    valor = 405;
    quantidade = 1;
    quantidade = 99;
    valor = 63;
    valor = 2048;
    quantidade = 8;
    valor = 7;
    quantidade = 150;
    valor = 91;
    quantidade = 3;
    quantidade = 10;
    valor = 500;
    quantidade = 128;
    valor = 33;
    valor = 1024;
    quantidade = 3;

}
'''
        nAtribuicoes= Code(code_string=strAtribuicoes,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to([0,-20,0])


        self.play(exampleCode.code_lines[6:].animate.move_to([0,-15,0]))
        self.play(exampleCode.code_lines[6:].animate.scale(0), run_time=0.2)
        self.play(nAtribuicoes.animate.move_to(exampleCode.code_lines[6].get_bottom()+[-0.5,-0.5,0], aligned_edge=UP), rate_func=rate_functions.ease_in_out_back)
        self.wait()
        self.play(self.camera.frame.animate.move_to([0,-24,0]))
        self.wait(2)
        nAtribuicoes.save_state()

        ram = Text("RAM").move_to([3,-22,0]).scale(0.8)
        box = Rectangle(height=3.2, width=2.8).move_to([3,-24,0])
        question = Text("quantidade = ?").scale(0.5).move_to(box.get_center())
        linhas = VGroup(Line([box.get_right()[0],box.get_center()[1] + 0.45,0], [box.get_left()[0],box.get_center()[1] + 0.45,0]),
                        Line([box.get_right()[0],box.get_center()[1] - 0.45,0], [box.get_left()[0],box.get_center()[1] - 0.45,0]))
        memory = VGroup(ram, box, linhas)

        self.play(nAtribuicoes.animate.shift([-1,0,0]))
        self.play(GrowFromPoint(memory, nAtribuicoes.code_lines[-3][4:].get_right()))
        self.play(GrowFromCenter(question))
        self.wait()
        self.play(FadeOut(memory, question))
        self.wait()
        self.play(Restore(nAtribuicoes))
        self.wait()
        #Printf aparece novamente na aula 5!
        sPrint = '''
    printf("Quantidade: %d \\n");
}
'''
        nPrint = Code(code_string=sPrint,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to([0,-30,0])

        lastBottom = nAtribuicoes.code_lines[-3].get_bottom()
        self.play(nAtribuicoes.code_lines[-1].animate.shift([0,-10,0]))
        self.play(nPrint.animate.move_to(lastBottom + [0.9, 0,0], aligned_edge=UP), rate_func=rate_functions.ease_in_out_back)
        self.wait(2)

        self.play(nPrint.code_lines[-1].animate.shift([0,-14,0]), nAtribuicoes.code_lines[0:-2].animate.shift([0,9,0]),
                  nPrint.code_lines[-2].animate.move_to([0,-25,0]))
        
        self.wait()
        self.play(Indicate(nPrint.code_lines[-2][24:26]))
        self.wait()

        svirgula = '''
    printf("Quantidade: %d \\n",);

'''
        virgula = Code(code_string=svirgula,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to([0,-25,0])
        self.play(Transform(nPrint, virgula))
        self.wait()

        svirgulaQuantidade = '''
            printf("Quantidade: %d \\n", quantidade);
        
        '''
        virgulaQuantidade = Code(code_string=svirgulaQuantidade,
                    tab_width=4,
                    language="C",
                    formatter_style= "material", 
                    add_line_numbers=False,
                    background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to([0,-25,0])
        
        self.play(Transform(nPrint, virgulaQuantidade))
        #Animação com terminal novo
        self.wait()
        terminal = CustomTerminal(height=2.5).move_to([0,-22.8,0])
        self.play(FadeIn(terminal))
        self.play(terminal.animate_prompt_and_command(command="./a.out"))
        self.wait(0.1)
        terminal.add_line("Quantidade: 3")
        terminal.add_line("manim@manim:~$ ", color=GREEN)
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        self.clear()
        self.play(self.camera.frame.animate.move_to(ORIGIN))

class Formatacao(Scene):
    def construct(self):
        code = '''            printf("Quantidade: %d Preço unitário: %f ", 
            quantidade, precoUnitario);

            printf("Total a pagar: R$ %f", total);'''
        rendered_code = Code(
            code_string=code, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.7).move_to([0,1,0])
        code = '''            printf("Quantidade: %d\\n Preço unitário: %f\\n", 
            quantidade, precoUnitario);

            printf("Total a pagar: R$ %f", total);'''
        rendered_codeN = Code(
            code_string=code, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.7).move_to([0,1,0])
        code = '''            printf("Quantidade: %d\\n Preço unitário: %f\\n", 
            quantidade, precoUnitario);

            printf("Total a pagar: R$ %.2f", total);'''
        rendered_codeNF = Code(
            code_string=code, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.7).move_to([0,1,0])

        output1 = Text("Quantidade: 3")
        output2 = Text("Preço unitário: 10.5")
        output3 = Text("Total a pagar: R$ 31.5")
        
        outputs = VGroup(output1, output2, output3).arrange(buff=0.5).scale(0.5).shift([0,-2,0])

        self.play(FadeIn(rendered_code))
        self.wait(0.5)
        self.play(GrowFromCenter(outputs))
        newLine = Text("\\n").scale(0.5).move_to([-3,5,0])
        newLine2 = Text("\\n").scale(0.5).move_to([-2,5,0])

        self.play(newLine.animate.move_to(rendered_code.code_lines[0][35].get_center() + [0,1.5,0]),
                  newLine2.animate.move_to(rendered_code.code_lines[0][54].get_center() + [0,1.5,0]))
        self.wait()
        self.play(newLine.animate.move_to(rendered_code.code_lines[0][35].get_center()).scale(0),
                  newLine2.animate.move_to(rendered_code.code_lines[0][54].get_center()).scale(0),
                  Transform(rendered_code, rendered_codeN),
                  outputs.animate.arrange(DOWN, aligned_edge=LEFT,center=False).move_to([0,-2,0]))
        self.wait()
        self.remove(newLine, newLine2)

        output4 = Text("Total a pagar: R$ 31.50").move_to(output3.get_center()).scale(0.5)
        self.play(Transform(rendered_code, rendered_codeNF), Transform(output3, output4))
        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.clear()

class Fim(Scene):

    def construct(self):
        printf = Text("printf()").move_to([8,0,0])
        variavel = Text("variavel").move_to([-8,0,0])
        handshake = SVGMobject("svgs\\handshake").scale(0.6)

        self.play(variavel.animate.move_to([-3,0,0]))
        self.play(printf.animate.move_to([3,0,0]))
        self.wait(0.5)
        self.play(FadeIn(handshake))
        self.play(printf.animate.move_to(ORIGIN).scale(0), variavel.animate.move_to(ORIGIN).scale(0),
                  handshake.animate.move_to(ORIGIN).scale(0))
        self.wait(0.25)
        self.play(GrowFromCenter(SVGMobject("svgs\\pdf")))
        self.wait()
        self.play(FadeOut(*self.mobjects))
        text = Text("Para a próxima aula:", font_size = 45)
        text2 = Text("Variáveis e mais variantes", color = PURPLE, font_size=50)
        rawTitle = VGroup(text, text2).arrange(DOWN, aligned_edge = LEFT, buff = 0.2)
        
        self.play(Write(rawTitle))
        self.wait()
        logo = ImageMobject("images/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        # O cursor
        cursorVinheta=ImageMobject("images/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)

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
            buff=0,
            tip_length=0.2,
            stroke_width=4, 
            color = YELLOW
        )

        marcaCentro = Line(
            UP * 0.15,
            DOWN * 0.15,
            stroke_width=3,
            color = YELLOW
        )

        marcaCentro.move_to(retaNumerica.get_center())

        zero = MathTex(
            "0",
            font_size=24
        )

        zero.next_to(
            marcaCentro,
            DOWN,
            buff=0.15
        )

        grupoReta = Group(
            retaNumerica,
            marcaCentro
        )

        # controla a posição e o valor do float
        tracker = ValueTracker(-3.4)

        menorFloat = MathTex(
            r"-3,4\times10^{38}",
            font_size=40,
            color=BLUE
        )

        menorFloat.next_to(
            retaNumerica.get_left(),
            DOWN,
            buff=0.2
        )

        maiorFloat = MathTex(
            r"3,4\times10^{38}",
            font_size=40,
            color=BLUE
        )

        maiorFloat.next_to(
            retaNumerica.get_right(),
            DOWN,
            buff=0.2
        )

        # seta na reta
        def posicaoNaReta():
            valor = tracker.get_value()

            # Converte [-3.4, 3.4] para [0, 1]
            proporcao = (valor + 3.4) / 6.8

            # tira erros de ponto flutuante
            proporcao = np.clip(proporcao, 0, 1)

            return retaNumerica.point_from_proportion(proporcao)

        # Seta que aponta para a reta
        setaFloat = always_redraw(
            lambda: Arrow(
                start=posicaoNaReta() + UP * 0.75,
                end=posicaoNaReta() + UP * 0.08,
                buff=0,
                stroke_width=4,
                tip_length=0.15,
                color="#AA77C7"
            )
        )

        # valor que acompanha a seta
        valorFloat = always_redraw(
            lambda: MathTex(
                rf"{tracker.get_value():.1f}".replace(".", ",")
                + r"\times10^{38}",
                font_size=40,
                color="#AA77C7"
            ).next_to(
                setaFloat,
                UP,
                buff=0.08
            )
        )

        posicaoFinalTexto = (
            retaNumerica.get_center() + UP * 0.8
        )

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

        sublinhadoFloat = Underline(
            VGroup(
                *rendered_codigoSoma.code_lines[4][0:11]
            ),
            stroke_width=1.6
        )

        sublinhadoFloat.shift(UP * 0.05)

        destacarPreco = VGroup(
            *rendered_codigoSoma.code_lines[7]
        )

        self.play(Write(tituloFloat))

        self.play(tituloFloat.animate.move_to([0, 2.5, 0]))

        self.wait()

        self.play(
            GrowFromCenter(grupoReta),
            run_time=1.2,
            rate_func=smooth
        )

        # os extremos, o zero, a seta e o valor
        self.play(
            FadeIn(menorFloat),
            FadeIn(zero),
            FadeIn(maiorFloat)
        )

        self.play( FadeIn(setaFloat), FadeIn(valorFloat))

        # A seta percorre toda a reta
        # e o número muda simultaneamente

        self.play(
            tracker.animate.set_value(3.4),
            run_time=5,
            rate_func=linear
        )

        self.play(FadeOut(setaFloat), FadeOut(valorFloat))

        self.play(
            tituloFloat.animate.move_to(posicaoFinalTexto),
            run_time=1.8,
            rate_func=rate_functions.ease_out_bounce
        )

        self.play(
            *[
                FadeOut(mob)
                for mob in self.mobjects
            ]
        )

        self.play(FadeIn(rendered_codigoSoma))

        self.play(Create(sublinhadoFloat))

        self.wait(2)

        self.play(Indicate(destacarPreco))

        self.wait()

        self.play(
            *[
                FadeOut(mob)
                for mob in self.mobjects
            ]
        )



class contaCaractereValor2(Scene):
    def construct(self):
        codigoSoma = '''#include <stdio.h>

int main(){
    int valor1, soma;
    float valor2;

    valor1 = 6;
    valor2 = 4.5;
    soma = valor1 + valor2;
    printf("A soma do valor 1 e 2 é igual a %f", soma);
    return 0;
}'''
        codigoSoma2 = '''#include <stdio.h>
        
int main(){
  int valor1, soma;
  float valor2;

  valor1 = 1;
  valor2 = 4.5;
  soma = valor1 + valor2;
  printf("A soma do valor 1 e 2 é igual a %d", soma); 
  return 0;
}'''
        codigoSoma3 = '''#include <stdio.h>

int main(){
  int valor1, soma;
  char valor2;
  
  valor1 = 1;
  valor2 = '1';
  soma = valor1 + valor2;
  printf("A soma do valor 1 e 2 é igual a %d", soma); 
  return 0;
}'''
        #Novo segmento para explicar "comunicar bem com o int"
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
        rendered_codigoSoma2 = Code(
            code_string=codigoSoma2, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)
        rendered_codigoSoma3 = Code(
            code_string=codigoSoma3, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)
        self.play(FadeIn(rendered_codigoSoma))
        self.wait()
        self.play(Transform(rendered_codigoSoma, rendered_codigoSoma2))
        self.wait()
        self.play(Transform(rendered_codigoSoma, rendered_codigoSoma3))
        self.wait()

        # expressão
        num1 = Text("1", font_size=60)
        mais = Text("+", font_size=60)
        char1 = Text("'1'", font_size=60)
        igual = Text("=", font_size=60)
        inter = Text("?", font_size=60)

        soma = VGroup(num1, mais, char1, igual, inter).arrange(RIGHT, buff=0.25)

        um = char1[1]

        num49 = Text("49", font_size=40, color=YELLOW)

        soma.move_to(ORIGIN)
        num49.next_to(um, DOWN, buff=1.3)
        num49.shift(RIGHT * 0.06)

        seta = Arrow(
            start=um.get_bottom() + RIGHT * 0.06,
            end=num49.get_top(),
            buff=0.1,
            color=YELLOW
        )
        

        self.play(Transform(rendered_codigoSoma.code_lines[8:9], soma), FadeOut(rendered_codigoSoma.code_lines[0:8]), FadeOut(rendered_codigoSoma.code_lines[9:]))
        self.add(soma)
        self.remove(*[obj for obj in self.mobjects if obj is not soma])

        self.wait()

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
        conteudoNum = Text("49", font_size=120, color=YELLOW).scale(0.4).move_to(caixa)

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
        self.play(cinq.animate.scale(1.5).set_color(YELLOW))

        exclamacao = Text("!", font_size=60, color=YELLOW).scale(1.5)
        exclamacao.match_height(cinq)
        exclamacao.next_to(cinq, RIGHT, buff=0.2)

        self.play(FadeIn(exclamacao))
        self.wait()

 
        self.play(FadeOut(exclamacao))
        self.play(cinq.animate.scale(1 / 1.5).set_color(WHITE))
        self.wait(2)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
class novoTipoChar(MovingCameraScene):
    def construct(self):
        tituloChar = Text(
            "char",
            font_size=160,
            disable_ligatures=True
        ).scale(0.5)    
        self.play(Write(tituloChar))
        self.wait()
        self.play(tituloChar.animate.shift(UP*2))
        letterC = Text("C", weight=BOLD, color=PURPLE).scale(1.5)
        self.play(DrawBorderThenFill(letterC, lag_ratio=0.1), run_time=0.5)
        self.wait()

        scanAnimation(self, letterC, 0.15, 0.05)

        sixSeven = Text("67").scale(1.5)
        q = Text("?").scale(3)
        self.play(Write(q), run_time=0.8)
        self.play(FadeOut(q))
        self.wait()

        self.play(Transform(letterC, sixSeven))
        self.wait()
        tabela = Text("Código ASCII", t2c={"ASCII":"#AA77C7"}, font_size = 100).scale(0.6).move_to([0,-8,0])
        self.play(tabela.animate.move_to([0,-2,0]))
        self.wait()

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
                color=YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            ),
            Flash(
                trechoAspasSimples2,
                color=YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            )
        )
        self.wait()

        self.play(
            Flash(
                trechoAspasDuplas1,
                color=YELLOW,
                line_length=0.1,
                flash_radius=0.06,
                num_lines=8
            ),
            Flash(
                trechoAspasDuplas2,
                color=YELLOW,
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
class tabelaASCII(MovingCameraScene):
    def construct(self):
        humano = SVGMobject("svgs\\person").move_to([-10,0,0]).scale(0.8).set_z_index(1)
        computer = SVGMobject("svgs\\monitor").move_to([10,0,0]).scale(0.8).set_z_index(1)

        self.play(humano.animate.move_to([-5,0,0]), computer.animate.move_to([5,0,0]))
        caixa = criar_card("ASCII", PURPLE_A, "").set_z_index(1)

        self.play(GrowFromCenter(caixa))
        self.wait(0.5)

        valores = [("A", "65"), ("B", "66"), ("C", "67")]

        for letra, numero in valores:
            obj_letra = Text(letra, font_size=48).set_z_index(-1).move_to(humano.get_right())
            
            self.play(FadeIn(obj_letra, run_time=0.2))
            self.play(obj_letra.animate.move_to(caixa.get_left()), run_time=0.8)
            self.play(FadeOut(obj_letra, scale=0.5, run_time=0.2))

            obj_numero = Text(numero, font_size=48, color=YELLOW).set_z_index(-1).move_to(caixa.get_right())
            
            self.play(FadeIn(obj_numero, scale=0.5, run_time=0.2))
            self.play(obj_numero.animate.move_to(computer.get_center()), run_time=0.8)

            self.play(
                FadeOut(obj_numero, run_time=0.2),
                computer.animate.scale(1.3), 
                rate_func=rate_functions.there_and_back,
                run_time=0.4
            )
            
            self.wait(0.2)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class Aula5(MovingCameraScene):
    config.background_color = "#1E1E1E"
    Text.set_default(font = "Manrope")
    def construct(self):
        Intro.construct(self)
        CriandoAVariavel.construct(self)
        RegrasNome.construct(self)
        CaseSensitive.construct(self)
        Atribucao.construct(self)
        segundoConjuntoRegras.construct(self)
        soma.construct(self)
        tiposPrimitivos.construct(self)
        tipoInt.construct(self)
        tipoFloat.construct(self)
        novoTipoChar.construct(self)
        tabelaASCII.construct(self)
        contaCaractereValor2.construct(self)
        intChar.construct(self)
        tipoChar.construct(self)
        tipoString.construct(self)
        Fim.construct(self)