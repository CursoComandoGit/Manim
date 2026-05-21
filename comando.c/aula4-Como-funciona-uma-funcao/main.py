from manim import *

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

class aulaCompleta(MovingCameraScene):
    def construct(self):
        # ----------- Cenas -----------
        animacaoAntigaWindows.construct(self)
        alunoPassou.construct(self)
        simMas.construct(self)

class animacaoAntigaWindows(Scene):
    def construct(self):
        # ----------- Objetos -----------
        # Exemplo
        exemplo = Text("exemplo")

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
        # Exemplo
        self.add(exemplo)
        #self.add(numberPlane)
        self.play(ShrinkToCenter(exemplo))

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
        codeMedia = r'''double calcularMedia(float n1, float n2) {
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
        ).scale(0.5)

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
        blocoCalcularMedia = codeRenderMedia.code_lines[0:8]
        blocoMain = codeRenderMedia.code_lines[8:30]

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
        self.play(Circumscribe(codeRenderMedia.code_lines[8], color=WHITE),run_time=1.2)

        # Circumscribe nas notas
        self.play(Circumscribe(codeRenderMedia.code_lines[12:16], color=WHITE),run_time=1.2)

        self.wait()

        # Zoom no calcularMedia
        self.play(self.camera.frame.animate.set(width = codeRenderMedia.code_lines[17].width*2).move_to(codeRenderMedia.code_lines[17]), Wiggle(codeRenderMedia.code_lines[17]))
        self.wait()

        # Move códigos para longe
        self.play(codeRenderMedia.code_lines[0:16].animate.shift(UP*2), codeRenderMedia.code_lines[18:].animate.shift(DOWN*2))
        self.wait()

        self.play(Circumscribe(blocoMain[9][11],color=WHITE))
        self.wait()
        self.play(Circumscribe(blocoMain[9][12:25],color=WHITE))
        self.wait()
        self.play(Circumscribe(blocoMain[9][26:29],color=WHITE))
        self.wait()

        # Move códigos de volta para perto
        self.play(codeRenderMedia.code_lines[0:16].animate.shift(DOWN*2), codeRenderMedia.code_lines[18:].animate.shift(UP*2))
        self.wait()

        # Câmera se desloca para a função calcular media
        self.play(self.camera.frame.animate.set(width = blocoCalcularMedia.width*2).move_to(blocoCalcularMedia))
        self.wait()

        # POsicao da camera
        cam_center = self.camera.frame.get_center()
        cam_width = self.camera.frame.width

        # Centraliaz na calcular media
        self.play(self.camera.frame.animate.set(width = blocoCalcularMedia[0].width*2).move_to(blocoCalcularMedia[0]), blocoMain.animate.shift(DOWN*3), blocoCalcularMedia[1:].animate.shift(DOWN*3))
        self.wait()

        self.play(Circumscribe(blocoCalcularMedia[0][0:6], color=WHITE))
        self.wait()
        self.play(Circumscribe(blocoCalcularMedia[0][6:19], color=WHITE))
        self.wait()
        self.play(Circumscribe(blocoCalcularMedia[0][20:35], color=WHITE))
        self.wait()

        # Retorna a focar no bloco todo
        self.play(self.camera.frame.animate.set(width=cam_width).move_to(cam_center),blocoMain.animate.shift(UP*3),blocoCalcularMedia[1:].animate.shift(UP*3))
        self.wait()

        # Variável retorna para onde foi chamada
        self.play(Indicate(blocoCalcularMedia[6]))
        self.wait()


        
        # Zoom na Main
        self.play(self.camera.frame.animate.set(width = codeRenderMedia.code_lines[17].width*2).move_to(codeRenderMedia.code_lines[17]))
        self.wait()

        self.play(Indicate(codeRenderMedia.code_lines[17]))
        self.wait()

        # Finalmente termina tudo, dá clear, e volta a câmera para a posição original
        self.play(self.camera.frame.animate.shift(RIGHT*20))
        self.clear()
        self.play(Restore(self.camera.frame))

class simMas(Scene):
    def construct(self):
        exemplo = Text("Exemplo")

        self.add(exemplo)
        self.wait()
