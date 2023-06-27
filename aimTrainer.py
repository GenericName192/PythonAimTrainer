import math
import random
import time
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 600 # I mean yeah.

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # Creating a display of that size
pygame.display.set_caption("Aim Trainer") # The name of the window

TARGET_INCREMENT = 400 # how many mseconds between the events
TARGET_EVENT = pygame.USEREVENT # custom event

TARGET_PADDING = 30 # how far away they have to be from the edge

LIVES = 5
TOP_BAR_HEIGHT = 40

LABEL_FONT = pygame.font.SysFont("Comicsans", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
    
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE: # If its gonna get to max size
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE # grow or shrink
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win): # creates 4 circles each on top each other progressively getting smaller to create the desired target.
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8) 
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size

def draw(win, targets):
    win.fill("black")

    for target in targets:
        target.draw(win)



def draw_top_bar(win, time_passed, targets_hit, misses):
    pygame.draw.rect(win, "grey", (0,0, WIDTH, TOP_BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {round(time_passed, 2)}", 1, "black")
    speed = round(targets_hit/ time_passed, 1) # how many hit you get per second
    speed_label = LABEL_FONT.render(f"Speed: {speed}t/s", 1, "black")
    hits_label = LABEL_FONT.render(f"Hits: {targets_hit}", 1, "black")
    lives_label = LABEL_FONT.render(f"Lives: {LIVES - misses}", 1, "black")

    win.blit(time_label, (5, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (400, 5))
    win.blit(lives_label, (600, 5))

def end_screen(win, time_passed, targets_hit, clicks):
    WIN.fill("black")
    time_label = LABEL_FONT.render(f"Time: {round(time_passed, 2)}", 1, "white")
    speed = round(targets_hit/ time_passed, 1) # how many hit you get per second
    speed_label = LABEL_FONT.render(f"Speed: {speed}t/s", 1, "white")
    hits_label = LABEL_FONT.render(f"Hits: {targets_hit}", 1, "white")
    accuracy = round(targets_hit / clicks * 100, 1)
    accuracy_label = LABEL_FONT.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 200))
    win.blit(hits_label, (get_middle(hits_label), 300))
    win.blit(accuracy_label, (get_middle(accuracy_label), 400))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
            

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()
    

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT) # trigger the target event every target increment

    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        time_passed = time.time() - start_time

        for event in pygame.event.get(): # Keep checking for events
            if event.type == pygame.QUIT: # if the event is quit it closes the game
                run = False
                break

            if event.type == TARGET_EVENT: # creates new targets whenever the target event is triggered.
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target) # removes any targets that arent visable anymore
                misses += 1

            if click and target.collide(*mouse_pos): # the * breaks down the tuple into x and y, same as mouse_pos[0] etc
                targets.remove(target)
                targets_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, time_passed, targets_pressed, clicks)
        
        draw(WIN, targets)
        draw_top_bar(WIN, time_passed, targets_pressed, misses)
        pygame.display.update() # redraw everything

    pygame.quit()

if __name__ == "__main__": # Will only run the game from this file, wont try run if we import it.
    main()
