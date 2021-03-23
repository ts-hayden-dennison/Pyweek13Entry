#! usr/bin/env python

# Hidas' Pyweek 13 entry

import pygame
import sys
import random
import os
pygame.init()
size = width, height = 640, 640
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
SCROLLOFFSET = 220
CAMERASPEED = 15
ENEMYSPEED = 6
ENEMYRESPAWN = 26
PLAYERHEALTH = 30
MAXENEMIES = 50
class Cave():
	# A procedurally generated cave. Stores its width and height in tiles, and references the tiles that make it up
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.tiles = pygame.sprite.Group()
		self.playerpos = [0, 0]
		self.deadlies = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.mothercell = MotherCell([0, 0])
	def update(self, worldmovement, player):
		global screen, MAXENEMIES
		self.deadlies.update(worldmovement)
		self.tiles.update(worldmovement, self)
		self.enemies.update(self, player, worldmovement)
		self.mothercell.update(self, player, worldmovement)
		if self.mothercell.dead == True:
			youWin()
		if len(self.enemies) > MAXENEMIES:
			self.enemies.remove(MAXENEMIES-len(self.enemies))
		screenrect = screen.get_rect()
		for tile in self.tiles:
			if tile.rect.colliderect(screenrect):
				screen.blit(tile.image, tile.rect)
		for deadly in self.deadlies:
			if deadly.rect.colliderect(screenrect):
				screen.blit(deadly.image, deadly.rect)
		for enemy in self.enemies:
			if enemy.rect.colliderect(screenrect):
				screen.blit(enemy.image, enemy.rect)
		return
	def setMother(self, position):
		self.mothercell = MotherCell(position)
		self.mothercell.gridpos = [position[0]//32, position[1]//32]
class MotherCell(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position, (32, 32))
		self.image = pygame.Surface((32, 32)).convert()
		self.image.fill((0, 100, 255))
		self.enemyrespawn = 0
		self.dead = False
	def update(self, cave, player, worldmovement):
		global ENEMYRESPAWN
		self.rect = self.rect.move(worldmovement)
		if self.rect.colliderect(player.rect) == True:
			self.dead = True
		if self.enemyrespawn == 0:
			enemy = Enemy(self.rect.topleft)
			enemy.gridpos = self.gridpos
			cave.enemies.add(enemy)
			self.enemyrespawn = ENEMYRESPAWN
		if self.enemyrespawn > 0:
			self.enemyrespawn -= 1
		screen.blit(self.image, self.rect)
class Enemy(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position, (32, 32))
		self.image = pygame.Surface((32, 32)).convert()
		self.image.fill((200, 60, 60))
		self.movetimer = 0
		self.gridpos = [0, 0]
	def update(self, cave, player, worldmovement):
		global ENEMYSPEED
		self.rect = self.rect.move(worldmovement)
		'''nearbyt = []
		nearbyt.append(cave.grid.index((self.gridpos[0], self.gridpos[1]-1)))
		nearbyt.append(cave.grid.index((self.gridpos[0], self.gridpos[1]+1)))
		nearbyt.append(cave.grid.index((self.gridpos[0]+1, self.gridpos[1])))
		nearbyt.append(cave.grid.index((self.gridpos[0]-1, self.gridpos[1])))
		if 5 in nearbyt:
			cave.enemies.remove(self)
			self.kill()
			self.remove(cave.enemies)'''
		pygame.draw.rect(screen, [255, 0, 0], (self.gridpos, (1, 1)))
		if self.movetimer == 0:
			if player.rect.centerx > self.rect.centerx and player.rect.centery > self.rect.centery:
				direction = random.choice([1, 2])
			elif player.rect.centerx < self.rect.centerx and player.rect.centery > self.rect.centery:
				direction = random.choice([2, 3])
			elif player.rect.centerx > self.rect.centerx and player.rect.centery < self.rect.centery:
				direction = random.choice([0, 1])
			else:
				direction = random.choice([3, 0])
			if direction == 0:
				if cave.grid.index([self.gridpos[0], self.gridpos[1]-1]) == 1:
					self.rect.centery -= 32
					self.gridpos[1] -= 1
				else:
					if cave.grid.index([self.gridpos[0], self.gridpos[1]-1]) == 5:
						cave.enemies.remove(self)
						self.remove(cave.enemies)
						self.kill()
			elif direction == 1:
				if cave.grid.index([self.gridpos[0]+1, self.gridpos[1]]) == 1:
					self.rect.centerx += 32
					self.gridpos[0] += 1
				else:
					if cave.grid.index([self.gridpos[0]+1, self.gridpos[1]]) == 5:
						cave.enemies.remove(self)
			elif direction == 2:
				if cave.grid.index([self.gridpos[0], self.gridpos[1]+1]) == 1:
					self.rect.centery += 32
					self.gridpos[1] += 1
				else:
					if cave.grid.index([self.gridpos[0], self.gridpos[1]+1]) == 5:
						cave.enemies.remove(self)
						cave.enemies.remove(self)
						self.kill()
						self.remove(cave.enemies)
			elif direction == 3:
				if cave.grid.index([self.gridpos[0]-1, self.gridpos[1]]) == 1:
					self.rect.centerx -= 32
					self.gridpos[0] -= 1
				else:

					if cave.grid.index([self.gridpos[0]-1, self.gridpos[1]]) == 5:
						cave.enemies.remove(self)
						cave.enemies.remove(self)
						self.kill()
						self.remove(cave.enemies)
			self.movetimer = ENEMYSPEED
		if self.movetimer > 0:
			self.movetimer -= 1
class Tile(pygame.sprite.Sprite):
	# Just your average tile. Stores its rect, image, and whether is has been given life.
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position, (32, 32))
		self.life = False
		self.image = pygame.Surface((32, 32)).convert()
		self.image.fill((100, 100, 100))
		pygame.draw.rect(self.image, (0, 0, 0), self.rect, 2)
		self.gridpos = [0, 0]
	def update(self, worldmovement, cave):
		# Update movement and return. Drawing is handled by the Cave class.
		self.rect = self.rect.move(worldmovement)
		#pygame.draw.rect(screen, [255, 255, 255], self.rect, 2)
		if self.life==True:
			cave.grid.replace(self.gridpos, 5)
			pygame.draw.rect(screen, [0, 255, 0], (self.gridpos, (1, 1)), 1)
		else:
			pygame.draw.rect(screen, [100, 100, 100], (self.gridpos, (1, 1)), 1)
		return
	def haslife(self):
		self.life = True
		self.image.fill((0, 255, 0))
class Deadly(pygame.sprite.Sprite):
	def __init__(self, position):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position, (32, 32))
		self.image = pygame.Surface((32, 32))
		self.image.fill((255, 10, 0))
	def update(self, worldmovement):
		self.rect = self.rect.move(worldmovement)
		return
class Player(pygame.sprite.Sprite):
	# Ho-hum, your average platforming guy.
	def __init__(self, position):
		global PLAYERHEALTH
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(position, (17, 17))
		self.rect.topleft = position
		self.xaccel = 1.5
		self.jumping = False
		self.onGround = False
		self.yaccel = 2.4
		self.jump_timer = 0
		self.velocity = [0, 0]
		self.health = PLAYERHEALTH
	def update(self, cave):
		# Update movement, tile collision, and drawing.
		collide = pygame.sprite.spritecollideany(self, cave.deadlies)
		if collide != None:
			self.health -= 1
		enemycollide = pygame.sprite.spritecollideany(self, cave.enemies)
		if enemycollide != None:
			self.health -= 1
		self.updateInput(cave)
		self.updateCollision(cave.tiles)
		worldmovement = self.updateMovement()
		self.draw()
		if self.jump_timer > 0:
			self.jump_timer -= 1
			if pygame.key.get_pressed()[pygame.K_UP]:
				self.velocity[1] -= self.yaccel/2
		if self.velocity[1] > 9:
			self.velocity[1] = 9
		if self.health < PLAYERHEALTH:
			self.health += 0.1
		if self.health < 0:
			gameOver()
		return worldmovement
	def updateInput(self, cave):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_r]:
			self.rect.topleft = cave.playerpos
		if keys[pygame.K_RIGHT]:
			self.velocity[0] += self.xaccel
		elif keys[pygame.K_LEFT]:
			self.velocity[0] += -self.xaccel
		else:
			self.velocity[0] /= 2.3
		if self.velocity[0] > 9:
			self.velocity[0] = 9
		elif self.velocity[0] < -9:
			self.velocity[0] = -9
		if keys[pygame.K_UP] and self.onGround == True:
			self.jumping = True
			self.velocity[1] = -self.yaccel*2
			#self.rect.bottom -= 1
			self.jump_timer = 9
			self.onGround = False
		return
	def updateCollision(self, tiles):
		#if self.velocity[0] != 0:
		keys = pygame.key.get_pressed()
		# Moving right collision test
		for tile in tiles:
			if tile.rect.colliderect(self.rect.move([self.velocity[0], 0])):
				if self.rect.centery >= tile.rect.top and self.rect.centery <= tile.rect.bottom:
					if self.rect.centerx <= tile.rect.centerx:
						self.velocity[0] = 0
						self.velocity[1] = 0
						self.onGround = True
						self.rect.right = tile.rect.left
						if keys[pygame.K_UP]:
							self.jumping = True
							self.velocity[1] = -self.yaccel*2.
							self.jump_timer = 4
							self.onGround = False
							self.velocity[0] = -5
					elif self.rect.centerx >= tile.rect.centerx:
						self.velocity[0] = 0
						self.velocity[1] = 0
						self.onGround = True	
						self.rect.left = tile.rect.right
						if keys[pygame.K_UP]:
							self.jumping = True
							self.velocity[1] = -self.yaccel*2.
							self.jump_timer = 4
							self.onGround = False
							self.velocity[0] = 5
					tile.haslife()
					break
		# Vertical collision tests
		#if self.jumping == True:
		if self.velocity[1] < 0:
			for tile in tiles:
				if tile.rect.colliderect(self.rect.move([0, self.velocity[1]])):
					if self.rect.centerx >= tile.rect.left and self.rect.centerx <= tile.rect.right:
						self.rect.top = tile.rect.bottom+1
						self.jumping = False
						self.velocity[1] = 1
						self.jump_timer = 0
						self.onGround = False
						tile.haslife()
						break
		if self.jump_timer == 0:
			self.jumping = False
		if self.velocity[1] >= 0:
			if self.velocity[1] == 0:
				self.velocity[1] = 1
			for tile in tiles:
				if not tile.rect.colliderect(self.rect.move([0, self.velocity[1]])):
					self.onGround = False
				else:
					if self.rect.centerx >= tile.rect.left and self.rect.centerx <= tile.rect.right:
						self.onGround = True
						self.velocity[1] = 0
						self.rect.bottom = tile.rect.top
						tile.haslife()
						break
		else:
			self.onGround = False
		if self.onGround == False:
			if self.jumping == False:
				self.onGround = False
				self.velocity[1] += self.yaccel
		return
	def updateMovement(self):
		global screen, SCROLLOFFSET
		worldmovement = [0, 0]
		playermovement = self.velocity[:]
		if self.rect.right > screen.get_width()-SCROLLOFFSET and self.velocity[0] > 0:
			worldmovement[0] = -self.velocity[0]
			playermovement[0] = 0
		if self.rect.left < SCROLLOFFSET and self.velocity[0] < 0:
			worldmovement[0] = -self.velocity[0]
			playermovement[0] =0
		if self.rect.top < SCROLLOFFSET and self.velocity[1] < 0:
			worldmovement[1] = -self.velocity[1]
			playermovement[1] = 0
		if self.rect.bottom > screen.get_height()-SCROLLOFFSET and self.velocity[1] > 0:
			worldmovement[1] = -self.velocity[1]
			playermovement[1] = 0
		self.rect = self.rect.move(playermovement)
		return worldmovement
	def draw(self):
		global screen
		pygame.draw.rect(screen, [255, 255, 255], self.rect)
		liferect = pygame.Rect((0, 0), (self.health, 3))
		pygame.draw.rect(screen, [255, 0, 0], liferect)
def gameOver():
	global screen
	screen.fill([0, 0, 0])
	font = pygame.font.Font(None, 32)
	text = font.render('You died! Press Enter to play again.', True, [255, 255, 255], [0, 0, 0])
	screen.blit(text, [0, 0])
	pygame.display.flip()
	e = pygame.event.wait()
	newGame()
def youWin():
	global screen
	screen.fill([0, 0, 0])
	font = pygame.font.Font(None, 32)
	text = font.render('You won! Press Enter to play again.', True, [255, 255, 255], [0, 0, 0])
	screen.blit(text, [0, 0])
	pygame.display.flip()
	e = pygame.event.wait()
	newGame()
def updateGame(player, cave):
	worldmovement = player.update(cave.tiles)
	cave.update(worldmovement)
	return
'''
def createCave(width, height):
	cave = pygame.Surface((width, height))
	cave.fill((0, 0, 0))
	pxarray = pygame.PixelArray(cave)
	running = False
	startpos = [random.randint(0, width), random.randint(0, height)]
	playerpos = startpos[:]
	green = (0, 255, 0)
	times = 0
	cutoff = 2000
	pxarray[startpos] = green
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
				pxarray[newpos] = green
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
	del pxarray
	screen.blit(cave, [0, 0])
	pygame.display.flip()
	time.sleep(2)
	cave.unlock()
	info = pygame.surfarray.array3d(cave)
	print info
	startpos = [0, 0]
	gamecave = Cave(width, height)
	gamecave.playerpos = playerpos[:]
	for i in info:
		if i == (0, 0, 0):
			gamecave.tiles.add(Tile(startpos[:]))
			startpos[0] += 32
			if startpos[0] >= width*32:
				startpos[0] = 0
				startpos[1] += 32
	print gamecave.tiles
	return gamecave'''
class Grid():
	def __init__(self, width, height):
		self.data = []
		for i in range(0, height):
			self.data.append([0]*width)
	def index(self, pos):
		if pos[1] >= len(self.data) or pos[1] < 0:
			return
		if pos[0] >= len(self.data[pos[1]]) or pos[0] < 0:
			return
		return self.data[pos[1]][pos[0]]
	def replace(self, pos, newitem):
		self.data[pos[1]][pos[0]] = newitem
		return
def createCave(width, height, size):
	cave = Grid(width, height)
	startpos = [0, 0]
	cave.replace(startpos, 2)
	times = 0
	for i in range(0, size):
		direction = random.randint(0, 4)
		if direction == 0:
			newpos = [startpos[0], startpos[1]-1]
			try:
				cave.replace(newpos, 1)
				startpos = newpos[:]
			except:
				continue
		if direction == 1:
			newpos = [startpos[0]+1, startpos[1]]
			try:
				cave.replace(newpos, 1)
				startpos = newpos[:]
			except:
				continue
		if direction == 2:
			newpos = [startpos[0], startpos[1]+1]
			try:
				cave.replace(newpos, 1)
				startpos = newpos[:]
			except:
				continue
		if direction == 3:
			newpos = [startpos[0]-1, startpos[1]]
			try:
				cave.replace(newpos, 1)
				startpos = newpos[:]
			except:
				continue
	cave.replace(startpos[:], 3)
	startpos = [0, 0]
	gamecave = Cave(width, height)
	gamecave.grid = cave
	top = [-128, -128]
	for i in range(0, width):
		gamecave.tiles.add(Tile(top[:]))
		top[0] += 32
	bottom = [-128, height*32+96]
	for i in range(0, height):
		gamecave.tiles.add(Tile(bottom[:]))
		bottom[0] += 32
	bottom = [-128, height*32+96]
	for i in range(0, 4):
		gamecave.tiles.add(Tile(bottom[:]))
		bottom[1] -= 32
	for row in cave.data:
		gamecave.tiles.add(Tile([startpos[0]-128, startpos[1]]))
		gamecave.tiles.add(Tile([width*32+128, startpos[1]]))
		for tile in row:
			if tile == 0:
				odds = random.randint(0, 60)
				if odds == 1:
					deadly = True
				else:
					deadly = False
				if deadly == False:
					tile = Tile(startpos[:])
					tile.gridpos = [startpos[0]//32, startpos[1]//32]
					gamecave.tiles.add(tile)
				else:
					deadly = Deadly(startpos[:])
					deadly.gridpos = [startpos[0]//32, startpos[1]//32]
					gamecave.deadlies.add(deadly)
			elif tile == 2:
				gamecave.playerpos = startpos[:]
			elif tile == 1:
				if random.randint(0, 80) == 9:
					enemy = Enemy(startpos[:])
					enemy.gridpos = [startpos[0]//32, startpos[1]//32]
					gamecave.enemies.add(enemy)
			elif tile == 3:
				gamecave.setMother(startpos[:])
			startpos[0] += 32
		startpos[0] = 0
		startpos[1] += 32
	
	return gamecave 
def moveCamera():
	global CAMERASPEED
	keys = pygame.key.get_pressed()
	movement = [0, 0]
	if keys[pygame.K_d]:
		movement[0] = -CAMERASPEED
	elif keys[pygame.K_a]:
		movement[0] = CAMERASPEED
	if keys[pygame.K_w]:
		movement[1] = CAMERASPEED
	elif keys[pygame.K_s]:
		movement[1] = -CAMERASPEED
	return movement
def main(cave):
	global screen, clock
	player = Player(cave.playerpos)
	while True:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
		screen.fill((3, 3, 3))
		worldmovement= player.update(cave)
		cave.update(worldmovement, player)
		clock.tick(35)
		pygame.display.set_caption("Automata " + 'FPS: '+ str(clock.get_fps()))
		pygame.display.flip()
def newGame():
	cave = createCave(70, 70, 9500)
	main(cave)
if __name__ == '__main__':
	newGame()
