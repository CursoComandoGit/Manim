from manim import *
import random
from manim_slides.slide import Slide

class Main(Slide, MovingCameraScene):
    config.background_color = "#1E1E1E"

    def windUpdater(self, mobject, dt):
        velocidadeAtual = velocidadeVento.get_value()
        for line in mobject:
            line.set_opacity(opacidadeVento.get_value())
            line.shift(UP * velocidadeAtual * dt)
            if line.get_y() > 5.5:
                line.set_y(-22)
                line.set_x(random.uniform(-7.5, 7.5))
    def cenaRepetida(self, palavra : str, logo):
        #use essa cor para as linhas aa77c7
        #Gravando posição original
        originalPos = self.camera.frame.get_center()

        #Linhas
        linhasE = VGroup(*[Line([x, 5, 0], [x, random.uniform(2.2, -1.75), 0], #Posições da linha
                                cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20) #Thickness e ponta
                                for max in range(1,5) if(separation := 1.5,x := random.uniform(-(separation*max)-1, -(separation*max)-0.6))]) #parâmetros de criação
        
        linhasD = VGroup(*[Line([x, 5, 0], [x, random.uniform(2.2, -1.75), 0], #Posições da linha
                                cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20) #Thickness e ponta
                                for max in range(1,5) if(separation := 1.5,x := random.uniform((separation*max)+1, (separation*max)+0.6))]) #parâmetros de criação
        
        linhasE2 = VGroup(*[Line(linha.get_end(), linha.get_end() + [random.uniform(0.75, -0.75), random.uniform(-1.5,-0.5), 0],
                                 cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
                                 for linha in linhasE])
        linhasD2 = VGroup(*[Line(linha.get_end(), linha.get_end() + [random.uniform(0.75, -0.75), random.uniform(-1.5,-0.5), 0],
                                 cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
                                 for linha in linhasD])

        linhaCentral = Line([0,5,0], [0,0,0], cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
        linhaCentral2 = Line([0,5,0], [0,-2.5,0], cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)

        nodesE = VGroup(*[Circle(0.3).set_stroke("#aa77c7", 20).next_to(linha.get_end(), DOWN, buff=0.1).set_fill(opacity=0)
                                 for linha in linhasE2])
        nodesD = VGroup(*[Circle(0.3).set_stroke("#aa77c7", 20).next_to(linha.get_end(), DOWN, buff=0.1).set_fill(opacity=0)
                                 for linha in linhasD2])

        nodeCentral = Ellipse(4.2, 2.5).set_stroke("#aa77c7", 20).next_to(linhaCentral2.get_end(), DOWN, buff = 0.1)
        palavraChave = Text(palavra, font="Oswald").move_to(nodeCentral.get_center())

        ultimasLinhasD = VGroup(*[Line(node.get_bottom(), [node.get_bottom()[0], random.uniform(-8, -10), 0],
                                       cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
                                  for node in nodesD[1:]])
        ultimasLinhasE = VGroup(*[Line(node.get_bottom(), [node.get_bottom()[0], random.uniform(-8, -10), 0],
                                       cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
                                  for node in nodesE[1:]])
        
        ultimaLinhaCentral = Line(nodeCentral.get_bottom(), [0,-10,0], cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
        objetosCentrais = VGroup(linhaCentral, nodeCentral, palavraChave)
        allLinhasD = VGroup(linhasD, linhasD2, nodesD)
        allLinhasE = VGroup(linhasE, linhasE2, nodesE)
        allLinhasFinais = VGroup(ultimaLinhaCentral, ultimasLinhasD, ultimasLinhasE)
        #Inicio animação#
        allLinhasE[1].set_stroke(opacity=0)
        allLinhasD[1].set_stroke(opacity=0)
        allLinhasE[2].set_stroke(opacity=0)
        allLinhasD[2].set_stroke(opacity=0)
        allLinhasFinais.set_stroke(opacity=0)
        
        self.play(velocidadeVento.animate.set_value(5), run_time=0.8)
        self.play(Create(linhasE),
                  Create(linhasD),
                  Create(linhaCentral),
                  allLinhasE.animate.shift([0,random.uniform(0, 0.2),0]),
                  allLinhasD.animate.shift([0,random.uniform(0, 0.2),0]),
                  run_time = 2)
        allLinhasE[2].set_stroke(opacity=0)
        allLinhasD[2].set_stroke(opacity=0)
        allLinhasE[1].set_stroke(opacity=1)
        allLinhasD[1].set_stroke(opacity=1)
        
        self.play(Create(linhasE2),
                  Create(linhasD2),
                  Create(linhaCentral2),
                  self.camera.frame.animate.shift([0,-2.2,0]),
                  opacidadeVento.animate.set_value(0.4),
                  velocidadeVento.animate.set_value(10),
                  run_time=1.5
                  )
        
        allLinhasE[2].set_stroke(opacity=1)
        allLinhasD[2].set_stroke(opacity=1)
        self.play(Write(nodesE), Write(nodesD), Write(nodeCentral), Write(palavraChave),
                  opacidadeVento.animate.set_value(0),
                  velocidadeVento.animate.set_value(4.5), run_time = 0.5)
        self.wait(2)
        if palavra != "Aprofundado":
            allLinhasFinais.set_stroke(opacity=1)
            self.play(AnimationGroup(Create(ultimasLinhasD), Create(ultimasLinhasE), Create(ultimaLinhaCentral), run_time=0.5),
                    self.camera.frame.animate.shift([0,-15,0]),
                    allLinhasFinais.animate.shift([0,0,0]),
                    opacidadeVento.animate.set_value(0.4),
                    velocidadeVento.animate.set_value(15),
                    run_time=1.8)
            self.play(
                    velocidadeVento.animate.set_value(30))
            self.camera.frame.move_to(originalPos)
            self.remove(*[mobj for mobj in self.mobjects])
            
        else:
            logo.shift([0,-1,0])
            self.play(self.camera.frame.animate.scale(0.001), run_time=1.2)
            self.remove(*[mobj for mobj in self.mobjects if(self.mobjects) != logo])
            self.add(logo)
            logo.shift([0,-1,0])
            self.wait(0.5)
            self.play(self.camera.frame.animate.scale(1000),
                      logo.animate.shift([0,-0.2,0]),
                      run_time=1.2)
            self.wait()

    def construct(self):
        #Preparando vento
        vento = VGroup(*[
                 Line(UP,
                 DOWN,
                 stroke_width=2,
                 stroke_opacity = 0,
                 color=GREY).scale(random.uniform(0.5, 1))
                 .move_to([random.uniform(-7, 7), random.uniform(4, -22), 0]) for _ in range(50)])
        
        vento.add_updater(self.windUpdater)
        global velocidadeVento
        global opacidadeVento
        velocidadeVento = ValueTracker(5)
        opacidadeVento = ValueTracker(0)
        logo = SVGMobject("svgs\\comando").move_to([0,1.25,0]).scale(2)
        titulo = Text("comando.c", font="Major Mono Display").shift([0,-2.2,0]).scale(0.8)
        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 1.1,
            width = 0.5,
        ).scale(.5).move_to(titulo[0])

        self.next_slide(loop=True)
        self.add(logo)
        self.add(titulo)
        self.play(TypeWithCursor(titulo, cursor))
        self.play(Blink(cursor, blinks=2))
        #Dinâmico, Open Source, Qualidade, Aprofundado
        originalPos = self.camera.frame.get_center()
        for palavra in ["inicio","Dinâmico", "Open Source", "Aprofundado"]:
            self.add(vento)

            if palavra != "inicio":
                self.cenaRepetida(palavra, logo)
            else:
                self.play(opacidadeVento.animate.set_value(0.4))
                self.play(
                    self.camera.frame.animate.shift([0,-15,0]),
                    opacidadeVento.animate.set_value(0.4),
                    velocidadeVento.animate.set_value(15),
                    run_time=1.8)
                self.play(
                    velocidadeVento.animate.set_value(30))
                self.remove(logo)
                self.remove(titulo)
                titulo.set_opacity(0)
                self.camera.frame.move_to(originalPos)
        self.next_slide()
        