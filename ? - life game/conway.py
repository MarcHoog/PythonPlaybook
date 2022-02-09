import pygame
import numpy as np
import time


class conway:
    def __init__(self,
                 surface,
                 width:int,
                 height:int,
                 scale:int,
                 offset = 1,
                 active_color = (255,255,255),
                 inactive_color = (0,0,0)):
        
        self.surface = surface
        self.width = width
        self.heigt = height
        self.scale = scale
        self.offset = offset
        self.active_color = active_color
        self.inactive_color = inactive_color
        
        self.colomns = int(height / scale)
        self.rows = int(width / scale)
        
        self.grid = np.random.randint(0, 2, size=(self.colomns, self.rows), dtype=bool)
        
        
    def run(self):
        # simulates a generation
        start_time = time.time()
        self._draw_grid()
        self._update_grid()
        print(f"every generation takes {time.time() - start_time}")
        
        
    def _draw_grid(self):
        # I know this works
        # But I would have to read pygame more often to actually read how it's drawing works
        for row in range(self.rows):
            for col in range(self.colomns):
                _right = row * self.scale
                _left = col * self.scale
                _spacing = self.scale - self.offset 
                
                if self.grid[row,col]:
                    pygame.draw.rect(self.surface, self.active_color, [_right,_left,_spacing,_spacing])
                else:
                    pygame.draw.rect(self.surface, self.inactive_color, [_right,_left,_spacing,_spacing])

    def _update_grid(self):
        updated_grid = self.grid.copy()
        for row in range(self.rows):
            for col in range(self.colomns):
                updated_grid[row, col] = self._update_cell(row, col)

        self.grid = updated_grid

    def _update_cell(self,x,y):
        return self._update_cell_state(self.grid[x,y],self._get_neighbours(x,y))
            
    def _get_neighbours(self,x,y):
        # Calls an error for being out of index should be fixed
        neighbours = 0
        for i in range(-1,2):
            for j in range(-1,2):
                try:
                    if i == 0 and j == 0:
                        continue
                    elif self.grid[x + i, y + j]: 
                        # print(f"x: {x+i} y: {y+j}")
                        neighbours += 1
                except IndexError:
                    continue
        # print('-------------------')
        return neighbours
        # Updating the cell's state
   
    def _update_cell_state(self,current_state,neighbours):
        if current_state and neighbours < 2: # under population                                  
            return False
        elif current_state and (neighbours == 2 or neighbours == 3):  # stable population 
            return True
        elif current_state and neighbours > 3: # over population                                
            return False
        elif not current_state and neighbours == 3: # population growth                                
            return True
        else:
            return current_state
        