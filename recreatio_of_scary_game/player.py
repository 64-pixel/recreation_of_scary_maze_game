import pygame

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






    #running = True
    #while running:
            #for event in pygame.event.get():
              #   if event.type == pygame.QUIT:
             #         running = False

            #mouseX, mouseY = pygame.mouse.get_pos()

