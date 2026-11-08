import asyncio
import pygame
import time
from random import choice


pygame.init()
pygame.font.init()

# Rozměry hry
WINDOW_SIZE = (753, 603)
MAZE_SIZE = (603, 603)
TILE_SIZE = 30
FPS = 60

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Maze")


def load_image(path, size=None):
    image = pygame.image.load(path).convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    return image


def make_button_image(path):
    return load_image(path)




class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, surface):
        if self.image is not None:
            surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        color = self.hovering_color if self.rect.collidepoint(position) else self.base_color
        self.text = self.font.render(self.text_input, True, color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))



async def menu_screen(kind):
    pygame.display.set_caption(kind)
    frame_clock = pygame.time.Clock()
    font_size = 70 if kind in ("Win screen", "End screen") else 30
    font = pygame.font.SysFont("Arial", font_size)

    if kind == "Start screen":
        buttons = [
            (Button(make_button_image("buttons/Options rect.png"), (380, 200),
                    "BABY MODE (no jumpscare)", font, "#d7fcd4", "Red"), "option1"),
            (Button(make_button_image("buttons/Options rect.png"), (380, 300),
                    "MEDIUM MODE", font, "#d7fcd4", "Red"), "option2"),
            (Button(make_button_image("buttons/Options rect.png"), (380, 400),
                    "HARD MODE", font, "#d7fcd4", "Red"), "option3"),
            (Button(make_button_image("buttons/Quit rect.png"), (380, 505),
                    "Quit", font, "#d7fcd4", "Red"), "quit"),
        ]
        heading = "Select Difficulty"
        heading_color = "Blue"

    else:
        buttons = [
            (Button(make_button_image("buttons/Options rect.png"), (380, 300),
                    "restart", font, "#d7fcd4", "Red"), "restart"),
            (Button(make_button_image("buttons/Options rect.png"), (380, 400),
                    "change difficulty", font, "#d7fcd4", "Red"), "change_difficulty"),
            (Button(make_button_image("buttons/Quit rect.png"), (380, 500),
                    "Quit", font, "#d7fcd4", "Red"), "quit"),
        ]
        heading = "You Win" if kind == "Win screen" else "You Died"
        heading_color = "Gold" if kind == "Win screen" else "Red"

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button, result in buttons:
                    if button.checkForInput(event.pos):
                        return result

        screen.fill("#1A1D1C")
        heading_surface = font.render(heading, True, heading_color)
        heading_rect = heading_surface.get_rect(center=(380, 100))
        screen.blit(heading_surface, heading_rect)

        for button, _ in buttons:
            button.changeColor(mouse_pos)
            button.update(screen)

        pygame.display.flip()
        frame_clock.tick(FPS)
        await asyncio.sleep(0)


async def start_screen():
    return await menu_screen("Start screen")


async def end_screen():
    return await menu_screen("End screen")


async def win_screen():
    return await menu_screen("Win screen")


class Cell:
    def __init__(self, x, y, thickness):
        self.x, self.y = x, y
        self.thickness = thickness
        self.walls = {
            "top": True,
            "right": True,
            "bottom": True,
            "left": True,
        }
        self.visited = False

    def draw(self, surface, tile):
        x, y = self.x * tile, self.y * tile
        color = pygame.Color("darkBlue")

        if self.walls["top"]:
            pygame.draw.line(surface, color, (x, y), (x + tile, y), self.thickness)
        if self.walls["right"]:
            pygame.draw.line(surface, color, (x + tile, y), (x + tile, y + tile), self.thickness)
        if self.walls["bottom"]:
            pygame.draw.line(surface, color, (x + tile, y + tile), (x, y + tile), self.thickness)
        if self.walls["left"]:
            pygame.draw.line(surface, color, (x, y + tile), (x, y), self.thickness)

    def check_cell(self, x, y, cols, rows, grid_cells):
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return False
        return grid_cells[x + y * cols]

    def check_neighbors(self, cols, rows, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)

        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False


class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.thickness = 4
        self.grid_cells = [
            Cell(col, row, self.thickness)
            for row in range(rows)
            for col in range(cols)
        ]

    def remove_walls(self, current, next_cell):
        dx = current.x - next_cell.x
        if dx == 1:
            current.walls["left"] = False
            next_cell.walls["right"] = False
        elif dx == -1:
            current.walls["right"] = False
            next_cell.walls["left"] = False

        dy = current.y - next_cell.y
        if dy == 1:
            current.walls["top"] = False
            next_cell.walls["bottom"] = False
        elif dy == -1:
            current.walls["bottom"] = False
            next_cell.walls["top"] = False

    def generate_maze(self):
        current_cell = self.grid_cells[0]
        stack = []
        visited_count = 1

        while visited_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(
                self.cols, self.rows, self.grid_cells
            )

            if next_cell:
                next_cell.visited = True
                visited_count += 1
                stack.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif stack:
                current_cell = stack.pop()

        return self.grid_cells


class Enemy:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.speed = 2
        self.size = 15
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.color = "Red"
        self.tile = tile
        self.target = None

    def find_path(self, maze, player):
        enemy_cell_x = int(self.x // self.tile)
        enemy_cell_y = int(self.y // self.tile)
        player_cell_x = int(player.x // self.tile)
        player_cell_y = int(player.y // self.tile)

        if not (0 <= enemy_cell_x < maze.cols and 0 <= enemy_cell_y < maze.rows):
            return set(), []
        if not (0 <= player_cell_x < maze.cols and 0 <= player_cell_y < maze.rows):
            return set(), []

        start = maze.grid_cells[enemy_cell_x + enemy_cell_y * maze.cols]
        goal = maze.grid_cells[player_cell_x + player_cell_y * maze.cols]

        visited = {start}
        queue = [start]
        parent = {start: None}

        while queue:
            cell = queue.pop(0)
            if cell == goal:
                break

            neighbors = []
            if not cell.walls["top"] and cell.y > 0:
                neighbors.append(maze.grid_cells[cell.x + (cell.y - 1) * maze.cols])
            if not cell.walls["right"] and cell.x + 1 < maze.cols:
                neighbors.append(maze.grid_cells[cell.x + 1 + cell.y * maze.cols])
            if not cell.walls["bottom"] and cell.y + 1 < maze.rows:
                neighbors.append(maze.grid_cells[cell.x + (cell.y + 1) * maze.cols])
            if not cell.walls["left"] and cell.x > 0:
                neighbors.append(maze.grid_cells[cell.x - 1 + cell.y * maze.cols])

            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = cell

        if goal not in parent:
            return visited, []

        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return visited, path

    def update(self, maze, player):
        if self.target is None:
            _, path = self.find_path(maze, player)
            if len(path) >= 2:
                self.target = path[1]
            else:
                return

        target_x = self.target.x * self.tile + (self.tile - self.size) / 2
        target_y = self.target.y * self.tile + (self.tile - self.size) / 2

        if abs(self.x - target_x) <= 1 and abs(self.y - target_y) <= 1:
            self.x = target_x
            self.y = target_y
            self.target = None
            return

        if abs(self.x - target_x) > 1:
            if self.x < target_x:
                self.x = min(self.x + self.speed, target_x)
            else:
                self.x = max(self.x - self.speed, target_x)
        elif abs(self.y - target_y) > 1:
            if self.y < target_y:
                self.y = min(self.y + self.speed, target_y)
            else:
                self.y = max(self.y - self.speed, target_y)

    def draw(self, surface):
        self.rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)
        pygame.draw.rect(surface, self.color, self.rect)


class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 10
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        self.color = (63, 230, 22)
        self.velx = 0
        self.vely = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    def check_mouse_collision(self, x, y, grid_cells, tile, thickness):
        steps_x = int(x - self.x)
        steps_y = int(y - self.y)

        for step in range(abs(steps_y)):
            direction_y = 1 if steps_y > 0 else -1
            test_y = self.y + (step + 1) * direction_y
            test_player = pygame.Rect(self.x, test_y, self.player_size, self.player_size)

            for cell in grid_cells:
                cell_x = cell.x * tile
                cell_y = cell.y * tile

                if cell.walls["top"]:
                    wall = pygame.Rect(cell_x, cell_y, tile, thickness)
                    if test_player.colliderect(wall):
                        return True

                if cell.walls["bottom"]:
                    wall = pygame.Rect(
                        cell_x, cell_y + tile - thickness, tile, thickness
                    )
                    if test_player.colliderect(wall):
                        return True

        for step in range(abs(steps_x)):
            direction_x = 1 if steps_x > 0 else -1
            test_x = self.x + (step + 1) * direction_x
            test_player = pygame.Rect(test_x, self.y, self.player_size, self.player_size)

            for cell in grid_cells:
                cell_x = cell.x * tile
                cell_y = cell.y * tile

                if cell.walls["left"]:
                    wall = pygame.Rect(cell_x, cell_y, thickness, tile)
                    if test_player.colliderect(wall):
                        return True

                if cell.walls["right"]:
                    wall = pygame.Rect(
                        cell_x + tile - thickness, cell_y, thickness, tile
                    )
                    if test_player.colliderect(wall):
                        return True

        return False

    def draw(self, surface):
        self.rect = pygame.Rect(
            int(self.x), int(self.y), self.player_size, self.player_size
        )
        pygame.draw.rect(surface, self.color, self.rect)

    def update(self):
        self.velx = 0
        self.vely = 0

        if self.left_pressed and not self.right_pressed:
            self.velx = -self.speed
        if self.right_pressed and not self.left_pressed:
            self.velx = self.speed
        if self.up_pressed and not self.down_pressed:
            self.vely = -self.speed
        if self.down_pressed and not self.up_pressed:
            self.vely = self.speed

        self.x += self.velx
        self.y += self.vely
        self.rect = pygame.Rect(
            int(self.x), int(self.y), self.player_size, self.player_size
        )


class Game:
    def __init__(self, goal_cell, tile):
        self.font = pygame.font.SysFont("impact", 35)
        self.message_color = pygame.Color("darkorange")
        self.goal_cell = goal_cell
        self.tile = tile
        self.goal_image = load_image("img/gate.png", (tile, tile))

    def add_goal_point(self, surface):
        surface.blit(
            self.goal_image,
            (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile),
        )

    def message(self):
        return self.font.render("You WIN!!", True, self.message_color)

    def is_game_over(self, player):
        goal_x = self.goal_cell.x * self.tile
        goal_y = self.goal_cell.y * self.tile
        return (
            player.x + player.player_size > goal_x
            and player.y + player.player_size > goal_y
        )


class GameClock:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.font = pygame.font.SysFont("monospace", 35)
        self.message_color = pygame.Color("yellow")

    def start_timer(self):
        self.start_time = time.time()

    def update_timer(self):
        if self.start_time is not None:
            self.elapsed_time = time.time() - self.start_time

    def display_timer(self):
        secs = int(self.elapsed_time % 60)
        mins = int(self.elapsed_time / 60)
        return self.font.render(
            f"{mins:02}:{secs:02}", True, self.message_color
        )

    def stop_timer(self):
        self.start_time = None



class Main:
    def __init__(self, surface, difficulty):
        self.screen = surface
        self.font = pygame.font.SysFont("Arial", 30)
        self.message_color = pygame.Color("cyan")
        self.difficulty = difficulty
        self.touched_wall = False
        self.game_over = False
        self.frame_clock = pygame.time.Clock()

        scary_image = load_image("img/scary_img.jpg", WINDOW_SIZE)
        self.scary_image = scary_image

    def instructions(self):
        texts = [
            ("Left click", (655, 300)),
            ("on the cube", (610, 331)),
            ("and drag", (630, 362)),
            ("To Move", (640, 380)),
        ]
        for text, pos in texts:
            self.screen.blit(
                self.font.render(text, True, self.message_color), pos
            )

    def draw(self, maze, tile, player, game, game_clock, enemy=None):
        self.screen.fill("gray")
        self.screen.fill(pygame.Color("darkslategray"), (603, 0, 150, 603))

        for cell in maze.grid_cells:
            cell.draw(self.screen, tile)

        game.add_goal_point(self.screen)
        player.draw(self.screen)
        self.instructions()

        if self.game_over:
            game_clock.stop_timer()
            self.screen.blit(game.message(), (610, 120))
        else:
            game_clock.update_timer()

        self.screen.blit(game_clock.display_timer(), (625, 200))

        if enemy is not None:
            enemy.draw(self.screen)

        pygame.display.flip()

    def reset_positions(self, player, enemy):
        player.x = TILE_SIZE // 3
        player.y = TILE_SIZE // 3
        player.rect.topleft = (player.x, player.y)

        enemy.x = TILE_SIZE // 3
        enemy.y = TILE_SIZE // 3
        enemy.rect.topleft = (enemy.x, enemy.y)
        enemy.target = None

    async def main(self, frame_size, tile):
        cols = frame_size[0] // tile
        rows = frame_size[1] // tile

        maze = Maze(cols, rows)
        maze.generate_maze()

        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile // 3, tile // 3)
        enemy = Enemy(tile // 3, tile // 3, tile)
        game_clock = GameClock()
        game_clock.start_timer()

        dragging = False
        offset_x = 0
        offset_y = 0
        chase = False
        scare_start_time = None
        game_start_ticks = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if (
                        player.x <= mouse_x <= player.x + player.player_size
                        and player.y <= mouse_y <= player.y + player.player_size
                    ):
                        dragging = True
                        offset_x = mouse_x - player.x
                        offset_y = mouse_y - player.y

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False

                elif event.type == pygame.MOUSEMOTION and dragging:
                    mouse_x, mouse_y = event.pos
                    new_x = mouse_x - offset_x
                    new_y = mouse_y - offset_y

                    if not player.check_mouse_collision(
                        new_x, new_y, maze.grid_cells, tile, maze.thickness
                    ):
                        player.x = new_x
                        player.y = new_y
                        player.rect.topleft = (int(player.x), int(player.y))
                    else:
                        self.touched_wall = True
                        if scare_start_time is None:
                            scare_start_time = pygame.time.get_ticks()

            if self.difficulty == "option3":
                if pygame.time.get_ticks() - game_start_ticks >= 10000:
                    chase = True

            if chase:
                enemy.update(maze, player)
                enemy.draw(self.screen)

            player.draw(self.screen)

            # Jumpscare při dotyku zdi nebo při chycení nepřítelem
            caught = chase and enemy.rect.colliderect(player.rect)
            should_scare = (
                self.touched_wall and self.difficulty in ("option2", "option3")
            ) or caught

            if should_scare:
                if scare_start_time is None:
                    scare_start_time = pygame.time.get_ticks()

                self.screen.blit(self.scary_image, (0, 0))
                pygame.display.flip()

                if pygame.time.get_ticks() - scare_start_time >= 2000:
                    result = await end_screen()

                    if result == "quit":
                        return "quit"
                    if result == "change_difficulty":
                        return "change_difficulty"
                    if result == "restart":
                        self.reset_positions(player, enemy)
                        self.touched_wall = False
                        scare_start_time = None
                        chase = False
                        game_start_ticks = pygame.time.get_ticks()
                        game_clock = GameClock()
                        game_clock.start_timer()
                        continue

            else:
                self.draw(
                    maze, tile, player, game, game_clock,
                    enemy if chase else None
                )

            if game.is_game_over(player):
                self.game_over = True
                result = await win_screen()

                if result == "quit":
                    return "quit"
                if result == "change_difficulty":
                    return "change_difficulty"
                if result == "restart":
                    self.reset_positions(player, enemy)
                    self.touched_wall = False
                    scare_start_time = None
                    chase = False
                    game_start_ticks = pygame.time.get_ticks()
                    self.game_over = False
                    game_clock = GameClock()
                    game_clock.start_timer()
                    continue

            self.frame_clock.tick(FPS)
            await asyncio.sleep(0)


async def main():
    while True:
        selected = await start_screen()

        if selected == "quit":
            break

        game = Main(screen, selected)
        result = await game.main(MAZE_SIZE, TILE_SIZE)

        if result == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
