import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox


value = 10


def main_menu():
    #Основной экран
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((700, 600))
    running = True
    start_button = font.render("Start", True, (255, 255, 255))
    control_button = font.render("Controls", True, (255, 255, 255))
    exit_button = font.render("Exit", True, (255, 255, 255))
    font_m = pygame.font.Font(None, 100)
    settigns = font.render("Settings", True, (255, 255, 255))
    settigns_rect = settigns.get_rect(center=(350, 400))
    maddd = font_m.render("Red Light Signals", True, (255, 255, 255))
    exit_button_rect = exit_button.get_rect(center=(350, 500))
    control_button_rect = control_button.get_rect(center=(350, 300))
    start_button_rect = start_button.get_rect(center=(350, 200))
    while running:
        screen.fill((255, 255, 255))
        screen.blit(pygame.image.load("data/main_background.jpg"), (0, 0))
        screen.blit(maddd, (35, 20))
        screen.blit(start_button, start_button_rect)
        screen.blit(control_button, control_button_rect)
        screen.blit(exit_button, exit_button_rect)
        screen.blit(settigns, settigns_rect)

        pygame.display.flip()
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    running = False
                # Окно гайда управления
                elif control_button_rect.collidepoint(event.pos):
                    instructions = "Use arrow keys to move space to jump esc to pause."
                    text = font.render(instructions, True, (0, 0, 0))
                    screen.fill((255, 255, 255))
                    screen.blit(text, (350 - text.get_width() // 2, 200))
                    screen.blit(font.render("press esc to close",
                                True, (0, 0, 0)), (10, 10))
                    pygame.display.flip()
                    a = 0
                    while a == 0:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    a = 1
                # Окно насторек
                elif settigns_rect.collidepoint(event.pos):
                    slider = Slider(screen, 100, 200, 200, 20, min=0, max=100)
                    level = TextBox(screen, 350, 200, 50, 30)
                    run = 1
                    while run == 1:
                        screen.fill((255, 255, 255))
                        events = pygame.event.get()
                        for event in events:
                            if event.type == pygame.QUIT:
                                quit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    run = 0
                        screen.blit(font.render("Volume level",
                                    True, (0, 0, 0)), (100, 100))
                        screen.blit(font.render("press esc to close",
                                                True, (0, 0, 0)), (10, 10))
                        pygame_widgets.update(events)
                        global value
                        value = slider.getValue()
                        level.setText(str(value))
                        pygame.display.update()
                        pygame.display.flip()

                elif exit_button_rect.collidepoint(event.pos):
                    running = False
                    quit()

# Изменение громкости
def change_volume():
    pygame.mixer.music.set_volume(value / 100)
