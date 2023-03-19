import pygame
import os
# Learning pygame module with 'Tech with Tim: Pygame in 90 minutes'
# step 1: ensure that pygame is installed
# pygame is a 2d graphics library that lets you make simple games.
# Step 13: Add import os so that we can navigate the file structure.
# step 2: make the main surface.
# everything in pygame is referred to as a surface.


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# This says: create a new variable WIN (window) with specified height and width
# The convention to use CAPITALS for constant values. These values don't change, so we
# use capitals to indicate this.

pygame.display.set_caption("First Game!")
# Step 6: We add a little definition of the window name, so it doesnt
# just say "pygame window" forever

WHITE = (255, 255, 255)
# Step 7: We define a variable with the RGB values for displaying
# a solid colour, so we don't have to input the numerical information
# directly and risk getting confused.

FPS = 60
# Step 10: The main loop will be determined by the speed at which the
# computer can cycle through it. But we want to control this rate so
# that the game runs consistently regardless of the machine.

VEL = 5
# Step 19b: Set a variable that controls how fast the ships move when the
# keys are pressed down.

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
# Step 13: Load the assets into their respective variables by using the
# image.load() method
# The os module allows us to refer to a file structure without
# specifying the separators, so if a directory doesn't use a /,
# we can still direct the filepath.

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
# YELLOW_SPACESHIP = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
# RED_SPACESHIP = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
# Step 15: We are able to transform the displayed images in various ways.
# Resize the image with the scale() method.
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
# Step 16b: Update the transformation to rotate the image and resize.
# Make the two spaceships face each other by setting degree of rotation
# to 90 and 270 respectively.


def draw_window(red, yellow):
    # Step 17: We create variables red and yellow to represent the
    # rectangular space that the spaceships fill, and we can pass these
    # as arguments for the position of the ships
    WIN.fill(WHITE)
    # pygame.display.update()
    # Step 8: In order to display to screen, we give a command like
    # fill (fill the screen with a colour), then we must force
    # pygame to update the display before any change will happen.
    # We relegate this behaviour to a separate function outside of
    # the main loop.
    # WIN.blit(YELLOW_SPACESHIP_IMAGE, (300, 100))
    # Step 14: Once images are defined as SURFACES in Step 13, we use
    # the blit() function to display it to the screen at specified co-ordinates.
    # NOTE: the co-ordinate system of pygame:
    # 0, 0 is not the middle of the window.
    # 0, 0 is the top left corner of the screen. As we increase x, we go right,
    # as we increase y, we go down the screen.
    # We draw objects from their top left position. The width goes into the right
    # and the height goes down.
    # WIN.blit(YELLOW_SPACESHIP, (300, 100))
    # Step 15b: I updated the blit() call to reflect the new resized
    # spaceship image.
    # WIN.blit(RED_SPACESHIP, (700, 100))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    # Step 17: Since red and yellow are d

    # Step 16b: Add the red spaceship at a different position.
    pygame.display.update()
    # Don't forget that we need to specify to update the screen.
    # I moved this command down from step 8, because it causes flickering if
    # it exists multiple places in the same loop.

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a]:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_s]:  # DOWN
        yellow.y += VEL
    if keys_pressed[pygame.K_w]:  # UP
        yellow.y -= VEL
        # Step 19a: Define what happens when the keys are pressed.
        # Let WASD represent up left down right.
        # We need to set a rate at which the sprite will move (see above)
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_DOWN]:  # DOWN
        red.y += VEL
    if keys_pressed[pygame.K_UP]:  # UP
        red.y -= VEL

# step 3: make the main loop that does the other game functions
def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # x, y, width, height
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # Step 17a: define the parameters of red and yellow as pygame rectangles.
    # These have x, y, height, and width, which the blit() command
    # will be able to parse as red.x, red.y etc.

    clock = pygame.time.Clock()
    # Step 11: Add a clock to the main loop so we can control the FPS we
    # defined in step 10.
    run = True
    while run:
        # the loop will keep running until something changes the run variable
        # to False.
        clock.tick(FPS)
        # Step 12: Add a tick inside the running loop.
        # This controls the speed of the while loop. We run at 60 loops
        # per second Maximum.
        for event in pygame.event.get():
            # check for the different events that occur in pygame
            # get a list of all events in the game, and cycle through them
            # depending on the event type, take further action
            if event.type == pygame.QUIT:
                run = False
                # Step 4: the first event we define allows the user to exit the game
                # by setting run to False, allowing the condition to exit the loop

        keys_pressed = pygame.key.get_pressed()
        # Step 18: Add function to enable key presses. Pygame method
        # get_pressed() allows us to see what keys the user is pressing
        # If a key stays pressed, we can see that it is still being pressed

        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)
        # Step 20: call the yellow_handle_movement function to check
        # whether yellow has moved and move the sprite if so.


        draw_window(red, yellow)
        # Step 9: every time we run through the loop, end by drawing the window

    pygame.quit()
    # step 5: if the loop is no longer True, terminate the game
    # using pygame's built-in quit function.

if __name__ == "__main__":
    main()
    # Step 6: this condition ensures that we only run the main function
    # if we ran the file directly.
    # If this is the main file that was run, the name wil be __main__,
    # but if the file was imported then run, it will be assigned a
    # different name, and the file that caused it to run will be
    # designated __main__