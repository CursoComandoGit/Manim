from manim import *

class CustomTerminal(VGroup):
    def __init__(self, width=7, height=4.5, title="manim@manim: ~", font_size=16, **kwargs):
        super().__init__(**kwargs)
        self.font_size = font_size
        
        # Base do Terminal
        self.bg = Rectangle(width=width, height=height, color="#2c0822", fill_opacity=0.9, stroke_width=0)
        self.top_bar = Rectangle(width=width, height=0.4, color="#1E1E1E", fill_opacity=1, stroke_width=0)
        self.top_bar.next_to(self.bg, UP, buff=0)
        
        self.title_text = Text(title, font_size=12, font="Monospace").move_to(self.top_bar)
        
        # Botões da janela (Troquei para evitar SVGs)
        self.btn_close = Circle(radius=0.08, color="#FF5F56", fill_opacity=1, stroke_width=0)
        self.btn_close.move_to(self.top_bar.get_right() + LEFT * 0.3)
        self.btn_min = Circle(radius=0.08, color="#FFBD2E", fill_opacity=1, stroke_width=0)
        self.btn_min.next_to(self.btn_close, LEFT, buff=0.15)
        self.btn_max = Circle(radius=0.08, color="#27C93F", fill_opacity=1, stroke_width=0)
        self.btn_max.next_to(self.btn_min, LEFT, buff=0.15)
        
        # Container de Textos e Cursor
        self.text_container = VGroup()
        self.cursor = Rectangle(width=0.08, height=0.25, color=WHITE, fill_opacity=1, stroke_width=0)
        
        self.add(
            self.bg, self.top_bar, self.title_text, 
            self.btn_close, self.btn_min, self.btn_max, 
            self.text_container, self.cursor
        )

        self.time_passed = 0
        self.cursor.add_updater(self._update_cursor_position)

    def _update_cursor_position(self, mob, dt):
        """Faz o cursor seguir o último caractere desenhado na tela."""

        if self.bg.get_fill_opacity() < 0.8:
            return

        # Lógica de piscar o cursor a cada 0.5 segundos
        self.time_passed += dt
        if self.time_passed % 1.0 < 0.5: 
            mob.set_opacity(1)
        else:
            mob.set_opacity(0)
        if len(self.text_container) == 0:
            mob.set_opacity(0)
            mob.move_to(self.bg.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.3)
            return
            
        last_element = self.text_container[-1]

        extra_buff = 0.15 if getattr(last_element, "has_trailing_space", False) else 0.05

        chars = [c for c in last_element.get_family() if not c.submobjects]
        visible_chars = [c for c in chars if c.get_fill_opacity() > 0 or c.get_stroke_opacity() > 0]
        
        if visible_chars:
            if len(visible_chars) == len(chars):
                mob.move_to(last_element.get_right(), aligned_edge=LEFT)
                mob.shift(RIGHT * extra_buff)
            else:
                mob.next_to(visible_chars[-1], RIGHT, buff=0.05)

                mob.set_opacity(1)
                self.time_passed = 0
        else:
            target_x = self.text_container[0].get_left()[0] if len(self.text_container) > 0 else (self.bg.get_left()[0] + 0.2)
            mob.move_to([target_x, last_element.get_y(), 0], aligned_edge=LEFT)
            
    def _place_line(self, line):
        """Calcula a posição vertical correta da nova linha."""
        if len(self.text_container) == 0:
            line.move_to(self.bg.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.3, aligned_edge=UL)
        else:
            line.next_to(self.text_container[-1], DOWN, buff=0.05, aligned_edge=LEFT)

    def add_line(self, text, color=WHITE):
        """Adiciona uma linha instantaneamente."""
        line = Text(text, font="Monospace", font_size=self.font_size, color=color)
        self._place_line(line)
        self.text_container.add(line)
        self._update_cursor_position(self.cursor, 0)
        return line

    def animate_typing(self, text, color=WHITE, typing_speed=0.08):
        """Retorna a animação de uma linha sendo digitada do zero."""
        line = Text(text, font="Monospace", font_size=self.font_size, color=color)
        self._place_line(line)
        self.text_container.add(line)
        
        return AddTextLetterByLetter(line, run_time=len(text) * typing_speed)

    def animate_prompt_and_command(self, prompt="manim@manim:~$ ", command="", prompt_color=GREEN, cmd_color=WHITE, typing_speed=0.08):
        """
        Gera uma linha e digita o comando em seguida.
        Retorna um AnimationGroup para ser executado pela Scene.
        """
        full_line = VGroup()
        
        prompt_text = Text(prompt, font="Monospace", font_size=self.font_size, color=prompt_color)
        cmd_text = Text(command, font="Monospace", font_size=self.font_size, color=cmd_color)
        
        cmd_text.next_to(prompt_text, RIGHT, buff=0.1)
        full_line.add(prompt_text, cmd_text)
        
        self._place_line(full_line)
        self.text_container.add(full_line)
        
        return AnimationGroup(
            FadeIn(prompt_text, run_time=0.1),
            AddTextLetterByLetter(cmd_text, run_time=len(command) * typing_speed),
            lag_ratio=1
        )

    def resize_terminal(self, new_width=None, new_height=None, align_edge=ORIGIN):
        """
        Redimensiona o terminal mantendo a escala dos botões, barra e textos intactos. (Não testado ainda)
        """
        anchor_point = self.bg.get_critical_point(align_edge)
        
        if new_width:
            self.bg.stretch_to_fit_width(new_width)
            self.top_bar.stretch_to_fit_width(new_width)
        if new_height:
            self.bg.stretch_to_fit_height(new_height)
            
        self.bg.move_to(anchor_point, aligned_edge=align_edge)
            
        self.top_bar.next_to(self.bg, UP, buff=0)
        
        self.title_text.move_to(self.top_bar)
        
        self.btn_close.move_to(self.top_bar.get_right() + LEFT * 0.3)
        self.btn_min.next_to(self.btn_close, LEFT, buff=0.15)
        self.btn_max.next_to(self.btn_min, LEFT, buff=0.15)
        
        if len(self.text_container) > 0:
            self.text_container.move_to(
                self.bg.get_corner(UL) + RIGHT * 0.2 + DOWN * 0.3, 
                aligned_edge=UL
            )
            
        return self

    def clear_terminal(self):
        """Limpa o conteúdo gerado dentro do terminal."""
        self.text_container.clear()