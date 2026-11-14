from manim import *
from customTerminal import CustomTerminal

config.background_color="#1E1E1E"
Text.set_default(font = "Manrope", disable_ligatures=True)
MarkupText.set_default(font = "Manrope", disable_ligatures=True)
Circumscribe.set_default(color=WHITE)
Indicate.set_default(color="#AA77C7")

ROXO = "#AA77C7"
VERDE = "#98C379"
FUNDO = "#2A2A2E"
FUNDO_CENA = "#1E1E1E" 
VERMELHO = "#E06C75"



def fix_cap(mob):
    for m in mob.family_members_with_points():
        m.set_cap_style(CapStyleType.BUTT)
    return mob

def TX(texto, **kwargs):
    return fix_cap(Text(texto, **kwargs))

def T2(texto, **kwargs):
    return fix_cap(Tex(texto, **kwargs))

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
 
 
def icone_teclado(cor=ROXO):
    corpo = RoundedRectangle(
        width=1.7, height=1.0, corner_radius=0.14,
        color=cor, stroke_width=3, fill_color=FUNDO, fill_opacity=1,
    )
    teclas = VGroup(*[
        RoundedRectangle(width=0.15, height=0.15, corner_radius=0.03, stroke_width=0,
                         fill_color=GRAY_B, fill_opacity=0.9)
        for _ in range(21)
    ]).arrange_in_grid(rows=3, cols=7, buff=0.07)
    espaco = RoundedRectangle(width=0.9, height=0.14, corner_radius=0.03, stroke_width=0,
                              fill_color=GRAY_B, fill_opacity=0.9)
    interior = VGroup(teclas, espaco).arrange(DOWN, buff=0.09).move_to(corpo)
    return VGroup(corpo, interior)
 
 
def icone_arquivo(L=1.0, A=1.25, D=0.3, R=0.06):
    corpo = Polygon(
        [-L / 2, A / 2, 0], [L / 2 - D, A / 2, 0], [L / 2, A / 2 - D, 0],
        [L / 2, -A / 2, 0], [-L / 2, -A / 2, 0],
        color=ROXO, stroke_width=3, fill_color=FUNDO, fill_opacity=1,
    ).round_corners(R)
    gabarito = RoundedRectangle(
        width=D + 1, height=D + 1, corner_radius=R,
    ).move_to([L / 2 - D, A / 2 - D, 0], aligned_edge=DL)
    dobra = Intersection(
        corpo, gabarito,
        color=ROXO, stroke_width=3, fill_color=ROXO, fill_opacity=0.5,
    )
    linhas = VGroup(*[
        Line(LEFT * 0.28, RIGHT * 0.28, color=GRAY_B, stroke_width=3) for _ in range(3)
    ]).arrange(DOWN, buff=0.14).move_to(corpo.get_center() + DOWN * 0.18)
    return VGroup(corpo, dobra, linhas)
 
 
def icone_escudo():
    escudo = VMobject(color=ROXO, stroke_width=4, fill_color=ROXO, fill_opacity=0.25)
    escudo.start_new_path([0, 0.7, 0])
    escudo.add_cubic_bezier_curve_to([0.2, 0.58, 0], [0.4, 0.52, 0], [0.6, 0.52, 0])
    escudo.add_line_to(np.array([0.6, 0.0, 0]))
    escudo.add_cubic_bezier_curve_to([0.6, -0.32, 0], [0.32, -0.55, 0], [0, -0.75, 0])
    escudo.add_cubic_bezier_curve_to([-0.32, -0.55, 0], [-0.6, -0.32, 0], [-0.6, 0.0, 0])
    escudo.add_line_to(np.array([-0.6, 0.52, 0]))
    escudo.add_cubic_bezier_curve_to([-0.4, 0.52, 0], [-0.2, 0.58, 0], [0, 0.7, 0])
    check = VMobject(color=VERDE, stroke_width=8)
    check.set_points_as_corners([[-0.24, 0.0, 0], [-0.07, -0.2, 0], [0.27, 0.22, 0]])
    return escudo, check
 

def T(texto, **kw):
    """Text que guarda a string original em .src (o .text do Manim pode perder os espaços)
    e sem ligaduras, para as letras baterem sempre com os índices."""
    kw.setdefault("disable_ligatures", True)       # 1 letra = 1 índice (sem "fi", "fl"...)
    t = Text(texto, **kw)
    t.src = texto
    return t

def parte(texto, trecho, ocorrencia=0):
    """Letras de `trecho` dentro de um Text criado com T().

    Não depende de os espaços serem ou não submobjetos do Text (isso muda com
    `disable_ligatures`, versão e plataforma), então não precisa de índices à mão.
    """
    s = texto.src
    ini = -1
    for _ in range(ocorrencia + 1):
        ini = s.index(trecho, ini + 1)
    fim = ini + len(trecho)
    sem_espaco = lambda x: sum(1 for c in x if not c.isspace())
    if len(texto) == len(s):                       # espaços contam como letras
        return texto[ini:fim]
    if len(texto) == sem_espaco(s):                # espaços não contam
        a = sem_espaco(s[:ini])
        return texto[a:a + sem_espaco(trecho)]
    raise ValueError("Número de letras inesperado: use Text.set_default(disable_ligatures=True)")


def nota_sob(alvo, rotulo, cor):
    """Rótulo com uma seta curta apontando para `alvo`, logo abaixo dele."""
    txt = T(rotulo, font_size=80, color=cor).scale(0.24).next_to(alvo, DOWN, buff=0.75)
    seta = Arrow(txt.get_top(), alvo.get_bottom(), buff=0.12, color=cor,
                 stroke_width=3, tip_length=0.18)
    return VGroup(seta, txt)


def icone_x():
    return VGroup(
        Line([-0.15, 0.15, 0], [0.15, -0.15, 0]),
        Line([-0.15, -0.15, 0], [0.15, 0.15, 0]),
    ).set_color(VERMELHO).set_stroke(width=7)


def icone_ok():
    ok = VMobject(color=VERDE, stroke_width=7)
    ok.set_points_as_corners([[-0.2, 0, 0], [-0.05, -0.15, 0], [0.22, 0.18, 0]])
    return ok


class Aula7(Scene):
    def construct(self):
        #cenas

        Puts.construct(self)
        Capitulo3.construct(self)
        Fgets.construct(self)
        FgetsParametros.construct(self)
        FimLeituraFgets.construct(self)
        ExemploFgets.construct(self)
        ScanfVsFgets.construct(self)
        ExemploSizeof.construct(self)
        Scanf.construct(self)
        ScanfSemEComercial.construct(self)
        UsuarioDigitaMais.construct(self)
        ComoResolver.construct(self)
        ResumoAula7.construct(self)
        Creditos.construct(self)
        


class Puts(Scene):
    def construct(self):
        titulo = Text("puts()", font_size = 80).scale(0.8)
        titulo.move_to(ORIGIN)

        subtitulo = Text("Função de saída", color = ROXO, font_size = 80).scale(0.42)
        subtitulo.next_to(titulo, DOWN, buff=0.26)

        put = Text("put", font_size=80, color=BLUE).scale(0.8)
        string = Text("string", font_size=80, color=BLUE).scale(0.8)
        dividido = VGroup(put, string).arrange(RIGHT, buff=0.7).move_to([0,2.5,0])

 
        self.play(Write(titulo))
        self.play(FadeIn(subtitulo, shift=UP * 0.5))
        self.wait(1)
        self.play(FadeOut(subtitulo))
        self.play(titulo.animate.move_to([0,2.5,0]))

        self.wait(0.5)
        self.play(ReplacementTransform(titulo, dividido))
        self.wait(1)
    
        titulo = Text("puts()", font_size=80).scale(0.8).move_to([0,2.5,0])
        self.play(ReplacementTransform(dividido, titulo))
        self.titulo = titulo
        self.wait(0.8)

        editor = RoundedRectangle(
            corner_radius=0.15, width=9, height=0.9,
            fill_color="#252526", fill_opacity=1,
            stroke_color=GRAY_D, stroke_width=2,
        ).move_to([0, 1.3, 0])
 
        codigo = Text(
            'puts("Estude com o Comando");', font_size=80,
            t2c={"puts": ROXO, '"Estude com o Comando"': "#98C379"},
        ).scale(0.36).move_to(editor)

        terminal = CustomTerminal(width=9, height=2.0, font_size=28)
        terminal.move_to([0, -0.75, 0])
        terminal.cursor.stretch_to_fit_width(0.12).stretch_to_fit_height(0.34)
        terminal.cursor.set_opacity(0)
 
        self.play(FadeIn(editor))
        self.play(Write(codigo))
        self.play(FadeIn(terminal))
        self.wait(0.5)

        # Saída na primeira linha
        self.play(terminal.animate_typing("Estude com o Comando", typing_speed=0.09))
        self.wait(2)
 
        # \n surge em destaque
        saida = terminal.text_container[-1]
        nl = Text("\\n", font_size=80, color=ROXO).scale(0.36)
        nl.next_to(saida, RIGHT, buff=0.2)
        terminal.text_container.add(nl)
 
        self.play(GrowFromCenter(nl))
        self.play(Indicate(nl, color=WHITE))
        self.wait(0.5)

         # Cursor vai para a linha seguinte
        proxima = terminal.add_line("Estude com o Comando")
        proxima.set_opacity(0)
        proxima.set_y(saida.get_y() - 0.5)

        self.play(FadeOut(nl))
 
        aviso = Text(
            "Pulou a linha automaticamente", font_size=80, color=YELLOW
        ).scale(0.33).move_to(terminal.bg.get_bottom() + DOWN * 0.35, aligned_edge=UP)
        self.play(FadeIn(aviso, shift=UP * 0.2))

        self.wait(2)

        terminal.cursor.clear_updaters()
        terminal.cursor.set_opacity(1)
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob is not titulo]
        )

        X_ESQ, X_DIR, Y_TOPO = -3.5, 3.5, 2.5

        printf_titulo = Text("printf()", font_size=80).scale(0.8).move_to([X_ESQ, Y_TOPO, 0])
        divisor = Line([0, 3.3, 0], [0, -3.3, 0], color=ROXO, stroke_width=20, cap_style = CapStyleType.ROUND)
 
        # Divide a tela em duas colunas
        self.play(
            titulo.animate.move_to([X_DIR, Y_TOPO, 0]),
            FadeIn(printf_titulo, shift=RIGHT * 0.5)
        )
        self.play(Create(divisor))
        self.wait(0.5)
      

        # Coluna esquerda
        def linha(spec, var):
            s = Text(spec, font_size=40, color=ROXO)
            seta = Arrow(ORIGIN, RIGHT * 0.8, buff=0, color=YELLOW,
                         stroke_width=3, tip_length=0.2)
            v = Text(var, font_size=34, color=WHITE)
            return VGroup(s, seta, v).arrange(RIGHT, buff=0.35)
 
        linhas = VGroup(linha("%d", "idade"), linha("%s", "nome"))
        linhas.arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([X_ESQ, 0.4, 0])
 
        for l in linhas:
            self.play(FadeIn(l, shift=UP * 0.3))
            self.wait(0.4)
 
        # Coluna direita
        texto = TX('"Aula de Entradas e Saídas"', font_size=80, color="#98C379").scale(0.36)
        texto.move_to([X_DIR, 0, 0])
        texto.set_y(linhas[0].get_y()) 
        self.play(Write(texto), run_time=2)
        self.wait(0.5)
 
        aviso2 = Text("Não formata", font_size=80, color=YELLOW).scale(0.30)
        aviso2.next_to(texto, DOWN, buff=0.6)
        aviso2.set_x(X_DIR)
        self.play(FadeIn(aviso2, shift=UP * 0.2))
        caixa = (
            SurroundingRectangle(
                aviso2,
                corner_radius=0.3,
                buff=0.2
            )
            .set_stroke(YELLOW_E, width=2)
            .set_fill(YELLOW, opacity=0.1)
        )
        self.play(Create(caixa))

        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])
 
class Capitulo3(Scene):
    def construct(self):
        titulo = Text(" Inputs / Entradas", weight=BOLD, t2c={"/":"#AA77C7"}, font_size = 100).scale(0.6)
        descr = Text("Recebendo dados", weight=BOLD, font_size = 100).scale(0.3)

        criaCapitulo(self, titulo, descr, 3)
        
 

class Fgets(Scene):
    def construct(self):
        TAM_TITULO = 80 * 0.8              # tamanho dos títulos (80 com scale 0.8)
        ESC_TITULO = TAM_TITULO / 44       # fator para o fgets virar título

        # Biblioteca stdio.h: arquivo com a aba dobrada
        L, A, D = 2.1, 2.8, 0.55    # largura, altura e tamanho da dobra
        R = 0.1                     # raio dos cantos arredondados

        corpo = Polygon(
            [-L / 2, A / 2, 0], [L / 2 - D, A / 2, 0], [L / 2, A / 2 - D, 0],
            [L / 2, -A / 2, 0], [-L / 2, -A / 2, 0],
            color=ROXO, stroke_width=3, fill_color="#2A2A2E", fill_opacity=1,
        ).round_corners(R)

        gabarito = RoundedRectangle(
            width=D + 1, height=D + 1, corner_radius=R,
        ).move_to([L / 2 - D, A / 2 - D, 0], aligned_edge=DL)

        dobra = Intersection(
            corpo, gabarito,
            color=ROXO, stroke_width=3, fill_color=ROXO, fill_opacity=0.5,
        )

        stdio = Text("stdio.h", font_size=44).move_to(corpo.get_center() + DOWN * 0.15)
         
        biblioteca = VGroup(corpo, dobra, stdio).move_to([0, 1.4, 0])

        self.play(Create(corpo), run_time=1)
        self.play(GrowFromCenter(dobra), Write(stdio), run_time=0.8)
        self.wait(0.5)

        # scanf() e fgets() saem do stdio.h
        pos_scanf = np.array([-2.4, -0.9, 0])
        pos_fgets = np.array([2.4, -0.9, 0])

        scanf = Text("scanf()", font_size=44)
        fgets = Text("fgets()", font_size=44)
        for palavra in (scanf, fgets):
            palavra.scale(0.5).move_to(biblioteca.get_center())

        biblioteca.set_z_index(2)
        self.add(scanf, fgets)
    
        self.play(
            LaggedStart(
                AnimationGroup(scanf.animate.scale(1 / 0.5).move_to(pos_scanf)),
                AnimationGroup(fgets.animate.scale(1 / 0.5).move_to(pos_fgets)),
                lag_ratio=0.3,
            ),
            run_time=1.6,
        )
        self.wait(1)

        self.play(
            Indicate(fgets, scale_factor=1.3, color=ROXO),
            scanf.animate.set_opacity(0.3),
        )
        self.play(fgets.animate.set_color(ROXO))
        self.wait(0.8)
    
        self.play(
            FadeOut(scanf, shift=DOWN * 0.3),
            FadeOut(biblioteca, shift=UP * 0.3),
        )

        self.play(fgets.animate.move_to(ORIGIN).scale(2.2), run_time=1.2)
        self.wait(1)
    
        # segunda parte
        self.play(
            fgets.animate.scale(ESC_TITULO / 2.2)
            .move_to([0, 2.5, 0])
            .set_color(WHITE),
            run_time=1.2,
        )
        self.wait(0.3)

        Y_FLUXO = 0.95
        Y_ARRAY = -2.0

        # Posição provisória dos elementos do fluxo
        teclado = icone_teclado().move_to([-5.3, 1.85, 0])
        arquivo = icone_arquivo().move_to([-5.3, 0.1, 0])

        rot_teclado = Text("teclado", font_size=80, color=GRAY_B).scale(0.28).next_to(teclado, DOWN, buff=0.12)
        rot_arquivo = Text("arquivo", font_size=80, color=GRAY_B).scale(0.28).next_to(arquivo, DOWN, buff=0.12)

        # O título vai descer até o fluxo
        fantasma = fgets.copy().move_to([-0.8, Y_FLUXO, 0])
        palavra = Text("Dados", font_size=80).scale(0.6).move_to([3.5, Y_FLUXO, 0])

        # Centraliza o fluxo inteiro
        borda_esq = teclado.get_left()[0]
        borda_dir = palavra.get_right()[0]
        dx = -(borda_esq + borda_dir) / 2

        for m in (teclado, arquivo, rot_teclado, rot_arquivo, fantasma, palavra):
            m.shift(RIGHT * dx)

        destino = fantasma.get_center()
        centroPalavra = palavra.get_center()

        # Ícones à esquerda
        self.play(
            LaggedStart(
                AnimationGroup(FadeIn(teclado, shift=RIGHT * 0.4), FadeIn(rot_teclado)),
                AnimationGroup(FadeIn(arquivo, shift=RIGHT * 0.4), FadeIn(rot_arquivo)),
                lag_ratio=0.4,
            ),
            run_time=1.2,
        )
        self.wait(0.2)

        seta_teclado = Arrow(
            teclado.get_right(), fantasma.get_left() + UP * 0.2,
            buff=0.3, color=YELLOW, stroke_width=2, tip_length=0.2
        )
        seta_arquivo = Arrow(
            arquivo.get_right(), fantasma.get_left() + DOWN * 0.2,
            buff=0.3, color=YELLOW, stroke_width=2, tip_length=0.2
        )

        fgets.set_z_index(3)

        self.play(
            fgets.animate.move_to(destino),
            GrowArrow(seta_teclado),
            GrowArrow(seta_arquivo),
            run_time=1.2,
        )
        self.wait(0.2)

        # D, a, d, o, s saem de fgets() e formam Dados
        tapa = SurroundingRectangle(
            fgets,
            color=FUNDO_CENA,
            fill_color=FUNDO_CENA,
            fill_opacity=1,
            stroke_width=0,
            buff=0.1,
        ).set_z_index(2)

        letras = list(palavra)
        alvos = [l.get_center().copy() for l in letras]
        base_palavra = palavra.get_bottom()[1]

        for l in letras:
            l.set_z_index(1)
            l.scale(0.5).move_to(fgets.get_center())

        self.add(tapa, *letras)

        self.play(
            LaggedStart(
                *[l.animate.scale(2).move_to(a) for l, a in zip(letras, alvos)],
                lag_ratio=0.12,
            ),
            run_time=1.3,
        )

        self.remove(tapa)
        self.wait(0.3)

        # char texto[8]
        quadrados = VGroup(*[
            Square(
                side_length=0.95,
                color=BLUE,
                stroke_width=3,
                fill_color="#232326",
                fill_opacity=1
            )
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.12).move_to([0, Y_ARRAY, 0])

        indices = VGroup(*[
            Text(str(i), font_size=20, color=GRAY_B).next_to(q, DOWN, buff=0.15)
            for i, q in enumerate(quadrados)
        ])

        rotulo = Text(
            "char texto[8]",
            font_size=80,
            t2c={"char": ROXO}
        ).scale(0.3).move_to([0, Y_ARRAY - 1.2, 0])

        self.play(
            LaggedStart(*[GrowFromCenter(q) for q in quadrados], lag_ratio=0.1),
            run_time=0.9,
        )
        self.play(
            FadeIn(indices),
            Write(rotulo),
            run_time=0.8,
        )
        self.wait(0.3)

        # Letras descem uma após a outra
        dy = (Y_ARRAY - 0.22) - base_palavra

        self.play(
            LaggedStart(
                *[
                    letra.animate.shift([
                        q.get_center()[0] - a[0],
                        dy,
                        0
                    ])
                    for letra, q, a in zip(letras, quadrados[:5], alvos)
                ],
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )
        self.wait(0.2)

        # Quebra de linha e caractere nulo
        nova_linha = Text("\\n", font_size=40, color=ROXO)
        nova_linha.move_to(quadrados[5].get_center()).set_z_index(1)

        nulo = Text("\\0", font_size=40, color=WHITE)
        nulo.set_opacity(0.5).move_to(quadrados[6].get_center()).set_z_index(1)

        self.play(FadeIn(nova_linha, shift=DOWN * 0.8), run_time=0.4)
        self.wait(0.2)

        self.play(FadeIn(nulo, shift=DOWN * 0.8), run_time=0.4)
        self.wait(0.2)

        # Quadrado 7 com a borda tracejada
        tracejado = DashedVMobject(quadrados[7], num_dashes=24).set_color(BLUE)

        self.play(
            FadeOut(quadrados[7]),
            FadeIn(tracejado),
            run_time=0.5,
        )
        
        self.wait(0.8)

        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=0.8,
        )


class FgetsParametros(Scene):
    def construct(self):   
        def seta(parte, rotulo, cor):
            return Arrow(parte.get_bottom() + DOWN * 0.12, rotulo.get_top() + UP * 0.12, 
                         buff=0, color=cor, stroke_width=2, tip_length=0.2)
 
        # fgets(str, n, stream) no centro
        assinatura = Text("fgets(str, n, stream);", font_size=80).scale(0.7)
        self.play(Write(assinatura), run_time=1.5)
        self.wait(0.5)

        p_str, p_n, p_stream = assinatura[6:9], assinatura[11:12], assinatura[14:20]
        self.play(
            p_str.animate.set_color(ROXO),
            p_n.animate.set_color(YELLOW),
            p_stream.animate.set_color(BLUE),
        )
        self.wait(0.8)
        self.play(assinatura.animate.to_edge(UP, buff=1.4))

        destino = Text("Destino", font_size=80, color=ROXO).scale(0.35)
        limite = Text("Limite, incluindo o \\0", font_size=80, color=YELLOW).scale(0.35)
        fonte = Text("Fonte de dados", font_size=80, color=BLUE).scale(0.35)

        rotulos = VGroup(destino, limite, fonte).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        rotulos.next_to(assinatura, DOWN, buff=1.0)

        quadrados = VGroup(*[
            Square(side_length=0.5, color=GRAY_B, stroke_width=3,
                   fill_color="#232326", fill_opacity=1)
            for _ in range(8)
        ]).arrange(RIGHT, buff=0.06)
        quadrados.next_to(destino, DOWN, buff=1.7)

        rotulo_array = Text("char texto[8]", font_size=80).scale(0.3)
        rotulo_array[5:10].set_color(ROXO)      # texto
        rotulo_array[10:13].set_color(YELLOW)  # [8]
        rotulo_array.next_to(quadrados, DOWN, buff=0.35)

        chave = Brace(quadrados, UP, color=YELLOW, buff=0.1)
        oito = Text("8", font_size=80, color=YELLOW).scale(0.4).next_to(chave, UP, buff=0.1)

        teclado = icone_teclado().next_to(fonte, DOWN, buff=1.2)
        teclado[0].set_stroke(BLUE)
        rot_stdin = Text("stdin", font_size=80, color=BLUE).scale(0.32).next_to(teclado, DOWN, buff=0.2)

        # str -> destino 
        seta_str = seta(p_str, destino, ROXO)
        self.play(GrowArrow(seta_str), FadeIn(destino, shift=DOWN * 0.2))
        self.play(Uncreate(seta_str), run_time=0.6)
        self.wait(0.4)
 
        self.play(LaggedStart(*[GrowFromCenter(q) for q in quadrados], lag_ratio=0.1),
                  run_time=1.2)
        self.play(Write(rotulo_array))
        self.wait(0.6)

         # n -> limite 
        seta_n = seta(p_n, limite, YELLOW)
        self.play(GrowArrow(seta_n), FadeIn(limite, shift=DOWN * 0.2))
        self.play(Uncreate(seta_n), run_time=0.6)
        self.wait(0.4)
 
        self.play(GrowFromCenter(chave))
        self.play(Write(oito))
        self.wait(0.6)

        # stream -> fonte de dados
        seta_stream = seta(p_stream, fonte, BLUE)
        self.play(GrowArrow(seta_stream), FadeIn(fonte, shift=DOWN * 0.2))
        self.play(Uncreate(seta_stream), run_time=0.6)
        self.wait(0.4)
 
        self.play(FadeIn(teclado, shift=UP * 0.3))
        self.play(Write(rot_stdin))
        self.wait(1)

         # fgets(str, n, stream) -> fgets(texto, 8, stdin)
        nova = Text("fgets(texto, 8, stdin);", font_size=80).scale(0.7)
        nova.move_to(assinatura.get_center())
        nova[6:11].set_color(ROXO)      # texto
        nova[13:14].set_color(YELLOW)  # 8
        nova[16:21].set_color(BLUE)     # stdin
 
        self.play(
            ReplacementTransform(assinatura, nova),
            run_time=1.5,
        )
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])  
 

class FimLeituraFgets(Scene):
    def construct(self):
        titulo = Text("O fim de leitura ocorre em 3 ocasiões:", font_size=80).scale(0.50)

        primeiroItem = Text("1. EOF → Fim do arquivo", font_size=80,
            t2c={"EOF": BLUE, "→": GRAY_B})
        segundoItem = Text("2. \\n → Nova linha", font_size=80,
                    t2c={"\\n": ROXO, "→": GRAY_B})
        terceiroItem = Text("3. n - 1 → Limite atingido", font_size=80,
                            t2c={"n - 1": YELLOW, "→": GRAY_B})

        itensGrupo = VGroup(primeiroItem, segundoItem, terceiroItem).scale(0.44).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        bloco = VGroup(titulo, itensGrupo).arrange(DOWN, buff=0.9, aligned_edge=LEFT)
        bloco.move_to(ORIGIN)

        caixa = (
            SurroundingRectangle(
                titulo,
                corner_radius=0.3,
                buff=0.2
            )
            .set_stroke(BLUE, width=2)
            .set_fill(BLUE, opacity=0.1)
        )

        self.play(Create(caixa), Write(titulo), run_time=2)
        self.wait(0.6)
        self.play(FadeIn(primeiroItem, shift=RIGHT * 0.5), run_time=0.8)
        self.wait(0.7)
        self.play(FadeIn(segundoItem, shift=RIGHT * 0.5), run_time=0.8)
        self.wait(0.7)
        self.play(FadeIn(terceiroItem, shift=RIGHT * 0.5), run_time=0.8)
        self.wait(0.7)
 
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])  


class ExemploFgets(Scene):
    def construct(self):
        code = '''#include <stdio.h>

int main() {
    char nome[5];
    
    printf("Digite o nome (ex: Bruno): ");
    
    fgets(nome, 5, stdin);
    
    printf("O nome impresso será: %s\\n", nome);

    return 0;
}'''

        codigo = Code(
            code_string=code, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)

        bruno = Text("Bruno", font_size=80).scale(0.44)
        teclado = icone_teclado()
        teclado[0].set_stroke(BLUE)

        rot_stdin = Text("stdin", font_size=80, color=BLUE).scale(0.3)
        direita = VGroup(bruno, teclado, rot_stdin).arrange(DOWN, buff=0.4)
 
        partes = VGroup(codigo, direita).arrange(RIGHT, buff=1.0)

        quadrados = VGroup(*[
            Square(side_length=0.7, color=ROXO, stroke_width=3,
                   fill_color="#232326", fill_opacity=1)
            for _ in range(5)
        ]).arrange(RIGHT, buff=0.1).next_to(partes, DOWN, buff=0.8)
        indices = VGroup(*[
            Text(str(i), font_size=20, color=GRAY_B).next_to(q, DOWN, buff=0.12)
            for i, q in enumerate(quadrados)
        ])

        centralizaGrupos = VGroup(partes, quadrados, indices).move_to(ORIGIN)

        linhas = [l for l in codigo.code_lines if len(l.submobjects) > 0]
        self.play(
            LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in linhas], lag_ratio=0.25),
            run_time=4,
        )
        self.wait(0.6)

 
        def destaque(linha):
            ret = RoundedRectangle(
                width=linha.width + 0.3, height=0.35, corner_radius=0.10,
                color=ROXO, stroke_width=2, fill_color=ROXO, fill_opacity=0.2,
            ).move_to(linha.get_center())
            return ret.set_z_index(-1)
 
        dest_char = destaque(codigo.code_lines[3])
        dest_fgets = destaque(codigo.code_lines[7])

        self.play(FadeIn(dest_char), run_time=0.6)
        self.wait(0.4)
        self.play(FadeIn(dest_fgets), run_time=0.6)
        self.wait(0.8)

        self.play(FadeIn(teclado, shift=LEFT * 0.4), Write(rot_stdin))
        self.play(AddTextLetterByLetter(bruno, time_per_char=0.35))
        self.wait(0.6)

        interrogacao = Text("?", font_size=300, color=YELLOW, weight=BOLD)
        interrogacao.move_to(codigo.get_center()).set_opacity(0.9).set_z_index(5)

        self.play(FadeIn(interrogacao, scale=0.4))
        self.wait(1.5)
        self.play(FadeOut(interrogacao, scale=1.5))

        self.play(LaggedStart(*[GrowFromCenter(q) for q in quadrados], lag_ratio=0.12))
        self.play(FadeIn(indices))
        self.wait(0.5)

         # B, r, u, n descem; \0 no quadrado 4
        letras = list(bruno)                     
        base = bruno.get_bottom()[1]
        copias = []
        for i in range(4):
            c = letras[i].copy()
            self.add(c)
            dx = quadrados[i].get_x() - c.get_x()
            dy = (quadrados[i].get_y() - 0.2) - base
            self.play(c.animate.shift([dx, dy, 0]), run_time=0.8)
            copias.append(c)
 
        nulo = Text("\\0", font_size=80, color=WHITE).scale(0.32)
        nulo.set_opacity(0.5).move_to(quadrados[4].get_center())
        self.play(FadeIn(nulo, shift=DOWN * 0.6))
        self.wait(0.6)

         # "o" e "\n"
        o_fora = letras[4].copy().set_color(VERMELHO)
        self.add(o_fora)
        x_alvo = quadrados[4].get_right()[0] + 0.6
        self.play(o_fora.animate.shift([x_alvo - o_fora.get_x(),
                                        (quadrados[4].get_y() - 0.2) - base, 0]),
                  run_time=0.9)
        nl_fora = Text("\\n", font_size=80, color=VERMELHO).scale(0.38)
        nl_fora.next_to(o_fora, RIGHT, buff=0.15)
        nl_fora.set_y(o_fora.get_y())
        self.play(FadeIn(nl_fora, shift=DOWN * 0.5))
        self.wait(1.2)
        self.play(FadeOut(o_fora, shift=DOWN * 0.3))
        self.play(FadeOut(nl_fora, shift=DOWN * 0.3))
        self.wait(0.5)

        # Some o código e o teclado
        # entra o terminal com a saída 
        fila = VGroup(quadrados, indices, *copias, nulo)
 
        terminal = CustomTerminal(width=9, height=2.0, font_size=28)
        terminal.move_to([0, -0.75, 0])
        terminal.cursor.stretch_to_fit_width(0.12).stretch_to_fit_height(0.34)
        terminal.cursor.set_opacity(0)

        fantasma = fila.copy()                      # mede onde a fileira vai ficar
        VGroup(fantasma, terminal).arrange(DOWN, buff=1.0).move_to(ORIGIN)
 
        saem = (linhas + [dest_char, dest_fgets, teclado, bruno, rot_stdin])
        self.play(*[FadeOut(m) for m in saem], run_time=1)
        self.play(fila.animate.move_to(fantasma.get_center()), run_time=1.2)
        self.play(FadeIn(terminal))
        self.play(terminal.animate_typing("O nome impresso será: Brun", typing_speed=0.09))
        self.wait(1)

        saida = terminal.text_container[-1]

        # Cursor vai para a linha seguinte
        proxima = terminal.add_line("O nome impresso será: Brun")
        proxima.set_opacity(0)
        proxima.set_y(saida.get_y() - 0.5)


        self.wait(2)
        terminal.cursor.clear_updaters()
        terminal.cursor.set_opacity(1)
        self.play(*[FadeOut(m) for m in self.mobjects])   


class ScanfVsFgets(Scene):
    def construct(self):
        titulo = Text("fgets()", font_size=80).scale(0.8).move_to([0, 2.5, 0])
        self.play(Write(titulo))
        novo = Text("scanf()", font_size=80).scale(0.8).move_to([0, 2.5, 0])
        self.play(ReplacementTransform(titulo, novo))

        codigo = Text(
            'scanf("%s", nome);', font_size=80,
            t2c={"%s": "#98C379", "nome": ROXO},
        ).scale(0.34)
        codigo.next_to(novo, DOWN, buff=0.5)
        self.play(Write(codigo))

        teclado = icone_teclado()
        teclado[0].set_stroke(BLUE)
        teclado.move_to(LEFT * 5 + DOWN * 0.4)

        caixa = RoundedRectangle(
            width=2, height=1.2, corner_radius=0.3, color=GREEN,
        ).move_to(RIGHT * 4.3 + DOWN * 0.4)


        seta = Arrow(
            teclado.get_right(), caixa.get_left(),
            buff=0.2, color=GRAY, stroke_opacity=0.5,
        )

        grupoCentro = VGroup(teclado, seta, caixa).move_to(ORIGIN)
        rotulo = Text("nome", font_size=80, color=GREEN).scale(0.3)
        rotulo.next_to(caixa, UP, buff=0.15)

        self.play(FadeIn(teclado), Create(caixa), FadeIn(rotulo))
        self.play(GrowArrow(seta))

        # "Bruno" nasce no começo da seta e viaja por ela até a caixa
        bruno = Text("Bruno", font_size=80).scale(0.34)
        bruno.move_to(seta.get_start() + RIGHT * 0.6)
        bruno.set_z_index(2)
        self.play(FadeIn(bruno))
        self.play(bruno.animate.move_to(caixa), run_time=1.5)

        frase = Text("Prática e básica", font_size=80, color=YELLOW).scale(0.3).to_edge(DOWN, buff=2.2)
        self.play(Write(frase))
        self.wait(1.5)
        self.play(FadeOut(bruno), FadeOut(frase))

        bruno_d = Text("Bruno", font_size=80).scale(0.44)
        silva_d = Text("Silva", font_size=80).scale(0.44)
        digitado = VGroup(bruno_d, silva_d).arrange(RIGHT, buff=0.4)
        digitado.move_to(seta.get_start() + RIGHT * 0.3 + UP * 0.4, aligned_edge=LEFT)

        self.play(Succession(
            AddTextLetterByLetter(bruno_d),
            AddTextLetterByLetter(silva_d),
        ))

        # Barreira vertical entre as duas palavras
        x_espaco = (bruno_d.get_right()[0] + silva_d.get_left()[0]) / 2
        y_seta = seta.get_center()[1]
        barreira = Line(
            [x_espaco, y_seta + 0.9, 0],
            [x_espaco, y_seta - 0.9, 0],
            color=RED, stroke_width=8,
        )
        self.play(GrowFromCenter(barreira))

        self.play(bruno_d.animate.move_to(caixa), run_time=1.3)
        parou = Text("Parou no espaço", font_size=80, color=YELLOW).scale(0.3).to_edge(DOWN, buff=2.2)
        self.play(Write(parou), Indicate(silva_d, color=RED_D))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in (
            teclado, caixa, rotulo, seta, bruno_d, silva_d, barreira, parou,
        )])

        decl = Text("char nome[6];", font_size=80, color=GREEN).scale(0.3)
        decl.next_to(codigo, DOWN, buff=0.5)
        self.play(Write(decl))

        quadrados = VGroup(*[Square(side_length=0.95, color=GREEN, stroke_width=3, fill_color="#232326", fill_opacity=1) for _ in range(6)])
        quadrados.arrange(RIGHT, buff=0).move_to(LEFT * 2.2 + DOWN * 0.8)
        self.play(Create(quadrados))

        def pos(i):
            return quadrados[0].get_center() + RIGHT * 0.95 * i

        def letra(c, i, cor=WHITE):
            return Text(c, font_size=80, color=cor).scale(0.44).move_to(pos(i))

        # Caso correto
        bruno_q = VGroup(*[letra(c, i) for i, c in enumerate("Bruno")])
        nulo = letra("\\0", 5, YELLOW)
        self.play(LaggedStart(*[FadeIn(l) for l in bruno_q], lag_ratio=0.3))
        self.play(Write(nulo))
        cabe = Text(
            "5 letras + \\0 = 6 posições: cabe na memória",
            font_size=80, color=YELLOW,
        ).scale(0.28)
        cabe.next_to(quadrados, DOWN, buff=0.4)
        self.play(Write(cabe))
        self.wait(1.5)
        self.play(FadeOut(nulo), FadeOut(cabe))

        # caso com erro
        silva_q = VGroup(*[letra(c, i + 5) for i, c in enumerate("Silva")])
        self.play(LaggedStart(*[FadeIn(l) for l in silva_q], lag_ratio=0.4))

        nulo_fim = letra("\\0", 10, YELLOW)
        self.play(Write(nulo_fim))

        extras = VGroup(*silva_q[1:], nulo_fim)
        self.play(extras.animate.set_color(RED), quadrados.animate.set_stroke_color(RED))
        aviso = Text(
            "Estourou o vetor e o \\0 ficou de fora",
            font_size=80, color=RED,
        ).scale(0.28)
        aviso.to_edge(DOWN, buff=2.2)

        grupo = VGroup(quadrados, bruno_q, silva_q, nulo_fim)
        for d in [LEFT * 0.12, RIGHT * 0.24, LEFT * 0.24, RIGHT * 0.12]:
            self.play(grupo.animate.shift(d), run_time=0.07)
        self.play(Write(aviso))

        
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])  



class ExemploSizeof(Scene):
    def construct(self):
        W = config.frame_width / 2 - 1.0               # largura de cada painel

        def decl(n, tam):
            t = T(f"char nome[{n}];", font_size=tam, color=WHITE)
            parte(t, "nome").set_color(ROXO)
            parte(t, str(n)).set_color(YELLOW)
            return t

        def fg(arg, tam):
            t = T(f"fgets(nome, {arg}, stdin);", font_size=tam, color=WHITE)
            parte(t, "nome").set_color(ROXO)           
            parte(t, arg).set_color(YELLOW)           
            parte(t, "stdin").set_color(BLUE)          
            return t

        maior = fg("sizeof(nome)", 44)
        tam = min(34, 40 * (W - 1.0) / maior.width)

        titulo = T("O tamanho do vetor", font_size=80, color=WHITE).scale(0.8).move_to([0, 2.5, 0])

        assinatura = Text(
            "fgets(str, n, stream);",
            font_size=80,
            color=WHITE
        ).scale(0.8).move_to([0, 2.5, 0])

        assinatura[6:9].set_color(ROXO)    # str
        assinatura[11].set_color(YELLOW)   # n
        assinatura[13:20].set_color(BLUE)  # stream

        d0, f0 = decl(20, 44), fg("5", 44)
        VGroup(d0, f0).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(ORIGIN)
        nota = nota_sob(parte(f0, "5"), "Número fixo", YELLOW)

        d_e, f_e = decl(20, tam), fg("5", tam)
        d_d, f_d6, f_dsz = decl(20, tam), fg("5", tam), fg("sizeof(nome)", tam)
        col_e = VGroup(d_e, f_e).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        col_d = VGroup(d_d, f_dsz).arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        paineis = VGroup(*[
            RoundedRectangle(width=W, height=col_d.height + 1.2, corner_radius=0.2,
                             color=GRAY_D, stroke_width=2,
                             fill_color="#232326", fill_opacity=1)
            for _ in range(2)
        ]).arrange(RIGHT, buff=0.4)
        for col, painel in zip((col_e, col_d), paineis):
            col.align_to(painel, LEFT).shift(RIGHT * 0.5)
            col.match_y(painel)
        paineis.move_to(ORIGIN).set_z_index(-1)        
        for col, painel in zip((col_e, col_d), paineis):   # acompanha os painéis
            col.align_to(painel, LEFT).shift(RIGHT * 0.5)
            col.match_y(painel)
        f_d6.align_to(f_dsz, LEFT).match_y(f_dsz)          # o 5 fica onde ficará o sizeof

        tit_e = T("Tamanho fixo", font_size=80, color=WHITE).scale(0.3).next_to(paineis[0], UP, buff=0.2)
        tit_d = T("Com sizeof()", font_size=80, color=WHITE).scale(0.3).next_to(paineis[1], UP, buff=0.2)

        x_e = icone_x()
        txt_e = T("O 5 não foi atualizado!", font_size=80, color=VERMELHO).scale(0.3)
        msg_e = VGroup(x_e, txt_e).arrange(RIGHT, buff=0.25)
        ok_d = icone_ok()
        txt_d = T("Considera o novo tamanho", font_size=80, color=VERDE).scale(0.3)
        msg_d = VGroup(ok_d, txt_d).arrange(RIGHT, buff=0.25)

        # para que a mensagem sempre caiba no painel
        fator = min(1.0, (W - 0.4) / max(msg_e.width, msg_d.width))
        msg_e.scale(fator).next_to(paineis[0], DOWN, buff=0.5)
        msg_d.scale(fator).next_to(paineis[1], DOWN, buff=0.5)
        msg_d.match_y(msg_e)

        
        pergunta = T("E se o vetor mudar de tamanho?", font_size=80, color=YELLOW).scale(0.34)
        pergunta.next_to(VGroup(txt_e, txt_d), DOWN, buff=0.6).set_x(0)
        conclusao = T("sizeof() evita valores fixos!", font_size=80, color=WHITE).scale(0.38)
        parte(conclusao, "sizeof()").set_color(YELLOW)
        conclusao.move_to(pergunta)

        tudo = VGroup(paineis, col_e, col_d, f_d6, tit_e, tit_d, msg_e,
                      msg_d, pergunta, conclusao)
        tudo.set_y(0)
        tudo.shift(DOWN * 0.8)

        d20_e = decl(10, tam).align_to(d_e, LEFT).match_y(d_e)
        d20_d = decl(10, tam).align_to(d_d, LEFT).match_y(d_d)

        self.play(Write(titulo))
        self.play(FadeIn(d0, shift=UP * 0.2))
        self.play(Write(f0))
        self.play(Indicate(parte(f0, "5"), color=YELLOW, scale_factor=1.8),
                  FadeIn(nota, shift=UP * 0.2))
        self.wait(1.2)

        self.play(FadeOut(nota), FadeOut(titulo, shift=DOWN * 0.3))
        self.play(FadeIn(assinatura, shift=UP * 0.3))

        self.play(
            ReplacementTransform(d0, d_e),
            ReplacementTransform(f0, f_e),
            TransformFromCopy(d0, d_d),
            TransformFromCopy(f0, f_d6),
            run_time=1.5,
        )

        self.play(
            LaggedStart(
                Create(paineis[0]),
                Create(paineis[1]),
                lag_ratio=0.3,
            ),
            FadeIn(tit_e),
            FadeIn(tit_d),
            run_time=1.5,
        )

        self.wait(0.6)
   
        # o 6 dá lugar ao sizeof(nome)
        antes, seis_d, depois = (parte(f_d6, "fgets(nome, "), parte(f_d6, "5"),
                                 parte(f_d6, ", stdin);"))
        antes_sz, sizeof_g, depois_sz = (parte(f_dsz, "fgets(nome, "),
                                         parte(f_dsz, "sizeof(nome)"),
                                         parte(f_dsz, ", stdin);"))
        self.remove(f_d6)                       
        self.add(antes, seis_d, depois)
        self.play(
            FadeOut(seis_d, shift=UP * 0.3),
            FadeIn(sizeof_g, shift=UP * 0.3),
            ReplacementTransform(antes, antes_sz),
            ReplacementTransform(depois, depois_sz),
            run_time=1.4,
        )
        self.wait(1)

        # o vetor muda de tamanho
        self.play(Write(pergunta))
        self.wait(0.8)
        self.play(ReplacementTransform(d_e, d20_e),
                  ReplacementTransform(d_d, d20_d), run_time=1.3)
        self.play(Indicate(parte(d20_e, "10"), color=YELLOW, scale_factor=1.4),
                  Indicate(parte(d20_d, "10"), color=YELLOW, scale_factor=1.4))
        self.wait(0.6)

        # tamanho fixo
        arg_e = parte(f_e, "5")
        self.play(Indicate(arg_e, color=VERMELHO, scale_factor=1.6))
        self.play(arg_e.animate.set_color(VERMELHO))
        self.play(Create(x_e), Write(txt_e))
        self.wait(1)

        # sizeof
        self.play(Indicate(sizeof_g, color=YELLOW, scale_factor=1.15))
        self.play(Create(ok_d), Write(txt_d))
        self.wait(1.5)

        
        self.play(FadeOut(pergunta), FadeOut(x_e), FadeOut(ok_d), FadeOut(txt_e),
                  FadeOut(txt_d))
        self.play(Indicate(sizeof_g, color=YELLOW, scale_factor=1.15), Write(conclusao))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects if m is not assinatura])

        self.play(assinatura.animate.scale(0.5).move_to(ORIGIN + UP * 1.5))
        self.play(assinatura.animate.shift(LEFT * 2))
        strings = Text("strings", font_size=80).scale(0.4).next_to(assinatura, RIGHT, buff=2.5)
        seta = Arrow(assinatura.get_right(), strings.get_left(), buff=0.12, color=YELLOW,
                         stroke_width=3, tip_length=0.3)
        grupoString = VGroup(assinatura, seta, strings)
        tipos = [
            ("int", BLUE_D, "42"),
            ("float", RED_E , "3.14")
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
        cards.arrange(RIGHT, buff=0.5).move_to(ORIGIN + DOWN * 1)

        for card in cards:
            card.shift(DOWN * 5) #posição inicial na tela

        scan = Text("Scan formatted", t2c = {"Scan": ROXO, "formatted": BLUE}, font_size = 80).scale(0.44).move_to([0, 2.5, 0])
        scanf = Text("scanf()", font_size=80).scale(0.8).move_to([0, 2.5, 0])


        self.play(FadeIn(seta, shift=UP*0.4))
        self.play(FadeIn(strings, shift=RIGHT * 0.3))
        for card in cards:
            self.play(card.animate.shift(UP * 5), run_time = 0.5)
            self.wait(0.2)
        filtro = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            fill_color=GRAY_B,
            fill_opacity=0.3,
            stroke_width=0
        ).set_z_index(10)

        pensando = ImageMobject("images/pensar.png")
        pensando.scale(1).move_to(ORIGIN)
        pensando.set_z_index(12)

        self.play(FadeIn(filtro))

        self.play(FadeIn(pensando, scale=0.6, shift = LEFT * 5))
        self.wait(0.4)
        self.play(FadeOut(pensando, shift = RIGHT * 5))
        self.play(FadeOut(filtro), run_time=0.6)
        self.play(grupoString.animate.move_to([0, 2.5, 0]).scale(1.3))
        self.play(ReplacementTransform(grupoString, scan))
        self.wait(0.65)
        self.play(ReplacementTransform(scan, scanf))

        self.play(cards.animate.move_to(ORIGIN))
        self.play(Indicate(cards[0], color=PURE_BLUE))
        self.play(Indicate(cards[1], color=PURE_RED))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])  

class Scanf(Scene):
    def construct(self):
        scanfVar = Text('scanf("especificadores", &variavel);', font_size=80).scale(0.44).move_to(ORIGIN)
      
        scanfIdade = Text('scanf("%d", &idade);', font_size=80).scale(0.8)
        p_d, p_i = scanfIdade[6:10], scanfIdade[12:18]
        
        scanfVar.set_color(WHITE)

        self.play(Write(scanfVar))
        self.play(ReplacementTransform(scanfVar, scanfIdade))
        self.play(p_d.animate.set_color(GREEN))
        self.play(p_i.animate.set_color(ROXO))
        self.play(Indicate(scanfIdade[12], color=YELLOW))
        self.play(
            scanfIdade.animate.shift(UP * 2.5)
        )

        dados = [
            ["tipo", "printf", "scanf"],
            ["int", "%d", "%d"],
            ["float", "%f", "%f"],
            ["double", "%f", "%lf"],
            ["char", "%c", "%c"]
        ]

        # Dimensões das células
        largura = [2.4, 2.4, 2.4]
        altura = 0.75

        tabela = VGroup()
        celula_lf = None

        for i, linha_dados in enumerate(dados):
            linha = VGroup()

            for j, valor in enumerate(linha_dados):

                # Retângulo da célula
                fundo = Rectangle(
                    width=largura[j],
                    height=altura,
                    stroke_color=GREY_B,
                    stroke_width=1.5,
                    fill_color=BLUE if i == 0 else (
                        GREY_E if i % 2 == 1 else GREY_D
                    ),
                    fill_opacity=0.6
                )

                # Texto da célula
                texto = Text(
                    valor,
                    font_size=80,
                    color=WHITE
                ).scale(0.3)

                texto.move_to(fundo.get_center())

                celula = VGroup(fundo, texto)
                linha.add(celula)

                # Guarda a célula %lf
                if i == 3 and j == 2:
                    celula_lf = celula

            linha.arrange(RIGHT, buff=0)
            tabela.add(linha)

        tabela.arrange(DOWN, buff=0)
        tabela.move_to(ORIGIN + DOWN * 0.8)
        
        self.play(
            LaggedStart(
                *[FadeIn(celula) for celula in tabela[0]],
                lag_ratio=0.2
            )
        )

        for linha in tabela[1:]:
            self.play(
                LaggedStart(
                    *[FadeIn(celula) for celula in linha],
                    lag_ratio=0.15
                ),
                run_time=0.6
            )

        self.play(
            Indicate(celula_lf, color=ROXO, scale_factor=1.15)
        )
        self.play(celula_lf[0].animate.set_fill(ROXO, opacity=0.6))
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

        code = '''#include <stdio.h>

int main(){
    float p1, p2, p3, p4;
    double media;
    
    printf("Digite as notas das 4 provas: \\n");
    scanf("%f%f%f%f", &p1, &p2, &p3, &p4);
    
    media = (p1 + p2 + p3 + p4)/4.0;
    printf("\\nMEDIA: %.2f\\n", media);
    
    return 0;
}
'''
        
        codigo = Code(
            code_string=code, 
            language="c",
            formatter_style="material",
            add_line_numbers=False,
            background="rectangle", 
            background_config={
                "fill_opacity": 0,
                "stroke_width": 0
                }
        ).scale(0.8).move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[Write(linha) for linha in codigo.code_lines],
                lag_ratio=0.1
            )
        )

        self.play(codigo.animate.shift(UP * 1).scale(1))

        # Criar terminal
        terminal = CustomTerminal(
            width=8,
            height=1.8,
            font_size=20
        )

        # Aumentar o espaçamento entre as linhas
        terminal._place_line = lambda line: (
            line.move_to(
                terminal.bg.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.3,
                aligned_edge=UL
            ) if len(terminal.text_container) == 0 else
            line.next_to(
                terminal.text_container[-1],
                DOWN,
                buff=0.2,
                aligned_edge=LEFT
            )
        )

        terminal.move_to(DOWN * 2.3)

        self.play(FadeIn(terminal))

        # Mensagem e entrada das notas
        self.play(
            terminal.animate_typing(
                "Digite as notas das 4 provas: ",
                typing_speed=0.04
            )
        )
        self.play(
            terminal.animate_typing(
                "5.5 7.5 3.0 6.0",
                typing_speed=0.08
            )
        )

        self.wait(1)

        # Resultado
        self.play(
            terminal.animate_typing(
                "MEDIA: 5.50",
                typing_speed=0.08
            )
        )
        # Impedir que o updater reposicione o cursor
        terminal.cursor.clear_updaters()

        # Posicionar cursor abaixo da média
        self.play(
            terminal.cursor.animate.move_to(
                terminal.text_container[-1].get_left()
                + DOWN * 0.35
            )
        )

        terminal.cursor.set_opacity(1)

        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects])

class ScanfSemEComercial(Scene):
    def construct(self):
        errada = Text(
            'scanf("%s", &nome);', font_size=80,
            t2c={"%s": "#98C379", "&nome": ROXO},
        ).scale(0.5).move_to(UP * 2)
        self.play(Write(errada))
        self.play(Indicate(errada[12], color=RED, scale_factor=1.8))
 
        certa = Text(
            'scanf("%s", nome);', font_size=80,
            t2c={"%s": "#98C379", "nome": ROXO},
        ).scale(0.5).move_to(UP * 2)
        self.play(TransformMatchingShapes(errada, certa))
        self.wait(0.5)
 
        quadrados = VGroup()

        for i in range(5):
            q = Square(
                side_length=1.2,
                color=GREEN,
                stroke_width=3,
                fill_color="#232326",
                fill_opacity=1
            )

            indice = Text(str(i), font_size=18, color=WHITE)
            indice.next_to(q, DOWN, buff=0.15)

            quadrados.add(VGroup(q, indice))

        quadrados.arrange(RIGHT, buff=0.08).move_to(DOWN * 0.8)
        self.play(LaggedStart(*[GrowFromCenter(q) for q in quadrados], lag_ratio=0.1)) 
        lado = 1.2  # lado de cada quadrado

        # nome (no código) aponta para o primeiro quadrado
        seta = Arrow(
            certa[11:15].get_bottom(), quadrados[0].get_top(),
            buff=0.15, color=ROXO,
        )
        endereco = Text("&nome[0]", font_size=80).scale(0.3).move_to(seta).shift(RIGHT * 1.2)
        self.play(GrowArrow(seta), Indicate(quadrados[0][0], color=ROXO, scale_factor=1.15), FadeIn(endereco, shift=UP*0.3))

        frase = MarkupText('<i>nome</i> = endereço da string', font_size=80, color=YELLOW).scale(0.34)
        frase.to_edge(DOWN, buff=1.2)
        self.play(Write(frase))
        self.wait(2)
        
        self.wait(2)
 
        self.play(FadeOut(seta), FadeOut(endereco), FadeOut(frase))

        # segunda parte
 
        teclado = icone_teclado()
        teclado[0].set_stroke(BLUE)
        teclado.move_to(LEFT * 5.2 + DOWN * -1)
        digitado = Text("Bruno123", font_size=80).scale(0.34)
        digitado.next_to(teclado, RIGHT, buff=0.4)

        self.play(quadrados.animate.shift(LEFT * 2))
        alvos = [quadrados[i][0].get_center() for i in range(5)]

        # Posições extras após o último quadrado
        alvos += [
            quadrados[4][0].get_center() + RIGHT * lado * i
            for i in range(1, 5)
        ]
        self.play(FadeIn(teclado, shift=LEFT * 0.4))
        self.play(AddTextLetterByLetter(digitado, time_per_char=0.25))
        self.wait(0.5)
 
        copias = [digitado[i].copy() for i in range(8)]
        self.add(*copias)
 
        self.play(LaggedStart(
            *[copias[i].animate.move_to(alvos[i]) for i in range(5)],
            lag_ratio=0.5,
        ))
        self.wait(0.5)
 
        # As extras (1, 2, 3) continuam saindo fora do vetor, e depois o \0
        self.play(LaggedStart(
            *[copias[i].animate.move_to(alvos[i]) for i in range(5, 8)],
            lag_ratio=0.5,
        ))
        nulo = Text("\\0", font_size=80, color=YELLOW).scale(0.44).move_to(alvos[8])
        self.play(FadeIn(nulo, shift=DOWN * 0.3))
        self.wait(0.5)
 
        self.play(
            *[c.animate.set_color(RED) for c in copias[5:]],
            nulo.animate.set_color(RED),
            quadrados.animate.set_stroke_color(RED),
        )
        self.play(FadeOut(teclado), FadeOut(digitado))
        vetor = VGroup(quadrados, *copias[:5])
        self.play(Wiggle(vetor, scale_value=1.08, rotation_angle=0.015 * TAU,
                         n_wiggles=8, run_time=1.5))
 
        overflow = Text("Buffer Overflow", font_size=80, color=RED).scale(0.5)
        overflow.move_to(DOWN * 2.2)
        self.play(Write(overflow), run_time=0.6)
 
        
        self.wait(2)
 
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob is not overflow]
        )

        self.play(
            overflow.animate
                .set_color(WHITE)
                .scale(1.6)
                .move_to([0, 2.5, 0])
        )

        sub = Text("estouro de buffer", font_size=80, color=GRAY_B).scale(0.30)
        sub.next_to(overflow, DOWN, buff=0.25)
        self.play(FadeIn(sub, shift=UP * 0.2))
    
        # Limite do buffer (círculo tracejado)
        centro = DOWN * 0.6
        limite = DashedVMobject(Circle(radius=1.3, color=WHITE, stroke_width=3), num_dashes=30)
        limite.move_to(centro)
        rotulo = Text("limite do buffer", font_size=80, color=WHITE).scale(0.3)
        rotulo.next_to(limite, RIGHT, buff=0.4).shift(UP * 0.6)
        self.play(Create(limite), FadeIn(rotulo))
    
        # Balão e dados
        balao = Circle(radius=0.4, color=BLUE, fill_color=BLUE, fill_opacity=0.8).move_to(centro)
        seta = Arrow(LEFT * 5 + centro, LEFT * 2.6 + centro, buff=0, color=BLUE)
        dados = Text("dados", font_size=80, color=BLUE).scale(0.34).next_to(seta, UP, buff=0.15)
        self.play(FadeIn(balao), GrowArrow(seta), FadeIn(dados))
    
        # Enche até o limite
        self.play(balao.animate.scale(1.3 / 0.4), run_time=2.5)
        self.wait(0.5)
    
        # passa do limite
        self.play(Indicate(seta, color=BLUE, scale_factor=1.2))
        self.play(
            balao.animate.scale(1.35).set_color(RED),
            run_time=1.5,
        )
        self.play(Wiggle(balao, scale_value=1.05, n_wiggles=8, run_time=1))
    
        # Estoura
        self.play(
            Flash(centro, color=RED, flash_radius=2.4, line_length=0.5),
            FadeOut(balao, scale=1.4),
            run_time=0.8,
        )
    
        frase = Text("Mais dados do que o espaço suporta", font_size=80, color=YELLOW).scale(0.34)
        frase.to_edge(DOWN * 1.2, buff=0.6)
        self.play(Write(frase), run_time=0.6)
        self.wait(2.5)
    
        self.play(*[FadeOut(m) for m in self.mobjects])
    

class UsuarioDigitaMais(Scene):
    def construct(self):
        y_barra = -0.8  # altura da barra na tela
 
        codigo = Text(
            "char nome[50];", font_size=80, t2c={"50": YELLOW},
        ).scale(0.5).move_to([0, 2.9, 0])
        self.play(Write(codigo))
 
        pista = Rectangle(
            width=8, height=0.74, fill_color="#232326", fill_opacity=1, stroke_width=0,
        ).move_to([0, y_barra, 0])
        contorno = Rectangle(width=4, height=0.7, color=GREEN, stroke_width=4)
        contorno.move_to([-2, y_barra, 0])
 
        chave_ok = Brace(contorno, DOWN, color=GREEN, buff=0.15)
        texto_ok = Text("50 caracteres reservados", font_size=80, color=GREEN).scale(0.32)
        texto_ok.next_to(chave_ok, DOWN, buff=0.15)
 
        self.play(FadeIn(pista), Create(contorno))
        self.play(GrowFromCenter(chave_ok), FadeIn(texto_ok, shift=UP * 0.1))
 
        # Contador do que o usuário digita
        t = ValueTracker(0)
        numero = always_redraw(lambda: Text(
            str(int(t.get_value())), font_size=80,
            color=RED if t.get_value() > 50 else WHITE,
        ).scale(0.9).move_to([0, 1.7, 0]))
        legenda = Text(
            "caracteres digitados pelo usuário", font_size=80, color=GRAY_B,
        ).scale(0.34).move_to([0, 1.05, 0])
 
        dentro = always_redraw(lambda: Rectangle(
            width=max(min(t.get_value(), 50) * 0.08, 0.001), height=0.7,
            fill_color=GREEN, fill_opacity=0.8, stroke_width=0,
        ).move_to([-4, y_barra, 0], aligned_edge=LEFT))
        fora = always_redraw(lambda: Rectangle(
            width=max((t.get_value() - 50) * 0.08, 0.001), height=0.74,
            fill_color=RED, fill_opacity=0.8, stroke_width=0,
        ).move_to([0, y_barra, 0], aligned_edge=LEFT))
 
        self.play(FadeIn(numero), FadeIn(legenda))
        self.add(dentro, fora)
 
        self.play(t.animate.set_value(50), run_time=2, rate_func=linear)
        self.wait(0.5)
 
        self.play(t.animate.set_value(100), run_time=2, rate_func=linear)
 
        # para o tremor não ficar sobrescrito
        dentro.clear_updaters()
        fora.clear_updaters()
        numero.clear_updaters()
 
        chave_fora = Brace(fora, UP, color=RED, buff=0.13)
        texto_fora = Text("50 caracteres fora do vetor", font_size=80, color=RED).scale(0.32)
        texto_fora.next_to(chave_fora, UP, buff=0.15)
        self.play(
            GrowFromCenter(chave_fora),
            FadeIn(texto_fora, shift=UP * 0.1),
            Wiggle(fora, scale_value=1.1, n_wiggles=6),
        )
        self.wait(1.5)
 
        # segunda parte
        self.play(FadeOut(codigo), FadeOut(legenda), FadeOut(t), FadeOut(numero), FadeOut(chave_ok), FadeOut(texto_ok))

        rot_viz = Text("Memória vizinha", font_size=80, color=BLUE_B).scale(0.4)
        rot_viz.next_to(fora, DOWN, buff=0.25)
        texto_sobre = Text(
            "Sobrescreve a memória vizinha", font_size=80, color=RED,
        ).scale(0.32).move_to(texto_fora)
 
        self.play(FadeIn(rot_viz, shift=UP * 0.1))
        self.play(
            ReplacementTransform(texto_fora, texto_sobre),
            Wiggle(fora, scale_value=1.08, n_wiggles=6, run_time=1.2),
        )
        self.wait(1)
 
        # Consequências
        icone_x = VGroup(
            Line([-0.17, 0.17, 0], [0.17, -0.17, 0]),
            Line([-0.17, -0.17, 0], [0.17, 0.17, 0]),
        ).set_color(RED).set_stroke(width=7)
        txt_trav = Text("Travamento do programa", font_size=80).scale(0.36)
        bloco_trav = VGroup(icone_x, txt_trav).arrange(RIGHT, buff=0.25)
        bloco_trav.move_to([-3.3, 2.2, 0])
 
        tri = Triangle(color=YELLOW, stroke_width=3.5).scale(0.28)
        exclama = Text("!", font_size=80, color=YELLOW).scale(0.3).move_to(tri).shift(DOWN * 0.03)
        txt_seg = Text("Brechas de segurança", font_size=80).scale(0.36)
        bloco_seg = VGroup(VGroup(tri, exclama), txt_seg).arrange(RIGHT, buff=0.25)
        bloco_seg.move_to([3.3, 2.2, 0])
 
        bloco_trav.save_state()
        bloco_seg.save_state()
        for bloco in (bloco_trav, bloco_seg):
            bloco.move_to(fora.get_center()).scale(0.1).set_opacity(0)
        self.add(bloco_trav, bloco_seg)
 
        self.play(Restore(bloco_trav), run_time=1.5)
        self.wait(0.5)
        self.play(Restore(bloco_seg), run_time=1.5)
        self.wait(2.5)
 
        self.play(*[FadeOut(m) for m in self.mobjects])


class ComoResolver(Scene):
    def construct(self):
        titulo = Text("Como resolver esse problema?", font_size=80).scale(0.6).move_to([0, 2.5, 0])
        self.play(Write(titulo))
        self.wait(0.5)
 
        linha1 = Text(
            'scanf("%4s", nome);', font_size=80, color="#EEFFFF",
            t2c={"%4s": YELLOW},
        ).scale(0.5).move_to(ORIGIN)
        self.play(Write(linha1))
        self.play(Indicate(linha1[7:10], color=YELLOW, scale_factor=1.5))
 
        linha2 = Text(
            "fgets(nome, sizeof(nome), stdin);", font_size=80, color="#EEFFFF",
            t2c={"fgets": "#82AAFF"},
        ).scale(0.5).move_to(linha1)
        self.play(ReplacementTransform(linha1, linha2))

        p_str, p_n, p_stream = linha2[6:10], linha2[11:24], linha2[26:31]
        self.play(
            p_str.animate.set_color(ROXO),
            p_n.animate.set_color(YELLOW),
            p_stream.animate.set_color(BLUE),
        )
 
        ok = VMobject(color=GREEN, stroke_width=7)
        ok.set_points_as_corners([[-0.2, 0.0, 0], [-0.07, -0.15, 0], [0.22, 0.18, 0]])
        melhor = Text("A melhor forma", font_size=80, color=GREEN).scale(0.4)
        bloco_melhor = VGroup(ok, melhor).arrange(RIGHT, buff=0.25)
        bloco_melhor.next_to(linha2, DOWN, buff=0.6)
        self.play( Circumscribe(linha2, color=GREEN), Create(ok), Write(melhor))
        self.wait(2.5)
 
        self.play(*[FadeOut(m) for m in self.mobjects])


class ResumoAula7(Scene):
    def construct(self):
        titulo = Text("Resumo da aula", font_size=80).scale(0.7).move_to([0, 2.5, 0])
        self.play(Write(titulo))
        self.wait(0.4)
 
        topicos = [
            ("puts(): imprime e pula a linha", {"puts": ROXO}),
            ("printf(): saída formatada", {"printf": VERDE}),
            ("fgets(): lê strings com limite", {"fgets": BLUE}),
        ]

        topicos2 = [
            ("sizeof(nome): evita tamanho fixo", {"sizeof": YELLOW}),
            ("scanf(): para no espaço e não usa &", {"scanf": ORANGE, "&": VERMELHO}),
            ("Buffer Overflow: dados além do espaço", {"Buffer Overflow": VERMELHO})
        ]

        altura_x = Text("x", font_size=80).scale(0.42).height  # altura das minúsculas
        pontos, textos = VGroup(), VGroup()
 
        for i, (texto, cores) in enumerate(topicos):
            y = 0.8 - i * 0.75
            t = Text(texto, font_size=80, t2c=cores).scale(0.42)
            t.shift(UP * (y - max(m.get_bottom()[1] for m in t)))
            t.shift(RIGHT * (0.3 - t.get_left()[0]))
            pontos.add(Dot(radius=0.06).move_to([0, y + altura_x / 2, 0]))
            textos.add(t)
 
        VGroup(pontos, textos).set_x(0)  # bloco centralizado na tela
 
        for ponto, t in zip(pontos, textos):
            self.play(FadeIn(VGroup(ponto, t), shift=UP * 0.2), run_time=0.8)
            self.wait(0.4)
        
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob is not titulo]
        )

        pontos2, textos2 = VGroup(), VGroup()
         
        for i, (texto, cores) in enumerate(topicos2):
            y = 0.8 - i * 0.75
            t = Text(texto, font_size=80, t2c=cores).scale(0.42)
            t.shift(UP * (y - max(m.get_bottom()[1] for m in t)))
            t.shift(RIGHT * (0.3 - t.get_left()[0]))
            pontos2.add(Dot(radius=0.06).move_to([0, y + altura_x / 2, 0]))
            textos2.add(t)
    
        VGroup(pontos2, textos2).set_x(0)  # bloco centralizado na tela
    
        for ponto, t in zip(pontos2, textos2):
            self.play(FadeIn(VGroup(ponto, t), shift=UP * 0.2), run_time=0.8)
            self.wait(0.4)
 
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects])
 
        ok = VMobject(color=VERDE, stroke_width=7)
        ok.set_points_as_corners([[-0.2, 0.0, 0], [-0.07, -0.15, 0], [0.22, 0.18, 0]])
        melhor = Text("Para ler strings, prefira o fgets()", font_size=80, t2c={"fgets": BLUE}).scale(0.4)
        bloco = VGroup(ok, melhor).arrange(RIGHT, buff=0.25).move_to(ORIGIN)
        caixa = (
            SurroundingRectangle(bloco, corner_radius=0.3, buff=0.25)
            .set_stroke(VERDE, width=2)
            .set_fill(VERDE, opacity=0.1)
        )
        self.play(Create(caixa), Create(ok), Write(melhor))
        self.play(Circumscribe(bloco, color=VERDE))
        self.wait(2)
 
        self.play(*[FadeOut(m) for m in self.mobjects])

        #FINAL
        text = Text("Para a próxima aula:", font_size = 45)
        text2 = Text("Operadores matemáticos", t2c={"Operadores": PURPLE}, font_size=50)
        rawTitle = VGroup(text, text2).arrange(DOWN, aligned_edge = LEFT, buff = 0.2)

        self.play(Write(text), run_time = 1.5)
        self.play(Write(text2), run_time = 1.5)
        self.wait()

class Creditos(Scene):
    def construct(self):
        #creditos
        logo = ImageMobject("images/icon_c.png").scale(0.2)
        logoOrigin=logo.copy().move_to(UP*8).rotate(PI)
        cursor=ImageMobject("images/cursor.png").move_to(DOWN*6+LEFT*2).scale(0.05)
        titulo=Text("Créditos", font_size=80)
        titulo.color="#AA77C7"

   
        diretor = VGroup(T2("Diretor", color = "#AA77C7", font_size=60), T2("Rainier R. Waki", font_size=50)).arrange(DOWN, buff=0.3)
        tutor = VGroup(T2("Tutor", color = "#AA77C7", font_size=60), T2("Alyson V. Isaluski", font_size=50)).arrange(DOWN, buff=0.3)
        animadores = VGroup(
            T2("Animadores", color = "#AA77C7", font_size=60),
            VGroup(
                T2("Eduarda dos R. Mendes", font_size=50),
                T2("Leandro M. M. Hyeda", font_size=50)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        editora = VGroup(T2("Editora", color = "#AA77C7", font_size=60), T2("Sophia B. Peraza", font_size=50)).arrange(DOWN, buff=0.3)
        roteirista = VGroup(
            T2("Roteiristas", color = "#AA77C7", font_size=60),
            VGroup(
                T2("Alyson V. Isaluski", font_size=50),
                T2("Kia de P. Marins", font_size=50)
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
 