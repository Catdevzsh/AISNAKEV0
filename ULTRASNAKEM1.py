import pygame
import random
from array import array

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Display dimensions
dis_width = 800
dis_height = 600
display = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Enhanced Snake Game with Sound Effects')

# Clock for controlling the game speed
clock = pygame.time.Clock()
snake_speed = 15

# Colors and Font
white = (255, 255, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
font_style = pygame.font.Font(None, 36)
score = 0

# Function to generate beep sounds
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sounds for different events
move_sound = generate_beep_sound(440, 0.05)  # Beep on movement
eat_sound = generate_beep_sound(523.25, 0.1)  # Beep on eating
game_over_sound = generate_beep_sound(220, 0.3)  # Beep on game over

# Game Loop
running = True
snake_list = [[dis_width / 2, dis_height / 2]]
length_of_snake = 1
direction = 'RIGHT'
change_to = direction
food_pos = [random.randrange(1, (dis_width // 10)) * 10, random.randrange(1, (dis_height // 10)) * 10]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                move_sound.play()  # Play sound on direction change
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            elif event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'

    # Move the snake head
    head = snake_list[0].copy()
    if direction == 'LEFT':
        head[0] -= 10
    elif direction == 'RIGHT':
        head[0] += 10
    elif direction == 'UP':
        head[1] -= 10
    elif direction == 'DOWN':
        head[1] += 10

    # Game over conditions
    if head[0] < 0 or head[0] >= dis_width or head[1] < 0 or head[1] >= dis_height or head in snake_list[1:]:
        game_over_sound.play()
        running = False
        continue

    snake_list.insert(0, head)

    # Eating food
    if head == food_pos:
        eat_sound.play()  # Play sound when eating food
        food_pos = [random.randrange(1, (dis_width // 10)) * 10, random.randrange(1, (dis_height // 10)) * 10]
        length_of_snake += 1
        score += 10
    else:
        snake_list.pop()

    # Rendering
    display.fill(black)
    for pos in snake_list:
        pygame.draw.rect(display, yellow, [pos[0], pos[1], 10, 10])
    pygame.draw.rect(display, red, [food_pos[0], food_pos[1], 10, 10])
    score_text = font_style.render(f"Score: {score}", True, white)
    display.blit(score_text, [0, 0])
    pygame.display.update()

    # Control the game speed
    clock.tick(snake_speed)

pygame.quit()
quit()
