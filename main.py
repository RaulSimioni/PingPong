import sys
import pygame

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('Music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

point = pygame.mixer.Sound('Ponto.mp3')

hit_sound = pygame.mixer.Sound('bater.mp3')
hit_sound.set_volume(5)

game_over_sound = pygame.mixer.Sound('game_over.wav')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong")

clock = pygame.time.Clock()
fps = 60

background = pygame.image.load('bg.jpg')
background = pygame.transform.scale(background, (screen_width, screen_height))

paddle_width = 10
paddle_height = 100
paddle_speed = 7

paddle_a = pygame.Rect(30, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle_b = pygame.Rect(screen_width - 40, screen_height // 2 - paddle_height // 2, paddle_width, paddle_height)

ball_width = 10
ball = pygame.Rect(screen_width // 2 - ball_width // 2, screen_height // 2 - ball_width // 2, ball_width, ball_width)
ball_speed_x = 5
ball_speed_y = 5

score_a = 0
score_b = 0
font = pygame.font.Font(None, 36)

def draw_objects():
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (screen_width // 2, 0), (screen_width // 2, screen_height))
    score_text = font.render(f"{score_a}   {score_b}", True, WHITE)
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, 20))

def reset_game():
    global score_a, score_b, ball_speed_x, ball_speed_y
    score_a = 0
    score_b = 0
    ball.x = screen_width // 2 - ball_width // 2
    ball.y = screen_height // 2 - ball_width // 2
    ball_speed_x = 5
    ball_speed_y = 5

def game_over():
    pygame.mixer.music.pause()
    
    game_over_sound.play()
    
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("FIM DE JOGO", True, WHITE)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))

        restart_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
        exit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 70, 200, 50)
        
        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, exit_button)
        
        restart_text = font.render("Reiniciar", True, BLACK)
        exit_text = font.render("Sair", True, BLACK)
        
        screen.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2, 
                                   restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
        screen.blit(exit_text, (exit_button.x + (exit_button.width - exit_text.get_width()) // 2, 
                                exit_button.y + (exit_button.height - exit_text.get_height()) // 2))
        
        pygame.display.flip()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if restart_button.collidepoint(mouse_pos):
                    reset_game()
                    pygame.mixer.music.unpause()
                    return

                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= paddle_speed
    if keys[pygame.K_s] and paddle_a.bottom < screen_height:
        paddle_a.y += paddle_speed
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle_b.bottom < screen_height:
        paddle_b.y += paddle_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        hit_sound.play()
        ball_speed_x *= -1

    if ball.left <= 0:
        score_b += 1
        ball.x = screen_width // 2 - ball_width // 2
        ball.y = screen_height // 2 - ball_width // 2
        point.play()
        ball_speed_x *= -1
        if score_b >= 10:
            game_over()

    if ball.right >= screen_width:
        score_a += 1
        ball.x = screen_width // 2 - ball_width // 2
        ball.y = screen_height // 2 - ball_width // 2
        point.play()
        ball_speed_x *= -1
        if score_a >= 10:
            game_over()

    draw_objects()
    pygame.display.flip()
    clock.tick(fps)
