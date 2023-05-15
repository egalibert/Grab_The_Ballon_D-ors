import pygame
from random import *

pygame.init()
leveys = 700
korkeus = 520
naytto = pygame.display.set_mode((leveys, korkeus))
	#Kuvat

	#Original Version
# robo = pygame.image.load("robo.png")
# coin = pygame.image.load("kolikko.png")
# hirvio = pygame.image.load("hirvio.png")


	#Football one
robo = pygame.image.load("ronaldo.png")
robo = pygame.transform.scale(robo, (60, 110))

coin = pygame.image.load("bdor.png")
coin = pygame.transform.scale(coin, (40, 40))

hirvio = pygame.image.load("messi.png")
hirvio = pygame.transform.scale(hirvio, (80, 90))
h_w = hirvio.get_width()
h_h = hirvio.get_height()

robo_leveys = robo.get_width()
robo_korkeus = robo.get_height()

POISSA = 0
KAYNNISSA = 1

	#Fontit
fontti = pygame.font.SysFont("Arial", 36)
iso = pygame.font.SysFont("Arial", 100)

kello = pygame.time.Clock()
class Hirvio:
	def __init__(self):
		self.x = randint(0, leveys - 50)
		self.y = randint(-1500, -300)
		self.velocity = 2
		self.finished = False

	def tiputa_hirvio(self, counter :int):
		if (counter >= 10):
			self.velocity += counter / 1000
		if (counter >= 90):
			self.velocity += 1
		if self.y < korkeus + 100:
			self.y += self.velocity
		if self.y > (korkeus - 50) or self.y > korkeus:
			self.finished = True

class Coins:
	def __init__(self):
		self.x = randint(0, leveys - 50)
		self.y = randint(-1500, -300)
		self.finished = False
		self.velocity = 2
		
	def tiputa_kolikko(self, counter :int):
		if counter >= 10:
			self.velocity += counter / 10000
		if self.y < korkeus + 100:
			self.y += self.velocity
		if self.y > korkeus - 50 or self.y > korkeus:
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
		if self.oikealle and self.x < leveys - robo_leveys:
			self.x += 3
		if self.vasemmalle and self.x >= 0:
			self.x -= 3
		if self.ylos and self.y >= 0:
			self.y -= 3
		if self.alas and self.y < korkeus - robo_korkeus:
			self.y += 3

class GrabtheCash:
	def __init__(self):
		pygame.display.set_caption("Grab The Ca$h")

		self.state = POISSA
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
			if self.p1.x + robo_leveys > mon.x + (h_w / 4) and self.p1.x < mon.x + h_w - (h_w / 3) and \
				self.p1.y + robo_korkeus > mon.y + (h_h / 5) and self.p1.y < mon.y + h_h - (h_h / 5):
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
			# pygame.time.delay(100)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						main()
						
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

	def start_menu(self):
		naytto.fill((100, 200, 100))
		i_str = "COLLECT COINS TO EARN POINTS"
		i_text = fontti.render(i_str, True, (0, 0, 0))
		i_rect = i_text.get_rect()
		i_rect.y = 10
		i_rect.centerx = naytto.get_rect().centerx
		rule_str = "AVOID THE GHOSTS, HIT ONE AND YOU LOSE A LIFE"
		rule_text = fontti.render(rule_str, True, (0, 0, 0))
		rule_rect = rule_text.get_rect()
		rule_rect.y = 60
		rule_rect.centerx = naytto.get_rect().centerx
		life_str = "YOU HAVE 5 LIVES"
		life_text = fontti.render(life_str, True, (0, 0, 0))
		life_rect = life_text.get_rect()
		life_rect.y = 110
		life_rect.centerx = naytto.get_rect().centerx
		inten_str = "INTENSITY INCREASES EVERY 5 COINS"
		inten_text = fontti.render(inten_str, True, (0, 0, 0))
		inten_rect = inten_text.get_rect()
		inten_rect.y = 160
		inten_rect.centerx = naytto.get_rect().centerx
		g_str = "ROBO GAME!"
		g_text = iso.render(g_str, True, (255, 255, 0))
		g_rect = g_text.get_rect()
		g_rect.center = naytto.get_rect().center
		ctrl_str = "USE ARROW KEYS TO MOVE"
		space_str = "PRESS 'SPACE' TO START"
		esc_str = "PRESS 'q' or 'esc' TO ESCAPE"
		ctrl_text = fontti.render(ctrl_str, True, (0, 0, 0))
		ctrl_rect = ctrl_text.get_rect()
		ctrl_rect.y = naytto.get_rect().centery + 70
		ctrl_rect.centerx = naytto.get_rect().centerx
		esc_text = fontti.render(esc_str, True, (0, 0, 0))
		esc_rect = esc_text.get_rect()
		esc_rect.y = naytto.get_rect().centery + 150
		esc_rect.centerx = naytto.get_rect().centerx
		space_text = fontti.render(space_str, True, (0, 0, 0))
		space_rect = space_text.get_rect()
		space_rect.centerx = naytto.get_rect().centerx
		space_rect.y = naytto.get_rect().centery + 230
		naytto.blit(g_text, (g_rect))
		naytto.blit(space_text, (space_rect))
		naytto.blit(esc_text, (esc_rect))
		naytto.blit(i_text, (i_rect))
		naytto.blit(rule_text, (rule_rect))
		naytto.blit(life_text, (life_rect))
		naytto.blit(inten_text, (inten_rect))
		naytto.blit(ctrl_text, (ctrl_rect))

	def pyorita(self):
		while (True):
			self.tapahtumat()
			if self.state == POISSA:
				self.start_menu()
			if self.state == KAYNNISSA:
				naytto.fill((50, 170, 50))
				self.p1.liikuta_roboa(self)

				if self.robo_health == 0:
					self.endScreen()
				if self.counter == 100:
					self.endScreen()
				self.tarkasta_hirvio()
				self.tarkasta_kolikko()
				self.detect_collision_hirvio()
				self.detect_collision_coin()

			self.teksti = fontti.render(f"Counter: {self.counter}", True, (0, 0, 0))
			self.health = fontti.render(f"Health: {self.robo_health}", True, (0, 0, 0))

			naytto.blit(robo, (self.p1.x, self.p1.y))
			naytto.blit(self.teksti, (leveys - self.teksti.get_width() - 15,korkeus - 50))
			naytto.blit(self.health, (15,korkeus - 50))
			pygame.display.flip()
			kello.tick(60)

def main():
	game = GrabtheCash()
	game.pyorita()

main()