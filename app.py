import pygame
from pygame.locals import *
import cevent

FPS = 15
WIDTH = 800
HEIGHT = 600
white = (255, 255, 255)
gray = (128, 128, 128)
red = (255, 0, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
green = (0, 200, 0)

class App(cevent.CEvent):
    def __init__(self):
        self.running = True
        self.screen = None
        self.area = None
        self.width, self.height = (WIDTH, HEIGHT)
        self.thick = 10
        self.off = 15
        self.board = []
        self.ehks = set([])
        self.oh = set([])
        self.grid = []
        self.pos = [0,0]
        self.xPlayer = True
        self.winner = None
        self.yesRect = Rect(0,0,0,0)
        self.noRect = Rect(0,0,0,0)
        self._time = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.area = self.screen.get_rect()
        self.width, self.height = self.area.size
        self.bw = (self.width-2*self.off-2*self.thick)//3+1
        self.bh = (self.height-2*self.off-2*self.thick)//3+1
        self.board = [Rect(self.off,self.off, self.bw, self.bh), 
                      Rect(self.off+self.thick+self.bw, self.off, self.bw, self.bh), 
                      Rect(self.off+2*(self.bw+self.thick), self.off, self.bw, self.bh),
                      
                      Rect(self.off,self.off+self.bh+self.thick, self.bw, self.bh), 
                      Rect(self.off+self.thick+self.bw, self.off+self.bh+self.thick, self.bw, self.bh), 
                      Rect(self.off+2*(self.bw+self.thick), self.off+self.bh+self.thick, self.bw, self.bh),
                      
                      Rect(self.off,self.off+2*(self.bh+self.thick), self.bw, self.bh), 
                      Rect(self.off+self.thick+self.bw, self.off+2*(self.bh+self.thick), self.bw, self.bh), 
                      Rect(self.off+2*(self.bw+self.thick), self.off+2*(self.bh+self.thick), self.bw, self.bh)]

        self.grid = [Rect(self.off + self.bw, self.off, self.thick, 2*self.thick + 3*self.bh),
                     Rect(self.off + 2*self.bw + self.thick, self.off, self.thick, 2*self.thick + 3*self.bh),
                     Rect(self.off, self.off + self.bh, 3*self.bw + 2*self.thick, self.thick),
                     Rect(self.off, self.off + 2*self.bh + self.thick, 3*self.bw + 2*self.thick, self.thick)]

    def on_lbutton_down(self, event):
        self.pos = event.pos
        self.xPlayer = True

    def on_rbutton_down(self, event):
        self.pos = event.pos
        self.xPlayer = False

    def on_exit(self):
        self.running = False

    def on_loop(self):
        if self.winner == None:
            self._time.tick(FPS)
            for g in self.board:
                if g.collidepoint(self.pos):
                    # mark board for current player
                    if self.xPlayer:
                        self.ehks.add(self.board.index(g))
                    else:
                        self.oh.add(self.board.index(g))
                    self.pos = [0,0]
                    print(self.ehks)
                    print(self.oh)
        else:
            if self.noRect.collidepoint(self.pos):
                self.running = False
            elif self.yesRect.collidepoint(self.pos):
                self.winner = None
                self.pos = (0,0)

    def check_for_winner(self):
        winning_sets = [ set([0,1,2]),
                         set([3,4,5]),
                         set([6,7,8]),
                         set([0,3,6]),
                         set([1,4,7]),
                         set([2,5,8]),
                         set([0,4,8]),
                         set([2,4,6])
                       ]
        for w in winning_sets:
            if w.issubset(self.ehks):
                self.winner = 'X'
                self.ehks.clear()
                break
            elif w.issubset(self.oh):
                self.winner = 'O'
                self.oh.clear()
                break;
        if self.winner == None and self.is_draw():
            self.winner = 'SCRATCH'

    def is_draw(self):
        marked = len(self.ehks) + len(self.oh)
        if marked == 9 and self.winner == None:
            return True
        return False
        
    def on_render(self):
        if self.winner != None:
            # Draw menu
            print('Drawing new game menu')
            self.draw_new_game_menu()
        else:
            self.screen.fill(black)
            self.draw_grid()
            
            self.draw_exes()

            self.draw_ohs()

            self.check_for_winner()

        pygame.display.flip()

    def draw_grid(self):
        for l in self.grid:
            pygame.draw.rect(self.screen, white, l)
    def draw_exes(self):
        for x in self.ehks:
            self.draw_x(self.screen, self.board[x])
    def draw_ohs(self):
        for o in self.oh:
            self.draw_o(self.screen, self.board[o])

    def draw_new_game_menu(self):
        rect = Rect(0,0,WIDTH,HEIGHT)
        rect = rect.inflate(-WIDTH//3, -HEIGHT//3)
        pygame.draw.rect(self.screen, gray, rect)

        font = pygame.font.Font(pygame.font.get_default_font(), 28)
        font.bold = True
        text = font.render(self.winner + ' Wins!  Play Again?', True, green)
        textRect = text.get_rect()
        textRect.center = rect.center
        self.screen.blit(text, textRect)

        self.yesRect = Rect(rect.left + rect.width//4, rect.top + 3*rect.height//4, rect.width//4, rect.height//8)
        yes = font.render('YES', True, white)
        yesR = yes.get_rect()
        yesR.center = self.yesRect.center
        pygame.draw.rect(self.screen, blue, self.yesRect)
        self.screen.blit(yes, yesR)

        self.noRect = Rect(rect.right - 2*rect.width//4, rect.top + 3*rect.height//4, rect.width//4, rect.height//8)
        no = font.render('NO', True, white)
        noR = yes.get_rect()
        noR.center = self.noRect.center
        pygame.draw.rect(self.screen, blue, self.noRect)
        self.screen.blit(no, noR)

    def draw_x(self, surf, rect):
        pygame.draw.line(surf, red, (rect.left, rect.top), (rect.right, rect.bottom), 5)
        pygame.draw.line(surf, red, (rect.left, rect.bottom), (rect.right, rect.top), 5)

    def draw_o(self, surf, rect):
        pygame.draw.circle(surf, blue, rect.center, rect.width//3, 5)
        

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False
        
        while(self.running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__":
    game = App()
    if game.on_init() == False:
        game.running = False

    while (game.running):
        for event in pygame.event.get():
            game.on_event(event)
        game.on_loop()
        game.on_render()
    game.on_cleanup()
