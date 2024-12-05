import pygame
import RPi.GPIO as GPIO

# GPIO-innstillinger
BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Pygame-innstillinger
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Button")
clock = pygame.time.Clock()

# Spillvariabler
bird_y = 300
bird_dy = 0
gravity = 0.5
flap_strength = -10
running = True
game_started = False

def draw_bird(y):
    pygame.draw.circle(screen, (255, 255, 0), (200, int(y)), 20)

def show_start_screen():
    screen.fill((0, 0, 255))  # Bakgrunnsfarge (blå)
    font = pygame.font.Font(None, 50)
    text = font.render("Trykk for å starte!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(200, 300))
    screen.blit(text, text_rect)
    pygame.display.update()

# Startskjerm
while not game_started:
    show_start_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            game_started = True

    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        game_started = True

# Spill-løkke
while running:
    screen.fill((0, 0, 255))  # Bakgrunnsfarge (blå)

    # Håndter avslutning
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Les knappetrykk
    if GPIO.input(BUTTON_PIN) == GPIO.LOW:
        bird_dy = flap_strength

    # Oppdater fuglens bevegelse
    bird_dy += gravity
    bird_y += bird_dy

    # Tegn fuglen
    draw_bird(bird_y)

    # Sjekk om fuglen går ut av skjermen
    if bird_y < 0 or bird_y > 600:
        running = False

    pygame.display.update()
    clock.tick(30)

# Rydd opp
GPIO.cleanup()
pygame.quit()
