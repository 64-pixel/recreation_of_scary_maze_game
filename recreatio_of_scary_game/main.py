import pygame, sys, time


pygame.init()
pygame.font.init()
from cell import Cell

class Maze:
    def __init__(self,cols,rows):
        self.cols = cols
        self.rows = rows
        self.thickness = 4
        self.grid_cells = [Cell(col,row,self.thickness)for row in range(self.rows) for col in range(self.cols)]

    def remove_walls(self,current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top']= False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom']= False
            next.walls['top'] = False

    def generate_maze(self):
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1
        while break_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.cols,self.rows,self.grid_cells)
            if next_cell:
                next_cell.visited = True
                break_count +=1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        return self.grid_cells

class Player:
    def __init__(self,x,y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 10
        self.rect = pygame.Rect(self.x, self.y, self.player_size, self.player_size)
        self.color = (255, 166, 125)
        self.velx = 0
        self.vely = 0
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.speed = 4

    def get_current_cell(self, x, y, grid_cells):
        for cell in grid_cells:
            if cell.x ==x and cell.y == y:
                return cell

    def check_move(self,tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x  * tile, current_cell_y * tile
        if self.left_pressed:
            if current_cell.wall['left']:
                if self.x <= current_cell_abs_x + thickness:
                    self.left_pressed = False
        if self.right_pressed:
            if current_cell.wall['right']:
                if self.x >= current_cell_abs_x + tile - (self.player_size + thickness):
                    self.right_pressed = False
        if self.up_pressed: 
            if current_cell.wall['up']:
                            if self.y <= current_cell_abs_y + thickness:
                                self.up_pressed = False
        if self.down_pressed:
                    if current_cell.wall['bottom']:
                        if self.y >= current_cell_abs_y + tile - (self.player_size + thickness):
                            self.down_pressed = False
    def draw(self, screen):
         pygame.draw.rect(screen, self.color, self.rect, )

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
        self.rect = pygame.Rect(int(self.x), int(self.y), self.player_size, self.player_size)

class Game:
    def __init__(self, goal_cell, tile):
        self.font = pygame.font.SysFont("impact", 35)
        self.message_color = pygame.Color("darkorange")
        self.goal_cell = goal_cell
        self.tile = tile

    def add_goal_point(self,screen):
        img_path = 'img/gate.png'
        img = pygame.image.load(img_path)
        img = pygame.transform.scale(img, (self.tile, self.tile))
        screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

    def message(self):
        msg = self.font.render("You WIN!!", True, self.message_color)
        return msg
    def is_game_over(self,player):
        goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
        if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
            return True
        else:
            return False

class Clock:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.font = pygame.font.SysFont("monospace", 35)
        self.message_color = pygame.Color("yellow")

    def start_timer(self):
        self.start_time = time.time()

    def update_timer(self):
        if self.start_time is not None:
            self.elapsed_time = time.time() - self.start_time

    def display_timer(self):
        secs = int(self.elapsed_time %60)
        mins = int(self.elapsed_time / 60)
        my_time = self.font.render(f"{mins:02}:{secs:02}", True, self.message_color)
        return my_time

    def stop_timer(self):
        self.start_time = None

class Main():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()

    def instructions(self):
        instructions1 = self.font.render("Use", True, self.message_color)
        instructions2 = self.font.render("Arrow Keys", True, self.message_color)
        instructions3 = self.font.render("To Move", True, self.message_color)
        self.screen.blit(instructions1, (655,300))
        self.screen.blit(instructions2, (610,331))
        self.screen.blit(instructions3, (630,362))

    def _draw(self, maze, tile, player, game, clock):
        [cell.draw(self.screen, tile) for cell in maze.grid_cells]
        game.add_goal_point(self.screen)
        player.update() 
        player.draw(self.screen)


        self.instructions()
        if self.game_over:
            clock.stop_timer()
            self.screen.blit(game.message(), (610,120))
        else:
            clock.update_timer()
        self.screen.blit(clock.display_timer(), (625,200))
        pygame.display.flip()

    def main(self, frame_size,clock ,tile):
        cols, rows = frame_size[0] // tile, frame_size[-1] // tile
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile //3, tile //3)
        cube_x = player.x
        cube_y = player.y
        cube_size = player.player_size
        dragging = False
        offset_x = 0
        offset_y = 0
        clock = Clock()
        maze.generate_maze()
        clock.start_timer()
        while self.running:
            self.screen.fill("gray")
            self.screen.fill(pygame.Color("darkslategray"), (603,0,752,752))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if(
                            player.x <= mouse_x <= player.x + cube_size and player.y <= mouse_y <= player.y + cube_size

                        ):
                            dragging = True
                            offset_x = mouse_x - player.x
                            offset_y = mouse_y - player.y
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        mouse_x, mouse_y = event.pos
                        player.x = mouse_x - offset_x
                        player.y = mouse_y - offset_y

            
            if game.is_game_over(player):
                self.game_over = True
                #player.left_pressed = False
                #player.right_pressed = False
                #player.up_pressed = False
                #player.down_pressed = False
            self._draw(maze,tile,player,game,clock)
            self.FPS.tick(60)

            
if __name__ == "__main__":
    window_size = (602,602)
    screen = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze")

    game = Main(screen)
    game.main(window_size, tile_size, tile_size)

