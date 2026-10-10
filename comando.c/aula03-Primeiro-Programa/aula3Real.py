from manim import *
from customTerminal import CustomTerminal
from crack import Crack
import random

def fix_cap(mob):
    for m in mob.family_members_with_points():
        m.set_cap_style(CapStyleType.BUTT)
    return mob

def TX(texto, **kwargs):
    return fix_cap(Text(texto, **kwargs))


def T(texto, **kwargs):
    return fix_cap(Tex(texto, **kwargs))
class Part1(Scene): #Essa aula é o último teste com updaters para uma cena só. Na próxima separarei em diferentes classes
    config.background_color = "#1E1E1E"
    Text.set_default(font = "Manrope")
    #Updater para scale
    #com interpolação
    def modifyTerminal(self, mob , alpha):
        target_width = interpolate(mob.sizeX, mob.newWidth, alpha)
        target_height = interpolate(mob.sizeY, mob.newHeight, alpha)
        mob.resize_terminal(new_width = target_width, new_height = target_height)

    def grow_until_target(self, mob, dt): #altura final é const
            if mob.height < 0.3:
                mob.scale(1 + 4.0 * dt) #porcentagem de crescimento
            if mob.height > 0.3:
                mob.height = 0.3
    #Caixinha (agora so texto)
    def physics_updater(self, obj, dt):
        if not 0 < dt < 0.1: #Check para ver se deltaTime foi interrompido
            return
        if obj.active == False: #Matar animação
            return
        
        obj.velocity= obj.velocity + obj.gravity * dt 

        obj.shift(obj.velocity * dt) #aplicando transformacao com deltaTime
        box_half_width= obj.width / 2
        box_half_height= obj.height / 2
        #Começo de verificação de colisão e aplicando bounce
        if obj.get_right()[0] >= config.frame_width/2:
            obj.set_x(config.frame_width/2 - box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_left()[0] <= -config.frame_width/2:
            obj.set_x(-config.frame_width/2 + box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_top()[1] >= config.frame_height/2:
            obj.set_y(config.frame_height/2 - box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping
        if obj.get_bottom()[1] <= -config.frame_height/2:
            obj.set_y(-config.frame_height/2 + box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping

    #----Funções de animação----

    def codigoLivroCarta(self):
        tituloCodigo = Text(
            "Código é texto",
            t2c={"texto": PURPLE},
            font_size=80
        ).scale(0.5)

        tituloCodigo.move_to([0,3,0])

        blocoNotas = ImageMobject("images/blocoNotas.png").scale(1.5).shift(DOWN * 0.4)

        textoNotasComp = Text(
            '#include <stdio.h>\n'
            'int main() {\n'
            '    int v[5] = {10, 20, 30, 40, 50};\n'
            '    printf("Original: ");\n'
            '    for(int i = 0; i < 5; i++) {\n'
            '        printf("%d ", v[i]);\n'
            '    }\n'
            '\n'
            '    printf("\\nInvertido: ");\n'
            '    for(int i = 4; i >= 0; i--) {\n'
            '        printf("%d ", v[i]);\n'
            '    }\n'
            '\n'
            '    return 0;\n'
            '}', font_size = 80, color = "#000000", line_spacing = 0.8
        ).scale(0.15)

        textoNotasComp.move_to(blocoNotas.get_center())
        textoNotasComp.shift(LEFT*1.25, DOWN*0.32)

        # carta, livro, codigo-fonte
        ApenasTextoComp = Text(
            "Tudo é texto",
            t2c={"texto": PURPLE}, 
            font_size=80
        ).scale(0.5)
        ApenasTextoComp.move_to([0,3,0])

        carta = ImageMobject("images/carta.png").scale(0.5)
        livro = ImageMobject("images/livro.png").scale(0.5)
        codigo = ImageMobject("images/coding.png").scale(0.5)

        igual1 = Text("=", font_size = 90).scale(1)
        igual2 = Text("=", font_size = 90).scale(1)

        grupo = Group(codigo, igual1, carta, igual2, livro)
        grupo.arrange(RIGHT, buff=1.0)
        grupo.move_to(ORIGIN)

        # linguagem de programacao vs linguagem humana
        tituloTexto = Text("Texto", font_size=80).scale(0.5)
        tituloCode = Text("Código", font_size=80).scale(0.5)

        tituloCode.align_to(tituloTexto, DOWN)
        grupo2 = VGroup(tituloTexto, tituloCode).arrange(RIGHT, buff=1)
        grupo2.move_to([0,3,0])

        seta = Arrow(tituloTexto.get_right(), tituloCode.get_left(), buff = 0.1, color=PURPLE)

        aprender1 = Text("Se o usuário demonstra interesse em C, iniciamos sua trilha", font_size = 80).scale(0.35)
        aprender2 = Text("de aprendizado e começamos pelos fundamentos.", font_size = 80).scale(0.35)
        condicaoAprender = VGroup(aprender1, aprender2).arrange(DOWN, aligned_edge = LEFT, buff = 0.3)

        codeAprender = '''if (usuario->quer_aprender_c) {
    iniciar_trilha("C");
    usuario->nivel = 1;
    printf("Fundamentos iniciados...");
}'''
        rendered_codeAprender = Code(
            code_string = codeAprender, 
            language = "c", 
            formatter_style = "monokai", 
            background = "rectangle", 
            background_config = {"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}).scale(1) 


        word = ImageMobject("images/docWord.png").shift(DOWN * 0.4)

        textoWord = Text(
            'if (usuario->quer_aprender_c) {\n'
            '    iniciar_trilha("C");\n'
            '    usuario->nivel = 1;\n'
            '    printf("Fundamentos iniciados...");\n'
            '}', font_size=80, color="#000000", line_spacing=0.8
        ).scale(0.15)
        
        textoWord.move_to(word.get_center())
        textoWord.shift(LEFT * 0.5)

        # codigo no bloco de notas
        self.play(Write(tituloCodigo))
        self.play(FadeIn(blocoNotas))
        self.play(AddTextLetterByLetter(textoNotasComp), run_time = 2.5)
        self.play(FadeOut(tituloCodigo),FadeOut(blocoNotas), FadeOut(textoNotasComp))
        self.wait()


        self.play(Write(ApenasTextoComp))
        self.play(
            LaggedStart(
                FadeIn(codigo),
                Write(igual1),
                FadeIn(carta),
                Write(igual2),
                FadeIn(livro),
                lag_ratio=0.5
            ), run_time = 1.6
        )

        self.play(FadeOut(ApenasTextoComp), FadeOut(codigo), FadeOut(igual1), FadeOut(carta), FadeOut(igual2), FadeOut(livro), run_time = 1)

        self.play(
            LaggedStart(
                Write(tituloTexto),
                GrowArrow(seta),
                Write(tituloCode),
                lag_ratio=0.3
            )
        )
        self.play(AddTextLetterByLetter(aprender1), run_time = 1.5)
        self.play(AddTextLetterByLetter(aprender2), run_time = 1.5)
        self.wait(0.5)

        self.play(FadeOut(condicaoAprender))
        self.play(Write(rendered_codeAprender))
        self.play(Unwrite(tituloTexto), Uncreate(seta), Unwrite(tituloCode))
        self.play(rendered_codeAprender.animate.scale(0.6).move_to([0,3,0]))
        self.play(FadeIn(word))
        self.play(rendered_codeAprender.animate.shift(DOWN * 2), TransformMatchingShapes(rendered_codeAprender, textoWord))
        self.wait()
        self.play(FadeOut(textoWord), FadeOut(word), run_time = 1)
        self.wait()


    def introComando(self):
        logoComando = SVGMobject("svgs/comando.svg").scale(2)
        comando = Text("comando.c", font="Major Mono Display").shift(2*DOWN).scale(0.8)
        cursor = Rectangle(
            color = GREY_A,
            fill_color = GREY_A,
            fill_opacity = 1.0,
            height = 1.1,
            width = 0.5,
        ).scale(0.5).move_to(comando[0])
        self.play(Write(logoComando), run_time=2)
        self.play(logoComando.animate.shift(0.5*UP))
        self.play(TypeWithCursor(comando, cursor), run_time=1.5)
        self.play(Blink(cursor, blinks=2))
        self.wait()
        self.clear()

    
    def configurandoAmbiente(self):
        text = Text("Configurando seu", font_size = 45)
        text2 = Text("ambiente de programação", color = PURPLE, font_size=50)

        acronym = Tex("{{I}}{{D}}{{E}}")
        acronym.font_size = 128
        acronym.set_color(PURPLE)
        fullText = Tex("{{I}}ntegrated {{D}}evelopment {{E}}nvironment")

        # trocar a cor das iniciais para roxo
        fullText.set_color_by_tex("I", PURPLE)
        fullText.set_color_by_tex("D", PURPLE)
        fullText.set_color_by_tex("E", PURPLE)

        codeblocks = SVGMobject("svgs\\codeblocks")
        eclipse = SVGMobject("svgs\\eclipseide")
        pycharm = SVGMobject("svgs\\pycharm")
        mvs = SVGMobject("svgs\\visualstudio").scale(0.75)

        delphi = SVGMobject("svgs\\delphi")
        intellij = SVGMobject("svgs\\intellij")
        webstorm = SVGMobject("svgs\\webstorm")
        netbeans = SVGMobject("svgs\\netbeans")


        ide = VGroup(pycharm, mvs, eclipse, codeblocks)
        top = VGroup(mvs, intellij, webstorm, pycharm).arrange(RIGHT, buff=1)
        bottom = VGroup(eclipse, netbeans, codeblocks, delphi).arrange(RIGHT, buff=1)
        retirarIDEs= VGroup(intellij, webstorm, netbeans, delphi)

        text2Group = VGroup(VGroup(letter for letter in text2[:8]),
                            VGroup(letter for letter in text2[8:10]),
                            VGroup(letter for letter in text2[10:]))
        
        rawTitle = VGroup(text, text2).arrange(DOWN, aligned_edge = LEFT, buff = 0.2)

        #Adicionando "ferramentas desnecessárias" e ajustando parâmetros
        #Ainda to devendo de criar uma classe para esse bgl
        globalGravity = np.array([0, -9.8, 0])
        iaText = Text("Agentes de IA", font_size=78).scale(0.4)
        iaText.velocity = np.array([5.0, -1, 0]) #velocidade inicial
        iaText.gravity = globalGravity
        iaText.damping = 0.9
        iaText.active = True

        net = Text("Integração .NET", font_size=100).scale(0.2)
        net.velocity = np.array([-1.0, -2.0, 0]) #velocidade inicial
        net.gravity = globalGravity
        net.damping = 0.9
        net.active = True

        dataBase = Text("Integração com GIT", font_size=100).scale(0.2)
        dataBase.velocity = np.array([-1.0, 7.0, 0]) #velocidade inicial
        dataBase.gravity = globalGravity
        dataBase.damping = 0.9
        dataBase.active = True

        compilacao = Text("Compilador incremental", font_size=78).scale(0.1)
        compilacao.velocity = np.array([2.0, 8.0, 0]) #velocidade inicial
        compilacao.gravity = globalGravity
        compilacao.damping = 0.9
        compilacao.active = True

        debugger = Text("Debugger", font_size=78).scale(0.1)
        debugger.velocity = np.array([4.0, 3.0, 0]) #velocidade inicial
        debugger.gravity = globalGravity
        debugger.damping = 0.9
        debugger.active = True

        terminalInteg = Text("Terminal integrado", font_size=78).scale(0.1)
        terminalInteg.velocity = np.array([-7.0, 0, 0]) #velocidade inicial
        terminalInteg.gravity = globalGravity
        terminalInteg.damping = 0.9
        terminalInteg.active = True

        features = VGroup(iaText, net, dataBase, compilacao, debugger, terminalInteg)

        #Correção de svgs
        
        pycharm[0].set_color("#07C3F2")
        pycharm[1].set_color("#21D789")
        pycharm[2].set_color("#32DA84")
        pycharm[3].set_color("#CFE865")
        pycharm[4].set_color("#F1EB5E")

        eclipse[0].set_color("#2C2255")
        eclipse[1].set_color("#2C2255")
        eclipse[2].set_color("#F7941E")
        
        eclipse[3].set_color("#3E2F7F")
        eclipse[4].set_color("#5441A8")
        eclipse[5].set_color("#6A56C0")
        eclipse[6].set_color(WHITE)

        #Separando palavras e começando animação
        self.play(Write(rawTitle))
        self.wait()
        
        #Separando letras e apps
        self.play(AnimationGroup(FadeOut(text), FadeOut(text2Group[1]), run_time=0.4),
                  text2Group[0][2].animate.move_to([5,-1.5,0]).scale(0), #B
                  text2Group[0][4].animate.move_to([-5,-1.5,0]).scale(0), #E
                  text2Group[0][7].animate.move_to([-5,-1.5,0]).scale(0), #E
                  text2Group[0][3].animate.move_to([-2,-1.5,0]).scale(0), #I
                  text2Group[0][1].animate.move_to([-5,1,0]).scale(0), #M
                  text2Group[2][6].animate.move_to([-5,1,0]).scale(0), #M
                  text2Group[0][5].animate.move_to([-2,1,0]).scale(0), #N
                  text2Group[0][6].animate.move_to([2,1,0]).scale(0), #T
                  text2Group[2][0].animate.move_to([5,1,0]).scale(0), #P
                  text2Group[2][2].animate.move_to([0,0,0]).scale(0), #O
                  text2Group[2][10].animate.move_to([0,0,0]).scale(0), #O
                  text2Group[2][1].animate.move_to([0,0,0]).scale(0), #R
                  text2Group[2][4].animate.move_to([0,0,0]).scale(0), #R
                  text2Group[2][3].animate.move_to([0,0,0]).scale(0), #G
                  text2Group[0][0].animate.move_to([0,0,0]).scale(0), #A
                  text2Group[2][5].animate.move_to([0,0,0]).scale(0), #A
                  text2Group[2][7].animate.move_to([0,0,0]).scale(0), #A
                  text2Group[2][9].animate.move_to([0,0,0]).scale(0), #Ã
                  text2Group[2][8].animate.move_to([2,-1.5,0]).scale(0) #Ç
                  )
        
        logos = VGroup(
            top,
            bottom
        ).arrange(DOWN, buff=1)

        self.wait()

        #Escrevendo logos em cima
        self.play(Write(codeblocks), Write(eclipse), Write(netbeans), Write(mvs),
                  Write(intellij), Write(pycharm), Write(delphi), Write(webstorm), run_time=2)
        self.wait(3)
        
        #Fade em tudo que não saiu
        self.play(*[FadeOut(obj) for obj in self.mobjects])

        fullText.font_size = 80
        fullText[0].scale(1.1)
        fullText[2].scale(1.1)
        fullText[4].scale(1.1)
        fullText.scale(0.95)

        #Reposicionando ferramentas
        top.shift([-15, 1, 0]).scale(0.8)
        bottom.shift([15, -1, 0]).scale(0.8)
        #---Texto expandindo e ferramentas---
        self.wait()
        self.play(Write(acronym))
        self.wait()
        
        self.play(TransformMatchingTex(acronym, fullText))
        
        self.wait(2)
        self.play(fullText.animate.scale(0.6))
        self.play(
                  top.animate.shift([15,0,0]),
                  bottom.animate.shift([-15,0,0]),
                  rate_func = rate_functions.ease_out_back)
        self.wait()
        self.play(top.animate.move_to(ORIGIN).scale(0), bottom.animate.move_to(ORIGIN).scale(0),
                  TransformMatchingTex(fullText, acronym))
        self.remove(top, bottom)
        hand = SVGMobject("svgs\\hand").scale(0.6).move_to(acronym.get_right(), aligned_edge=LEFT).shift([0.6,0,0]).set_color(WHITE)
        extensions = Text("extension", font="Major mono display").scale(0.8).move_to(hand.get_top(), aligned_edge=DOWN).shift([0.8,0.2,0])

        self.play(FadeIn(hand, target_position=[-0.5,0,0]),
                  FadeIn(extensions, target_position=LEFT))
        self.wait()
        self.play(*[FadeOut(obj) for obj in self.mobjects])

    def editoresTexto(self):
        titulo = Text("Editores de texto")

        vim = SVGMobject("svgs\\vim")
        sublimeText = SVGMobject("svgs\\sublimetext")
        notePad = SVGMobject("svgs\\notepad")
        vscode = SVGMobject("svgs\\vscode")
        editors = VGroup(vim, sublimeText, notePad, vscode).scale(0.9)

        caixa1 = RoundedRectangle(corner_radius=0.5, color = BLUE,
                          fill_opacity=0.1,height=2.0,width=8.0).move_to([0,0,-1])
        caixa2 = RoundedRectangle(corner_radius=0.5, color = BLUE,
                          fill_opacity=0.1,height=2.0,width=2.5)

        vscode[0].set_color("#32B5F1")
        vscode[1].set_color("#0E69AC")
        vscode[2].set_color("#0F6FB3")
        sublimeText[0].set_color("#D06F00")
        vim[0].set_color("#019833")
        vim[10].set_color("#049A20")

        for elements in notePad[:11]:
            elements.set_color(WHITE)

        titulo.move_to([0,3,0])
        editors.arrange(direction=RIGHT, buff=0.8)
        
        #Editores aparecem, destaque em vs code
        self.play(Write(titulo), run_time = 1.5)
        self.play(Write(editors), run_time=2)
        self.wait(1)
        
        self.play(editors.animate.shift([0,-0.5,0]))
        caixa1.move_to(editors.get_center())
        self.play(editors.animate.scale(0.8), Create(caixa1))
        
        self.play(Wiggle(vim, run_time=0.8))
        self.play(Wiggle(sublimeText, run_time=0.8))
        self.play(Wiggle(notePad, run_time=0.8))
        self.play(Wiggle(vscode, run_time=0.8))
        self.wait()
        
        self.play(FadeOut(vim, sublimeText, notePad), run_time=0.6)
        self.play(vscode.animate.move_to([0,-0.5,0]),
                  Transform(caixa1, caixa2.move_to([0,-0.5,0])))
        self.wait()
        
        #Nao precisa desse segmento
        # tem que ser na caixa1, porque não foi feita uma copia da caixa2 no Transform
        #self.play(Uncreate(caixa1), run_time = 0.5)
        #self.play(vscode.animate.move_to(ORIGIN))
        #self.play(vscode.animate.scale(1.6))

        #Fade em tudo que não saiu
        self.play(*[FadeOut(obj) for obj in self.mobjects])
        self.wait()

    def posInstalacao(self):
        # text = Text(
        #     "Configurando um ambiente de programação:",
        #     t2c={"ambiente": PURPLE},
        #     font_size = 45
        # )

        # text.move_to[0,-3,0]

        terminal = ImageMobject("images/terminal.png")
        compilador = ImageMobject("images/compilador.png")
        vscode = ImageMobject("images/vscode.png")

        vscodeGroup = Group(vscode, Text("Editor de texto", font_size = 80).scale(0.3))
        vscodeGroup[1].next_to(vscode, UP, buff = 0.2)
        vscodeGroup[1].align_to(vscode, ORIGIN) # centraliza no meio horizontal

        compiladorGroup = Group(compilador, Text("Compilador", font_size = 80).scale(0.3))
        compiladorGroup[1].next_to(compilador, UP, buff = 0.1)
        compiladorGroup[1].align_to(compilador, ORIGIN) 

        terminalGroup = Group(terminal, Text("Terminal", font_size = 80).scale(0.3))
        terminalGroup[1].next_to(terminal, UP, buff = 0.1)
        terminalGroup[1].align_to(terminal, ORIGIN)

        imsGroup = Group(vscodeGroup, compiladorGroup, terminalGroup)
        imsGroup.arrange(direction=RIGHT, buff=0.8)

        # check (editor de texto já instalado)
        check = VGroup(
            Line([-0.2, -0.3, 0], [0.1, -0.6, 0], cap_style = CapStyleType.ROUND),   # perna curta
            Line([0.1, -0.6, 0], [0.6, 0, 0], cap_style = CapStyleType.ROUND)      # perna longa
        ).set_color(GREEN).set_stroke(width=10)

        check.set_cap_style(CapStyleType.ROUND)
        check.next_to(vscode, DOWN, buff = 0.3)

        #Riscando
        # self.play(Write(text))
        

        self.play(GrowFromCenter(vscodeGroup[0]),
                GrowFromCenter(compiladorGroup[0]),
                GrowFromCenter(terminalGroup[0])
        )

        self.play(Wiggle(vscodeGroup[0]), run_time = 0.8)
        self.play(Wiggle(compiladorGroup[0]), run_time = 0.8)
        self.play(Wiggle(terminalGroup[0]), run_time = 0.8)

        self.play(
                FadeIn(vscodeGroup[1], shift=UP*0.2),
                FadeIn(compiladorGroup[1], shift=UP*0.2),
                FadeIn(terminalGroup[1], shift=UP*0.2)
        )
        self.wait(0.5)
        self.play(Create(check), run_time = 0.3)
        self.wait(2)
        self.play(Uncreate(check), run_time = 0.3)

        #Fade em tudo que não saiu
        self.play(*[FadeOut(obj) for obj in self.mobjects], run_time = 0.5)

    def linuxEWindows(self):
        sample = "1. Estabilidade; 2. Confiabilidade; 3. Flexibilidade; 4. Servidores rodam linux; 5. Customização; 6. Segurança; 7. Privacidade; 8. Open Source; 9. Compatibilidade; 10. Portabilidade; 11. Performance; 12. Escalabilidade; 13. Ambiente de Desenvolvimento Nativo; 14. “Scriptable”; 15. Gerenciador de Pacotes"
        sample = sample.split(';')
        linux = SVGMobject("svgs\\linux").move_to([-1,0,0]).scale(1.2)
        windows = SVGMobject("svgs\\windows").scale(0.8).shift([9.8,0,0])
        linuxBeneficios = VGroup(*[Text(texto, fill_opacity=0, font_size=75).scale(1/3) for texto in sample])
        linuxBeneficiosVisivel = VGroup(*[Text(texto, font_size=75).scale(1/3) for texto in sample])
        linuxBeneficios.arrange(DOWN, buff=0.2, aligned_edge = LEFT, center = False).move_to([-2.5,0,0])
        linuxBeneficiosVisivel.arrange(ORIGIN, buff=0.2, aligned_edge = LEFT, center=False).move_to([-12,0,0])
        #arrumando logo
        linux[0].set_color("#000000")
        #Cada elemento aparece individualmente
        self.add(linuxBeneficiosVisivel)
        i = 0
        while i < len(linuxBeneficios):
            self.play(linuxBeneficiosVisivel[i].animate.move_to(linuxBeneficios[i].get_center()), run_time=0.1)
            i+=1
        #Comparação
        self.play(GrowFromCenter(linux),
                  run_time = 0.65)
        self.wait()
        
        ###---Linux dando tiro no windows?---###

        #Fade em tudo que não saiu
        self.play(*[FadeOut(obj) for obj in self.mobjects])

    #Trocar pela da eduarda
    def separacao(self):
        linha1 = Line([-3,2,0], [-3,-2,0],  cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)
        linha2 = Line([3,2,0], [3,-2,0],  cap_style = CapStyleType.ROUND).set_stroke("#aa77c7", 20)

        linux = SVGMobject("svgs\\linux")
        mac = SVGMobject("svgs\\mac")
        windows = SVGMobject("svgs\\windows11")

        fix_cap(linux)
        fix_cap(mac)
        fix_cap(windows)

        winText1 = Text("Windows", font_size = 90).scale(0.5)
        winText2 = Text("Windows 11", font_size = 90).scale(0.5)

        linux[0].set_color("#000000")

        logos = VGroup(linux, windows, mac).arrange(buff=3)

        winText1.move_to(windows.get_center())
        winText2.move_to(windows.get_center())

        winText1.next_to(windows, DOWN, buff = 1)

        winText2.next_to(windows, DOWN, buff = 1)

        self.play(Create(linha1), Create(linha2))
        self.wait(0.5)
        self.play(Write(logos), run_time=1.45)
        self.wait()
        self.play(FadeOut(linha1), FadeOut(linha2), FadeOut(mac), FadeOut(linux))
        self.wait(0.6)
        self.play(windows.animate.scale(1.5))
        self.play(FadeIn(winText1))
        self.play(Transform(winText1, winText2))
        self.wait(2)
        #Why?
        cracks = VGroup(Crack(windows.get_center(), windows.get_corner([1,1,0])),
                        Crack(windows.get_center(), windows.get_corner([1,-1,0])),
                        Crack(windows.get_center(), windows.get_corner([-1,1,0])),
                        Crack(windows.get_center(), windows.get_corner([-1,-1,0])),
                        Crack(windows.get_center(), windows.get_corner([0.05,-0.75,0])))
        self.play(AnimationGroup(*[Create(crack) for crack in cracks], run_time=0.3), windows.animate.rotate(25).scale(1.1),
                  winText1.animate.shift([0,-0.75,0]), run_time=0.5)
        self.wait()
        self.play(FadeOut(winText1))
        self.play(ShrinkToCenter(windows), ShrinkToCenter(cracks), run_time = 0.5)
        self.clear()
        self.wait(1)

        ################################
        editor = Text("Editor pode separar aqui o do mac e o do linux")
        self.add(editor)
        self.wait(3)
        self.remove(editor)
        # animação focando no sistema operacional MAC OS
        windows = SVGMobject("svgs\\windows11")
        fix_cap(windows)

        logos = VGroup(linux, windows, mac).arrange(buff=3)

        macText1 = Text("mac", font_size = 90).scale(0.5)
        macText2 = Text("macOS", font_size = 90).scale(0.5)

        self.play(Create(linha1), Create(linha2))
        self.wait(0.5)
        self.play(Write(logos), run_time=1.45)
        self.wait()
        self.play(FadeOut(linha1), FadeOut(linha2), FadeOut(windows), FadeOut(linux))
        self.play(mac.animate.move_to(windows.get_center()))
        self.wait(0.6)
        self.play(mac.animate.scale(1.5))

        macText1.move_to(mac.get_center())
        macText2.move_to(mac.get_center())

        macText1.next_to(mac, DOWN, buff = 0.4)
        macText2.next_to(mac, DOWN, buff = 0.4)

        self.play(FadeIn(macText1))
        self.play(Transform(macText1, macText2))
        self.play(FadeOut(macText1))
        self.play(ShrinkToCenter(mac), run_time = 0.5)
        self.wait(1)

        # animação focando no sistema operacional LINUX™
        mac = SVGMobject("svgs\\mac")
        fix_cap(mac)

        logos = VGroup(linux, windows, mac).arrange(buff=3)

        linuxText1 = Text("LINUX", font_size = 90).scale(0.5)
        linuxText2 = Text("LINUX™", font_size = 90).scale(0.5)

        self.play(Create(linha1), Create(linha2))
        self.wait(0.5)
        self.play(Write(logos), run_time=1.45)
        self.wait()
        self.play(FadeOut(linha1), FadeOut(linha2), FadeOut(windows), FadeOut(mac))
        self.play(linux.animate.move_to(windows.get_center()))
        self.wait(0.6)
        self.play(linux.animate.scale(1.5))

        linuxText1.move_to(linux.get_center())
        linuxText2.move_to(linux.get_center())

        linuxText1.next_to(linux, DOWN, buff = 0.4)
        linuxText2.next_to(linux, DOWN, buff = 0.4)

        self.play(FadeIn(linuxText1))
        self.play(Transform(linuxText1, linuxText2))
        self.play(FadeOut(linuxText1))
        self.play(ShrinkToCenter(linux), run_time = 0.5)
        self.wait(1)

class Main(Scene):
    def physics_updater(self, obj, dt):
        if not 0 < dt < 0.1: #Check para ver se deltaTime foi interrompido
            return
        if obj.active == False: #Matar animação
            return
        
        obj.velocity= obj.velocity + obj.gravity * dt 

        obj.shift(obj.velocity * dt) #aplicando transformacao com deltaTime
        box_half_width= obj.width / 2
        box_half_height= obj.height / 2
        #Começo de verificação de colisão e aplicando bounce
        if obj.get_right()[0] >= config.frame_width/2:
            obj.set_x(config.frame_width/2 - box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_left()[0] <= -config.frame_width/2:
            obj.set_x(-config.frame_width/2 + box_half_width)
            obj.velocity[0]= -obj.velocity[0] * obj.damping
        if obj.get_top()[1] >= config.frame_height/2:
            obj.set_y(config.frame_height/2 - box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping
        if obj.get_bottom()[1] <= -config.frame_height/2:
            obj.set_y(-config.frame_height/2 + box_half_height)
            obj.velocity[1]= -obj.velocity[1] * obj.damping

    def grow_until_target(self, mob, dt): #altura final é const
            if mob.height < 0.3:
                mob.scale(1 + 4.0 * dt) #porcentagem de crescimento
            if mob.height > 0.3:
                mob.height = 0.3
    #---Trocada por edição.---
    def porqueUsasWindows(self):
        throne = SVGMobject("svgs\\throne").scale(1.1)
        linux = SVGMobject("svgs\\linux").set_z_index(2)
        crown = SVGMobject("svgs\\crown").set_z_index(3).scale(0.25).move_to(linux.get_top(), aligned_edge=DOWN)
        machine = SVGMobject("svgs\\maquina").scale(0.8)
        money = SVGMobject("svgs\\money").scale(0.8).move_to([5,-6,0])
        openLock = SVGMobject("svgs\\openLock").scale(0.8).move_to([5,6,0]).set_color(WHITE)
        closedLock = SVGMobject("svgs\\closedLock.svg").scale(0.8).set_color(WHITE)

        tcompilador = Text("Compilador", font_size=45).move_to(machine.get_bottom(), aligned_edge=UP).shift([0,-0.25,0])
        compilador = VGroup(machine, tcompilador).move_to([-5,6,0])
        msgErro = Text("Undeclared identifier 'varivel'", font_size=30,color=RED)
        sugestao = Text("Did you mean 'variavel'?", font_size=30,color=RED)

        linux[0].set_color("#000000")

        self.add(money)
        self.add(compilador)
        self.play(FadeIn(linux))
        self.wait()
        self.play(compilador.animate.move_to([-5,2.25,0]))
        msgErro.move_to(machine.get_right(), aligned_edge=LEFT).shift([0.25,0,0])
        sugestao.move_to(msgErro.get_center())

        self.play(Wiggle(machine, run_time=1), GrowFromPoint(msgErro, machine.get_center()))
        self.wait()
        self.play(Transform(msgErro, sugestao))
        self.wait()

        self.play(money.animate.move_to([5,-2.25,0]))
        cross = Cross(money, color=RED)
        self.play(Create(cross), FadeOut(msgErro))
        self.wait()

        stringKernel = ''' static int get_random_numbers(u8 *buf, unsigned int len)
{
    struct crypto_rngrng = NULL;
    chardrbg = "drbg_nopr_sha256"; /* Hash DRBG with SHA-256, no PR */
    int ret;
    if (!buf || !len) {
        pr_debug("No output buffer provided\n");
        return -EINVAL;
    }
    rng = crypto_alloc_rng(drbg, 0, 0);
    if (IS_ERR(rng)) {
        pr_debug("could not allocate RNG handle for %s\n", drbg);
        return -PTR_ERR(rng);
    }
    ret = crypto_rng_get_bytes(rng, buf, len);
    if (ret < 0)
        pr_debug("generation of random numbers failed\n");
    else if (ret == 0)
        pr_debug("RNG returned no data");
    else
        pr_debug("RNG returned %d bytes of data\n", ret);
out:
    crypto_free_rng(rng);
    return ret;
} '''
        kernelCode = Code(code_string=stringKernel, language="c", formatter_style="monokai", background="rectangle", background_config={"fill_color": "#4400FFFF", "stroke_color": "WHITE", "fill_opacity":0.1}).scale(0.25)
        kernelCode.move_to([-5,-2.25,0]).set_cap_style(CapStyleType.AUTO)
        self.play(Write(kernelCode))
        self.wait()

        self.play(openLock.animate.move_to([5,2.25,0]))
        closedLock.move_to(openLock.get_center())
        self.wait(0.6)
        self.play(openLock.animate.remove(), closedLock.animate.add(), Flash(closedLock, flash_radius=0.8))
        self.wait(2)
        self.play(FadeIn(throne, crown))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

    def trocarDeOS(self):
        linux = SVGMobject("svgs\\linux").set_z_index(2).move_to([-8,0,0])
        windows = SVGMobject("svgs\\windows").set_z_index(2).scale(0.8)
        laptop = SVGMobject("svgs\\laptop").scale(1.5)

        acronym = Tex("{{W}}{{S}}{{L}}").move_to([0,-2,0]).set_color(PURPLE)
        fullText = Tex("{{W}}indows {{S}}ubsystem {{L}}inux").move_to([0,-2,0])

        rectangle = Rectangle(color=RED_E, height=3).set_fill(RED, opacity=1)
        rectangle2 = Rectangle(color=WHITE, height=1.5,width=4).set_fill(WHITE, opacity=1).move_to(rectangle.get_bottom(), aligned_edge=DOWN).shift([0,0.5,0])
        texto = Text("Hello!\nMy name is", font_size=35, weight=BOLD).move_to(rectangle.get_top(), aligned_edge=UP)
        name = Text("Linux", font_size=45,font="Segoe Script", color=BLACK).move_to(rectangle2.get_center())
        hello = VGroup(rectangle, rectangle2, texto, name).set_z_index(5)
        linux[0].set_color("#000000")

        self.add(linux)
        self.play(Write(windows), Write(laptop))
        self.play(linux.animate.move_to(laptop.get_left(), aligned_edge=RIGHT))
        self.play(linux.animate.shift([1.5,0,0]), windows.animate.shift([0.5,0,0]), rate_func=rate_functions.ease_in_circ, run_time=1.5)
        self.play(linux.animate.move_to([-9,0,0]).rotate(-90), windows.animate.shift([-1,0,0]), rate_func=rate_functions.ease_out_back,  run_time=0.8)
        self.play(windows.animate.center(), run_time=0.6)
        self.wait(0.5)
        self.play(Write(acronym))
        self.wait(0.5)
        self.play(TransformMatchingTex(acronym, fullText))
        self.wait()

        hello.move_to(windows.get_corner([1,-1,0])).scale(0.35)
        self.play(FadeIn(hello))

        self.wait(2)
        self.play(FadeOut(*self.mobjects))
    
    def interfaceTerminal(self):
        download = SVGMobject("svgs\\download").set_color(WHITE).set_stroke(WHITE, 5)
        terminal = CustomTerminal()
        interface = ImageMobject("images\\interface")
        cursor=ImageMobject("images/cursor.png").move_to(DOWN*6).scale(0.05)
        cross = Cross(interface, color=RED)

        self.play(Write(download))
        self.wait()
        # Cursor aparece e se move
        self.play(cursor.animate.move_to(ORIGIN+RIGHT*0.25+DOWN*0.45))
        self.play(cursor.animate.scale(0.8),run_time=0.1,rate_func=linear)  # Clica
        self.play(cursor.animate.scale(1.2),run_time=0.1,rate_func=linear)  #
        
        self.play(FadeOut(cursor), ShrinkToCenter(download))
        self.remove(download)
        self.wait(1.2)
        self.play(FadeIn(interface))
        self.play(Create(cross))
        self.wait()
        self.play(FadeOut(cross), FadeOut(interface),
                  FadeIn(terminal))
        self.wait(3)
        terminal.initialize_line(self, "find . -name \"*.txt\"")
        terminal.cursorNewLine()
        terminal.initializeMultiLineString(self, 0.1, r'''./notes.txt
./todo_list.txt
./project_ideas.txt
./comando/aula2/roteiro.txt
./teste.txt
./testDates.txt
./ssssspi.txt
./comando/aula1/roteiro.txt
./prova.txt
./ed.txt''')
        terminal.initialize_path("manim@manim:~$")

        self.wait(2)
        self.play(FadeOut(*self.mobjects))

    def proximaAula(self):
        #FINAL
        text = TX("Para a próxima aula:", font_size = 45)
        text2 = TX("Seu primeiro programa", t2c={"programa": PURPLE}, font_size=50)
        rawTitle = VGroup(text, text2).arrange(DOWN, aligned_edge = LEFT, buff = 0.2)

        self.play(Write(text), run_time = 1.5)
        self.play(Write(text2), run_time = 1.5)
        self.wait()
        self.play(FadeOut(*self.mobjects))

        
    def creditos(self):
        #creditos
        logo = ImageMobject("images/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        cursor=ImageMobject("images/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)
        titulo=Text("Créditos", font_size=80)
        titulo.color="#AA77C7"

   
        diretor = VGroup(T("Diretor", color = "#AA77C7", font_size=60), T("Rainier R. Waki", font_size=50)).arrange(DOWN, buff=0.3)
        tutor = VGroup(T("Tutor", color = "#AA77C7", font_size=60), T("Alyson V. Isaluski", font_size=50)).arrange(DOWN, buff=0.3)
        animadores = VGroup(
            T("Animadores", color = "#AA77C7", font_size=60),
            VGroup(
                T("Eduarda dos R. Mendes", font_size=50),
                T("Leandro M. M. Hyeda", font_size=50)
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
        utfpr = ImageMobject("images/utfpr.png").scale(0.7)
        
        creditos = VGroup(diretor, tutor, animadores, editora, roteirista).scale(0.6)

        for bloco in creditos:
            if isinstance(bloco, VGroup):
                bloco.arrange(DOWN, aligned_edge=LEFT)

        creditos.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        creditos.to_edge(LEFT, buff=0.5).shift(UP*0.2)

        utfpr.scale(0.4)
        utfpr.next_to(creditos, DOWN, buff = 0.2)
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
        self.play(Write(creditos), FadeIn(utfpr))
        self.wait()
        self.play(FadeOut(utfpr), Unwrite(creditos))
        self.wait()

    def construct(self):
        Part1.codigoLivroCarta(self)
        Part1.introComando(self)
        Part1.configurandoAmbiente(self)
        Part1.editoresTexto(self)
        Part1.posInstalacao(self)
        Part1.linuxEWindows(self)
        Part1.separacao(self)
        self.trocarDeOS()
        self.interfaceTerminal()
        self.proximaAula()
        self.creditos()
