from manim import *

config.background_color = "#1E1E1E"
MarkupText.set_default(font = "Manrope")
Text.set_default(font = "Manrope")
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

def criar_codigo(codeMedia: str, show_background=False):
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

class PreIntro(MovingCameraScene):
    def construct(self):
        list_objects = [["youtube", [0,0,0]], ["github", [-4.5,1,0]], ["wikipedia", [4.5,1,0]], ["moodle", [0,3,0]],
                        ["unity", [-3,-2,0]], ["bash", [4,-2,0]]]
        aplications = VGroup(*[SVGMobject("assets\\"+obj[0]).move_to(obj[1]).scale(0.9) for obj in list_objects]).shift([0,0.15,0])

        self.play(LaggedStart(*[GrowFromPoint(ap, ORIGIN, rate_func=rate_functions.ease_in_out_back) for ap in aplications],
                  lag_ratio=1),
                  rate_func=rate_functions.ease_in_sine, run_time=2.5)
        titulo = Text("Entradas e Saídas", t2c={"e":WHITE}, weight=BOLD, color=PURPLE).scale(1.5)
        self.wait()
        self.play(aplications.animate.set_opacity(0.15), FadeIn(titulo))

        self.wait()
        self.play(aplications.animate.move_to(ORIGIN).scale(0), titulo.animate.scale(0))
        self.remove(aplications, titulo)
        self.wait(0.2)


#Para facilitar legibilidade humana, adicionei alguns comentários do que ta acontecendo e fiz algumas mudanças
#Nota que ajustes precisaram ser feitos para atingir bom fluxo com roteiro
class SiteLogin(MovingCameraScene):
    def construct(self):
        roxo = "#AA77C7"
        verde = "#3FB56F"
        escuro = "#2B2B33"
        cinza = "#6B6B76"
        borda = "#C9C9D2"

        def texto(conteudo, tamanho, **kwargs):
            return Text(conteudo, font_size=tamanho*10, **kwargs).scale(0.1)

        #Definição de objetos para o site hipotético
        janela = RoundedRectangle(corner_radius=0.2, width=10, height=6.6,
                                  fill_color="#F1F1F5", fill_opacity=1, stroke_width=0)
        barra = RoundedRectangle(corner_radius=[0.2,0,0,0.2], width=10, height=0.6,
                                 fill_color="#DCDCE3", fill_opacity=1, stroke_width=0).align_to(janela, UP)
        botoes_janela = VGroup(*[Dot(radius=0.08, color=cor) for cor in ["#ED6A5E", "#F4BF4F", "#61C554"]]).arrange(RIGHT, buff=0.14)
        botoes_janela.move_to(barra).align_to(barra, LEFT).shift(RIGHT*0.3)
        caixa_url = RoundedRectangle(corner_radius=0.16, width=7, height=0.36,
                                     fill_color=WHITE, fill_opacity=1, stroke_width=0).move_to(barra)
        url = texto("www.exemplo.com/login", 18, color=cinza).move_to(caixa_url)

        #Definições dos campos
        cartao = RoundedRectangle(corner_radius=0.15, width=5.4, height=5.4,
                                  fill_color=WHITE, fill_opacity=1, stroke_color=borda, stroke_width=1.5).move_to(DOWN*0.3)
        titulo = texto("Bem-vindo", 36, weight=BOLD, color=escuro)
        rotulo_email = texto("Email", 20, color=cinza)
        caixa_email = RoundedRectangle(corner_radius=0.08, width=4.6, height=0.6,
                                       fill_color=WHITE, fill_opacity=1, stroke_color=borda, stroke_width=2)
        campo_email = VGroup(rotulo_email, caixa_email).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        rotulo_senha = texto("Senha", 20, color=cinza)
        caixa_senha = caixa_email.copy()
        campo_senha = VGroup(rotulo_senha, caixa_senha).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        caixa_botao = RoundedRectangle(corner_radius=0.08, width=4.6, height=0.65,
                                       fill_color=roxo, fill_opacity=1, stroke_width=0)
        botao = VGroup(caixa_botao, texto("Login", 24, weight=BOLD, color=WHITE))
        formulario = VGroup(titulo, campo_email, campo_senha, botao).arrange(DOWN, buff=0.36).move_to(cartao)

        #Finalmente tudo é unido
        site = VGroup(janela, barra, botoes_janela, caixa_url, url, cartao)

        #Definições dos valores a serem preenchidos
        email = texto("aluno@gmail.com", 24, color=escuro)
        email.move_to(caixa_email).align_to(caixa_email, LEFT).shift(RIGHT*0.18)
        senha = VGroup(*[Dot(radius=0.07, color=escuro) for _ in range(8)]).arrange(RIGHT, buff=0.1)
        senha.move_to(caixa_senha).align_to(caixa_senha, LEFT).shift(RIGHT*0.18)

        #Definição do ponteiro (no caso aqui o claude preencheu o objeto com o "miolo" porque eu peguei um svg ruim)
        ponteiro = SVGMobject("assets\\pointer").set_color(BLACK).scale(0.3)
        miolo = VMobject(fill_color=WHITE, fill_opacity=1, stroke_width=0)
        miolo.set_points(ponteiro[0].get_subpaths()[1])
        cursor = VGroup(miolo, ponteiro).move_to([4,-2.6,0], aligned_edge=UL)

        #Funções do ponteiro
        def mover_cursor(alvo, run_time=0.6):
            self.play(cursor.animate(path_arc=-0.3).move_to(alvo, aligned_edge=UL), run_time=run_time)

        def clicar(*animacoes):
            ponta = cursor.get_corner(UL)
            onda = Circle(radius=0.08, color=roxo, stroke_width=4).move_to(ponta)
            self.play(cursor.animate.scale(0.8, about_point=ponta), rate_func=there_and_back, run_time=0.25)
            self.play(FadeOut(onda, scale=5), *animacoes, run_time=0.3)

        #Funções para preencher os campos (o claude optou uma função rodando em updaters por alpha func em vez de AddLetterByLetter)
        def digitar(conteudo, caixa, run_time):
            barra_texto = Rectangle(width=0.03, height=0.36, fill_color=escuro, fill_opacity=1, stroke_width=0)
            barra_texto.move_to(caixa).set_x(conteudo.get_left()[0])
            conteudo.set_opacity(0)
            self.add(conteudo, barra_texto)

            def revelar(grupo, alpha):
                visiveis = int(alpha*len(grupo))
                for i, letra in enumerate(grupo):
                    letra.set_opacity(1 if i < visiveis else 0)
                if visiveis > 0:
                    barra_texto.set_x(grupo[visiveis-1].get_right()[0] + 0.05)

            self.play(UpdateFromAlphaFunc(conteudo, revelar, rate_func=linear), run_time=run_time)
            self.remove(barra_texto)
        #Animações começam
        self.play(FadeIn(site, formulario, scale=0.9), run_time=0.75)
        self.play(FadeIn(cursor), run_time=0.2)
        self.add_foreground_mobject(cursor)
        self.wait(0.1)

        mover_cursor(caixa_email.get_right() + LEFT*0.7, 0.5)
        clicar(caixa_email.animate.set_stroke(roxo))
        digitar(email, caixa_email, 0.8)
        self.wait(0.4)

        mover_cursor(caixa_senha.get_right() + LEFT*0.7, run_time=0.4)
        clicar(caixa_email.animate.set_stroke(borda), caixa_senha.animate.set_stroke(roxo))
        digitar(senha, caixa_senha, 0.6)
        self.wait(0.4)

        mover_cursor(botao.get_center() + RIGHT*0.5, run_time=0.3)
        clicar(caixa_senha.animate.set_stroke(borda), Indicate(botao, color=WHITE, scale_factor=1.04))

        site.add(formulario, email, senha)
        self.play(FadeOut(cursor), site.animate.scale(0.68).to_edge(LEFT, buff=0.5), run_time=0.8)
        #Card para as entradas
        def criar_card(conteudo, cor):
            fundo = SurroundingRectangle(conteudo, corner_radius=0.12, buff=0.13, fill_color=cor, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
            return VGroup(fundo, conteudo)
        #Definição box programa (parte de entrada, processamento e saida)
        caixa_programa = RoundedRectangle(corner_radius=0.2, width=3.2, height=3.4, fill_color="#2A2A30", fill_opacity=1, stroke_color=roxo, stroke_width=3).move_to(RIGHT*4.7)
        dentes = VGroup(*[Rectangle(width=0.26, height=1.7, fill_color=roxo, fill_opacity=1, stroke_width=0).rotate(i*PI/4) for i in range(4)])
        engrenagem = VGroup(dentes, Circle(radius=0.65, fill_color=roxo, fill_opacity=1, stroke_width=0), Circle(radius=0.26, fill_color="#2A2A30", fill_opacity=1, stroke_width=0))
        engrenagem.move_to(caixa_programa).shift(UP*0.35)
        nome_programa = texto("Programa", 30, weight=BOLD).next_to(engrenagem, DOWN, buff=0.3)
        programa = VGroup(caixa_programa, engrenagem, nome_programa)

        seta_entrada = Arrow(site.get_right() + UP*0.9, caixa_programa.get_left() + UP*0.9, buff=0.12, color=roxo, stroke_width=5)
        seta_saida = Arrow(caixa_programa.get_left() + DOWN*0.9, site.get_right() + DOWN*0.9, buff=0.12, color=verde, stroke_width=5)
        rotulo_entrada = texto("Entradas", 30, weight=BOLD, color=roxo).next_to(seta_entrada, UP, buff=0.5)
        rotulo_saida = texto("Saída", 30, weight=BOLD, color=verde).next_to(seta_saida, DOWN, buff=0.5)
        #Animações de processamento
        self.play(FadeIn(programa, shift=LEFT*0.3), GrowArrow(seta_entrada), FadeIn(rotulo_entrada), run_time=0.8)
        self.wait()

        cards = VGroup(*[criar_card(texto(nome, 20, color=WHITE), roxo) for nome in ["aluno@gmail.com", "senha", "clique"]])
        for chip, origem in zip(cards, [caixa_email, caixa_senha, botao]):
            chip.move_to(origem)
        self.play(FadeIn(cards, scale=1.2), run_time=0.4)
        self.bring_to_front(programa)
        #Definição do caminho que os cards vão seguir
        caminhos = [VMobject().set_points_as_corners([chip.get_center(), seta_entrada.get_start(), caixa_programa.get_left() + UP*0.9, caixa_programa.get_center()]) for chip in cards]
        self.play(*[MoveAlongPath(chip, caminho, rate_func=squish_rate_func(smooth, i*0.2, i*0.2+0.6)) for i, (chip, caminho) in enumerate(zip(cards, caminhos))], run_time=1.6)
        self.remove(cards)
        
        self.play(Rotating(engrenagem, angle=2*TAU, run_time=1, rate_func=smooth), caixa_programa.animate(run_time=1, rate_func=there_and_back).set_stroke(WHITE, width=6))
        #Movimentação da saída para a tela novamente
        check = VMobject(stroke_color=WHITE, stroke_width=7).set_points_as_corners([[-0.2,0,0], [-0.05,-0.15,0], [0.22,0.16,0]])
        selo = VGroup(Circle(radius=0.34, fill_color=verde, fill_opacity=1, stroke_width=0), check).move_to(caixa_programa)
        selo_final = selo.copy().scale(1.5).move_to(cartao).shift(UP*0.45)
        mensagem = texto("Cadastro realizado\ncom sucesso!", 28, weight=BOLD, color=escuro, line_spacing=0.9).next_to(selo_final, DOWN, buff=0.3)

        #Animações de processamento finais
        self.add(selo)
        self.bring_to_front(programa)
        self.play(FadeOut(formulario, email, senha), GrowArrow(seta_saida), FadeIn(rotulo_saida), run_time=0.7)
        site.remove(formulario, email, senha)
        caminho_saida = VMobject().set_points_as_corners([selo.get_center(), caixa_programa.get_left() + DOWN*0.9, seta_saida.get_end()])
        self.play(MoveAlongPath(selo, caminho_saida), rate_func=rate_functions.ease_in_cubic, run_time=1)
        self.play(ReplacementTransform(selo, selo_final), FadeIn(mensagem, shift=UP*0.2), run_time=0.7)
        self.wait(2)

        #Animação para o que será tratado na aula
        self.play(FadeOut(site, selo_final, mensagem, seta_entrada, seta_saida, rotulo_entrada, rotulo_saida),
                  programa.animate.center())
        self.wait(0.2)
        #Definição dos objetos de input e output
        camera = self.camera.frame
        camera.save_state()
        conteudo_input = VGroup(texto("input", 30, weight=BOLD, color=WHITE), texto("entrada", 20, color=WHITE)).arrange(DOWN, buff=0.1)
        conteudo_output = VGroup(texto("output", 30, weight=BOLD, color=WHITE), texto("saída", 20, color=WHITE)).arrange(DOWN, buff=0.1)
        card_input = criar_card(conteudo_input, roxo).move_to(engrenagem).shift(LEFT*5.5)
        card_output = criar_card(conteudo_output, verde).move_to(engrenagem)

        #O svg do monitor tem um quadrado invisível no índice 0, por isso pego só o desenho. O shift centraliza a tela no card
        monitor = SVGMobject("assets\\monitor")[1].scale_to_fit_width(3.4).move_to(engrenagem).shift(RIGHT*6 + DOWN*0.27)

        pasta_aberta = SVGMobject("assets\\openFolder").scale_to_fit_width(3.2).move_to(engrenagem).shift(RIGHT*6 + DOWN*0.75)
        pasta_fechada = SVGMobject("assets\\closedFolder").scale_to_fit_width(3.2).move_to(pasta_aberta)

        #Parte da frente da pasta aberta, fica por cima do card para ele parecer entrar nela. Coordenadas retiradas do svg
        def ponto_pasta(x, y):
            return pasta_aberta.get_corner(UL) + (RIGHT*x + DOWN*(y-1))*pasta_aberta.width/16
        frente_pasta = Polygon(*[ponto_pasta(x, y) for x, y in [[2.03,11], [4.11,11], [5.25,7], [16,7], [14,14], [0,14]]],
                               fill_color=roxo, fill_opacity=1, stroke_width=0)

        #Câmera vai até o card e acompanha ele entrando no processamento
        self.play(FadeIn(card_input, shift=RIGHT*0.5), camera.animate.move_to(card_input).set(width=8.5), run_time=1)
        self.bring_to_front(programa)
        self.wait(0.5)
        self.play(card_input.animate.move_to(engrenagem), camera.animate.move_to(engrenagem), run_time=1.85)
        self.remove(card_input)
        self.play(Rotating(engrenagem, angle=TAU, run_time=0.6, rate_func=smooth))

        #Output sai do processamento com a câmera acompanhando
        self.add(card_output)
        self.bring_to_front(programa)
        self.play(card_output.animate.shift(RIGHT*6), camera.animate.shift(RIGHT*6), run_time=1.8)

        self.play(FadeIn(monitor, scale=1.15), run_time=0.7)
        self.wait(1)

        #Gravar em arquivo
        self.play(FadeOut(monitor), FadeIn(pasta_aberta, shift=UP*0.2), card_output.animate.shift(UP*1.5), run_time=0.8)
        self.add(card_output, frente_pasta)
        self.play(card_output.animate.move_to(frente_pasta).shift(RIGHT*0.25), run_time=0.8)
        self.remove(card_output, frente_pasta)
        self.play(ReplacementTransform(pasta_aberta, pasta_fechada), run_time=0.4)
        self.wait(2.5)

        self.play(FadeOut(*self.mobjects))
        camera.restore()
class Intro(Scene):
    def construct(self):
        logo_svg = SVGMobject("assets/comando.svg").scale(1.5).move_to(ORIGIN)
                
        self.play(Write(logo_svg))

        self.play(logo_svg.animate.shift(UP*0.6))        
        comando = MarkupText('<b>comando.c</b>', font="Major Mono Display").next_to(logo_svg, DOWN, buff=0.2).scale(0.6)
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
        self.wait()
        self.play(FadeOut(*self.mobjects))

class ExplicandoIO(MovingCameraScene):
    def construct(self):
        roxo = "#AA77C7"
        cinza = "#8A8A96"
        cores = [roxo, "#3FB56F", "#58C4DD", "#F4BF4F", "#ED6A5E"]

        def texto(conteudo, tamanho, **kwargs):
            return Text(conteudo, font_size=tamanho*10, **kwargs).scale(0.1)

        def codigo(conteudo, tamanho, cor):
            return Text(conteudo, font="Monospace", font_size=100, color=cor).scale(tamanho)

        #Definição do computador, usuário e dispositivos (o svg do monitor tem um quadrado invisível no índice 0)
        computador = SVGMobject("assets\\monitor")[1].scale_to_fit_width(2.6).move_to(LEFT*5.3)
        usuario = SVGMobject("assets\\user").scale_to_fit_height(2.2).move_to(RIGHT*5.3)
        teclado = SVGMobject("assets\\keyboard").scale_to_fit_height(1.3)
        mouse = SVGMobject("assets\\mouse").scale_to_fit_height(1.3)
        #O corpo do mouse é preto no svg, sumiria no fundo escuro
        for parte in [0, 2, 3]:
            mouse[parte].set_fill(WHITE)
        microfone = SVGMobject("assets\\mic").scale_to_fit_height(1.3).set_stroke(width=5)
        dispositivos = VGroup(teclado, mouse, microfone).arrange(DOWN, buff=0.7)

        #Cada dispositivo tem uma linha até o computador e outra até o usuário
        conexoes = [[DashedLine(computador.get_right(), d.get_left(), buff=0.15, dash_length=0.12, color=cinza),
                     DashedLine(d.get_right(), usuario.get_left(), buff=0.15, dash_length=0.12, color=cinza)] for d in dispositivos]
        linhas = VGroup(*[linha for par in conexoes for linha in par])
        ponte = VGroup(computador, usuario, dispositivos, linhas)

        #Pontos de informação. Ficam fora do grupo ponte porque o .animate pausa os updaters do grupo,
        #então eles leem a posição das linhas a cada quadro e assim acompanham a redução
        def criar_ponto(i):
            ponto = Dot(radius=0.08, color=cores[i%len(cores)]).set_opacity(0)
            ida, volta = conexoes[i%len(conexoes)]
            ponto.progresso = -i*0.12
            velocidade = 0.7 + 0.15*(i%4)

            def mover(ponto, dt):
                ponto.progresso += velocidade*dt
                if ponto.progresso >= 1:
                    ponto.progresso -= 1
                t = max(ponto.progresso, 0)
                #Pares vão do computador para o usuário e ímpares fazem o caminho contrário
                posicao = t if i%2 == 0 else 1 - t
                linha = ida if posicao < 0.5 else volta
                ponto.move_to(interpolate(linha.get_start(), linha.get_end(), (posicao*2) % 1))
                ponto.scale_to_fit_width(0.16*computador.width/2.6)
                ponto.set_opacity(min(1, min(t, 1 - t)*10))

            ponto.add_updater(mover, call_updater=False)
            return ponto

        pontos = VGroup(*[criar_ponto(i) for i in range(15)])

        #Funções da stdio flutuando
        nomes = ["printf", "scanf", "fgets", "fputs", "getchar", "putchar", "puts", "fopen", "fclose", "fprintf", "fscanf", "fread"]
        funcoes = VGroup(*[codigo(nome + "()", 0.36, GREEN_C) for nome in nomes]).arrange_in_grid(rows=3, cols=4, buff=(0.7, 0.7)).move_to(DOWN*1.5)

        #Updater para deixar funções de stdio flutuando
        def flutuar(funcao, dt):
            funcao.fase += 2*dt
            funcao.shift(UP*0.15*np.cos(funcao.fase)*dt)

        for i, funcao in enumerate(funcoes):
            funcao.shift([0.2*np.sin(i*2.4), 0.08*np.cos(i*1.7), 0])
            funcao.fase = i
            funcao.add_updater(flutuar)

        #Card no mesmo padrão do criar_card da aula 05, com a largura ajustada ao conteúdo
        def criar_card(conteudo):
            caixa = RoundedRectangle(width=conteudo.width + 0.9, height=1.1, corner_radius=0.2, color=roxo, fill_color=roxo, fill_opacity=0.15, stroke_width=3)
            conteudo.move_to(caixa.get_center())
            return VGroup(caixa, conteudo)

        #O manim 0.19 conta os espaços como caracteres e o 0.20 não. O índice passado é do texto e é convertido se precisar
        def letra(mob, conteudo, indice):
            if len(mob) != len(conteudo):
                indice = len(conteudo[:indice].replace(" ", ""))
            return mob[indice]

        #Card da biblioteca e seu significado
        nome_stdio = texto("stdio.h", 44, weight=BOLD, color=roxo, disable_ligatures=True)
        card_stdio = criar_card(nome_stdio).move_to(DOWN*1.5)
        definicao = texto("Standard Input-Output", 44, weight=BOLD, disable_ligatures=True)
        card_definicao = criar_card(definicao).move_to(card_stdio)
        traducao = texto("Entrada e saída padrão", 30, color="#C9C9D2").next_to(card_definicao, DOWN, buff=0.35)

        #s, t, d, i, o de stdio.h viram o S, t, d, I, O da definição, que ficam destacados
        pares = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 15)]
        iniciais = [letra(definicao, "Standard Input-Output", j) for _, j in pares]
        for inicial in iniciais:
            inicial.set_color(roxo)
        resto_definicao = [l for l in definicao if l not in iniciais]

        #Animações começam
        self.play(FadeIn(computador, shift=RIGHT*0.4), FadeIn(usuario, shift=LEFT*0.4), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d, scale=0.8) for d in dispositivos], lag_ratio=0.3), Create(linhas), run_time=1)
        self.add(pontos)
        self.wait(2.5)

        #Os pontos continuam passando por updater enquanto tudo reduz e sobe
        self.play(ponte.animate.scale(0.5, scale_stroke=True).to_edge(UP, buff=0.3), run_time=1)
        self.play(LaggedStart(*[FadeIn(funcao, shift=UP*0.3) for funcao in funcoes], lag_ratio=0.15), run_time=2)
        self.wait(2)

        #As funções se juntam no card
        self.play(*[funcao.animate.move_to(card_stdio).scale(0.3).set_opacity(0) for funcao in funcoes],
                  FadeIn(card_stdio, scale=0.5, rate_func=squish_rate_func(smooth, 0.4, 1)), run_time=1)
        self.remove(*funcoes)
        self.wait(0.5)

        #Significado de stdio: o card expande, as letras se separam com bounce e o resto da definição cresce junto
        #O resto cresce a partir do centro do card para acompanhar a expansão e não aparecer fora dele
        bounce = rate_functions.ease_out_bounce
        self.play(ReplacementTransform(card_stdio[0], card_definicao[0], rate_func=bounce),
                  *[ReplacementTransform(nome_stdio[i], inicial, rate_func=bounce) for (i, _), inicial in zip(pares, iniciais)],
                  *[GrowFromPoint(l, card_stdio.get_center(), rate_func=bounce) for l in resto_definicao],
                  FadeOut(nome_stdio[5:], scale=0.3, rate_func=squish_rate_func(smooth, 0, 0.3)), run_time=1.2)
        self.remove(card_stdio)
        self.add(card_definicao)
        self.wait(0.5)
        self.play(FadeIn(traducao, shift=DOWN*0.2), run_time=0.6)
        self.wait(2)

        #Sem isso o updater dos pontos sobrescreve a opacidade e eles não somem junto com o resto
        for ponto in pontos:
            ponto.clear_updaters()
        self.play(FadeOut(*self.mobjects))

        titulo = Text("Outputs / Saídas", weight=BOLD, t2c={"/":"#AA77C7"}, font_size = 100).scale(0.6)
        descr = Text("Exibindo informações ao usuário", weight=BOLD, font_size = 100).scale(0.3)
        criaCapitulo(self, titulo, descr, 1)

class Outputs(MovingCameraScene):
    def construct(self):
        roxo = "#AA77C7"
        camera = self.camera.frame

        #Mesmo card da classe ExplicandoIO, começa abaixo da tela
        nome_stdio = Text("stdio.h", font_size=440, weight=BOLD, color=roxo, disable_ligatures=True).scale(0.1)
        caixa_stdio = RoundedRectangle(width=nome_stdio.width + 0.9, height=1.1, corner_radius=0.2, color=roxo, fill_color=roxo, fill_opacity=0.15, stroke_width=3)
        #O fundo do card é transparente, então uma cópia com a cor do fundo da cena esconde o printf atrás dele
        fundo_stdio = caixa_stdio.copy().set_fill(config.background_color, 1).set_stroke(width=0)
        card_stdio = VGroup(fundo_stdio, caixa_stdio, nome_stdio.move_to(caixa_stdio)).move_to(DOWN*5)

        printf = criar_codigo("printf();").scale(1.25).move_to(DOWN*2)

        #O manim 0.19 conta os espaços como caracteres e o 0.20 não. Os índices passados são do texto e são convertidos se precisar
        def trecho(codigo, conteudo, inicio, fim=None):
            inicio, fim, _ = slice(inicio, fim).indices(len(conteudo))
            if len(codigo.code_lines[0]) != len(conteudo):
                inicio = len(conteudo[:inicio].replace(" ", ""))
                fim = len(conteudo[:fim].replace(" ", ""))
            return codigo.code_lines[0][inicio:fim]

        texto_ola = 'printf("Olá, mundo!");'
        texto_formatado = 'printf("Olá, mundo! %s", "Esta é a aula 7");'

        #Versão com o parâmetro. O caractere 7 é o primeiro depois do parêntese e os 2 últimos são ");"
        printf_texto = criar_codigo(texto_ola).scale(1.25).move_to(UP)
        linha = printf_texto.code_lines[0]
        parametro = linha[7:-2]
        lugar_parametro = parametro.get_center()
        parametro.shift(UP*3)

        #Versão com a formatação. Até o caractere 19 (printf("Olá, mundo!) é igual à anterior
        printf_formatado = criar_codigo(texto_formatado).scale(1.25).move_to(UP)
        # %s e , "Esta é a aula 7"
        novos_parametros = VGroup(trecho(printf_formatado, texto_formatado, 19, 22), trecho(printf_formatado, texto_formatado, 23, -2))
        novos_parametros.shift(UP*5)

        #Movimento brusco do card: recua e dá um tranco para cima no instante em que o bounce do printf sai
        def tranco(t):
            if t < 0.4:
                return -0.5*smooth(t/0.4)
            if t < 0.5:
                return -0.5 + 1.5*(t - 0.4)/0.1
            return 1 - smooth((t - 0.5)/0.5)

        #Animações começam
        self.play(card_stdio.animate.move_to(DOWN*2), run_time=1)
        self.wait(1.5)

        #Printf começa escondido atrás do card
        self.add(printf, card_stdio)
        self.play(card_stdio.animate(rate_func=tranco).shift(UP*0.4),
                  printf.animate(rate_func=rate_functions.ease_in_out_bounce).move_to(UP), run_time=1.6)

        #Zoom no printf, o card fica fora do enquadramento
        self.play(camera.animate.move_to(printf).set(width=8), run_time=1)
        self.remove(card_stdio)
        self.wait(1)

        #Parênteses abrem espaço e o texto cai no lugar
        self.play(ReplacementTransform(printf.background, printf_texto.background),
                  ReplacementTransform(printf.code_lines[0][:7], linha[:7]),
                  ReplacementTransform(printf.code_lines[0][7:], linha[-2:]), run_time=0.7)
        self.play(parametro.animate.move_to(lugar_parametro), rate_func=rate_functions.ease_out_cubic, run_time=1.1)
        self.add(printf_texto)

        #Segunda aspas e segundo parênteses abrem espaço enquanto a câmera afasta, o texto novo cai igual ao anterior
        self.wait(1.5)
        self.play(ReplacementTransform(printf_texto.background, printf_formatado.background),
                  ReplacementTransform(trecho(printf_texto, texto_ola, 0, 19), trecho(printf_formatado, texto_formatado, 0, 19)),
                  ReplacementTransform(trecho(printf_texto, texto_ola, 19, 20), trecho(printf_formatado, texto_formatado, 22, 23)),
                  ReplacementTransform(trecho(printf_texto, texto_ola, 20), trecho(printf_formatado, texto_formatado, -2)),
                  camera.animate.set(width=14), run_time=0.7)
        self.play(novos_parametros.animate.shift(DOWN*5), rate_func=rate_functions.ease_out_cubic, run_time=1.1)
        self.remove(printf_texto)
        self.add(printf_formatado)
        self.wait(1.5)

        #Especificadores que saem do %s. %d e %i ficam no meio da linha de cima para o card ficar em cima deles
        simbolo_s = trecho(printf_formatado, texto_formatado, 20, 22)
        nomes_especificadores = ["%c", "%d", "%i", "%f", "%s", "%lf", "%u", "%x"]
        especificadores = VGroup(*[Text(nome, font="Monospace", font_size=100, color=simbolo_s[0].get_color()).scale(0.3) for nome in nomes_especificadores])
        especificadores.arrange_in_grid(rows=2, cols=4, buff=(0.8, 0.5)).move_to(UP*6)
        inteiros = VGroup(especificadores[1], especificadores[2])
        outros = VGroup(especificadores[0], *especificadores[3:])

        #Card igual ao criar_card da aula 05
        def criar_card(nome, cor, exemplo):
            caixa = RoundedRectangle(width=2.2, height=2.4, corner_radius=0.2, color=cor, fill_color=cor, fill_opacity=0.15, stroke_width=3)
            rotulo_nome = Text(nome, font_size=30, color=cor, weight=BOLD, disable_ligatures=True)
            rotulo_exemplo = Text(exemplo, font_size=26)
            conteudo = VGroup(rotulo_nome, rotulo_exemplo).arrange(DOWN, buff=0.5)
            conteudo.move_to(caixa.get_center())
            return VGroup(caixa, conteudo)

        card_int = criar_card("int", BLUE_D, "10").scale(0.6).next_to(inteiros, UP, buff=0.4)

        #Frase do Jorge e a versão com os especificadores em branco (os '-' ficam invisíveis e um quadrado branco entra no lugar)
        texto_jorge = 'printf("Meu nome é Jorge e eu nasci em 1990");'
        texto_variaveis = 'printf("Meu nome é %- e eu nasci em %-", nome, anoNascimento);'
        printf_jorge = criar_codigo(texto_jorge).move_to(ORIGIN)
        printf_variaveis = criar_codigo(texto_variaveis).move_to(ORIGIN)
        porcentos = []
        quadrados = VGroup()
        #Os dois % estão nos caracteres 19 e 36 do texto, cada um seguido de um '-'
        for i in (19, 36):
            porcento = trecho(printf_variaveis, texto_variaveis, i, i + 1)
            traco = trecho(printf_variaveis, texto_variaveis, i + 1, i + 2).set_opacity(0)
            porcentos.append(porcento)
            quadrados.add(Square(side_length=porcento.height, color="#87916c", fill_color="#87916c", fill_opacity=1, stroke_width=0).move_to([traco.get_x(), porcento.get_y(), 0]))

        #Os especificadores se espalham para cima e a câmera vai até eles, deixando o printf de fora
        self.play(*[TransformFromCopy(simbolo_s, especificador, rate_func=squish_rate_func(smooth, i*0.05, i*0.05 + 0.65)) for i, especificador in enumerate(especificadores)],
                  camera.animate.move_to(UP*6.5).set(width=7.5), run_time=1.6)
        self.remove(printf_formatado)
        self.wait(1)

        #Destaque do %d e %i com o card de int
        self.play(outros.animate.set_opacity(0.25), *[inteiro.animate.scale(1.3).set_color(BLUE_D) for inteiro in inteiros], run_time=0.6)
        self.wait(0.5)
        self.play(GrowFromCenter(card_int), run_time=0.6)
        self.wait(1.2)

        #Câmera volta ao enquadramento normal e o printf do Jorge aparece
        self.play(FadeOut(especificadores, card_int), camera.animate.move_to(ORIGIN).set(width=config.frame_width), run_time=1)
        self.play(FadeIn(printf_jorge, shift=UP*0.3), run_time=0.8)
        self.wait(1.5)

        #Jorge e 1990 são destacados e viram os especificadores em branco
        self.play(LaggedStart(Indicate(trecho(printf_jorge, texto_jorge, 19, 24)),
                  Indicate(trecho(printf_jorge, texto_jorge, 39, 43)), lag_ratio=0.5), run_time=1)
        self.wait(0.5)
        self.play(ReplacementTransform(trecho(printf_jorge, texto_jorge, 0, 19), trecho(printf_variaveis, texto_variaveis, 0, 19)),
                  ReplacementTransform(trecho(printf_jorge, texto_jorge, 19, 24), VGroup(porcentos[0], quadrados[0])),
                  ReplacementTransform(trecho(printf_jorge, texto_jorge, 24, 39), trecho(printf_variaveis, texto_variaveis, 21, 36)),
                  ReplacementTransform(trecho(printf_jorge, texto_jorge, 39, 43), VGroup(porcentos[1], quadrados[1])),
                  ReplacementTransform(trecho(printf_jorge, texto_jorge, 43, 44), trecho(printf_variaveis, texto_variaveis, 38, 39)),
                  ReplacementTransform(trecho(printf_jorge, texto_jorge, 44), trecho(printf_variaveis, texto_variaveis, -2)),
                  FadeIn(trecho(printf_variaveis, texto_variaveis, 39, -2), shift=LEFT*0.3, rate_func=squish_rate_func(smooth, 0.4, 1)), run_time=1.2)
        self.remove(printf_jorge)
        self.add(printf_variaveis, quadrados)
        self.wait(1.5)

        #Versão final com os especificadores. Tem o mesmo tamanho da anterior, então o 's' e o 'd' ficam onde estavam os '-'
        texto_final = 'printf("Meu nome é %s e eu nasci em %d", nome, anoNascimento);'
        printf_final = criar_codigo(texto_final).move_to(ORIGIN)
        letras_especificadores = [trecho(printf_final, texto_final, i, i + 1) for i in (20, 37)]
        for letra_especificador in letras_especificadores:
            letra_especificador.shift(UP*5)

        #Nome seria uma string... o 's' cai no lugar do primeiro quadrado, que some logo em seguida
        self.play(Indicate(trecho(printf_variaveis, texto_variaveis, 41, 45)), run_time=1)
        self.wait(1.5)
        self.play(letras_especificadores[0].animate.shift(DOWN*5), rate_func=rate_functions.ease_out_cubic, run_time=1.1)
        self.play(FadeOut(quadrados[0], scale=0.5), run_time=0.4)
        self.wait(1)

        #...números inteiros utilizamos %d ou %i: a mesma coisa com o 'd'
        self.play(Indicate(trecho(printf_variaveis, texto_variaveis, 47, -2)), run_time=1)
        self.wait(1)
        self.play(letras_especificadores[1].animate.shift(DOWN*5), rate_func=rate_functions.ease_out_cubic, run_time=1.1)
        self.play(FadeOut(quadrados[1], scale=0.5), run_time=0.4)
        self.remove(printf_variaveis, *letras_especificadores)
        self.add(printf_final)
        self.wait(1.5)
        self.play(FadeOut(*self.mobjects))

class Especificadores(MovingCameraScene):
    def construct(self):
        roxo = "#AA77C7"
        verde_string = "#C3E88D"

        #Texto com font_size 10x maior e scale(0.1) para não estragar o espaçamento das letras
        def texto(conteudo, tamanho, **kwargs):
            return Text(conteudo, font_size=tamanho*10, disable_ligatures=True, **kwargs).scale(0.1)

        #Tabela: cabeçalho + uma linha por especificador
        linhas_tabela = [
            ("%c", "Um único caractere"),
            ("%d e %i", "Um número inteiro com sinal"),
            ("%f", "Um número com casas decimais"),
            ("%s", "Uma sequência de caracteres"),
            ("%u", "Um número inteiro sem sinal"),
            ("%%", "O próprio caractere %"),
        ]
        conteudo_tabela = [[texto("Especificador", 30, weight=BOLD, color=roxo), texto("O que será impresso", 30, weight=BOLD, color=roxo)]]
        for especificador, descricao in linhas_tabela:
            conteudo_tabela.append([texto(especificador, 28, font="Monospace", color=verde_string), texto(descricao, 26)])

        tabela = MobjectTable(conteudo_tabela, v_buff=0.4, h_buff=0.8,
                              arrange_in_grid_config={"col_alignments": "cl"},
                              line_config={"color": GRAY, "stroke_width": 2})
        tabela.move_to(ORIGIN)
        grade = VGroup(tabela.get_horizontal_lines(), tabela.get_vertical_lines())

        #Código de exemplo, -5 visto como int e como unsigned int
        texto_codigo = 'int numero = -5;\nprintf("%d", numero);\nprintf("%u", numero);'
        codigo = criar_codigo(texto_codigo)

        #Saídas no terminal: texto branco monoespaçado com a mesma altura de letra do código
        saidas = VGroup()
        flechas = VGroup()
        for linha, valor in zip(codigo.code_lines[1:], ("-5", "4294967291")):
            flecha = Arrow(ORIGIN, RIGHT*0.8, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.3, color=WHITE).next_to(linha, RIGHT, buff=0.3)
            saida = Text(valor, font="Monospace", font_size=240).scale(0.1).next_to(flecha, RIGHT, buff=0.3)
            flechas.add(flecha)
            saidas.add(saida)
        exemplo = VGroup(codigo, flechas, saidas).scale(0.85)

        #Posições finais: tabela menor à esquerda e o exemplo à direita
        escala_tabela = 0.6
        largura_tabela = tabela.width*escala_tabela
        espaco = 0.6
        largura_total = largura_tabela + espaco + exemplo.width
        centro_tabela = LEFT*(largura_total/2 - largura_tabela/2)
        exemplo.move_to(RIGHT*(largura_total/2 - exemplo.width/2))
        #As flechas e saídas são alinhadas em x pelo fim do código, então as linhas do printf têm o mesmo tamanho

        #Grade aparece e depois as linhas de cima para baixo
        self.play(FadeIn(grade), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(linha, shift=DOWN*0.2) for linha in tabela.get_rows()], lag_ratio=0.35), run_time=2.2)
        self.wait(2.5)

        #Tabela diminui e vai para a esquerda, o código aparece com write
        self.play(tabela.animate.scale(escala_tabela).move_to(centro_tabela), run_time=1)
        #Write só nas linhas: no Code inteiro o Write desenha o contorno do retângulo de fundo por um instante
        self.play(Write(codigo.code_lines), run_time=1.8)
        self.add(codigo)
        self.wait(1.5)

        #%d: -5
        self.play(GrowArrow(flechas[0]), run_time=0.5)
        self.play(FadeIn(saidas[0], shift=RIGHT*0.2), run_time=0.5)
        self.wait(1)

        #%u: o mesmo dado interpretado como inteiro sem sinal
        self.play(GrowArrow(flechas[1]), run_time=0.5)
        self.play(FadeIn(saidas[1], shift=RIGHT*0.2), run_time=0.5)
        self.wait(3)

        #Tabela completa: as linhas anteriores + os outros especificadores, ajustada para caber na altura da tela
        linhas_extras = [
            ("%e e %E", "Um número em notação científica"),
            ("%g e %G", "O que for menor, %e ou %f"),
            ("%o", "Um número em formato octal"),
            ("%x e %X", "Um número em formato hexadecimal"),
            ("%p", "Um ponteiro"),
        ]
        conteudo_completo = [[texto("Especificador", 30, weight=BOLD, color=roxo), texto("O que será impresso", 30, weight=BOLD, color=roxo)]]
        for especificador, descricao in linhas_tabela + linhas_extras:
            conteudo_completo.append([texto(especificador, 28, font="Monospace", color=verde_string), texto(descricao, 26)])
        tabela_completa = MobjectTable(conteudo_completo, v_buff=0.4, h_buff=0.8,
                                       arrange_in_grid_config={"col_alignments": "cl"},
                                       line_config={"color": GRAY, "stroke_width": 2})
        if tabela_completa.height > 7.4:
            tabela_completa.scale_to_fit_height(7.4)
        tabela_completa.move_to(ORIGIN).to_edge(UP, buff=0.3)

        linhas_antigas = tabela.get_rows()
        linhas_novas = tabela_completa.get_rows()
        horizontais_antigas = tabela.get_horizontal_lines()
        horizontais_novas = tabela_completa.get_horizontal_lines()
        n_antigas = len(linhas_antigas)

        #Esses seriam os especificadores mais importantes...: código some, tabela volta ao tamanho original e sobe
        self.play(FadeOut(exemplo),
                  tabela.animate.scale(1/escala_tabela).move_to(ORIGIN).to_edge(UP, buff=0.3), run_time=1)
        self.wait(1.5)

        #...porém, existem diversos outros: a tabela se ajusta e as linhas novas entram de cima para baixo
        #A linha vertical primeiro vai só até o fim das linhas antigas e depois cresce junto com as novas
        vertical_nova = tabela_completa.get_vertical_lines()
        vertical_parcial = vertical_nova.copy()
        #O ponto de baixo da linha é trocado pelo corte, mantendo a mesma direção da linha da tabela para o transform não inverter
        inicio, fim = vertical_nova[0].get_start(), vertical_nova[0].get_end()
        corte = np.array([vertical_nova[0].get_x(), horizontais_novas[n_antigas - 1].get_y(), 0])
        if inicio[1] < fim[1]:
            inicio = corte
        else:
            fim = corte
        vertical_parcial[0].put_start_and_end_on(inicio, fim)
        self.play(*[ReplacementTransform(linhas_antigas[i], linhas_novas[i]) for i in range(n_antigas)],
                  *[ReplacementTransform(horizontais_antigas[i], horizontais_novas[i]) for i in range(len(horizontais_antigas))],
                  ReplacementTransform(tabela.get_vertical_lines(), vertical_parcial), run_time=1)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(horizontais_novas[i - 1]), FadeIn(linhas_novas[i], shift=DOWN*0.2))
                                for i in range(n_antigas, len(linhas_novas))], lag_ratio=0.35),
                  ReplacementTransform(vertical_parcial, vertical_nova, rate_func=linear), run_time=2)
        self.remove(tabela)
        self.add(tabela_completa)
        self.wait(1)

        #...comentados mais a fundo no PDF: a tabela fica de fundo e o pdf aparece
        pdf = SVGMobject("assets\\pdf").scale_to_fit_height(3.5)
        self.play(tabela_completa.animate.set_opacity(0.25), run_time=0.8)
        self.play(FadeIn(pdf, scale=0.8), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

class EscapeS(MovingCameraScene):
    def construct(self):
        titulo = Text("Escape Sequences", weight=BOLD, font_size = 100).scale(0.6)
        descr = Text("Formatação de output", weight=BOLD, font_size = 100).scale(0.3)
        criaCapitulo(self, titulo, descr, 2)
        
class Main(MovingCameraScene):
    def construct(self):
        PreIntro.construct(self)
        SiteLogin.construct(self)
        Intro.construct(self)
        ExplicandoIO.construct(self)
        Outputs.construct(self)
        Especificadores.construct(self)