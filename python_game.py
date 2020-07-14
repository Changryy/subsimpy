import pygame

pygame.init()



player = [26,26]


RANGE = 51


screen = pygame.display.set_mode((RANGE*12, RANGE*10+10))
done = False




pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('monospace', 30)




world = []
for y in range(RANGE): world.append("~"*RANGE)

def set_tile(tile, pos_x, pos_y):
        global world
        pos_x, pos_y -= RANGE/2+0.5
        for y in range(len(world)):
                if y+1 == pos_y: world[y] = world[y][:pos_x-1]+tile+world[y][pos_x:]


def move(axis, direction):
        global player
        if abs(player[axis]+direction) < 25:
                player[axis] += direction



while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        pygame.display.update()
        screen.fill((0))


        
        for y in range(len(world)):
                textsurface = myfont.render(world[y], False, (255,255,255))
                screen.blit(textsurface,(0,y*10))

        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_UP]:
                player[1] -= 1
        if key_input[pygame.K_DOWN]:
                player[1] += 1
        if key_input[pygame.K_RIGHT]:
                player[0] += 1
        if key_input[pygame.K_LEFT]:
                player[0] -= 1
        set_tile("+",player[0],player[1])







