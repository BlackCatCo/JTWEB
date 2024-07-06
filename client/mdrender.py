import pygame
from pygame.math import Vector2 as vec2
import os

pygame.init()
os.chdir(os.path.dirname(__file__))

FONT_SIZE = 18
FONT = pygame.font.Font('Consolas-Font/CONSOLA.TTF', FONT_SIZE)

BG_COLOR = (20, 20, 20)
TEXT_COLOR = (200, 200, 200)

TEXTBOX_COLOR = (60, 60, 60)
TEXTBOX_COLOR_ACTIVE = (70, 70, 70)
LINK_COLOR = (68, 58, 124)
LINK_CLICK_COLOR = (115, 124, 58)


class TextBox:
    def __init__(self, pos: vec2, width: int, value: str):
        self.pos = pos
        self.width = width
        self.value = value

        self.action_click = None
        self.action_enter = None

        self.active = False

        self._rect = pygame.Rect(self.pos[0], self.pos[1]-2, self.width, FONT_SIZE+4)
        self._txt_surf = FONT.render(self.value, True, TEXT_COLOR)
    
    def render(self, surf: pygame.Surface):
        pygame.draw.rect(surf, TEXTBOX_COLOR_ACTIVE if self.active else TEXTBOX_COLOR, self._rect, 0, 4)
        pygame.draw.rect(surf, TEXT_COLOR, self._rect, 2, 4)
        surf.blit(self._txt_surf, self.pos+vec2(4, 0))
    
    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self._rect.collidepoint(event.pos):
                self.active = True
                if self.action_click:
                    self.action_click(self)
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.action_enter:
                        self.action_enter(self)
                elif event.key == pygame.K_BACKSPACE:
                    self.value = self.value[:-1]
                else:
                    self.value += event.unicode
                
                self._txt_surf = FONT.render(self.value, True, TEXT_COLOR)

class TextBoxes:
    def __init__(self):
        self.txtboxes = []

    
    def add(self, pos, width, default_value=''):
        txtbox = TextBox(pos, width, default_value)
        self.txtboxes.append(txtbox)
        return txtbox
    
    def update(self, event):
        for b in self.txtboxes:
            b.update(event)
    
    def render(self, surf: pygame.Surface):
        for b in self.txtboxes:
            b.render(surf)

class Link:
    def __init__(self, text: str, target: str):
        self.text = text
        self.target = target
        self.hover = False

        self._surf = FONT.render(self.text, True, LINK_COLOR)
        self._surf_hover = FONT.render(self.text, True, LINK_CLICK_COLOR)

    def is_null(self):
        return self.text == '' or self.target == ''
    
    @property
    def surf(self):
        if self.hover:
            return self._surf_hover
        return self._surf
        
    
    def __repr__(self):
        return f'Link[{self.text}]({self.target})'


class app:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self._title = title

        self.lines = []

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(self._title)

        self.txtboxes = TextBoxes()

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value
        pygame.display.set_caption(self._title)
    
    
    def compile_md(self, markdown: str):
        self.lines = []
        raw_lines = markdown.splitlines()

        link_txtst = None
        link_tgst = None
        link_txt = None
        link_tg = None

        for j, l in enumerate(raw_lines):
            x = 0
            sx = 0
            self.lines.append([''])
            for i, c in enumerate(l):
                if c == '[': link_txtst = i-sx
                elif c == '(': link_tgst = i-sx

                elif link_txtst != None and c == ']': link_txt = l[link_txtst+1:i-sx]
                elif link_tgst != None and c == ')': link_tg = l[link_tgst+1:i-sx]

                self.lines[j][x] += c
                if link_txt and link_tg:
                    self.lines[j][x] = self.lines[j][x][:link_txtst]
                    sx += len(self.lines[j][x])
                    x += 2
                    self.lines[j].append(Link(link_txt, link_tg))
                    self.lines[j].append('')

                    link_txt = None
                    link_tg = None
        
        # Clean up and render
        for i, l in enumerate(self.lines):
            for s, seg in enumerate(l):
                if isinstance(seg, str):
                    if seg == '': l.remove(seg)
                    else:
                        self.lines[i][s] = FONT.render(seg, True, TEXT_COLOR)
                elif isinstance(seg, Link):
                    if seg.is_null(): l.remove(seg)
        

    def blit_md(self, surf: pygame.Surface, start_pos: vec2):
        dpos = vec2(0, 0)
        for l in self.lines:
            dpos.x = 0
            for seg in l:
                txtsurf: pygame.Surface
                render_pos: vec2 = dpos+start_pos

                if isinstance(seg, Link):
                    txtsurf = seg.surf
                    seg.hover = txtsurf.get_rect(topleft=render_pos).collidepoint(pygame.mouse.get_pos())

                else:
                    txtsurf = seg
                
                surf.blit(txtsurf, render_pos)
                dpos.x += txtsurf.get_width()
            dpos.y += FONT_SIZE+2

    def draw(self):
        # self.screen.blit(self.font.render('Hello World!', True, self.txt_color), (10, 10))
        self.txtboxes.render(self.screen)

        self.blit_md(self.screen, vec2(4, 45))
    
    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.txtboxes.update(event)
            
            self.screen.fill(BG_COLOR)
            self.draw()

            pygame.display.flip()
            clock.tick(60)