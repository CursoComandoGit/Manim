from manim import *
import random
from objetoFisico import ObjetoFisico
import numpy as np
from customTerminal import CustomTerminal

def criaCapitulo(cena : Scene, titulo : Text, descricao = Text(""), numero = 1, comFade = False):
        
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
        cena.wait(0.75)
        cena.add(titulo)
        cena.wait(0.1)
    cena.play(anim, rate_func=rate_functions.ease_in_out_back, run_time=2.5)
    cena.wait(0.75)
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
        print = Text("printf(\"blablabla\")").move_to([3,0,0]).scale(0.8)
        string = Text("\"blablabla\"").move_to([3,0,0]).scale(0.8)
        char = Text("'C'").move_to([3,-2,0]).scale(0.8)
        numero = Text("27").scale(0.8).move_to([3,2,0])

        #Novas animações do roteiro
        bitSegment = VGroup(block2[-i] for i in range(5, 35))
        bitSegment2 = VGroup(block2[-i] for i in range(40, 48))
        bitSegment3 = VGroup(block2[-i] for i in range(60, 124))

        self.play(Transform(bitSegment, print))
        self.wait(0.5)
        self.play(Transform(bitSegment, string))
        self.wait(0.5)
        self.play(Transform(bitSegment2, char))
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
                  bitSegment3.animate.set_opacity(0.5), Succession(*[Transform(correspondingBits[i], things[i]) for i in range(0,int(len(textoCoisas)/2))]))
        self.play(Succession(*[Transform(correspondingBits[i], things[i]) for i in range(int(len(textoCoisas)/2), len(textoCoisas))]), run_time=0.5)
        self.wait(0.2)
        self.play(bitSegment.animate.scale(0).move_to([3,0,0]),
                  bitSegment2.animate.scale(0).move_to([3,0,0]),
                  bitSegment3.animate.scale(0).move_to([3,0,0]),
                  correspondingBits.animate.scale(0).move_to([3,0,0]))
        self.remove(bitSegment, bitSegment2, bitSegment3, correspondingBits, things)

        variavel = Text("variavel", color=PURPLE).move_to([3,0,0])
        ram = Text("RAM").move_to([-3,2,0]).scale(0.8)
        box = Rectangle(height=4, width=2.5).move_to([-3,-1,0])

        self.play(GrowFromCenter(variavel))
        self.wait()
        self.play(scrolling_group.animate.scale(0).move_to([-3,0,0]), GrowFromCenter(ram), GrowFromCenter(box))
        self.remove(scrolling_group)
        arrow = CurvedArrow(variavel.get_left(), box.get_right()+[0,0.25,0], color=YELLOW)
        valor = Text("3").scale(0.8).move_to(arrow.get_end()+[-1,0,0])
        novoValor = Text("6").scale(0.8).move_to(arrow.get_end()+[-1,0,0])
        novoValor2 = Text("12").scale(0.8).move_to(arrow.get_end()+[-1,0,0])
        self.wait()
        self.play(Create(arrow))
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
        self.play(box.animate.shift([-9,0,0]), ram.animate.shift([-9,0,0]), valor.animate.shift([-9,0,0]),
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
        self.wait(0.5)

        titulo = Text("Declaração de variável", weight=BOLD, t2c={"variável":"#AA77C7"}, font_size = 100).scale(0.6)
        descr = Text("Sintaxe básica", weight=BOLD, font_size = 100).scale(0.3)
        criaCapitulo(self, titulo, descr, 1, True)

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
    int void;
    char %Comando*CÊ-;
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
    int void;
    char %Comando*CÊ-;
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
        self.play(FadeIn(incorrect3))
        self.wait()
        #Mostrando último incorreto sintaxe
        codigoString = '''#include <stdio.h>

int main(){
    int quantidade;
    int QuAntiDaDe;
    char comando_c;

    int aula4;
    int contador;
    char ComandoC;
}
'''
        exampleCode3 = Code(code_string=codigoString,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0})
        
        self.play(incorrect2.animate.scale_to_fit_width(0),
                  incorrect3.animate.scale_to_fit_width(0),
                  Transform(exampleCode, exampleCode3))
        self.remove(incorrect2, incorrect3)
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
    int contador;
    char ComandoC;
}
'''
        exampleCode4 = Code(code_string=codigoString,
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
        self.play(bestName.animate.move_to(exampleCode.get_center()).scale(0), Transform(exampleCode, exampleCode4))
        self.wait()
        questionMark = Text("?").scale(1.5).move_to(programmer.get_top()+[0,1,0])
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

        self.play(FadeOut(*self.mobjects))
        self.clear()

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
        self.play(exampleCode.code_lines[3][18:19].animate.scale(1.25).shift([0.5,0,0]))
        self.play(alyBemAly(exampleCode.code_lines[3][18:19].get_center(), 8, 0.1, 1, 1, run_time=1))
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
        memory = VGroup(ram, box)
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
    printf("Quantidade: %d \\n", quantidade);
}
'''
        nPrint = Code(code_string=sPrint,
            tab_width=4,
            language="C",
            formatter_style= "material", 
            add_line_numbers=False,
            background_config = {"stroke_opacity" : 0,  "fill_opacity":0}).move_to([2.125,-30,0])

        lastBottom = nAtribuicoes.code_lines[-3].get_bottom()
        self.play(nAtribuicoes.code_lines[-1].animate.shift([0,-10,0]))
        self.play(nPrint.animate.move_to(lastBottom + [2.125, 0,0], aligned_edge=UP), rate_func=rate_functions.ease_in_out_back)
        self.wait(2)

        self.play(nPrint.code_lines[-1].animate.shift([0,-14,0]), nAtribuicoes.code_lines[0:-2].animate.shift([0,9,0]),
                  nPrint.code_lines[-2].animate.move_to([0,-25,0]))
        
        self.wait()
        self.play(Indicate(nPrint.code_lines[-2][24:26]))
        self.wait()
        self.play(Circumscribe(nPrint.code_lines[-2][30:31], color=WHITE))
        self.wait()
        self.play(Indicate(nPrint.code_lines[-2][32:42]))
        output = Text("Quantidade: 3").move_to([0,-22,0])
        self.play(AddTextLetterByLetter(output))

        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        self.clear()
        self.play(self.camera.frame.animate.move_to(ORIGIN))

#Ponderando em remover completamente
class calculandoCorretamente(Scene):
    def construct(self):
        # codeCompras = '''   #include <stdio.h>

        # float calcularTotal(int qtd, float uni)
        # {
        #     float t = qtd * uni;
        #     return t;
        # }

        # int main() {
        #     int quantidade;
        #     float precoUnitario, total; 
            
        #     quantidade = 3;
        #     //char quantidade = '3'
        #     precoUnitario = 10.50;

        #     total = calcularTotal(quantidade, precoUnitario);

        #     printf("Quantidade: %d \\n Preço unitário: %f\\n", 
        #     quantidade, precoUnitario);

        #     printf("Total a pagar: R$ %.2f\\n", total);
            
        #     return 0;
        # }'''
        # rendered_codeCompras = Code(
        #     code_string=codeCompras, 
        #     language="c",
        #     formatter_style="material",
        #     add_line_numbers=False,
        #     background="rectangle", 
        #     background_config={
        #         "fill_opacity": 0,
        #         "stroke_width": 0
        #         }
        # ).scale(0.6).move_to(ORIGIN)

        # LinhaTotal = [
        #     linha.animate.set_opacity(0.2)
        #     for linha in rendered_codeCompras.code_lines
        # ]

        # LinhaTotal.append(
        #     rendered_codeCompras.code_lines[16].animate.set_opacity(1)
        # )

        # interrogacao = Text("?", font_size = 130, color = BLUE)

        # destacarPrintf = rendered_codeCompras.code_lines[21]


        # self.play(FadeIn(rendered_codeCompras))
        # rendered_codeCompras.save_state()

        # self.play(*LinhaTotal)
        # self.play(rendered_codeCompras.code_lines[16].animate.scale(1.6))
        # interrogacao.next_to(rendered_codeCompras.code_lines[16], UP * 4)
        # self.play(FadeIn(interrogacao))
        # self.play(ShrinkToCenter(interrogacao))
        # self.play(Restore(rendered_codeCompras))
        # self.play(Circumscribe(destacarPrintf, buff=0.05, fade_out=True, color=WHITE, stroke_width = 1.4), run_time=2)
        # self.wait()
        # rendered_codeCompras.save_state()
        # printfFormatacao = rendered_codeCompras.code_lines[18]
        # printfFormatacao2 = rendered_codeCompras.code_lines[19]
        # LinhaPrintf = [
        #     linha.animate.set_opacity(0)
        #     for linha in rendered_codeCompras.code_lines
        # ]

        # LinhaPrintf.extend([
        #     rendered_codeCompras.code_lines[18].animate.set_opacity(1),
        #     rendered_codeCompras.code_lines[19].animate.set_opacity(1)
        # ])
        # grupoPrintf = VGroup(printfFormatacao, printfFormatacao2)

        # self.play(*LinhaPrintf)

        # self.play(grupoPrintf.animate.scale(1.2).move_to([0, 2.5, 0]))
        # sublinhadoPrintf = Underline(VGroup(*rendered_codeCompras.code_lines[18][8:41]), stroke_width = 1.6)
        # sublinhadoPrintf.shift(UP * 0.05)

        linhaPrinf = Code(
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
        porcentagem = Text("%", font_size = 80, color = BLUE)
        tipo = Text("tipo", font_size = 80, color = PURPLE)
        porcTipo = VGroup(porcentagem, tipo).arrange(RIGHT, buff = 0.15).move_to(ORIGIN)

        self.play(Create(linhaPrinf))
        self.play(GrowFromCenter(porcentagem))
        self.play(Write(tipo))
        self.wait()

        #Parte nova
        # self.play(porcTipo.animate.move_to([-4,0,0]).scale(0.75), FadeOut(linhaPrintf))
        # self.wait()

        # parametro = Text("valor", font_size = 80, color = PURPLE)
        # self.play(Write(parametro))
        # self.play(parametro.animate.move_to([4,0,0]).scale(0.75))
        # self.wait()
        # intExemplo = Text("51", font_size = 80, color = PURPLE).move_to(parametro.get_center())
        # self.play(Transform(parametro, intExemplo))
        # linha = DashedLine(start=parametro.get_left()+[-0.5,0,0], end=tipo.get_right()+[0.5,0,0])
        # self.play(Create(linha), run_time=0.6)
        # porcentoI = Text("i", font_size = 80, color = PURPLE).move_to(tipo.get_center(), aligned_edge=LEFT)
        # self.play(Transform(tipo, porcentoI))
        # self.wait()

        # self.play(Circumscribe(rendered_codeCompras.code_lines[18][21:32]), Circumscribe(rendered_codeCompras.code_lines[18][38:54]))
        # self.play(Circumscribe(rendered_codeCompras.code_lines[18][32:34]), Circumscribe(rendered_codeCompras.code_lines[18][54:56]))
        # self.wait()

        # self.play(FadeOut(tipo, porcentagem, parametro, linha), Restore(rendered_codeCompras))
        # self.wait(2)
        # LinhaTotal = [
        #     linha.animate.set_opacity(0.2)
        #     for linha in rendered_codeCompras.code_lines
        # ]

        # LinhaTotal.append(
        #     rendered_codeCompras.code_lines[21].animate.set_opacity(1)
        # )

        # rendered_codeCompras.save_state()

        # self.play(*LinhaTotal)
        # self.play(rendered_codeCompras.code_lines[21].animate.scale(1.6))
        # self.play(Restore(rendered_codeCompras))

        self.wait()
        self.play(FadeOut(*self.mobjects))
        self.clear()

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
        setaCalcular.set_color(YELLOW)

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
            color = YELLOW
        )

        marcaCentro = Line(
            UP * 0.15,
            DOWN * 0.15,
            stroke_width=3,
            color = YELLOW
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
            color=YELLOW,
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

class Main(MovingCameraScene):
    config.background_color = "#1E1E1E"
    Text.set_default(font = "Manrope")
    
    def construct(self):
        Intro.construct(self)
        CriandoAVariavel.construct(self)
        #RegrasNome.construct(self)
        #CaseSensitive.construct(self)
        #Atribucao.construct(self)
        #segundoConjuntoRegras.construct(self)
        #tipoInt.construct(self)
        #tipoFloat.construct(self)
        #tipoChar.construct(self)
        #tipoString.construct(self)
        #globalLocal.construct(self)
        #porExemplo.construct(self)
        #cuidado.construct(self)
        #calculandoCorretamente.construct(self)
        #Formatacao.construct(self)
        #Fim.construct(self)