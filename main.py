import pygame
import random
from mainmenu import main_menu, change_volume

pygame.init()
# Параметры экрана
WIDTH, HEIGHT = 400, 600
# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
new_wave = False

# Параметры игры
LANE_WIDTH = WIDTH // 3
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40, 60
FPS = 60
font = pygame.font.Font(None, 36)


def load_sprite(path, size):
    sprite = pygame.image.load(path)
    colorkey = sprite.get_at((0, 0))
    sprite.set_colorkey(colorkey)
    sprite = sprite.convert_alpha()
    return pygame.transform.scale(sprite, size)


player_sprite = load_sprite("data/player.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
obs_sprite = load_sprite(
    "data/obstacle.png", (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obs_sprite.set_colorkey(WHITE)
obs_sprite = obs_sprite.convert_alpha()
green_sprite = load_sprite("data/green.png", (40, 40))
blue_sprite = load_sprite("data/blue.png", (40, 40))

# Загрузка фона
background = pygame.image.load("data/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Параметры для анимации фона
background_y1 = 0
background_y2 = -HEIGHT

timer = pygame.time.get_ticks()

clock = pygame.time.Clock()

# Функция для отрисовки игрока


def draw_player():
    if is_jumping:
        screen.blit(pygame.transform.scale(player_sprite, (PLAYER_WIDTH * (jump_offset // 30), PLAYER_HEIGHT *
                    (jump_offset // 30),),), (player_x + player_lane * LANE_WIDTH, player_y - jump_offset),)
    else:
        screen.blit(player_sprite, (player_x + player_lane *
                    LANE_WIDTH, player_y - jump_offset))


# Функция для отрисовки препятствий


def draw_obstacles():
    for obs in obstacles:
        screen.blit(obs_sprite, (obs.x, obs.y))


# Функция для обновления положения препятствий


def update_obstacles():
    global score
    for obs in obstacles[:]:
        obs.y += speed
        if obs.y > HEIGHT:
            obstacles.remove(obs)
            score += 1


# Функция для проверки столкновений


def check_collision():
    global lives, invincible_time, player_rect
    if is_jumping or invincible_time > pygame.time.get_ticks():
        return False

    player_rect = pygame.Rect(
        player_x + player_lane * LANE_WIDTH,
        player_y - jump_offset,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )
    for obs in obstacles:
        if player_rect.colliderect(obs):
            damage_sound.play()
            lives -= 1

            if lives > 0:
                invincible_time = pygame.time.get_ticks() + invincible_duration
            return True
    return False


# Функция для увеличения сложности игры


def increase_difficulty():
    global new_wave, wave, speed, lives
    if score >= wave * 50:
        wave += 1
        wave_sound.play()
        speed += 1
    if wave % 10 == 0 and lives < 5:
        lives += 1


# Функция для отрисовки экрана окончания игры


def draw_game_over():
    defeat_sound.play()
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, WHITE)
    stat = open("stats.txt", "w")
    stat = stat.write(f"Score: {score} Wave: {score // 50}")

    screen.blit(
        game_over_text, (WIDTH // 2 -
                         game_over_text.get_width() // 2, HEIGHT // 3)
    )
    screen.blit(score_text, (WIDTH // 2 -
                score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(
        restart_text, (WIDTH // 2 - restart_text.get_width() //
                       2, HEIGHT // 1.5)
    )


# Основной цикл игры
green_square = None
green_square_wave = 0
blue_square = None
blue_square_wave = 0


def update_green_square():
    global green_square, lives
    if green_square:
        green_square.y += speed
        if green_square.y > HEIGHT:
            green_square = None
        elif player_rect.colliderect(green_square):
            lives += 1
            green_square = None


def update_blue_square():
    global blue_square, invincible_time
    if blue_square:
        blue_square.y += speed
        if blue_square.y > HEIGHT:
            blue_square = None
        elif player_rect.colliderect(blue_square):
            invincible_time = pygame.time.get_ticks() + 10000  # 10 секунд неуязвимости
            blue_square = None


def game_loop():
    global green_sprite, blue_sprite, blue_square, blue_square_wave, green_square_wave, green_square, player_x, player_y, player_lane, is_jumping, jump_offset, jump_speed, obstacles, score, wave, speed, lives, invincible_time, invincible_duration, wave_sound, damage_sound, jump_sound, defeat_sound, background_y1, background_y2
    damage_sound = pygame.mixer.Sound("data/damage.mp3")
    jump_sound = pygame.mixer.Sound("data/jump.wav")
    defeat_sound = pygame.mixer.Sound("data/defeat.mp3")
    wave_sound = pygame.mixer.Sound("data/new_wave.mp3")
    background_music = pygame.mixer.music.load("data/background_music.mp3")
    change_volume()
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mixer.music.play()
    paused = False
    player_x = LANE_WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = HEIGHT - PLAYER_HEIGHT - 20
    player_lane = 1
    is_jumping = False
    jump_offset = 0
    jump_speed = 10
    jump_height = 150
    obstacles = []
    score = 0
    wave = 1
    speed = 5
    lives = 9999
    invincible_time = 0
    invincible_duration = 1000

    running = True
    while running:
        screen.blit(background, (0, background_y1))
        screen.blit(background, (0, background_y2))

        # Двигаем фон вниз
        background_y1 += speed - 2
        background_y2 += speed - 2
        # Перезапускаем фоны, когда они выходят за экран
        if background_y1 >= HEIGHT:
            background_y1 = -HEIGHT
        if background_y2 >= HEIGHT:
            background_y2 = -HEIGHT

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                if event.key == pygame.K_RIGHT and player_lane < 2:
                    player_lane += 1
                if event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    jump_sound.play()
                if event.key == pygame.K_ESCAPE:
                    paused = True

        # Обработка прыжка
        if is_jumping:
            jump_offset += jump_speed
            if jump_offset >= jump_height:
                jump_speed = -jump_speed
            if jump_offset <= 0:
                jump_offset = 0
                jump_speed = abs(jump_speed)
                is_jumping = False

        if len(obstacles) == 0 or obstacles[-1].y > OBSTACLE_HEIGHT + 10:
            lane = random.randint(0, 2)
            obs_x = lane * LANE_WIDTH + LANE_WIDTH // 2 - OBSTACLE_WIDTH // 2
            obs_y = -OBSTACLE_HEIGHT
            obstacles.append(pygame.Rect(
                obs_x, obs_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        increase_difficulty()
        update_obstacles()

        draw_obstacles()
        draw_player()

        if check_collision():
            if lives <= 0:
                draw_game_over()
                pygame.display.flip()
                running = False

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        wave_text = font.render(f"Wave: {wave}", True, BLACK)
        screen.blit(wave_text, (WIDTH - 100, 10))

        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(lives_text, (10, HEIGHT - 40))

        if wave % 2 == 0 and green_square is None and green_square_wave != wave:
            green_square = pygame.Rect(
                random.choice([0, LANE_WIDTH, 2 * LANE_WIDTH]) +
                LANE_WIDTH // 2 - 20,
                -40,
                40,
                40,
            )
            green_square_wave = wave

        if wave % 3 == 0 and blue_square is None and blue_square_wave != wave:
            blue_square = pygame.Rect(
                random.choice([0, LANE_WIDTH, 2 * LANE_WIDTH]) +
                LANE_WIDTH // 2 - 20,
                -40,
                40,
                40,
            )
            blue_square_wave = wave

        player_rect = pygame.Rect(
            player_x + player_lane * LANE_WIDTH,
            player_y - jump_offset,
            PLAYER_WIDTH,
            PLAYER_HEIGHT,
        )

        update_green_square()
        update_blue_square()

        if green_square:
            screen.blit(green_sprite, green_square)
        if blue_square:
            screen.blit(blue_sprite, blue_square)

        pygame.display.flip()
        clock.tick(FPS)

        if not running:
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game_loop()
                            waiting_for_restart = False
        while paused:
            screen.blit(font.render("Paused", True, BLACK),
                        (WIDTH // 2 - 50, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False


main_menu()
game_loop()
