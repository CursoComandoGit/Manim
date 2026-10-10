from manim import *
from manim import UpdateFromFunc
MarkupText.set_default(font = "Trade Gothic")
PATH_COLOR = "#aa77c7"
BG_COLOR = "#0D0D1A"

#config.background_color="#1E1E1E"
Text.set_default(font = "Trade Gothic")

class AulaCompleta(MovingCameraScene):
    def construct(self):
          LinkedinParte1.construct(self)
          Rotatoria.construct(self)
          LogodaUTF.construct(self)
          CenaFinal.construct(self)

class LinkedinParte1(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BG_COLOR
        logo_svg = SVGMobject("assets/logoComando.svg").scale(1.5).move_to(ORIGIN)
        
        self.play(Write(logo_svg))
        self.play(logo_svg.animate.shift(UP*0.7))        
        comando = MarkupText('<b>comando.c</b>', font="Major Mono Display").next_to(logo_svg, DOWN, buff=0.1).scale(0.6)

        path = [
            np.array([0.000,  -2.000, 0.0]),# inicio do ponto q aparece na tela
            np.array([0.000, -8.000, 0.0]), 
            np.array([0.907, -8.707, 0.0]),# pausa aqui i=1
            np.array([0.907, -14.707, 0.0]),
            np.array([0.000, -15.414, 0.0]),# pausa aqui i=3
            np.array([0.000, -21.414, 0.0]),
            np.array([0.907, -22.121, 0.0])# pausa aqui i=5
        ] # path que será percorrido

        guia = VGroup(*[
            Line(path[i], path[i + 1])
            .set_color(PATH_COLOR)
            .set_stroke(width=1.5, opacity=0.15)
            for i in range(len(path) - 1)
        ])
        self.add(guia)

        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 1.1,
            width = 0.5
        ).move_to(comando[0]).scale(0.3)

        self.play(TypeWithCursor(comando, cursor))
        self.play(Blink(cursor, blinks=1))
        self.remove(cursor)
        self.wait(0.6)

        ponto = Dot(color=PATH_COLOR, radius=0.13)
        brilho = ponto.copy().scale(2).set_opacity(0.18)
        traveller = VGroup(brilho, ponto)
        traveller.move_to(path[0])
        self.add(traveller)

        # ------------------------animações em cada parada-----------------------
        primeira = MarkupText('<span><b>Qualidade</b> de ensino</span>', font_size=70).scale(0.7).next_to(path[2], RIGHT, buff=0.6)
        capelo = ImageMobject("assets/capelo.png").scale(0.6).next_to(primeira, UP, buff=0.1)
        a1 = Group(primeira, capelo)

        segunda = MarkupText('<span><b>Democratização</b>\ndo Conhecimento</span>', font_size=70).scale(0.7).next_to(path[4], LEFT, buff=0.6)
        pessoas = ImageMobject("assets/grupopessoas.png").scale(0.6).next_to(segunda, UP, buff=0.1)
        a2=Group(segunda, pessoas)

        terceira = MarkupText('<span><b>Fidelidade</b> ao\nconhecimento técnico</span>', font_size=70).scale(0.7).next_to(path[6], RIGHT, buff=0.6)
        livro = SVGMobject("assets/livro.svg").next_to(terceira, UP, buff=0.4)
        lampada = SVGMobject("assets/lampada.svg").scale(1.2).next_to(terceira, UP, buff=0.4)
        engrenagem = SVGMobject("assets/engrenagem.svg").scale(0.6).next_to(terceira, UP, buff=0.4)

        lampada.shift(UP*0.5)
        lampada.shift(RIGHT*1.2)
        
        engrenagem.shift(DOWN*0.2)
        engrenagem.shift(LEFT*1.4)
        
        a3 = Group(terceira, livro, lampada)
        #-------------------------------------------------------------------------

        offset = 0 # ajusta câmera em relação ao traveller

        def follow_camera(m):
            m.move_to(traveller.get_center() + offset)

        self.play(
            self.camera.frame.animate.move_to(traveller.get_center() + offset),
            run_time=0.3,
            rate_func=linear
        )
        for i in range(len(path) - 1):
            inicio = path[i]
            fim = path[i+1]

            dist = np.linalg.norm(fim - inicio)
            tempo = dist * 0.15 # percorre 1 unidade de distância do path em 0.3s

            seg = Line(inicio, fim).set_color(PATH_COLOR).set_stroke(width=4)

            self.play(
                MoveAlongPath(traveller, Line(inicio, fim)),
                UpdateFromFunc(self.camera.frame, follow_camera),
                Create(seg),
                run_time=tempo,
                rate_func=linear
            )

            if i in [1, 3, 5]:
                

                if i == 1:
                    self.play(
                        FadeIn(primeira),
                        SpinInFromNothing(capelo),
                        self.camera.frame.animate.move_to(a1),
                        run_time=1
                    )
                    self.play(Circumscribe(primeira, color="#5CE1E6", buff=0.1))
                    self.wait(0.5)
                    
                    #calcula o novo offset
                    offset = self.camera.frame.get_center() - traveller.get_center()
                elif i == 3:
                    self.play(
                        FadeIn(segunda),
                        SpinInFromNothing(pessoas),
                        self.camera.frame.animate.move_to(a2),
                        run_time=1
                    )
                    self.play(Circumscribe(segunda, color="#5CE1E6", buff=0.1))
                    self.wait(0.5)

                    #calcula o novo offset
                    offset = self.camera.frame.get_center() - traveller.get_center()
                elif i == 5:
                    self.play(
                        FadeIn(terceira),
                        SpinInFromNothing(livro),
                        FadeIn(lampada),
                        FadeIn(engrenagem),
                        self.camera.frame.animate.move_to(a3),
                        run_time=1
                    )
                    self.play(Circumscribe(terceira, color="#5CE1E6", buff=0.1))
                    self.wait(0.5)

                    #calcula o novo offset
                    offset = self.camera.frame.get_center() - traveller.get_center()

        # Aqui começa a parte DOIS, mas eu retirei a classe por questão de interoperabilidade
        # ----- Objetos ------
        # Ai a câmera se move para cima desse objeto
        textPresenca = Text("Marcamos presença nas plataformas",
                            color="#1E1E1E",
                            t2c={"presença":"#AA77C7","plataformas":"#58C4DD"}).move_to((20,1,0))
        
        # Agora aqui vai ser definido um monte de svg (amooooo)
        svgDiscord = SVGMobject("./assets/discord.svg").move_to((15.5,-6,0)).scale(0.7)
        svgInstagram = SVGMobject("./assets/instagram.svg").move_to((18.5,-6,0)).scale(0.7)
        svgLinkedin = SVGMobject("./assets/linkedin.svg").move_to((21.5,-6,0)).scale(0.7)
        svgYoutube = SVGMobject("./assets/youtube.svg").move_to((24.5,-6,0)).scale(0.7)

        # ----- Animações -----
        self.camera.frame.save_state()
        # Antes
        self.wait()
        
        # Algumas limpezas
        self.remove(primeira,segunda, capelo)
        self.wait()
        
        # A câmera se move
        self.play(self.camera.frame.animate.move_to(textPresenca),
                  lampada.animate.move_to(textPresenca))
        self.play(lampada.animate.scale(2))
        
        
        # Cria o bg e faz ele SEGUIR a câmera
        bg = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=BG_COLOR,      # começa com a cor atual
            fill_opacity=1,
            stroke_width=0,
        ).set_z_index(-100)


        # Faz o retângulo sempre ficar no centro do frame da câmera
        bg.add_updater(lambda m: m.move_to(self.camera.frame.get_center()))
        self.add(bg)


        # Agora a transição funciona mesmo com câmera se movendo
        self.play(
            bg.animate.set_fill("#ece6e2"),  # cor destino
            run_time=2,
            rate_func=smooth,
        )

        # Lampada some
        self.play(ShrinkToCenter(lampada))

        # Presenca
        self.play(Write(textPresenca))

        # Logos
        self.play(textPresenca.animate.shift(UP),
                  svgDiscord.animate.move_to((15.5,0,0)),
                  svgInstagram.animate.move_to((18.5,0,0)),
                  svgLinkedin.animate.move_to((21.5,0,0)),
                  svgYoutube.animate.move_to((24.5,0,0)))
        self.wait()

        # Destroi tudo
        self.play(self.camera.frame.animate.shift(DOWN*10))
        #self.remove(textExemplo)
        self.clear()
        
        
        self.camera.frame.move_to(ORIGIN)
        self.camera.frame.set_width(config.frame_width)
        
class Rotatoria(MovingCameraScene):
    def construct(self):
        # ----- Objetos ------

        # Equipe unida
        textEquipe1 = Text("Apresentamos resultados,",color="#1E1E1E",t2c={"resultados":"#AA77C7"}).move_to((0,0.5,0))
        textEquipe2 = Text("graças a uma equipe unida e dedicada:", color="#1E1E1E",t2c={"unida":"#58C4DD","dedicada":"#236B8E"}).move_to((0,-0.5,0))


        # Circulo (mais grosso) sendo criado
        circleBonito = Circle(stroke_width=20, color="#1E1E1E")
        
        # Diretoria
        textDiretoria = Text("Diretoria",color="#AA77C7").move_to((0,2.5,0)).scale(0.6)
        pathDiretoria = VMobject(color="#1E1E1E")
        dotDiretoria = Dot(color="#1E1E1E").move_to([0,1,0])

        pathDiretoria.set_points_as_corners([dotDiretoria.get_center(), dotDiretoria.get_center()])

        def update_path(path):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dotDiretoria.get_center()])
                path.become(previous_path)
        pathDiretoria.add_updater(update_path)



        # Tesouraria
        textTesouraria = Text("Tesouraria",color="#58C4DD").move_to((3.2,1.2,0)).scale(0.6)
        pathTesouraria = VMobject(color="#1E1E1E")
        dotTesouraria = Dot(color="#1E1E1E").move_to([0.7,0.7,0])

        pathTesouraria.set_points_as_corners([dotTesouraria.get_center(), dotTesouraria.get_center()])

        def update_path(path):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dotTesouraria.get_center()])
                path.become(previous_path)
        pathTesouraria.add_updater(update_path)


        # Desenvolvimento
        textDesenvolvimento = Text("Desenvolvimento",color="#236B8E").move_to((4,-1.2,0)).scale(0.6)
        pathDesenvolvimento = VMobject(color="#1E1E1E")
        dotDesenvolvimento = Dot(color="#1E1E1E").move_to([0.7,-0.7,0])

        pathDesenvolvimento.set_points_as_corners([dotDesenvolvimento.get_center(), dotDesenvolvimento.get_center()])

        def update_path(path):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dotDesenvolvimento.get_center()])
                path.become(previous_path)
        pathDesenvolvimento.add_updater(update_path)

        # Conteudo
        textConteudo = Text("Conteúdo",color="#AA77C7").move_to((0,-2.5,0)).scale(0.6)
        pathConteudo = VMobject(color="#1E1E1E")
        dotConteudo = Dot(color="#1E1E1E").move_to([0,-1,0])

        pathConteudo.set_points_as_corners([dotConteudo.get_center(), dotConteudo.get_center()])

        def update_path(path):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dotConteudo.get_center()])
                path.become(previous_path)
        pathConteudo.add_updater(update_path)

        # Produtos
        textProdutos = Text("Produtos",color="#236B8E").move_to((-3.2,-1.2,0)).scale(0.6)
        pathProdutos = VMobject(color="#1E1E1E")
        dotProdutos = Dot(color="#1E1E1E").move_to([-0.7,-0.7,0])

        pathProdutos.set_points_as_corners([dotProdutos.get_center(), dotProdutos.get_center()])

        def update_path(path):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dotProdutos.get_center()])
                path.become(previous_path)
        pathProdutos.add_updater(update_path)

        # Eem
        textEem1 = Text("Estratégia e",color="#58C4DD").move_to((-3.3,1.4,0)).scale(0.6)
        textEem2 = Text("Marketing",color="#58C4DD").move_to((-3.3,0.9,0)).scale(0.6)

        pathEem = VMobject(color="#1E1E1E")
        dotEem = Dot(color="#1E1E1E").move_to([-0.7,0.7,0])

        pathEem.set_points_as_corners([dotEem.get_center(), dotEem.get_center()])

        def update_path(path):
                previous_path = path.copy()
                previous_path.add_points_as_corners([dotEem.get_center()])
                path.become(previous_path)
        pathEem.add_updater(update_path)



        
        


        # ----- Animações -----
        self.camera.frame.save_state()
        self.camera.background_color = "#ece6e2"

        self.play(Write(textEquipe1))
        self.wait()
        self.play(Write(textEquipe2))
        self.wait()
        self.play(textEquipe1.animate.move_to((-20,0.5,0)),textEquipe2.animate.move_to((-20,-0.5,0)))

        self.play(Create(circleBonito))

        # Flecha diretoria
        self.add(pathDiretoria, dotDiretoria)
        self.play(dotDiretoria.animate.shift(UP),run_time=0.5)
        self.play(Write(textDiretoria),run_time=0.5)

        # Flecha tesouraria + Eem
        self.add(pathTesouraria, dotTesouraria, pathEem, dotEem)
        self.play(dotTesouraria.animate.shift((UP+RIGHT)*0.5), dotEem.animate.shift((UP+LEFT)*0.5), run_time=0.5)
        self.play(dotTesouraria.animate.shift((RIGHT)*0.8),dotEem.animate.shift((LEFT)*0.8),run_time=0.5)
        self.play(Write(textTesouraria),Write(textEem1),run_time=0.5)
        self.play(Write(textEem2),run_time=0.5)

        # Flecha Eem
        #self.add()
        #self.play(),run_time=0.5)
        #self.play(,run_time=0.5)
        #self.play(,run_time=0.5)
        

        # Flecha Desenvolvimento + Produtos
        self.add(pathDesenvolvimento, dotDesenvolvimento, 
                 pathProdutos, dotProdutos)
        self.play(dotDesenvolvimento.animate.shift((DOWN+RIGHT)*0.5),
                  dotProdutos.animate.shift((DOWN+LEFT)*0.5),
                  run_time=0.5)
        self.play(dotDesenvolvimento.animate.shift((RIGHT)*0.8),
                  dotProdutos.animate.shift((LEFT)*0.8),run_time=0.5)
        self.play(Write(textDesenvolvimento),
                    Write(textProdutos),
                    run_time=0.5)

        # Flecha Produtos
        #self.add(pathProdutos, dotProdutos)
        #self.play(dotProdutos.animate.shift((DOWN+LEFT)*0.5),run_time=0.5)
        #self.play(dotProdutos.animate.shift((LEFT)*0.8),run_time=0.5)
        #self.play(Write(textProdutos),run_time=0.5)
        
        # Flecha Conteudo
        self.add(pathConteudo, dotConteudo)
        self.play(dotConteudo.animate.shift(DOWN),run_time=0.5)
        self.play(Write(textConteudo),run_time=0.5)


        

        

        
        self.wait()

        self.play(self.camera.frame.animate.shift(DOWN*10))

        # Destroi turu e toros
        self.remove(textEquipe1, textEquipe2,
                    circleBonito,
                
                # Diretoria
                textDiretoria, pathDiretoria, dotDiretoria,
                
                # Tesouraria
                textTesouraria, pathTesouraria, dotTesouraria,
                
                # Desenvolvimento
                textDesenvolvimento, pathDesenvolvimento, dotDesenvolvimento,
                
                # Conteudo
                textConteudo, pathConteudo, dotConteudo,
                
                # Produtos
                textProdutos, pathProdutos, dotProdutos,
                
                # Eem
                textEem1, textEem2, pathEem, dotEem
                )
        
        self.play(Restore(self.camera.frame))
        
class LogodaUTF(MovingCameraScene):
    def construct(self):
        # ----- Objetos ------
        textComputacao = Text("Um projeto de computação",color="#1E1E1E",t2c={"computação":"#AA77C7"}).move_to((-1.6,1,0))
        textUTF = Text("da UTFPR",color="#1E1E1E",t2c={"UTFPR":"#ABAB3F"}).next_to(textComputacao, RIGHT, buff=0.2).shift(UP*0.07)
        #.move_to((4.5,1.4,0))
        imageUTF = ImageMobject("./assets/utfpr.png").move_to((0,-1,0))
        


        # ----- Animações ------
        self.camera.background_color = "#ece6e2"
        self.camera.frame.save_state()

        # Abracadabra
        self.play(Write(textComputacao))
        self.wait()
        self.play(Write(textUTF))
        self.wait()
        self.play(FadeIn(imageUTF))
        self.wait()

        # Câmera desce para ver a cena final
        self.play(self.camera.frame.animate.shift(DOWN*10))
        self.remove(textComputacao,textUTF,imageUTF)
        self.play(Restore(self.camera.frame))

class CenaFinal(Scene):
    def construct(self):
        # ----- Objetos ------
        textComando = Text("Você é que está no comando!",color="#1E1E1E",t2c={"Você":"#236B8E","comando":"#AA77C7"}).move_to((1,0,0)).scale(0.8)
        
        svgComando = SVGMobject("./assets/comando.svg")

        # ----- Animações ------
        self.camera.background_color = "#ece6e2"

        self.play(SpinInFromNothing(svgComando))
        self.play(svgComando.animate.move_to((-4,0,0)))
        self.play(Write(textComando))
        self.wait()
        self.wait()

        self.play(Unwrite(textComando),ShrinkToCenter(svgComando),run_time=1.5)

        self.wait()
