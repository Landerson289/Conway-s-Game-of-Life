import pygame
import time

pygame.init()
screen = pygame.display.set_mode((400, 400))
cellSize = (20,20)

class Cell:
  def __init__(self, pos, value):
    self.pos = pos
    self.value = value
    self.sprite = pygame.image.load("square.png")
    self.sprite = pygame.transform.scale(self.sprite, cellSize)
    var = pygame.PixelArray(self.sprite)
    if value == 0:
      var.replace((0,0,0),(100,100,100))
    else:
      var.replace((0,0,0),(255,255,255))
    del var
    self.prevValue = self.value
    self.newValue = self.value
  def update(self, neighbours):
    

    
    sum = 0
    for i in neighbours:
      sum += i.value
  
    if self.value == 0:
      if sum == 3:
        self.newValue = 1
      else:
        self.newValue = 0
    else:
      if sum < 2:
        self.newValue = 0
      elif sum == 2 or sum == 3:
        self.newValue = 1
      else:
        self.newValue = 0

    self.show()
    #self.prevValue = self.value
  def show(self):
    if self.value != self.prevValue:
      var = pygame.PixelArray(self.sprite)
      if self.value == 0:
        var.replace((255,255,255),(100,100,100))
      else:
        var.replace((100,100,100),(255,255,255))
      del var
    self.prevValue = self.value
      
    screen.blit(self.sprite, (cellSize[0]*self.pos[0], cellSize[1]*self.pos[1]))
    

class Grid:
  def __init__(self, size):
    self.grid = []
    for i in range(size[0]):
      self.grid.append([])
      for j in range(size[1]):
        self.grid[i].append(Cell([i,j],0))        
  def update(self):
    for i in range(len(self.grid)):
      for j in range(len(self.grid[i])):
        neighbours = []
        for a in range(-1, 2):
          for b in range(-1, 2):
            if 0 <= i-a < len(self.grid) and 0 <= j-b < len(self.grid[i]):
              if not (a == 0 and b == 0):
                neighbours.append(self.grid[i-a][j-b])
        
        self.grid[i][j].update(neighbours)

    for i in self.grid:
      for j in i:
        j.prevValue = j.value
        j.value = j.newValue
         
    

GRID = Grid((400//cellSize[0], 400//cellSize[1]))

pygame.display.set_caption('Hello World!')
start = False
while True:
  if start == True:
    GRID.update()
    pygame.display.update()
    time.sleep(0.5)
  else:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          start = True
      elif event.type == pygame.MOUSEBUTTONDOWN:
        mousePos = pygame.mouse.get_pos()
        if GRID.grid[mousePos[0]//cellSize[0]][mousePos[1]//cellSize[1]].value == 0:
          GRID.grid[mousePos[0]//cellSize[0]][mousePos[1]//cellSize[1]].value = 1
        else:
          GRID.grid[mousePos[0]//cellSize[0]][mousePos[1]//cellSize[1]].value = 0
    for i in GRID.grid:
      for j in i:
        j.show()
  pygame.display.update()
