from manim import *
import numpy as np
import random
config.background_color = "#1E1E1E"
Text.set_default(font = "Segoe UI")

def codigoComando(code_string: str):
    if not isinstance(code_string, str):
        raise TypeError("Passe uma string (o código ) como parâmetro")

    code = Code(
        code_string=code_string,
        language="c",
        formatter_style="monokai",
        background="rectangle",
        background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}
    )
    code.scale(0.7)
    return code

class Aula(MovingCameraScene):
    def physics_updater(self, obj, dt):
        #Vou criar um objeto que tenhas as propriedades generalizadas depois
        if not 0 < dt < 0.1: #Check para ver se deltaTime foi interrompido
            return
        if obj.active == False: #Matar animação
            return
        
        obj.velocity= obj.velocity + obj.gravity * dt 
    
        obj.shift(obj.velocity * dt) #aplicando transformacao com deltaTime
        box_half_width= obj.width / 2
        box_half_height= obj.height / 2
        #Começo de verificação de colisão e aplicando bounce
        if obj.get_right()[0] >= 2:
            obj.set_x(2 - box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_left()[0] <= -2:
            obj.set_x(-2 + box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_top()[1] >= 2:
            obj.set_y(2 - box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping
        if obj.get_bottom()[1] <= -2:
            obj.set_y(-2 + box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping

    def construct(self):
        Introducao.construct(self)
        Binarios.construct(self)
        LinguagemDeProgramacao.construct(self)
        Final.construct(self)

class Introducao(Scene):
    def construct(self):
        title_text1 = Text("O que é", font_size=60)
        title_text2 = Text("programação?", color="#AA77C7", font_size=75)
        title_text2[-1].color = WHITE
        title = VGroup(title_text1, title_text2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.play(Write(title), run_time=1.5)
        self.wait()
        self.play(FadeOut(title))

        svg_cellphone = SVGMobject("assets/cellphone.svg")
        svg_card_machine = SVGMobject("assets/card-machine-atm")
        svg_laptop = SVGMobject("assets/laptop")
        svg_elevator = SVGMobject("assets/elevator")
        svg_car_key = SVGMobject("assets/car-key")
        svg_computer = SVGMobject("assets/computer")
        svg_motherboard = SVGMobject("assets/motherboard").scale(1.5)
        svg_hardware = SVGMobject("assets/hardware").scale(0.8)

        #sistemas embarcados ou computadores de proposito especifico
        svg_group1 = VGroup(svg_computer,svg_cellphone, svg_laptop).arrange(RIGHT, buff=2)
        svg_group2 = VGroup(svg_car_key, svg_elevator, svg_card_machine).arrange(RIGHT, buff=2)
        svg_group_hardware = VGroup(svg_motherboard, svg_hardware).arrange(RIGHT, buff=2)

        self.play(Write(svg_group1))
        self.wait()
        self.play(FadeOut(svg_group1))

        self.play(Write(svg_group2))
        self.wait()
        self.play(FadeOut(svg_group2))

        self.play(Write(svg_group_hardware))
        self.wait()
        question_mark = Text("?", font_size=200)
        self.play(svg_group_hardware.animate.scale(0.6), Write(question_mark), linear=True)
        self.wait()

        self.play(FadeOut(svg_group_hardware), FadeOut(question_mark))
        self.clear()
        code_string = '''#include <stdio.h>

int fatorial(int n) {
    int resultado = 1;
    for(int i = 1; i <= n; i++) {
        resultado = resultado * i;
    }
    return resultado;
}

int main() {
    int numero = 5;
    int resultado = fatorial(numero);
    printf("Fatorial de %d é %d",numero, resultado);
    return 0;
}'''
        code_example = codigoComando(code_string)
        self.play(Create(code_example), run_time=1.5)
        self.wait()

        self.play(Uncreate(code_example))
        MaquinaTuring.construct(self)
        self.wait()
        logo_svg = SVGMobject("assets/arvore.svg").scale(2)
        comando = Text("comando.c", font="Major Mono Display").shift(2*DOWN).scale(.8)
        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 1.1,
            width = 0.5,
        ).scale(.5).move_to(comando[0])
        self.play(Write(logo_svg), run_time=2)
        self.play(logo_svg.animate.shift(.5*UP))
        self.play(TypeWithCursor(comando, cursor), run_time=1.5)
        self.play(Blink(cursor, blinks=2))
        self.wait()
        self.clear()
        instrucoes = ["add", "save", "compare"]
        cards = VGroup()
        for i in instrucoes:
            rectangle = RoundedRectangle(
                corner_radius=0.1,
                height=1.0,
                width=3.0,
                color=BLUE,
                fill_opacity=0.1,
                stroke_width=2
            )

            text = Text(i, font_size=60).scale(1/2)
            text.move_to(rectangle.get_center())
            card = VGroup(rectangle, text)
            cards.add(card)

        cards.arrange(DOWN, buff=0.3)
        cards.scale(0.7).shift(DOWN)
        cards[2][1].shift(0.05*DOWN) # a palavra "compare" n está exatamente no centro, talvez pelo 'p' o centro do Text fica mais baixo
        
        svg_computer.move_to(ORIGIN)
        svg_computer.shift(2*UP)
        comando = Text("comando.c", font_size=60).scale(1/4).move_to(svg_computer.get_center()+0.5*UP)
        self.play(Write(svg_computer))
        self.play(Write(comando))

        self.play(FadeIn(cards[0]), run_time=0.5)
        self.play(FadeIn(cards[1]), run_time=0.5)
        self.play(FadeIn(cards[2]), run_time=0.5)
        for i in cards:
            InstructionPointer = Arrow(i.get_left()+LEFT, i.get_left())
            self.play(Write(InstructionPointer), run_time=0.5)
            self.play(Circumscribe(i), run_time=1)
            self.play(Unwrite(InstructionPointer), run_time=0.5)

        todos_objetos = VGroup(svg_computer, cards, comando)
        self.wait()
        self.play(
            FadeOut(todos_objetos),
            run_time=0.8
        )

        textos = ["add", "compare", "save", "jump", "sub", "save", "add", "jump", "exit"]
        
        # Posições iniciais dos cards
        instruction_positions = [
            UP * 2 + LEFT * 3,
            UP * 2,
            UP * 2 + RIGHT * 3,
            RIGHT * 3,
            ORIGIN,
            LEFT * 3,
            DOWN * 2 + LEFT * 3,
            DOWN * 2,
            DOWN * 2 + RIGHT * 3
        ]
        
        cards = VGroup()
        #ligar os cards
        for text, pos in zip(textos, instruction_positions):
            rect = RoundedRectangle(
                corner_radius=0.1,
                height=1.0,
                width=2.5,
                color=BLUE,
                fill_opacity=0.1,
                stroke_width=2
            )
            text_obj = Text(text, font_size=72).scale(1/3)
            text_obj.move_to(rect.get_center())
            
            card = VGroup(rect, text_obj)
            card.move_to(pos)
            cards.add(card)
        
        self.play(FadeIn(cards))
        self.wait(1)
        
        cards_list = list(cards)
        conection_list= VGroup()
        for i in range(len(cards_list) - 1):
            if i == 2 or i==5:
                conection = Line(
                    cards_list[i].get_bottom(),
                    cards_list[i+1].get_top(),
                    stroke_width=4,
                    color=YELLOW_B
                )

            elif i>=3 and i<=5:
                conection = Line(
                    cards_list[i].get_left(),
                    cards_list[i+1].get_right(),
                    stroke_width=4,
                    color=YELLOW_B
                )
            else:
                conection = Line(
                    cards_list[i].get_right(),
                    cards_list[i+1].get_left(),
                    stroke_width=4,
                    color=YELLOW_B
                )
            conection_list.add(conection)
            self.play(Create(conection), run_time=0.2)
        
        program = VGroup(conection_list, cards_list)
        self.play(program.animate.scale(0.7))
        self.play(Create(RoundedRectangle(corner_radius=0.5,
                                          color = "#8728BE",
                                          stroke_color= "#AA77C7",
                                          fill_opacity=0.1,
                                          height=5.0,
                                          width=8.0)))
        self.wait()
        program_text = MarkupText("Programa = <b>conjunto de instruções</b>", font_size=60).shift(3*UP).scale(0.5)
        program_text[:8].color = "#AA77C7"
        self.play(Write(program_text))
        self.wait()
        self.clear()

class MaquinaTuring(Scene):
    def construct(self):
        texto_cor = WHITE
        
        fita = VGroup()
        celulas = []
        valores = ["1", "0", "1", "1", "0"]
        
        for i, valor in enumerate(valores):
            celula = Rectangle(
                height=1, width=1,
                fill_color=BLUE_E,
                fill_opacity=0.4,
                stroke_color=WHITE,
                stroke_width=2
            )
            texto = Text(valor, color=texto_cor, font_size=36)
            
            grupo_celula = VGroup(celula, texto)
            grupo_celula.move_to(np.array([i - len(valores)/2 + 0.5, 0, 0]))
            celulas.append(grupo_celula)
            fita.add(grupo_celula)
        
        cabecote = Triangle(
            fill_color="#AA77C7",
            fill_opacity=0.6,
            stroke_color="#8728BE",
            stroke_width=4
        )
        cabecote.scale(0.4)
        cabecote.move_to(celulas[2][0].get_center() + DOWN * 0.8)
        
        self.play(LaggedStartMap(Create, fita, lag_ratio=0.2))
        self.play(Create(cabecote), run_time=0.5)
        
        posicao_atual = 2
        
        for i in range(posicao_atual + 1, len(celulas)):
            self.play(
                cabecote.animate.move_to(celulas[i][0].get_center() + DOWN * 0.8),
                run_time=0.3,
                rate_func=smooth
            )
            #destaque na célula
            self.play(
                celulas[i][0].animate.set_fill(BLUE_C, opacity=0.9),
                celulas[i][1].animate.set_color("#CAD800DD"),
                run_time=0.2
            )
            self.play(
                celulas[i][0].animate.set_fill(BLUE_E, opacity=0.4),
                celulas[i][1].animate.set_color(texto_cor),
                run_time=0.2
            )
        
        for i in range(len(celulas) - 2, -1, -1):
            self.play(
                cabecote.animate.move_to(celulas[i][0].get_center() + DOWN * 0.8),
                run_time=0.3,
                rate_func=smooth
            )

            self.play(
                celulas[i][0].animate.set_fill(BLUE_C, opacity=0.9),
                celulas[i][1].animate.set_color(YELLOW),
                run_time=0.2
            )
            
            if i == 1:
                novo_valor = "1" if valores[i] == "0" else "0"
                novo_texto = Text(novo_valor, color=YELLOW, font_size=36)
                novo_texto.move_to(celulas[i][1].get_center())
                self.play(
                    Transform(celulas[i][1], novo_texto),
                    run_time=0.2
                )
                valores[i] = novo_valor
                
            self.play(
                celulas[i][0].animate.set_fill(BLUE_E, opacity=0.4),
                celulas[i][1].animate.set_color(texto_cor),
                run_time=0.2
            )
        
        self.play(
            cabecote.animate.move_to(celulas[2][0].get_center() + DOWN * 0.8),
            run_time=0.3
        )
        
        self.play(
            FadeOut(fita),
            FadeOut(cabecote),
        )

class Binarios(Scene):
    def construct(self):
        binary_block = VGroup(Text("11000111010001011111010000000101", font="DejaVu Sans Mono"),
                              Text("00000000000000000000000011000111", font="DejaVu Sans Mono"),
                              Text("01000101111110000000011100000000", font="DejaVu Sans Mono"),
                              Text("00000000000000001000101101010101", font="DejaVu Sans Mono"),
                              Text("11110100100010110100010111111000", font="DejaVu Sans Mono"),
                              Text("00000001110100001000100101000101", font="DejaVu Sans Mono"),
                              Text("11111110", font="DejaVu Sans Mono")).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        self.add(binary_block)
        self.wait()
        self.play(binary_block.animate.set_opacity(0.3))

        all_chars = []
        for linha in binary_block:
            all_chars.extend(linha.submobjects)
        
        
        total_chars = len(all_chars)
        byte_size = 8
        
        num_bytes = total_chars // byte_size
        #lendo bytes
        for byte_index in range(num_bytes):
            start_idx = byte_index * byte_size
            end_idx = start_idx + byte_size
            
            for char in all_chars:
                char.set_opacity(0.3)
            
            for i in range(start_idx, end_idx):
                all_chars[i].set_opacity(0.9)
            
            self.wait(0.2)
        self.play(binary_block.animate.set_opacity(0.3))
        self.play(binary_block.animate.scale(0.6))
        
        binary_block_organized = VGroup(Text("11000111 0100010111110100 00000101000000000000000000000000", font="DejaVu Sans Mono"),
                                        Text("11000111 0100010111111000 00000111000000000000000000000000", font="DejaVu Sans Mono"),
                                        Text("10001011 0101010111110100", font="DejaVu Sans Mono"),
                                        Text("10001011 0100010111111000", font="DejaVu Sans Mono"),
                                        Text("00000001 11010000", font="DejaVu Sans Mono"),
                                        Text("10001001 0100010111111100", font="DejaVu Sans Mono")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).scale(0.6)

        for i in range(0,6):
            binary_block_organized[i][0:8].color = BLUE_E
            if i==4:
                binary_block_organized[i][8:16].color = MAROON_E
            else:
                binary_block_organized[i][8:24].color = MAROON_E
                if i==0 or i==1:
                    binary_block_organized[i][24:].color = ORANGE

        self.play(ReplacementTransform(binary_block, binary_block_organized), run_time=1)

        #layout de instruções de máquina
        campo1 = Text("o que", font_size=30)
        campo2 = Text("onde", font_size=30)
        campo3 = Text("dado", font_size=30)
        campo1.next_to(binary_block_organized[0][3], UP)
        campo2.next_to(binary_block_organized[0][15], UP)
        campo3.next_to(binary_block_organized[0][40], UP)
        self.play(Write(campo1))
        self.play(Write(campo2))
        self.play(Write(campo3))

        #provavelmente um laço for seria melhor. Não me pergunte pq fiz desse jeito, quando percebi ja tinha me comprometido a fazer na mão
        self.play(FadeOut(campo1), FadeOut(campo2), FadeOut(campo3))
        self.play(binary_block_organized.animate.to_edge(UP))
        self.wait(.1)
        rectangle_reader = Rectangle(height=.3, width=20, color="#8728BEC1", ).set_opacity(0.2).to_edge(UP)
        self.play(FadeIn(rectangle_reader), run_time=0.2)
        self.play(binary_block_organized[1:].animate.shift(.6*DOWN))
        op_code = Text("salvar", color=BLUE_E, font="DejaVu Sans Mono",font_size=24)
        pos_memory = Text("memória", color=MAROON_E, font="DejaVu Sans Mono",font_size=24)
        number = Text("5", color=ORANGE, font="DejaVu Sans Mono",font_size=24)
        op_code.next_to(binary_block_organized[0][:8], .86*DOWN)
        pos_memory.next_to(binary_block_organized[0][8:24], .86*DOWN)
        number.next_to(binary_block_organized[0][24], .86*DOWN)
        self.play(Write(op_code), Write(pos_memory), Write(number))

        RAM_body = Rectangle(height=4.5, width=2).to_corner(DR)
        RAM_label = Text("RAM", font_size=34).next_to(RAM_body, UP)
        CPU_body = RoundedRectangle(corner_radius=0.3, height=2.5, width=2.5).next_to(RAM_body, 8*LEFT)
        CPU_label = Text("CPU", font_size=34).next_to(CPU_body, UP)
        self.play(Create(RAM_body), Write(RAM_label), Create(CPU_body), Write(CPU_label))
        self.wait()

        self.play(FadeOut(op_code), FadeOut(pos_memory), FadeOut(number))
        number.move_to(RAM_body.get_corner(UL)).shift(.5*DOWN + .3*RIGHT)
        self.play(Write(number), binary_block_organized[1].animate.shift(.6*UP), rectangle_reader.animate.shift(.36*DOWN))
        self.wait(.2)
        
        number = Text("7", color=ORANGE, font="DejaVu Sans Mono",font_size=24)
        op_code.next_to(binary_block_organized[1][:8], .86*DOWN)
        pos_memory.next_to(binary_block_organized[1][8:24], .86*DOWN)
        number.next_to(binary_block_organized[1][24], .86*DOWN)
        self.play(Write(op_code), Write(pos_memory), Write(number))
        self.wait(.2)
        self.play(FadeOut(op_code), FadeOut(pos_memory), FadeOut(number))
        number.move_to(RAM_body.get_corner(UL)).shift(.9*DOWN + .3*RIGHT)
        self.play(Write(number), binary_block_organized[2].animate.shift(.6*UP), rectangle_reader.animate.shift(.36*DOWN))
        self.wait(.2)

        op_code = Text("carregar", color=BLUE_E, font="DejaVu Sans Mono",font_size=24) #TA TORTOOOO!
        pos_memory = Text("processador", color=MAROON_E, font="DejaVu Sans Mono",font_size=24)
        op_code.next_to(binary_block_organized[2][:8], .86*DOWN)
        pos_memory.next_to(binary_block_organized[2][8:24], .86*DOWN)
        self.play(Write(op_code), Write(pos_memory))
        self.play(FadeOut(op_code), FadeOut(pos_memory))
        number = Text("5", color=ORANGE, font="DejaVu Sans Mono",font_size=24)
        number.move_to(CPU_body.get_top()).shift(.5*DOWN)
        self.play(Write(number), binary_block_organized[3].animate.shift(.6*UP), rectangle_reader.animate.shift(.36*DOWN))
        self.wait(.2)

        op_code.next_to(binary_block_organized[3][:8], .86*DOWN)
        pos_memory.next_to(binary_block_organized[3][8:24], .86*DOWN)
        self.play(Write(op_code), Write(pos_memory))
        self.play(FadeOut(op_code), FadeOut(pos_memory))
        number = Text("7", color=ORANGE, font="DejaVu Sans Mono",font_size=24)
        number.move_to(CPU_body.get_top()).shift(DOWN)
        self.play(Write(number), binary_block_organized[4].animate.shift(.6*UP), rectangle_reader.animate.shift(.36*DOWN))
        self.wait(.2)

        op_code = Text("adicionar", color=BLUE_E, font="DejaVu Sans Mono",font_size=24)
        op_code.next_to(binary_block_organized[4][:8], .86*DOWN)
        pos_memory.next_to(binary_block_organized[4][8:24], .86*DOWN)
        self.play(Write(op_code), Write(pos_memory))
        self.play(FadeOut(op_code), FadeOut(pos_memory))
        number = Text("12", color=ORANGE, font="DejaVu Sans Mono",font_size=24)
        number.move_to(CPU_body.get_top()).shift(1.5*DOWN)
        self.play(Write(number), binary_block_organized[5].animate.shift(.6*UP), rectangle_reader.animate.shift(.36*DOWN))
        self.wait(.2)

        op_code = Text("salvar", color=BLUE_E, font="DejaVu Sans Mono",font_size=24)
        pos_memory = Text("memória", color=MAROON_E, font="DejaVu Sans Mono",font_size=24)
        op_code.next_to(binary_block_organized[5][:8], .86*DOWN)
        pos_memory.next_to(binary_block_organized[5][8:24], .86*DOWN)
        self.play(Write(op_code), Write(pos_memory))
        number = Text("12", color=ORANGE, font="DejaVu Sans Mono",font_size=24)
        number.move_to(RAM_body.get_corner(UL)).shift(1.3*DOWN + .3*RIGHT)
        self.play(Write(number))
        self.wait(.2)
        self.play(FadeOut(op_code), FadeOut(pos_memory), FadeOut(rectangle_reader))

        self.clear()
        binary_lines = []
        for _ in range(80):
            binary_string = ''.join(random.choice(['0', '1']) for _ in range(32))
            binary_lines.append(binary_string)
        
        long_binary_block = VGroup()
        for line in binary_lines:
            text = Text(line, font="DejaVu Sans Mono", font_size=24)
            long_binary_block.add(text)
        long_binary_block.arrange(DOWN, aligned_edge=LEFT, buff=0.1).scale(0.6)
        long_binary_block.to_edge(UP)
        self.play(LaggedStartMap(FadeIn, long_binary_block, lag_ratio=0.1))
        self.play(long_binary_block.animate.shift(10*UP), rate_func=rate_functions.linear, run_time=5)
        self.wait()

        self.play(FadeOut(long_binary_block))
        binary_block = VGroup(Text("11000111010001011111010000000101", font="DejaVu Sans Mono"),
                              Text("00000000000000000000000011000111", font="DejaVu Sans Mono"),
                              Text("01000101111110000000011100000000", font="DejaVu Sans Mono"),
                              Text("00000000000000001000101101010101", font="DejaVu Sans Mono"),
                              Text("11110100100010110100010111111000", font="DejaVu Sans Mono"),
                              Text("00000001110100001000100101000101", font="DejaVu Sans Mono"),
                              Text("11111110101001001001110010110010", font="DejaVu Sans Mono"),
                              Text("11000111010001011111010000000101", font="DejaVu Sans Mono"),
                              Text("00000000000000000000000011000111", font="DejaVu Sans Mono"),
                              Text("01000101111110000000011100000000", font="DejaVu Sans Mono"),
                              Text("00000000000000001000101101010101", font="DejaVu Sans Mono"),).arrange(DOWN, aligned_edge=LEFT, buff=0.1).scale(0.8)
        self.play(FadeIn(binary_block))
        self.wait(.5)
        self.play(binary_block.animate.set_opacity(0.3))

        all_chars = []
        for linha in binary_block:
            all_chars.extend(linha.submobjects)
        
        
        total_chars = len(all_chars)
        byte_size = 8
        
        num_bytes = total_chars // byte_size
        #lendo bytes
        for byte_index in range(num_bytes):
            start_idx = byte_index * byte_size
            end_idx = start_idx + byte_size
            
            for char in all_chars:
                char.set_opacity(0.3)
            
            for i in range(start_idx, end_idx):
                all_chars[i].set_opacity(0.9)
            
            self.wait(0.2)
        for byte_index in range(num_bytes):
            start_idx = byte_index * byte_size
            end_idx = start_idx + byte_size
            
            for char in all_chars:
                char.set_opacity(0.3)
            
            for i in range(start_idx, end_idx):
                all_chars[i].set_opacity(0.9)
            
            self.wait(0.05)
        self.wait()
        self.clear()

class LinguagemDeProgramacao(Scene):
    def physics_updater(self, obj, dt):
        #Vou criar um objeto que tenhas as propriedades generalizadas depois
        if not 0 < dt < 0.1: #Check para ver se deltaTime foi interrompido
            return
        if obj.active == False: #Matar animação
            return
        
        obj.velocity= obj.velocity + obj.gravity * dt 
    
        obj.shift(obj.velocity * dt) #aplicando transformacao com deltaTime
        box_half_width= obj.width / 2
        box_half_height= obj.height / 2
        #Começo de verificação de colisão e aplicando bounce
        if obj.get_right()[0] >= 2:
            obj.set_x(2 - box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_left()[0] <= -2:
            obj.set_x(-2 + box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_top()[1] >= 2:
            obj.set_y(2 - box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping
        if obj.get_bottom()[1] <= -2:
            obj.set_y(-2 + box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping
    def construct(self):
        title_text1 = Text("O que é", font_size=60)
        title_text2 = Text("linguagem de programação?", font_size=75)
        title_text2[11:22].color = "#AA77C7"
        title = VGroup(title_text1, title_text2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).scale(0.7)
        self.play(Write(title))
        self.wait()
        self.play(Unwrite(title))
        self.wait(.1)


        self.play(FadeOut(title))
        self.play(Write(Text("binario sendo digitado aqui")))
        self.wait()
        self.clear()

        binary_block = VGroup(Text("11000111010001011111010000000101", font="DejaVu Sans Mono"),
                              Text("00000000000000000000000011000111", font="DejaVu Sans Mono"),
                              Text("01000101111110000000011100000000", font="DejaVu Sans Mono"),
                              Text("00000000000000001000101101010101", font="DejaVu Sans Mono"),
                              Text("11110100100010110100010111111000", font="DejaVu Sans Mono"),
                              Text("00000001110100001000100101000101", font="DejaVu Sans Mono"),
                              Text("11111110", font="DejaVu Sans Mono")).arrange(DOWN, aligned_edge=LEFT, buff=0.1).scale(.8)
        self.play(FadeIn(binary_block))
        self.wait(.1)


        code = Code(
            code_string='''int main(){
    int a = 5;
    int b = 7;
    int soma = a + b;
}''',
            language="c",
            formatter_style="monokai",
            background="rectangle",
            background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}
        )
        self.play(Transform(binary_block, code))
        self.wait()


        self.play(FadeOut(binary_block))
        svg_python = SVGMobject("assets/python.svg")
        svg_C = SVGMobject("assets/C.svg").set_opacity(0)
        png_C = ImageMobject("assets/C.png")
        svg_java = SVGMobject("assets/java.svg")
        svg_JS = SVGMobject("assets/JS.svg").scale(.8)
        svg_lua = SVGMobject("assets/lua.svg")
        svg_php = SVGMobject("assets/php.svg").scale(.6)
        svg_cpp = SVGMobject("assets/c++.svg")
        svg_cs = SVGMobject("assets/c#.svg")
        svg_swift = SVGMobject("assets/swift.svg")
        languages = VGroup(svg_python, svg_cpp, svg_JS, svg_lua, svg_C, svg_java , svg_php, svg_cs, svg_swift).arrange_in_grid(rows=3, cols=3, buff=1).scale(.8)
        for i in range(len(languages)):
            if languages[i] != svg_C:
                self.play(Write(languages[i]))
        self.wait(.2)


        self.play(FadeIn(png_C), run_time=2)
        self.wait(.1)
        self.play(png_C.animate.scale(1.5), FadeOut(languages))
        self.play(Circumscribe(png_C))
        self.wait()


        svg_linux = SVGMobject("assets/linux2.svg")
        svg_android = SVGMobject("assets/android2.svg")
        OS_group = VGroup(svg_linux, svg_android).arrange(RIGHT, buff=1).shift(DOWN)
        self.play(png_C.animate.shift(2*UP))
        self.wait(.5)

        gravity= np.array([0, -9.8, 0])
        damping= 0.8
        
        secondBox = Square(side_length=0.5, fill_opacity= 0, color=PURPLE)
        secondBox.move_to([-8, 0,0])
        secondBox.velocity= np.array([3.0, 1.0, 0]) #velocidade inicial
        secondBox.gravity= gravity
        secondBox.damping= damping
        secondBox.active= True
        
        frame = Rectangle(height=2.5, width=4).shift(0.75*DOWN)
        self.play(Create(secondBox), Create(frame))
        secondBox.add_updater(self.physics_updater)
        self.wait(5)
        secondBox.remove_updater(self.physics_updater)
        self.play(FadeOut(secondBox), FadeOut(frame))
        self.wait()


        self.play(Write(OS_group))
        self.wait()


        self.clear()
        self.play(Write(code))
        self.wait(.1)


        self.play(FadeOut(code))
        code = Code(
            code_string='''#include <stdio.h>

int calcularSoma(int a, int b){
    int soma = a + b;
    return soma;
}

int main(){
    int a = 5;
    int b = 9;
    int soma = calcularSoma(a, b);
    printf("A soma de %d e %d é %d", a, b, soma);
}''',
            language="c",
            formatter_style="monokai",
            background="rectangle",
            background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}
        )
        self.play(Write(code))
        self.wait(.1)


        self.play(FadeOut(code))
        reserverd_words = VGroup(Text("break", font="DejaVu Sans Mono"),
                                 Text("case", font="DejaVu Sans Mono"),
                                 Text("char", font="DejaVu Sans Mono"),
                                 Text("const", font="DejaVu Sans Mono"),
                                 Text("continue", font="DejaVu Sans Mono"),
                                 Text("do", font="DejaVu Sans Mono"),
                                 Text("else", font="DejaVu Sans Mono"),
                                 Text("float", font="DejaVu Sans Mono"),
                                 Text("for", font="DejaVu Sans Mono"),
                                 Text("if", font="DejaVu Sans Mono"),
                                 Text("int", font="DejaVu Sans Mono"),
                                 Text("long", font="DejaVu Sans Mono"),
                                 Text("return", font="DejaVu Sans Mono"),
                                 Text("sizeof", font="DejaVu Sans Mono"),
                                 Text("static", font="DejaVu Sans Mono"),
                                 Text("struct", font="DejaVu Sans Mono"),
                                 Text("switch", font="DejaVu Sans Mono"),
                                 Text("typedef", font="DejaVu Sans Mono"),
                                 Text("unsigned", font="DejaVu Sans Mono"),
                                 Text("void", font="DejaVu Sans Mono"),
                                 Text("volatile", font="DejaVu Sans Mono"),
                                 Text("while", font="DejaVu Sans Mono")
                                ).arrange_in_grid(cols=2, rows=11, buff=(1, 0.3)).scale(0.5)
        symbols = VGroup(Text("aritméticos: +, -, *, /, %", font="DejaVu Sans Mono"),
                         Text("relacionais: ==, !=, <, >, <=, >=", font="DejaVu Sans Mono"),
                         Text("lógicos: &&, ||, !", font="DejaVu Sans Mono"),
                         Text("bit a bit: &, |, ^, ~, <<, >>", font="DejaVu Sans Mono")
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).scale(0.5)
        self.play(Write(VGroup(reserverd_words, symbols).arrange(RIGHT, buff=1)))
        self.wait(.1)


        reserverd_words_card = RoundedRectangle(corner_radius=0.5, color = "#8728BE",stroke_color= "#AA77C7",fill_opacity=0.1,height=5.0,width=4).move_to(reserverd_words)
        symbols_card = RoundedRectangle(corner_radius=0.5, color = "#8728BE",stroke_color= "#AA77C7",fill_opacity=0.1,height=2.5,width=7).move_to(symbols)
        self.play(Create(reserverd_words_card))
        self.wait()



        self.play(Uncreate(reserverd_words_card), Create(symbols_card))
        self.wait()


        self.play(Uncreate(symbols_card))
        self.wait(.1)


        self.play(Unwrite(symbols), Unwrite(reserverd_words), run_time=0.8)
        code.scale(0.4).to_edge(LEFT)
        codigo_text = Text("Código", font_size=30).next_to(code, UP)
        self.play(Write(code), Write(codigo_text))
        self.wait(.1)


        svg_machine = SVGMobject("assets/machine.svg")
        compilador_texto = Text("Compilador").next_to(svg_machine, UP).scale(.7)
        self.play(Write(svg_machine), Write(compilador_texto))
        self.wait()


        self.play(Unwrite(codigo_text))
        self.play(code.animate.scale(0).move_to(ORIGIN))
        self.play(Wiggle(svg_machine))

        binary_text = Text("11011010101010000...", font="DejaVu Sans Mono").scale(0.5).shift(RIGHT)
        programa_text = Text("Programa executável").scale(.7).shift(4.5*RIGHT+1.55*UP)
        self.play(GrowFromCenter(binary_text), binary_text.animate.to_edge(RIGHT))
        self.play(Write(programa_text))
        self.wait(1)
        scene = VGroup(binary_text, programa_text, svg_machine, compilador_texto)
        self.play(scene.animate.shift(15*LEFT))
        self.clear()

        Warning.construct(self)
        
        self.clear()
        title_text1 = Text("O que é", font_size=60)
        abstracao = Text("Abstração?", font_size=75, color="#AA77C7")
        abstracao[-1].set_color(WHITE)
        title2 = VGroup(title_text1, abstracao).arrange(DOWN, aligned_edge=LEFT, buff=0.2).scale(0.7)
        self.play(Write(title2))
        self.wait(.1)

        
        self.play(FadeOut(title2))
        logo_comando = SVGMobject("assets/arvore.svg")
        svg_tree1 = SVGMobject("assets/tree1.svg")
        svg_tree2 = SVGMobject("assets/tree2.svg")
        svg_tree3 = SVGMobject("assets/tree3.svg")
        svg_tree4 = SVGMobject("assets/tree4.svg")
        svg_tree5 = SVGMobject("assets/tree5.svg")
        trees = VGroup(svg_tree2, svg_tree3, svg_tree4, svg_tree5).arrange_in_grid(rows=2, cols=2, buff=1)
        self.play(Write(svg_tree1))
        self.wait()

        
        self.play(Unwrite(svg_tree1))
        self.wait(.5)
        self.play(Write(logo_comando.scale(1.5)))
        self.wait(3)
        self.clear()
        self.play(FadeIn(trees), run_time=2.5)
        self.play((Circumscribe(trees)), run_time=4)
        self.wait(.1)

        implies_latex = MathTex(r"\implies").scale(2)
        svg_sound_wave = SVGMobject("assets/sound-wave.svg").scale(1.5).next_to(implies_latex, LEFT, buff=2)
        svg_bubble = SVGMobject("assets/thought-bubble.svg").scale(2.5)
        self.play(trees.animate.to_edge(RIGHT, buff=1))
        self.play(Write(svg_sound_wave), AddTextLetterByLetter(Text("\"árvore\"", font_size=30).next_to(svg_sound_wave, DOWN)))
        self.play(Create(implies_latex))
        self.wait(2)


        self.play(trees.animate.scale(.5))
        self.play(Create(svg_bubble.move_to(trees.get_center()+0.5*DOWN+0.2*LEFT)))
        self.wait()
        

        self.clear()
        svg_computer = SVGMobject("assets/computer")
        binary_text = Text("101011", font_size=15).move_to(svg_computer.get_center()+0.5*UP)
        computer = VGroup(svg_computer, binary_text).scale(1.5)
        self.play(Write(computer))
        self.wait()


        svg_circuits = SVGMobject("assets/circuit.svg").scale(1.5)
        self.play(Transform(computer, svg_circuits))
        self.wait(.5)
        binary_text = Text("101011?", font="DejaVu Sans Mono",font_size=15).next_to(computer, UP)
        self.play(AddTextLetterByLetter(binary_text), run_time=2)
        self.wait()


        self.clear()
        voltage_lines = VGroup(Line(start=(-7.4, 0.5, 0), end=(7.4, 0.5, 0)).set_stroke(YELLOW, 3, 0.5),
                               Line(start=(-7.4, -0.5, 0), end=(7.4, -0.5, 0)).set_stroke(YELLOW, 3, 0.5),
                               Text("5V", font="DejaVu Sans Mono", font_size=20, color=GRAY).move_to((-6.8, 0.8, 0)),
                               Text("0V", font="DejaVu Sans Mono", font_size=20, color=GRAY).move_to((-6.8, -0.8, 0))
                            )
        all_dots = VGroup()
        points = [
            [-7.4, -0.5, 0],
            [-6.4, -0.5, 0],
            [-6.4, 0.5, 0],
            [-5.4, 0.5, 0],
            [-5.4, -0.5, 0]
        ]
        zero = Text("0", font="DejaVu Sans Mono", font_size=25).move_to((-6.9, -0.8, 0))
        zeros = VGroup(zero)
        one = Text("1", font="DejaVu Sans Mono", font_size=25).move_to((-7.9, 0.8, 0))
        ones = VGroup(one)
        v_lines = VGroup()
        for i in range(2,16, 2):
            zeros.add(zero.copy().shift(i*RIGHT))
            ones.add(one.copy().shift(i*RIGHT))
            points.append([-7.4+i, -0.5, 0])
            points.append([-6.4+i, -0.5, 0])
            points.append([-6.4+i, 0.5, 0])
            points.append([-5.4+i, 0.5, 0])
            points.append([-5.4+i, -0.5, 0])
        for i in range(0,16):
            v_line = Line(UP, DOWN).set_height(1080)
            v_line.set_stroke(GREY_C, 1, 0.75)
            v_line.set_x(-6.4+i)
            v_line.set_y(0)
            v_lines.add(v_line)
        all_dots.set_points_as_corners(points).set_color(YELLOW)
        self.play(Create(all_dots))
        self.wait()
        self.play(Create(voltage_lines))
        self.wait()
        self.play(Write(v_lines), FadeOut(voltage_lines))
        self.wait()
        self.play(Write(zeros))
        self.wait(.5)
        self.play(Write(ones))
        self.wait(.1)


        self.play(FadeOut(zeros), FadeOut(ones), FadeOut(all_dots), FadeOut(v_lines))

        volt_rectan = Rectangle(height=2, width=7)
        binary_rectan = Rectangle(height=2, width=7)
        programming_language_rectan = Rectangle(height=2, width=7)
        rectangles = VGroup(volt_rectan, binary_rectan, programming_language_rectan).arrange(UP, buff=0.3)

        binary_label = Text("010101010000", font="DejaVu Sans Mono", font_size=30).move_to(binary_rectan.get_center())
        programming_language_label = Text("Linguagens de programação", font_size=30).move_to(programming_language_rectan.get_center())
        programming_language_label[12:].color = "#AA77C7"
        all_dots = VGroup()
        points = [
            [-7.4, -0.5, 0],
            [-6.4, -0.5, 0],
            [-6.4, 0.5, 0],
            [-5.4, 0.5, 0],
            [-5.4, -0.5, 0]
        ]
        for i in range(2,8, 2):
            points.append([-7.4+i, -0.5, 0])
            points.append([-6.4+i, -0.5, 0])
            points.append([-6.4+i, 0.5, 0])
            points.append([-5.4+i, 0.5, 0])
            points.append([-5.4+i, -0.5, 0])
        points.append([-5.4+9, -0.5, 0])
        all_dots.set_points_as_corners(points).set_color(YELLOW).scale(0.5)
        all_dots.move_to(volt_rectan.get_center())

        self.play(Write(rectangles))
        self.play(Create(all_dots))
        self.play(Write(binary_label))
        self.play(Write(programming_language_label))
        self.wait()


        self.play(Group(*self.mobjects).animate.scale(0.5,about_point=ORIGIN))
        svg_CPU = SVGMobject("assets/cpu.svg").scale(0.8).to_edge(DOWN)
        svg_person = SVGMobject("assets/person.svg").scale(0.8).to_edge(UP)
        self.play(Write(svg_CPU), Write(svg_person))
        self.wait()


        self.play(Unwrite(rectangles), Unwrite(all_dots), Unwrite(binary_label), Unwrite(svg_CPU), Unwrite(svg_person))
        self.play(programming_language_label.animate.scale(2.5).to_edge(UP))


        bracket_left = Line(UP*2.5, DOWN*3.5).shift(3*LEFT)
        bracket_right = Line(UP*2.5, DOWN*3.5).shift(3*RIGHT)

        frame = VGroup(bracket_left, bracket_right).set_color(BLUE_E)
        title = Text("Abstração", font_size=36, color="#AA77C7").rotate(PI/2)
        up_arrow = Arrow(start=DOWN, end=UP, buff=0.3).next_to(title, UP)
        down_arrow = Arrow(start=UP, end=DOWN, buff=0.3).next_to(title, DOWN)
        label_abstraction = VGroup(up_arrow, title, down_arrow).arrange(DOWN).next_to(bracket_left, LEFT, buff=0.3)
        languages_high = VGroup(Text("Ruby"),
                                Text("Python"),
                                Text("JavaScript"),
                                Text("Java"),
                                Text("PHP"),
                                Text("C#"),
                                Text("Swift"),
                                Text("Kotlin"),
                                ).arrange_in_grid(cols=4, buff=0.5).shift(UP*2).scale(0.5)
        
        mid_lang = Text("C", font_size=60, color="#AA77C7")
        
        assembly = VGroup(Text("Intel assembly"),
                          Text("ARM assembly"),
                          Text("AT&T assembly")
                        ).arrange(buff=1).shift(DOWN*1.5).scale(0.3)
        
        machine = VGroup(Text("Binário x86"),
                         Text("Binário ARM"),
                         Text("Binário x86-64")
                        ).arrange(buff=1).shift(DOWN*2.5).scale(0.3)
        
        self.play(Write(frame))
        self.play(FadeIn(label_abstraction))
        self.play(FadeIn(languages_high))
        self.wait()


        self.play(FadeIn(assembly))
        self.play(FadeIn(machine))
        self.wait()


        self.play(FadeIn(mid_lang))
        self.wait()
        self.clear()

class Warning(Scene): #FEITO PELO GABRIEL COVALSKI!!!
    def construct(self):

# --- CENA 1 ----
        # A warning sign
        warningSign = SVGMobject("assets/warning_sign.svg")

        # Texto que acompanha a WarningSign
        synText = Text("Sintaxe != Semântica").move_to(DOWN)





# --- CENA 2 ----
        # Código
        codigo = '''#include <stdio.h>

int main(){
    int um=1
    int dois=2;

    int tres=um+dois

    printf("Resultado: %d",tres);
}'''

        codigoRenderizado = Code(code_string = codigo, 
                               language = "c", 
                               formatter_style = "monokai", 
                               background = "rectangle", 
                               background_config = {"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})
        
        codigoRenderizado.save_state() # Isso aqui é importante para desfazer as transformações depois!!!

        # Acessa a linha específica
        textoAgrupado = codigoRenderizado[2]
        linhaErrada1 = textoAgrupado[3] 
        linhaErrada2 = textoAgrupado[6] 

        # Mensagem de erro
        erro = Text('''prog.c: In function ‘main’:
prog.c:5:5: error: expected ‘,’ or ‘;’ before ‘int’
    5 |     int dois=2;
      |     ^~~
prog.c:9:5: error: expected ‘,’ or ‘;’ before ‘printf’
    9 |     printf("Resultado: %d",tres);
      |     ^~~~~~''',color = RED).move_to(RIGHT*3).scale(0.4)





# --- CENA 3 ----
        # Código correto para dar Become() depoiss :)))))))) Eu perdi a minha sanidade tentando achar outro método, não, não estou bem depois de ficar 1h tentando coisas sem efeito.
        codigoCorreto = '''#include <stdio.h>

int main(){
    int um=1;
    int dois=2;

    int tres=um+dois;

    printf("Resultado: %d",tres);
}'''

        codigoRenderizadoCorreto = Code(code_string = codigoCorreto, 
                               language = "c", 
                               formatter_style = "monokai", 
                               background = "rectangle", 
                               background_config = {"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1})

        # Acessa a linha específica (Lembre-se: o índice começa em 0)
        textoAgrupado = codigoRenderizado[2]
        linhaErrada1 = textoAgrupado[3] 

        # Resultado correto 
        resultado = Text('''Resultado: 3''',color = GREEN).move_to(RIGHT*3).scale(0.8)





# --- CENA 4 ----
        # Linhas de código Certas, e Erradas
        codigo =  '''int um=1.

int um=1:

int um=1;'''

        synCodigoRenderizado = Code(code_string = codigo, 
                               language = "c", 
                               formatter_style = "monokai", 
                               background = "rectangle", 
                               background_config = {"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}).scale(1.5)
        
        # Acessa a linha específica, reutilizando as variáveis de antes
        synTextoAgrupado = synCodigoRenderizado[2]
        synLinhaErrada1 = synTextoAgrupado[0] 
        synLinhaErrada2 = synTextoAgrupado[2] 
        synLinhaCorreta = synTextoAgrupado[4]

        # Texto bem grandão e bonito escrito Sintaxe (Como se não desse para entender só lendo o código)
        sintaxe = Text("Sintaxe").move_to(UP*5)
        





# --- CENA 5 ----
        # É um pássaro? É um avião? NÃO! É um bloco de código HAHAHAHAHAHHAHHHAHAHHAHAHHAHAHAHAHAHAHAH
        logCodigo = '''int numeroPar=1;

printf("Exibir valor par: %d",numeroPar);'''

        logCodigoRenderizado = Code(code_string = logCodigo, 
                               language = "c", 
                               formatter_style = "monokai", 
                               background = "rectangle", 
                               background_config = {"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}).move_to(ORIGIN)
        
        logResultado = Text("Exibir valor par: 1",color=GREEN).move_to(DOWN).scale(0.8)





# -------- CENA 6 ----------
        # SVG do ícone de usuário
        iconeUsuario = ImageMobject("assets/user_icon.png").move_to(RIGHT*2).scale(0.8)

        # Espaço de login 
        fundoCard = RoundedRectangle(corner_radius=0.2, # Fundo
            height=3,
            width=3.5,
            fill_color="#222222", # Cinza escuro
            fill_opacity=1,
            stroke_color=WHITE
        )

        # Espaço do nome
        lblNome = Text("Nome", font_size=24).move_to(fundoCard.get_top() + DOWN*0.5 + LEFT*0.8) # Escrita
        lblNome.align_to(fundoCard, LEFT).shift(RIGHT*0.3) # Alinha o texto à esquerda dentro do card
        
        inputNome = Rectangle(      # Input
            height=0.5, 
            width=2.8, 
            stroke_color=BLUE_B, 
            fill_opacity=0
        )
        inputNome.next_to(lblNome, DOWN, aligned_edge=LEFT, buff=0.1) # Alinhamento do input

        # Espaço da idade
        lblIdade = Text("Idade", font_size=24)  # Escrita
        lblIdade.next_to(inputNome, DOWN, aligned_edge=LEFT, buff=0.5) # Alinha o texto à esquerda dentro do card
        
        inputIdade = Rectangle( # Input
            height=0.5, 
            width=2.8, 
            stroke_color=BLUE_B, 
            fill_opacity=0
        )
        inputIdade.next_to(lblIdade, DOWN, aligned_edge=LEFT, buff=0.1) # Alinhamento do input

        # Junta tudo numa coisa só
        CardVazio = VGroup(fundoCard,lblNome,inputNome,lblIdade,inputIdade).move_to(LEFT*2)



# -------- CENA 7-9 ----------
        # SVG do teclado para incluir
        teclado = SVGMobject("assets/keyboard.svg")

        # Escrita do Input
        txtNome = Text("Erikson", font_size=60, color=LIGHT_GREY).scale(1/3)
        txtNome.next_to(inputNome, LEFT).shift(RIGHT*1.4)

        txtIdade = Text("20", font_size=60, color=LIGHT_GREY).scale(1/3)
        txtIdade.next_to(inputIdade, LEFT).shift(RIGHT*0.8)

        # Flecha?
        flecha = MathTex(r"\implies", font_size=50).move_to(ORIGIN)

        # Card
        outCard = RoundedRectangle(corner_radius=0.5, color = "#8728BE",stroke_color= "#AA77C7",fill_opacity=0.1,height=5.0,width=8.0).scale(0.4).move_to(DOWN+RIGHT*3)
        outCorretoText = Text("Olá Erikson, seja bem vindo(a)!").scale(0.3).move_to(DOWN+RIGHT*3)
        outErradoText = Text("Olá 20, seja bem vindo(a)!").scale(0.3).move_to(DOWN)

        # Escrita de código
        outCodigo = Text("printf(''Olá %s, seja bem vindo(a)!'', nome);",
                         font="Manrope",
                         t2c={
                                "''Olá": YELLOW,
                                "%s": GREEN,
                                ", seja bem vindo(a)!''": YELLOW,
                                "nome": GREEN

                        }).scale(0.3).move_to(RIGHT*3)

        # Sublinhado e "???" do grande final, cortina e aplausos
        interrogacao = Text("???").next_to(outCard, RIGHT, aligned_edge=LEFT, buff=0.2)













        # ------------------------- ANIMAÇÕES -------------------------------------
        # Transição para o que realmente ta sendo mostrado
        self.play(GrowFromCenter(warningSign))

        # Movimentos ultra legais da Warning Sign
        # Para cima e texto aparece
        self.play(warningSign.animate.move_to(UP),
                Write(synText))
        
        # Diminui tamanho E vai para a esquerda
        self.play(warningSign.animate.scale(0.4), synText.animate.scale(0.7))
        self.play(warningSign.animate.move_to(UP*3+LEFT*3.5), synText.animate.move_to(UP*3))

        self.play(GrowFromCenter(codigoRenderizado))
        self.wait()

        # O Código vai para a esquerda para dar espaço à mensagem de erro
        self.play(codigoRenderizado.animate.move_to(LEFT*3).scale(0.7))
        # Sublinhado de erro
        sublinhado1=Underline(linhaErrada1, color=RED, buff=0.05)
        sublinhado2=Underline(linhaErrada2, color=RED, buff=0.05)

        self.play(Write(erro))
        self.play(Create(sublinhado1), Create(sublinhado2))

        self.wait()
        # Retorna ao que tava antes e desublinha os erros
        self.play(Unwrite(erro), Uncreate(sublinhado1), Uncreate(sublinhado2))
        self.play(Restore(codigoRenderizado))

        # Corrige
        self.play(TransformMatchingShapes(codigoRenderizado, codigoRenderizadoCorreto))
        self.wait()

        # Transforma para a esquerda de novo para mostrar que deu certo
        self.play(codigoRenderizadoCorreto.animate.move_to(LEFT*3).scale(0.7))
        self.play(Write(resultado))

        self.wait()

        # Limpa a tela
        self.play(Uncreate(resultado), Uncreate(codigoRenderizadoCorreto), Uncreate(synText), Uncreate(warningSign))
        self.wait()

        # Linhas certas e erradas
        self.play(GrowFromCenter(synCodigoRenderizado))

        sublinhado1=Underline(synLinhaErrada1, color=RED, buff=0.05)
        sublinhado2=Underline(synLinhaErrada2, color=RED, buff=0.05)
        sublinhado3=Underline(synLinhaCorreta, color=GREEN, buff=0.05)
        self.play(Create(sublinhado1), Create(sublinhado2), Create(sublinhado3))
        self.wait()

        # Codigo vai para baixo, texto da Syntaxe desce para o centro da tela
        self.play(Uncreate(sublinhado1), Uncreate(sublinhado2), Uncreate(sublinhado3))
        self.play(synCodigoRenderizado.animate.move_to(DOWN*10),
                sintaxe.animate.move_to(ORIGIN))
        self.wait()
        
        





        # CENA 5, TOMADA 1
        # CONTAGEM REGRESSIVA: 3,2,1 EEEEEE AÇÃO!
        self.play(Unwrite(sintaxe),Uncreate(synCodigoRenderizado))
        
        self.play(GrowFromCenter(logCodigoRenderizado))
        self.play(logCodigoRenderizado.animate.move_to(UP))
        self.play(Write(logResultado))
        self.wait()

        # Limpando o cenário pessoal, licença
        self.play(Uncreate(logCodigoRenderizado), Uncreate(logResultado))







        # CERTO, TODOS ATENTOS PARA A CONTAGEM REGRESSIVA
        # CENA 6, TOMADA 1
        # 3, 2, 1 EEEEEEEEEEEEEEEEEE AÇÃO!!
        self.play(GrowFromCenter(iconeUsuario),DrawBorderThenFill(CardVazio))
        self.wait()
        





        # Perfeito, agora avançemos para a Cena 7, é onde os espaços de input são preenchidos
        self.play(AddTextLetterByLetter(txtNome), run_time=0.8)
        self.play(AddTextLetterByLetter(txtIdade), run_time=0.5)

        CardVazio.add(txtNome,txtIdade)






        # Em seguida, na Cena 8, o card vai para a esquerda, a Arrow do manim aparece e então o output é mostrado
        self.play(CardVazio.animate.scale(0.5),iconeUsuario.animate.scale(0.5))
        self.play(CardVazio.animate.move_to(LEFT*4),iconeUsuario.animate.move_to(LEFT*2))
        
        self.play(Create(flecha))

        self.play(Create(outCodigo))
        self.play(Create(outCorretoText),Create(outCard),outCodigo.animate.shift(UP))

        self.wait()





        # E finalmente, na Cena 9 como desenhado, o output ganha enfoque
        # Primeiro limpamos a tela
        self.play(CardVazio.animate.move_to(LEFT*10),
                iconeUsuario.animate.move_to(LEFT*10),
                flecha.animate.move_to(LEFT*10))
        
        self.remove(CardVazio,iconeUsuario,flecha)

        # Agora a gente centraliza 
        self.play(outCodigo.animate.move_to(ORIGIN+UP),
                outCard.animate.move_to(ORIGIN+DOWN),
                Transform(outCorretoText,outErradoText)
                )
        



        # Alas, le grand final
        self.play(outCard.animate.scale(1.5), outCorretoText.animate.scale(1.5), outCodigo.animate.scale(1.5))

        self.wait()

        sublinhadoVerde = Underline(outCodigo, color=GREEN, buff=0.05)
        self.play(Create(sublinhadoVerde))
        self.play(AddTextLetterByLetter(interrogacao),run_time=2.5)

        self.wait()

        # Aplausos, Cortinas, Pão e Circo
        self.play(Uncreate(sublinhadoVerde))
        self.play(Uncreate(outCorretoText), Uncreate(outCard), Uncreate(outCodigo), Uncreate(interrogacao))
        self.wait()

class Final(MovingCameraScene):
    def construct(self):
        plus = Text("+", font_size=60)
        svg_person = SVGMobject("assets/person.svg")
        programmer = VGroup(svg_person, plus).arrange(DOWN, buff=0.3)
        png_C = ImageMobject("assets/C.png").next_to(programmer, DOWN)

        codigo_fonte_text = Text("código-fonte", color="#AA77C7")
        codigo_fonte_retangulo = SurroundingRectangle(codigo_fonte_text, color=WHITE,buff=0.5)
        arrow1 = LabeledArrow("codar", start=programmer.get_right(), end=programmer.get_right()+3.5*RIGHT, label_position=0.5)
        codigo_fonte = VGroup(codigo_fonte_retangulo, codigo_fonte_text).next_to(arrow1, RIGHT)

        compilador_text = Text("compilador", color="#AA77C7")
        compilador_retangulo = SurroundingRectangle(compilador_text, color=WHITE, buff=0.5)
        arrow2 = LabeledArrow("entrada", start=codigo_fonte.get_right(), end=codigo_fonte.get_right()+4*RIGHT, label_position=0.5)
        compilador = VGroup(compilador_text, compilador_retangulo).next_to(arrow2, RIGHT)

        binary_text = Text("1001011", color="#AA77C7")
        binary_rectangle = SurroundingRectangle(binary_text, color=WHITE, buff=0.5)
        arrow3 = LabeledArrow("saida", start=compilador.get_right(), end=compilador.get_right()+3.5*RIGHT, label_position=0.5)
        binary = VGroup(binary_text, binary_rectangle).next_to(arrow3, RIGHT)

        maquina_text = Text("Computador", color="#AA77C7")
        maquina_rectangle = SurroundingRectangle(maquina_text, color=WHITE, buff=0.5)
        arrow4 = LabeledArrow("executar", start=binary.get_right(), end=binary.get_right()+4*RIGHT, label_position=0.5)
        maquina = VGroup(maquina_text, maquina_rectangle).next_to(arrow4, RIGHT)

        self.play(Create(programmer), FadeIn(png_C), Create(codigo_fonte), Create(compilador), Create(arrow1), Create(arrow2), Create(arrow3), Create(binary), Create(arrow4), Create(maquina))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.move_to(codigo_fonte))
        self.wait(2)
        self.play(self.camera.frame.animate.move_to(compilador))
        self.wait(2)
        self.play(self.camera.frame.animate.move_to(binary))
        self.wait(2)
        self.play(self.camera.frame.animate.scale(2))
        self.play(self.camera.frame.animate.move_to(17*RIGHT))
        compilacao = RoundedRectangle(corner_radius=0.5, color = "#8728BE",stroke_color= "#AA77C7",fill_opacity=0.1,height=8,width=15).shift(17*RIGHT)
        compilacao_text = Text("Compilação", font_size=60).next_to(compilacao, UP)
        self.play(Create(compilacao))
        self.play(Write(compilacao_text))
        self.wait(2)
        self.play(self.camera.frame.animate.move_to(maquina), Uncreate(compilacao), Unwrite(compilacao_text))
        self.play(self.camera.frame.animate.scale(0.5))
        self.wait(2)
        self.play(Uncreate(arrow4), Uncreate(maquina), Uncreate(binary))
        self.wait()


        self.clear()
        self.camera.frame.move_to(ORIGIN)
        bonus = Text("Bônus")
        bonus_text = Text("Programa vs Algoritmo", color="#AA77C7")
        bonus_text[8:10].color=WHITE
        self.play(Write(bonus))
        self.play(bonus.animate.to_edge(UP))
        self.play(Write(bonus_text))
        self.wait()
        self.play(Unwrite(bonus_text))
        self.wait()

        final_text1 = Text("Próxima aula:",font_size=60)
        final_text2 = Text("Origem, filosofia e importância de C",font_size=75)
        final_text2[-1].color = "#AA77C7"
        final = VGroup(final_text1, final_text2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(.7)
        self.play(Write(final))
        self.wait()

        #creditos
        logo = ImageMobject("assets/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        cursor=ImageMobject("assets/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)
        titulo=Text("Créditos", font_size=80)
        titulo.color="#AA77C7"

        diretor = Group(Text("Diretor", font_size=60), Text("Rainier R. Waki", font_size=45)).arrange(DOWN, buff=0.3)
        tutor = Group(Text("Tutor (voz)", font_size=60), Text("Alyson V. Isaluski", font_size=45)).arrange(DOWN, buff=0.3)
        redator = Group(Text("Redator", font_size=60),Text("Wallace P. F. Junior", font_size=45)).arrange(DOWN, buff=0.3)
        manimator = Group(Text("Manimators", font_size=60),Text("Rainier R. Waki", font_size=45), Text("Gabriel Covalski", font_size=40)).arrange(DOWN, buff=0.3)

        utfpr= ImageMobject("assets/utfpr.png").scale(0.7)
        creditos = Group(titulo, diretor, tutor, redator, manimator,utfpr).arrange(DOWN, buff=1).scale(0.5)

        self.play(
            logoOrigin.animate.become(logo),
            run_time=2
        )

        # Cursor aparece e se move
        self.play(cursor.animate.move_to(ORIGIN+RIGHT*0.25+DOWN*0.45))
        self.play(cursor.animate.scale(0.8),run_time=0.1,rate_func=linear)  # Clica
        self.play(cursor.animate.scale(1.2),run_time=0.1,rate_func=linear)  #

        # Vinheta Puxada
        self.play(
            GrowFromCenter(Rectangle(color="#0A0A0A",fill_opacity=1,width=20, height=10),run_time=0.5)
        )

        # Nomes e Cargos
        self.play(AnimationGroup(FadeIn(creditos.move_to(ORIGIN))))
        self.wait()
