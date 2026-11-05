import pygame, sys, time
from random import choice

pygame.init()
pygame.font.init()


class Cell:
    def __init__(self,x,y,thickness):
        self.x, self.y = x,y
        self.thickness = thickness
        self.walls = {'top': True, 'right':True, 'bottom':True, 'left': True}
        self.visited = False

    def draw(self, sc, tile):
        x,y = self.x * tile, self.y * tile
        if self.walls['top']:
            pygame.draw.line(sc, pygame.Color('darkBlue'), (x,y), (x + tile,y), self.thickness)
        if self.walls['right']:
                    pygame.draw.line(sc, pygame.Color('darkBlue'), (x + tile,y), (x + tile,y + tile), self.thickness)
        if self.walls['bottom']:
                    pygame.draw.line(sc, pygame.Color('darkBlue'), (x + tile,y + tile), (x,y + tile), self.thickness)
        if self.walls['left']:
                    pygame.draw.line(sc, pygame.Color('darkBlue'), (x,y + tile), (x,y), self.thickness)

    def check_cell(self,x,y,cols,rows,grid_cells):
           find_index = lambda x,y: x+y*cols
           if x<0 or x> cols - 1 or y< 0 or y >rows - 1:
                  return False
           return grid_cells[find_index(x,y)]

    def check_neighbors(self,cols,rows, grid_cells):
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
        self.color = (63, 230, 22)
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

    def check_mouse_collision(self,x,y, grid_cells, tile, thickness):
        collision = False
        new_player = pygame.Rect(x,y, self.player_size, self.player_size)
        for cell in grid_cells:
            steps_x = new_x - player.x
            if cell.walls['left']:
                for i in steps_x:
                    if new_x + i == cell:
                        wall_rect_left = pygame.Rect(cell.x * tile, cell.y * tile, thickness, tile)
                        if new_player.colliderect(wall_rect_left):
                                collision = True
            if cell.walls['right']:
                wall_rect_right = pygame.Rect(cell.x * tile + tile - thickness, cell.y * tile, thickness, tile)
                if new_player.colliderect(wall_rect_right):
                    collision = True
            if cell.walls['top']:
                wall_rect_top = pygame.Rect(cell.x*tile, cell.y * tile, tile, thickness)
                if new_player.colliderect(wall_rect_top):
                    collision = True
            if cell.walls['bottom']:
                wall_rect_bottom = pygame.Rect(cell.x*tile, cell.y * tile + tile - thickness, tile, thickness)
                if new_player.colliderect(wall_rect_bottom):
                    collision = True       
        return collision    

    def check_move(self,tile, grid_cells, thickness):
        current_cell_x, current_cell_y = self.x // tile, self.y // tile
        current_cell = self.get_current_cell(current_cell_x, current_cell_y, grid_cells)
        current_cell_abs_x, current_cell_abs_y = current_cell_x  * tile, current_cell_y * tile
        if self.left_pressed:
            if current_cell.wall == self.player.rect:
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
        instructions1 = self.font.render("Left click", True, self.message_color)
        instructions2 = self.font.render("on the cube", True, self.message_color)
        instructions3 = self.font.render("and drag", True, self.message_color)
        instructions4 = self.font.render("To Move", True, self.message_color)
        self.screen.blit(instructions1, (655,300))
        self.screen.blit(instructions2, (610,331))
        self.screen.blit(instructions3, (630,362))
        self.screen.blit(instructions4, (640,380))

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
                            new_x = mouse_x - offset_x
                            new_y = mouse_y - offset_y
                            if player.check_mouse_collision(new_x, new_y, maze.grid_cells, tile, maze.thickness) == False:
                                player.x = new_x 
                                player.y = new_y

            
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

