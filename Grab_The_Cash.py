import pygame
from random import *

pygame.init()
leveys = 640
korkeus = 480
naytto = pygame.display.set_mode((leveys, korkeus))
	#Kuvat
robo = pygame.image.load("robo.png")
coin = pygame.image.load("kolikko.png")
hirvio = pygame.image.load("hirvio.png")

robo_leveys = robo.get_width()
robo_korkeus = robo.get_height()
	#Fontit
fontti = pygame.font.SysFont("Arial", 36)
iso = pygame.font.SysFont("Arial", 100)

kello = pygame.time.Clock()
class Hirvio:
	def __init__(self):
		self.x = randint(0, 640 - 50)
		self.y = randint(-1500, -200)
		self.velocity = 2
		self.finished = False

	def tiputa_hirvio(self, counter :int):
		if (counter >= 10):
			self.velocity += counter / 1000
		if (counter >= 90):
			self.velocity += 1
		if self.y < 700:
			self.y += self.velocity
		if self.y > (480 - 70) or self.y > 480:
			self.finished = True

class Coins:
	def __init__(self):
		self.x = randint(0, 640 - 50)
		self.y = randint(-1500, -300)
		self.finished = False
		self.velocity = 2
		
	def tiputa_kolikko(self, counter :int):
		if counter >= 10:
			self.velocity += counter / 10000
		if self.y < 700:
			self.y += self.velocity
		if self.y > 480 - 50 or self.y > 480:
			self.finished = True

class Robootti:
	def __init__(self, leveys, korkeus):
		self.x = leveys
		self.y = korkeus
		self.oikealle = False
		self.vasemmalle = False
		self.ylos = False
		self.alas = False
		self.velocity = 1.0

	def liikuta_roboa(self, robootti):
		if self.oikealle and self.x + robo.get_width() <= 640:
			self.x += 3
		if self.vasemmalle and self.x >= 0:
			self.x -= 3
		if self.ylos and self.y >= 0:
			self.y -= 3
		if self.alas and self.y + robo.get_height() <= 480:
			self.y += 3

class GrabtheCash:
	def __init__(self):
		pygame.display.set_caption("Grab The Ca$h")

		self.robo_health = 5
		self.p1 = Robootti(leveys / 2, korkeus / 2)
		self.counter = 0

		self.teksti = fontti.render(f"Counter: {self.counter}", True, (0, 0, 0))
		self.health = fontti.render(f"Health: {self.robo_health}", True, (0, 0, 0))

		self.oikealle = False
		self.vasemmalle = False
		self.ylos = False
		self.alas = False

			#Kolikot
		self.kolikoita = 10
		self.kolikot = []
		for i in range(self.kolikoita):
			i = Coins()
			self.kolikot.append(i)

			#Viholliset
		self.monsters = 5
		self.mon_list = []
		for mon in range(self.monsters):
			mon = Hirvio()
			self.mon_list.append(mon)


	def detect_collision_coin(self):
		for c in self.kolikot:
			if self.p1.x < c.x + coin.get_width() and c.x < self.p1.x + robo_leveys and \
				self.p1.y < c.y + coin.get_height() and c.y < self.p1.y + robo_korkeus:
					self.kolikot.remove(c)
					c = Coins()
					self.kolikot.append(c)
					self.counter += 1
			if c.finished:
				self.kolikot.remove(c)
				c = Coins()
				self.kolikot.append(c)
		
	def detect_collision_hirvio(self):
		for mon in self.mon_list:
			if self.p1.x < mon.x + hirvio.get_width() and mon.x < self.p1.x + robo_leveys and \
				self.p1.y < mon.y + hirvio.get_height() and mon.y < self.p1.y + robo_korkeus:
					self.mon_list.remove(mon)
					mon = Hirvio()
					self.mon_list.append(mon)
					self.robo_health -= 1
			if mon.finished:
				self.mon_list.remove(mon)
				mon = Hirvio()
				self.mon_list.append(mon)

	def endScreen(self):
		run = True
		while run:
			pygame.time.delay(100)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						run = False
						self.counter = 0
						self.robo_health = 5
						self.oikealle = False
						self.vasemmalle = False
						self.ylos = False
						self.alas = False
						naytto.fill((255, 0, 255))
						self.pyorita()
						
			largeFont = pygame.font.SysFont('comicsans', 80) 
			currentScore = largeFont.render(f"Final Score: {self.counter}", True, (0, 0, 0))
			restart = fontti.render(f"Press R to restart:", True, (0,0,0))
			win = largeFont.render(f"YOU WON!", True, (0, 0, 0))
			if self.counter < 100:
				naytto.blit(currentScore, (50, 170))
			if self.counter == 100:
				naytto.blit(win, (50, 170))
			naytto.blit(restart, (0,0))

			pygame.display.update()
		

	def tapahtumat(self):
		for tapahtuma in pygame.event.get():
			if tapahtuma.type == pygame.KEYDOWN:
				if tapahtuma.key == pygame.K_LEFT:
					self.p1.vasemmalle = True
				if tapahtuma.key == pygame.K_RIGHT:
					self.p1.oikealle = True
				if tapahtuma.key == pygame.K_UP:
					self.p1.ylos = True
				if tapahtuma.key == pygame.K_DOWN:
					self.p1.alas = True

			if tapahtuma.type == pygame.KEYUP:
				if tapahtuma.key == pygame.K_LEFT:
					self.p1.vasemmalle = False
				if tapahtuma.key == pygame.K_RIGHT:
					self.p1.oikealle = False
				if tapahtuma.key == pygame.K_UP:
					self.p1.ylos = False
				if tapahtuma.key == pygame.K_DOWN:
					self.p1.alas = False

			if tapahtuma.type == pygame.QUIT:
				exit()

	def tarkasta_kolikko(self):
		for kolikko in self.kolikot:
			kolikko.tiputa_kolikko(self.counter)

			naytto.blit(coin, (kolikko.x, kolikko.y))
			self.detect_collision_coin()

	def tarkasta_hirvio(self):
		for monster in self.mon_list:
			monster.tiputa_hirvio(self.counter)

			naytto.blit(hirvio, (monster.x, monster.y))
			self.detect_collision_hirvio()

	def pyorita(self):
		while (True):
			self.tapahtumat()
			naytto.fill((255, 0, 255))
			self.p1.liikuta_roboa(self)
			self.tarkasta_hirvio()
			self.tarkasta_kolikko()
			self.detect_collision_hirvio()
			self.detect_collision_coin()

			if self.robo_health == 0:
				self.endScreen()
			if self.counter == 100:
				self.endScreen()

			self.teksti = fontti.render(f"Counter: {self.counter}", True, (0, 0, 0))
			self.health = fontti.render(f"Health: {self.robo_health}", True, (0, 0, 0))

			naytto.blit(robo, (self.p1.x, self.p1.y))
			naytto.blit(self.teksti, (450,430))
			naytto.blit(self.health, (15,430))
			pygame.display.flip()
			kello.tick(60)

def main():
	game = GrabtheCash()
	game.pyorita()

main()