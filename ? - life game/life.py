import sys
import pygame
from conway import conway

# Initialize pygame
pygame.init()
pygame.display.set_caption("A simple game of Life.")

# Screen width
WIDTH = 800 
HEIGHT = 800

# Create screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
game = conway(screen,width=WIDTH,height=HEIGHT,scale=10)

clock = pygame.time.Clock()
fps = 60


while True:
  clock.tick(fps)
  screen.fill((0,0,0))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      print("Bye bye...")
      sys.exit()
      
  game.run()    
  pygame.display.update()
  