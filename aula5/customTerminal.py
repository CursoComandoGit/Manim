from manim import *

class CustomTerminal(VGroup):
    
    def __init__(self, styleLinux : bool = True, sizeX : float = 6, sizeY : float = 4, textSize : float = 12,
                 title : str = "manim@manim: ~", corBack : str = "#800080FF", corTop : str= "#2D2D2D",
                 windowsPath :str = "C:\\>", **kwargs):
        super().__init__(**kwargs) #inicialização de variáveis
        #Extra for resize
        self.newWidth = 0
        self.newHeight = 0
        #
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.titulo = title
        self.styleLinux= styleLinux
        if styleLinux:
            self.corPath= "#00FF00"
        else:
            self.corPath= WHITE
        self.corBack = corBack
        self.corTop = corTop
        self.textSize = textSize #general size
        if self.styleLinux:
            self.currentPath = MarkupText(title+"$", color= self.corPath, font_size= 12, font= "Monospace")
        else:
            self.currentPath = MarkupText("", color= self.corPath, font_size= 12, font="Monospace")
        self.lineVector = []
    
        self.typeDelay = 0.07
        self.cursorIsOn = True
        self.blinkInterval = 0.5
        self.trackTime= 0

        #Setup objects
        self.fillRectangle = Rectangle(color = corBack, height = sizeY, width = sizeX,
                                       stroke_color = corBack, stroke_opacity = 0.25)

        self.fillRectangle.set_fill(corBack, 0.5)
        self.secondBorder= Rectangle(height = sizeY-0.3, width= sizeX-0.1)

        self.cursor= Rectangle(height = textSize/100, width = textSize/300)
        self.cursor.set_fill(WHITE,1)
        self.cursor.move_to(self.secondBorder.get_corner([-1,1,0]),
                            aligned_edge= self.cursor.get_corner([-1,1,0]))
        

        self.topRectangle = Rectangle(color = corTop, height = 0.5, width = sizeX)
        self.topRectangle.set_fill(corTop, 1)
        self.topRectangle.next_to(self.fillRectangle, UP, buff= 0)
        
        self.closeIcon= SVGMobject("svgs\\closeIcon.svg", opacity = 0.1)
        self.closeIcon.scale(0.15)
        self.closeIcon.move_to(self.topRectangle.get_corner([1,1,0]),
                          aligned_edge = self.closeIcon.get_corner([1,1,0]))
        self.titleNew = Text(title, font_size = 13)
        self.titulo = self.titleNew.move_to(self.topRectangle.get_center())

        #Start Initialize
        self.add(self.fillRectangle,
                 self.cursor,
                 self.topRectangle,
                 self.titulo,
                 self.closeIcon)
        if self.styleLinux:
            self.initialize_path(self.currentPath.text)
        else:
            self.initialize_path(windowsPath)
        self.add_updater(self.cursorBlink)

    #Inicializa texto novo na linha em que o cursor esta por padrão. Path é atualizado
    def initialize_path(self, path: str, createNewLine : bool = False):
        if createNewLine:
            self.cursorNewLine()
        self.suspend_updating(self.cursorBlink)
        self.cursorIsOn = True
        self.currentPath = MarkupText(path, font="Monospace",
                                     color = self.corPath,
                                     font_size = self.textSize,
                                     ).move_to(self.cursor.get_left(),
                                                                 aligned_edge= LEFT)
        if self.styleLinux:
            self.correctColor()
        self.lineVector.append(self.currentPath)
        self.cursor.move_to(self.currentPath.get_right(), aligned_edge = LEFT)
        self.cursor.shift([self.textSize/150,0,0])
        self.add(self.currentPath)
        self.resume_updating(self.cursorBlink)

    #Cria um texto na linha que o cursor está
    def instantInitializeLine(self, text_str: str, color: ParsableManimColor = WHITE):
        if len(text_str) == 0:
            return
        num_leading_spaces = len(text_str) - len(text_str.lstrip(" "))
        line = MarkupText(text_str, font="Monospace",
                          font_size=self.textSize, color=color)
        ref_char = MarkupText("A", font_size=self.textSize, font="Monospace") #para o shift
        char_width = ref_char.width
        indent_offset = RIGHT * (num_leading_spaces * char_width)
        line.move_to(self.cursor.get_left() + indent_offset, aligned_edge=LEFT)
        self.lineVector.append(line)
        self.add(line)
        self.cursor.move_to(line.get_right(), aligned_edge=LEFT)
        self.cursor.shift([self.textSize/300, 0, 0])
        self.cursorNewLineCheck()
    
    #Cria um texto na linha que o cursor está em forma type
    def initialize_line(self, scene: Scene, text_str: str, color: ParsableManimColor = WHITE):
        self.suspend_updating(self.cursorBlink)
        self.cursor.set_opacity(1) 
        
        if len(text_str) == 0:
            return

        line = MarkupText(text_str, font="Monospace" ,
                          font_size=self.textSize, color=color)
        line.move_to(self.cursor.get_left(), aligned_edge=LEFT)
        line.set_opacity(0) #Start invisible
        self.lineVector.append(line)
        self.add(line)

        visual_index = 0 #para pula espaços
        
        for char in text_str:
            if char == " ":
                space_width = self.textSize / 160 
                self.cursor.shift([space_width, 0, 0])
            else:
                if visual_index < len(line):
                    char_obj = line[visual_index]
                    char_obj.set_opacity(1)
                    self.cursor.move_to(char_obj.get_right(), aligned_edge=LEFT)
                    self.cursor.shift([self.textSize/300, 0, 0])
                    visual_index += 1
            
            self.cursorNewLineCheck()
            scene.wait(self.typeDelay)

        self.resume_updating(self.cursorBlink)

    #Cria um novo path com uma nova linha de texto em uma nova linha
    def initialize_lineP(self, path: str, string : str):
        self.cursorNewLine()
        self.initialize_path(path)
        self.initialize_line(string)

    #Updater do cursor
    def cursorBlink(self, mob, dt):
        self.trackTime += dt
        
        if self.trackTime <= self.blinkInterval:
            return
        self.trackTime = 0
        
        if self.cursorIsOn:
            self.cursor.set_opacity(0)
            self.cursorIsOn = False
        else:
            self.cursor.set_opacity(1)
            self.cursorIsOn = True
    #Cria uma nova linha com o path atual
    def cursorNewLine(self, willGeneratePath : bool= False, newPath : str= "null"):
        #Alinhamento
        self.cursor.move_to(self.secondBorder.get_left(),
                            aligned_edge = LEFT,
                            coor_mask = [1,0,0])
        self.cursor.shift([0,-self.textSize/85,0])
        #
        if not willGeneratePath:
            return
        if newPath == "null":
            self.initialize_path(self.currentPath.text)
        else:
            self.initialize_path(newPath)
    
    def initializeMultiLineString(self, scene: Scene, waitAmount: float,text_str: str, color: ParsableManimColor = WHITE):
        self.suspend_updating(self.cursorBlink)
        self.cursor.set_opacity(0)
        for lines in text_str.split("\n"):
            self.instantInitializeLine(lines)
            self.cursorNewLine()
            scene.wait(waitAmount)
        self.cursor.set_opacity(1)
        self.resume_updating(self.cursorBlink)

    #Verifica se cursor passou da borda do terminal
    def cursorNewLineCheck(self):
        if self.cursor.get_right()[0] < self.fillRectangle.get_right()[0]:
            return
        self.cursorNewLine()

    #Atualiza cores do path
    def correctColor(self):
        i = 0
        while self.currentPath.text[i] != ":":
            i += 1
        i += 1
        while self.currentPath.text[i] != "$":
            self.currentPath[i].set_color(BLUE)
            i += 1
        self.currentPath[i].set_color(WHITE)

    #Limpa o terminal inteiro
    def clear(self):
        if self.lineVector:
            self.remove(*self.lineVector)
        
        self.lineVector = []
        self.cursor.move_to(self.secondBorder.get_corner(UL), aligned_edge=UL)
        self.cursor.shift([self.textSize/100, -self.textSize/100, 0])

    #daqui pra baixo é logica de ajuste de tamanho do terminal e alinhamento
    def snap_content_to_top(self):
        if not self.lineVector:
            self.cursor.move_to(self.secondBorder.get_corner(UL), aligned_edge=UL)
            self.cursor.shift([self.textSize/100, -self.textSize/100, 0])
            return

        all_text_group = VGroup(*self.lineVector)
        
        target_x = self.secondBorder.get_left()[0] + (self.textSize / 100)
        target_y = self.secondBorder.get_top()[1] - (self.textSize / 100)
        
        all_text_group.move_to([target_x, target_y, 0], aligned_edge=UL)
        
        last_element = self.lineVector[-1]
        
        self.cursor.move_to(last_element.get_right(), aligned_edge=LEFT)
        self.cursor.shift([self.textSize/300, 0, 0])

    def resize_terminal(self, new_width=None, new_height=None):
            old_center = self.fillRectangle.get_center()

            if new_width: self.sizeX = new_width
            if new_height: self.sizeY = new_height
            
            self.fillRectangle.stretch_to_fit_width(self.sizeX)
            if new_height: 
                self.fillRectangle.stretch_to_fit_height(self.sizeY)
            
            self.fillRectangle.move_to(old_center)

            self.secondBorder.stretch_to_fit_width(self.sizeX - 0.1)
            if new_height:
                self.secondBorder.stretch_to_fit_height(self.sizeY - 0.3)
            
            self.secondBorder.move_to(self.fillRectangle)
            
            self.topRectangle.stretch_to_fit_width(self.sizeX)
            self.topRectangle.next_to(self.fillRectangle, UP, buff=0)
            
            self.titulo.move_to(self.topRectangle.get_center())
            self.closeIcon.move_to(self.topRectangle.get_right() + LEFT * 0.2)
            
            self.snap_content_to_top()