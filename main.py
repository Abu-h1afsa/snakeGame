import pygame
import sys
import random
import pygame_menu

pygame.init()

size_block = 20
count_blocks = 20
aqua = (0, 250, 255)
BLUE = (205, 255, 255)
red = (255, 0, 0)
frame_color = (0, 128, 128)
header_color = (0, 128, 128)
header_margin = 70
margin = 1
snake_color = (0, 128, 0)
size = [size_block * count_blocks + 2 * size_block + margin + count_blocks,
        size_block * count_blocks + 2 * size_block + margin * size_block + header_margin]
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Змейка")
timer = pygame.time.Clock()
font_check = pygame.font.SysFont('courier', 38)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < size_block and 0 <= self.y < size_block

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):
    pygame.draw.rect(screen, color,
                     [size_block + column * size_block + margin * (column + 1),
                      header_margin + size_block + row * size_block + margin * (row + 1),
                      size_block, size_block])


def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, count_blocks - 1)
        y = random.randint(0, count_blocks - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, count_blocks - 1)
            empty_block.y = random.randint(0, count_blocks - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    check = 0
    speed = 1

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('exit')
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(frame_color)
        pygame.draw.rect(screen, header_color, [0, 0, size[0], header_margin])

        text_check = font_check.render(f"Total: {check}", 0, (255, 255, 255))
        text_speed = font_check.render(f"Speed: {speed}", 1, (255, 255, 255))
        screen.blit(text_check, (size_block, size_block))
        screen.blit(text_speed, (size_block + 235, size_block))

        for row in range(count_blocks):
            for column in range(count_blocks):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = aqua

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print('Crash')
            # pygame.quit()
            # sys.exit()
            break

        draw_block(red, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(snake_color, block.x, block.y)

        if apple == head:
            check += 1
            speed = check // 5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()
        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            print("Crash yourself")
            # pygame.quit()
            # sys.exit()
            break
        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


# main_theme.set_background_color_opacity(0.6)   задает прозрачность
# main_theme = pygame_menu.themes.THEME_BLUE.copy()

menu = pygame_menu.Menu('', 200, 200,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.button('Играть', start_the_game)
menu.add.button('Выход', pygame_menu.events.EXIT)

menu.mainloop(screen)
