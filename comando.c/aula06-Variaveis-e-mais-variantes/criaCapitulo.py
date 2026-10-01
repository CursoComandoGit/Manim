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
    cena.wait()
    cena.play(animR)
    cena.remove(grupoCompleto)
    cena.play(*[obj.animate.set_opacity(1) for obj in cena.mobjects])
    
    cena.wait()
