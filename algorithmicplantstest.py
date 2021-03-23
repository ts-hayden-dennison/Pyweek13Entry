import pygame
import random
import sys
pygame.init()
screen = pygame.display.set_mode([640, 480])
clock = pygame.time.Clock()

def draw_plants():
	global screen
	surface = pygame.Surface((640, 480))
	pxarray = pygame.PixelArray(surface)
	running = False
	startpos = [random.randint(0, 640), random.randint(0, 480)]
	green = (0, 255, 0)
	times = 0
	cutoff = int(raw_input('How many runs? '))
	pxarray[startpos] = (255, 0, 0)
	while times < cutoff:
		direction = random.randint(0, 4)
		if direction == 0:
			try:
				newpos = [startpos[0], startpos[1]-1]
				if pxarray[newpos] == green:
					continue
				pxarray[newpos]=green
				startpos = newpos[:]
			except:
				continue
		if direction == 1:
			try:
				newpos = [startpos[0]+1, startpos[1]]
				if pxarray[newpos] == green:
					continue
				pxarray[newpos]=green
				startpos = newpos[:]
			except:
				continue
		if direction == 2:
			try:
				newpos = [startpos[0], startpos[1]+1]
				if pxarray[newpos] == green:
					continue
				pxarray[newpos]=green
				startpos = newpos[:]
			except:
				continue
		if direction == 3:
			try:
				newpos = [startpos[0]-1, startpos[1]]
				if pxarray[newpos] == green:
					continue
				pxarray[newpos]=green
				startpos = newpos[:]
			except:
				continue
		times += 1
	return pygame.transform.scale(surface, (640, 480))
surface = draw_plants()
screen.blit(surface, [0, 0])
while True:
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif e.type == pygame.KEYDOWN:
			if e.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			elif e.key == pygame.K_SPACE:
				screen.fill([0, 0, 0])
				surface = draw_plants()
				screen.blit(surface, [0, 0])
	clock.tick(30)
	pygame.display.flip()
