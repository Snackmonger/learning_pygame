import pygame
import os
import sys
pygame.font.init()
pygame.mixer.init()

# Step 28 initialize the font of pygame.
# Note: Beginning at Step 20 of the BASICS version.
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
# Step 21: Define a rectangle that will serve as the border of the
# game between the two ships. The border will be drawn halfway between the two
# zones. But remember that pygame draws from left to right, so we need to compensate
# and offset the drawing to make sure that it is not only drawn on the centre axis, but
# also that it itself is centred on that axis.
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
# Step 29a: define a font that we will use later.

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

FPS = 60
MAX_BULLETS = 3
VEL = 5
BULLETS_VEL = 7

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):

    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    # Step 21: Add a function to draw a rectangle, using the arguments
    # of the WINdow, the contents, and the rectangle information.

    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("HEALTH: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    # Step 29: Add text to represent the health of each player.
    # Then blit() it to a position on the screen.

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))



    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 10:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # DOWN
        yellow.y += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    # Step 22: We add the 'and' keyword to specify the range within which the ship is allowed
    # to move. The 0 is the leftmost x on the screen.
    # The BORDER must be the boundary for the yellow ship's x.
    # But remember that pygame draws from the top left, so we must consider
    # not only where the ship is being drawn from, but also the extent of the
    # drawing.

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL
    if keys_pressed[pygame.K_UP] and red.y + VEL > 10:  # UP
        red.y -= VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VEL
        # Step 26b: Create movement in the yellow bullets by moving them to the right
        # the bullet's x position += bullet velocity.
        if red.colliderect(bullet):
            # Step 26c: since yellow is defined as a rectangle, we can
            # use the colliderect() method to detect if another rectangle
            # intersects with it. (This only works if both objects are rectangles)
            pygame.event.post(pygame.event.Event(RED_HIT))
            # Step 27: Create an event for the main loop to check and respond to.
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            # Step 28: Add a condition to remove bullets if they go off the edge of the screen.wwwwwwwwwwwww

    for bullet in red_bullets:
        bullet.x -= BULLETS_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000) # Delay by 5000 ms,then restart the game.


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # x, y, width, height
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    # Step 23: Create lists to represent the bullets that each player has.

    red_health = 10
    yellow_health = 10
    # Step 27b: add health variables to count the hits.

    clock = pygame.time.Clock()

    run = True
    while run:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Step 24: Allow each user to fire one of their bullets
                # when they place the CTRL key on their side of the keyboard
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    # Step 25: define a bullet as a rectangle to be drawn at the edge of the image.
                    # since image drawing starts at the left, the edge is start + width for the left player.
                    # the y of the bullet is half the size of the yellow ship sprite, minus half the size of the
                    # bullet itself, to offset the drawing from top left. Then the bullet width is 10, and the height
                    # is 5.
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    # Step 25: For the right-side player, since we start drawing at the left,
                    # the bullet leaves at 0 x of the red ship.
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                # Step 28: Add a behaviour associated with the posted event for ships being hit.
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        # Step 26a: create a function to handle the bullets in the game
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    main()

if __name__ == "__main__":
    main()
