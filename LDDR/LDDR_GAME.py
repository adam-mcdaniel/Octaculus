import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("LDDR")
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

colors = [BLACK, WHITE, GREEN, RED, BLUE, YELLOW, PURPLE, CYAN, ORANGE]
directions = ["up", "upright", "right", "downright", "down", "downleft", "left", "upleft"]

PIXELS_PER_TICK = 4
CIRCLE_OFFSET = 35

class Nodes:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x+int(CIRCLE_OFFSET/2), y-10, 30, 50)
        self.color = color
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x + CIRCLE_OFFSET, self.y + 16), 30)
        pygame.draw.circle(screen, BLACK, (self.x + CIRCLE_OFFSET, self.y + 16), 25)

        #debug draw rect square
        # pygame.draw.rect(screen, self.color, self.rect)

    def collision(self, note_list):
        for note in note_list:
            if self.rect.colliderect(note.rect) and note.collided == False:
                note.collided = True
                return True
        return False

class Note:
    def __init__(self, y, color, direction):
        self.x = 80*direction+CIRCLE_OFFSET
        self.y = y
        # self.image = image
        self.color = color
        self.direction = direction
        self.collided = False
        if direction >= 0:
            self.rect = pygame.Rect(self.x, self.y+16, 32, 32)
        else:
            self.rect = pygame.Rect(0, 0, 0, 0) #The var still has the rect var but it wont ever return true for collisions

    def draw(self, screen):
        if self.direction == -1: #this is how we insert time between notes, -1 is a rest
            return
        # screen.blit(self.image, (self.x, self.y))
        pygame.draw.circle(screen, self.color, (self.x, self.y + 16), 16)

        # debug draw rect square
        # pygame.draw.rect(screen, self.color, self.rect)
    
    def update(self, screen):
        self.y += PIXELS_PER_TICK
        self.rect = pygame.Rect(self.x, self.y, 32, 32)
        self.draw(screen)
        if self.y > 480:
            return True
        else:
            return False


nodes = []
for i in range(8):
    node = Nodes(80 * i, 400, colors[i+1])
    nodes.append(node)

notes = []
for i in range(100):
    random_index = random.randint(-1, 7)
    if random_index == -1:
        note = Note(0, BLACK, -1)
    else:
        note = Note(i*-200, nodes[random_index].color, random_index)
    notes.append(note)

score = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_1:
                if nodes[0].collision(notes):
                    print("collision up")
                    score += 20
            if event.key == pygame.K_2:
                if nodes[1].collision(notes):
                    print("collision upright")
                    score += 20
            if event.key == pygame.K_3:
                if nodes[2].collision(notes):
                    print("collision right")
                    score += 20
            if event.key == pygame.K_4:
                if nodes[3].collision(notes):
                    print("collision downright")
                    score += 20
            if event.key == pygame.K_5:
                if nodes[4].collision(notes):
                    print("collision down")
                    score += 20
            if event.key == pygame.K_6:
                if nodes[5].collision(notes):
                    print("collision downleft")
                    score += 20
            if event.key == pygame.K_7:
                if nodes[6].collision(notes):
                    print("collision left")
                    score += 20
            if event.key == pygame.K_8:
                if nodes[7].collision(notes):
                    print("collision upleft")
                    score += 20

    screen.fill((0, 0, 0))
    for node in nodes:
        node.draw(screen)
    for note in notes:
        if note.update(screen):
            notes.remove(note)
    font = pygame.font.SysFont("comicsansms", 48)
    text = font.render(str(score), True, WHITE)
    screen.blit(text, (0, 0))


    pygame.display.update()
    clock.tick(60)