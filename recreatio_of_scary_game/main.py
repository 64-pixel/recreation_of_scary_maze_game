import pygame, sys, time
from random import choice
from button import Button
import os
from os import listdir
from os.path import isfile, join


pygame.init()
pygame.font.init()

def win_screen():
    pygame.display.set_caption("Win screen")
    clock = pygame.time.Clock()
    
    restart_button = Button(
        image=pygame.image.load(
            "buttons/Options rect.png"
        ),
        pos=(380,300),
        text_input="restart",
        font = pygame.font.SysFont("Arial", 70),
        base_color = "#d7fcd4",
        hovering_color = "Red"
    )
    change_difficulty_button = Button(
            image=pygame.image.load(
                "buttons/Options rect.png"
            ),
            pos=(380,400),
            text_input="change difficulty",
            font = pygame.font.SysFont("Arial", 70),
            base_color = "#d7fcd4",
            hovering_color = "Red"
        )
    quit_button = Button(
                image=pygame.image.load(
                    "buttons/Quit rect.png"
                ),
                pos=(380,500),
                text_input="Quit",
                font = pygame.font.SysFont("Arial", 70),
                base_color = "#d7fcd4",
                hovering_color = "Red"
            )
    while True:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill("#1A1D1C")
    
            end_text = pygame.font.SysFont("Arial", 70).render(
                "You Win", True, "Gold"
            )
            end_rect = end_text.get_rect(center=(380,100))
            screen.blit(end_text, end_rect)
    
            for button in (quit_button, restart_button, change_difficulty_button):
                button.changeColor(mouse_pos)
                button.update(screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if restart_button.checkForInput(event.pos):
                                pygame.display.set_caption("Restart")
                                return "restart"

                            if change_difficulty_button.checkForInput(event.pos):
                                pygame.display.set_caption("Maze")
                                return "change_difficulty"
        
                            if quit_button.checkForInput(event.pos):
                                pygame.quit()
                                sys.exit()
                
            pygame.display.update()
            clock.tick(60)

def end_screen():
    pygame.display.set_caption("End screen")
    clock = pygame.time.Clock()
    
    restart_button = Button(
        image=pygame.image.load(
            "buttons/Options rect.png"
        ),
        pos=(380,300),
        text_input="restart",
        font = pygame.font.SysFont("Arial", 70),
        base_color = "#d7fcd4",
        hovering_color = "Red"
    )
    change_difficulty_button = Button(
                image=pygame.image.load(
                    "buttons/Options rect.png"
                ),
                pos=(380,400),
                text_input="change difficulty",
                font = pygame.font.SysFont("Arial", 70),
                base_color = "#d7fcd4",
                hovering_color = "Red"
            )
    quit_button = Button(
                image=pygame.image.load(
                    "buttons/Quit rect.png"
                ),
                pos=(380,500),
                text_input="Quit",
                font = pygame.font.SysFont("Arial", 70),
                base_color = "#d7fcd4",
                hovering_color = "Red"
            )
    while True:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill("#1A1D1C")
    
            end_text = pygame.font.SysFont("Arial", 70).render(
                "You Died", True, "Red"
            )
            end_rect = end_text.get_rect(center=(380,100))
            screen.blit(end_text, end_rect)
    
            for button in (quit_button, restart_button, change_difficulty_button):
                button.changeColor(mouse_pos)
                button.update(screen)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
        
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if change_difficulty_button.checkForInput(event.pos):
                                pygame.display.set_caption("Maze")
                                return "change_difficulty"
                            if restart_button.checkForInput(event.pos):
                                pygame.display.set_caption("Restart")
                                return "restart"
        
                            if quit_button.checkForInput(event.pos):
                                pygame.quit()
                                sys.exit()
                
            pygame.display.update()
            clock.tick(60)

def start_screen():
    pygame.display.set_caption("Start screen")
    clock = pygame.time.Clock()
    current_difficulty = None

    option1 = Button(
        image=pygame.image.load(
            "buttons/Options rect.png"
        ),
        pos=(380,200),
        text_input="BABY MODE (no jumpscare)",
        font = pygame.font.SysFont("Arial", 30),
        base_color = "#d7fcd4",
        hovering_color = "Red"
    )
    option2 = Button(
            image=pygame.image.load(
                "buttons/Options rect.png"
            ),
            pos=(380,300),
            text_input="MEDIUM MODE",
            font = pygame.font.SysFont("Arial", 30),
            base_color = "#d7fcd4",
            hovering_color = "Red"
        )
    option3 = Button(
            image=pygame.image.load(
                "buttons/Options rect.png"
            ),
            pos=(380,400),
            text_input="HARD MODE",
            font = pygame.font.SysFont("Arial", 30),
            base_color = "#d7fcd4",
            hovering_color = "Red"
        )
    quit_button = Button(
            image=pygame.image.load(
                "buttons/Quit rect.png"
            ),
            pos=(380,505),
            text_input="Quit",
            font = pygame.font.SysFont("Arial", 30),
            base_color = "#d7fcd4",
            hovering_color = "Red"
        )
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill("#1A1D1C")

        start_text = pygame.font.SysFont("Arial", 70).render(
            "Select Difficulty", True, "Blue"
        )
        start_rect = start_text.get_rect(center=(380,100))
        screen.blit(start_text, start_rect)

        for button in (quit_button, option1, option2, option3):
            button.changeColor(mouse_pos)
            button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if option1.checkForInput(event.pos):
                            pygame.display.set_caption("Scary Maze Game")
                            current_difficulty = "difficulty1"
                            return "option1"
    
                        if option2.checkForInput(event.pos):
                            pygame.display.set_caption("Scary Maze Game")
                            current_difficulty = "difficulty2"
                            return "option2"

                        if option3.checkForInput(event.pos):
                            pygame.display.set_caption("Scary Maze Game")
                            current_difficulty = "difficulty3"
                            return "option3"
    
                        if quit_button.checkForInput(event.pos):
                            pygame.quit()
                            sys.exit()
                    return current_difficulty
            
        pygame.display.update()
        clock.tick(60)
        



class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input

        self.text = self.font.render(
            self.text_input, True, self.base_color
        )

        # Pokud nemáme obrázek, použijeme jako tlačítko samotný text.
        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(
            center=(self.x_pos, self.y_pos)
        )
        self.text_rect = self.text.get_rect(
            center=(self.x_pos, self.y_pos)
        )

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            color = self.hovering_color
        else:
            color = self.base_color

        self.text = self.font.render(
            self.text_input, True, color
        )
        self.text_rect = self.text.get_rect(
            center=(self.x_pos, self.y_pos)
        )


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
        steps_x = x - self.x
        steps_y = y - self.y
        abs_steps_y = abs(steps_y)
        abs_steps_x = abs(steps_x)

        for s in range(abs_steps_y):
            if collision:
                 break
            for cell in grid_cells:
                if collision:
                    break
            
                if cell.walls['top']:        
                    direction_y = 1 if steps_y > 0 else -1
                    test_y = self.y + (s+1) * direction_y
                    test_player = pygame.Rect(self.x, test_y, self.player_size, self.player_size)
                    wall_rect_top = pygame.Rect(cell.x*tile, cell.y * tile, tile, thickness)
                    wall_rect_bottom = pygame.Rect(cell.x*tile, cell.y * tile + tile - thickness, tile, thickness)
                    if test_player.colliderect(wall_rect_top) :
                        collision = True
                        break

                if cell.walls['bottom']:
                    direction_y = 1 if steps_y > 0 else -1
                    test_y = self.y + (s+1) * direction_y
                    test_player = pygame.Rect(self.x, test_y, self.player_size, self.player_size)
                    wall_rect_top = pygame.Rect(cell.x*tile, cell.y * tile, tile, thickness)
                    wall_rect_bottom = pygame.Rect(cell.x*tile, cell.y * tile + tile - thickness, tile, thickness)
                    if test_player.colliderect(wall_rect_bottom):
                        collision = True
                        break

        for i in range(abs_steps_x): 
            if collision:
                 break                  
            for cell in grid_cells:
                if collision:
                        break
                
                if cell.walls['left'] :
                    direction = 1 if steps_x > 0 else -1                  
                    test_x = self.x + (i+1) * direction
                    wall_rect_left = pygame.Rect(cell.x * tile, cell.y * tile, thickness, tile)
                    wall_rect_right = pygame.Rect(cell.x * tile + tile - thickness, cell.y * tile, thickness, tile)
                    test_player = pygame.Rect(test_x, self.y, self.player_size, self.player_size)
                    if test_player.colliderect(wall_rect_left):
                        collision = True
                        break    
                if cell.walls['right']:
                    direction = 1 if steps_x > 0 else -1                  
                    test_x = self.x + (i+1) * direction
                    wall_rect_left = pygame.Rect(cell.x * tile, cell.y * tile, thickness, tile)
                    wall_rect_right = pygame.Rect(cell.x * tile + tile - thickness, cell.y * tile, thickness, tile)
                    test_player = pygame.Rect(test_x, self.y, self.player_size, self.player_size)
                    if test_player.colliderect(wall_rect_right):
                        collision = True
                        break 
                             
        return collision    


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
            
#    def touch_wall2(self): 
        if collision == True:
            scary_img2 = pygame.image.load(scary_img2)
            screen.blit(scary_img2)


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
    def __init__(self, screen, difficulty):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)
        self.message_color = pygame.Color("cyan")
        self.running = True
        self.game_over = False
        self.FPS = pygame.time.Clock()
        self.difficulty = difficulty
        

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
        chase = False
        maze = Maze(cols, rows)
        game = Game(maze.grid_cells[-1], tile)
        player = Player(tile //3, tile //3)
        cube_size = player.player_size
        dragging = False
        offset_x = 0
        offset_y = 0
        clock = Clock()
        maze.generate_maze()
        clock.start_timer()
        self.touched_wall = False
        scary_img = pygame.image.load("img/scary_img.jpg")
        window_size2 = (800, 800)
        scary_img1 = pygame.transform.scale(scary_img, window_size2) 
        scare_start_time = None
        
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

                            if player.check_mouse_collision(new_x, new_y, maze.grid_cells, tile, maze.thickness) == True:
                                self.touched_wall = True
                                if self.touched_wall and scare_start_time == None:
                                    scare_start_time = pygame.time.get_ticks()

            if self.touched_wall and self.difficulty in ("option2", "option3"):
                self.screen.blit(scary_img1, (0,0))
                pygame.display.flip()
                if pygame.time.get_ticks() - scare_start_time >= 2000:
                    result = end_screen()

                    if result == "change_difficulty":
                        return

                    if result == "restart":
                        player.x = 10
                        player.y = 10
                        self.touched_wall = False
                        scare_start_time = None
                        continue
                        

            else:   
                self._draw(maze,tile, player, game, clock)

            if game.is_game_over(player):
                self.game_over = True
                result2 =win_screen()

                if result2 == "change_difficulty":
                    return
                if result2 == "restart":
                    player.x = 10
                    player.y = 10
                    self.touched_wall = False
                    scare_start_time = None
                    continue
            self.FPS.tick(60)

            

            
if __name__ == "__main__":


    window_size = (603,603)
    screen = (window_size[0] + 150, window_size[-1])
    tile_size = 30
    screen = pygame.display.set_mode(screen)
    pygame.display.set_caption("Maze")

    
    while True:
        choices = start_screen()

        if choices == "option1":
            #baby mode
            pygame.display.set_caption("Baby Maze")
            game = Main(screen, choices)
            game.main(window_size, tile_size, tile_size)
            chase = False

        elif choices == "option2":
            #medium
            pygame.display.set_caption("Medium Maze")
            game = Main(screen, choices)
            game.main(window_size, tile_size, tile_size)
            chase = False

        elif choices == "option3":
            #hard (chase after 15 s)
            pygame.display.set_caption("Hard Maze")
            game = Main(screen, choices)
            game.main(window_size, tile_size, tile_size)
            chase = True
            