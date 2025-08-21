import pygame
import time

class PONG_GAME:
    def __init__(self, fps):
        pygame.init()

        # Font that is used to render the text
        self.font20 = pygame.font.Font('freesansbold.ttf', 20)
        self.fps = fps
        # RGB values of standard colors
        self.colors = {}
        self.colors['BLACK'] = (0, 0, 0)
        self.colors['WHITE'] = (255, 255, 255)
        self.colors['GREEN'] = (0, 255, 0)
        self.colors['BLUE'] = (10, 20, 110)
        self.colors['ORANGE'] = (243, 115, 41)

        # Basic parameters of the screen
        self.WIDTH, self.HEIGHT = 900, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pong")
        # Used to adjust the frame rate
        self.clock = pygame.time.Clock()

        self.init_players()
        self.init_ball()

    def init_players(self):
        self.geek1 = Striker(self.screen, 20, self.HEIGHT//2 - 50, 10, 100, 10, self.colors['BLUE'], self.HEIGHT, self.font20)
        self.geek2 = Striker(self.screen, self.WIDTH - 30, self.HEIGHT // 2 - 50, 10, 100, 10, self.colors['ORANGE'], self.HEIGHT , self.font20)

        self.listOfGeeks = [self.geek1, self.geek2]

        self.geek1Score = 0
        self.geek2Score = 0

    def init_ball(self):
        self.ball = Ball(self.screen, self.WIDTH // 2, self.HEIGHT // 2, 7, 3, self.colors['WHITE'], self.HEIGHT, self.WIDTH)

    def step_forward(self, geek1YFac, geek2YFac, pause=False):
        start_time = time.time()
        self.screen.fill(self.colors['BLACK'])
        running = True
        # Event handling by PRESSING KEYS, overrides controller input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1
                if event.key == pygame.K_SPACE:
                    if pause:
                        pause = False
                    else:
                        pause = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0

        if not pause:
            # Collision detection
            for geek in self.listOfGeeks:
                if pygame.Rect.colliderect(self.ball.getRect(), geek.getRect()):
                    self.ball.hit()

            # Updating the objects
            self.geek1.update(geek1YFac)
            self.geek2.update(geek2YFac)
            point = self.ball.update()

            # -1 -> Geek_1 has scored
            # +1 -> Geek_2 has scored
            #  0 -> None of them scored
            if point == -1:
                self.geek1Score += 1
            elif point == 1:
                self.geek2Score += 1

            if point:   # Someone has scored a point and the
              # ball is out of bounds. So, we reset it's position
                self.ball.reset()

              # Displaying the objects on the screen
        self.geek1.display(self.screen)
        self.geek2.display(self.screen)
        self.ball.display(self.screen)

        # Displaying the scores of the players
        self.geek1.displayScore("Blue Team: ", self.geek1Score, 100, 20, self.colors['WHITE'])
        self.geek2.displayScore("Orange Team: ", self.geek2Score, self.WIDTH - 100, 20, self.colors['WHITE'])

        pygame.display.update()
        end_time = time.time()
        elapsed_time = end_time - start_time
        # print("Elapsed time: ", elapsed_time)

        # Adjusting the frame rate
        self.clock.tick(self.fps)

        return running

    def quit(self):
        pygame.quit()


class Striker:

    # Take the initial position,
    # dimensions, speed and color of the object
    def __init__(self, screen, posx, posy, width, height, speed, color, max_height, font):
        self.screen = screen
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.max_height = max_height
        self.font = font
        # Rect that is used to control the
        # position and collision of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.geek = pygame.draw.rect(self.screen, self.color, self.geekRect)

    # Used to display the object on the screen
    def display(self, screen):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    # Used to update the state of the object
    # yFac represents the direction of the striker movement
    # if yFac == -1 ==> The object is moving upwards
    # if yFac == 1 ==> The object is moving downwards
    # if yFac == 0 ==> The object is not moving
    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac

        # Restricting the striker to be below
        # the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above
        # the bottom surface of the screen
        elif self.posy + self.height >= self.max_height:
            self.posy = self.max_height - self.height

        # Updating the rect with the new values
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    # Used to render the score on to the screen
    # First, create a text object using the font.render() method
    # Then, get the rect of that text using the get_rect() method
    # Finally blit the text on to the screen
    def displayScore(self, text, score, x, y, color):
        text = self.font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        self.screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect


# ----------------------------------------------------------------------------#
# Ball class
class Ball:
    def __init__(self, screen, posx, posy, radius, speed, color, max_height, max_width):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1
        self.max_height = max_height
        self.max_width = max_width

    def display(self, screen):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and it
        # results in a reflection
        if self.posy <= 0 or self.posy >= self.max_height:
            self.yFac *= -1

        # If the ball touches the left wall for the first time,
        # The firstTime is set to 0 and we return 1
        # indicating that Geek2 has scored
        # firstTime is set to 0 so that the condition is
        # met only once and we can avoid giving multiple
        # points to the player
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= self.max_width and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    # Used to reset the position of the ball
    # to the center of the screen
    def reset(self):
        self.posx = self.max_width // 2
        self.posy = self.max_height // 2
        self.xFac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball