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

iso_robo = pygame.image.load("ronaldo.png")
iso_hirvio = pygame.image.load("messi.png")
iso_robo = pygame.transform.scale(iso_robo, (iso_hirvio.get_width() - 120, iso_hirvio.get_height()))

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
largeFont = pygame.font.SysFont('comicsans', 80)
fontti = pygame.font.SysFont("Arial", 36)
iso = pygame.font.SysFont("Arial", 100)
font = pygame.font.SysFont('arial', 40)

kello = pygame.time.Clock()

class Hirvio:
	def __init__(self):
		self.x = randint(0, leveys - 50)
		self.y = randint(-1500, -300)
		self.velocity = 2
		self.finished = False

	def tiputa_hirvio(self, counter :int, level :float):

		if counter >= 10:
			self.velocity += counter / 5000
		if counter >= 90:
			self.velocity += counter / 10

		if self.y < korkeus + 100:
			self.y += self.velocity * level
		if self.y > (korkeus - 50) or self.y > korkeus:
			self.finished = True

class Coins:
	def __init__(self):
		self.x = randint(0, leveys - 50)
		self.y = randint(-1500, -300)
		self.finished = False
		self.velocity = 2
		
	def tiputa_kolikko(self, counter :int, level :float):

		if counter >= 10:
			self.velocity += counter / 10000

		if self.y < korkeus + 100:
			self.y += self.velocity * level
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
		self.level = 0
		self.cr7_mode = False

			#Fontit
		self.teksti = fontti.render(f"Counter: {self.counter}", True, (0, 0, 0))
		self.health = fontti.render(f"Health: {self.robo_health}", True, (0, 0, 0))

		self.oikealle = False
		self.vasemmalle = False
		self.ylos = False
		self.alas = False

			#Kolikot
		self.kolikoita = 10
		self.coins_made = 0
		self.kolikot = []
		# for i in range(self.kolikoita):
		# 	i = Coins()
		# 	self.kolikot.append(i)

			#Viholliset
		self.monsters = 5
		self.mon_list = []
		for mon in range(self.monsters):
			mon = Hirvio()
			self.mon_list.append(mon)

	def detect_collision_coin(self):
		while self.coins_made < self.kolikoita:
			c = Coins()
			self.kolikot.append(c)
			self.coins_made += 1
		for c in self.kolikot:
			if self.p1.x < c.x + coin.get_width() and c.x < self.p1.x + robo_leveys and \
				self.p1.y < c.y + coin.get_height() and c.y < self.p1.y + robo_korkeus:
					self.kolikot.remove(c)
					self.counter += 1
					self.coins_made -= 1
			if c.finished:
				self.kolikot.remove(c)
				self.coins_made -= 1
		
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
			naytto.fill((0, 0, 0))
 
			currentScore = fontti.render(f"Final Score: {self.counter}", True, (255, 255, 255))
			game_over = largeFont.render(f"GAME OVER", True, (255, 255, 255))
			goat = fontti.render(f"Messi is the Goat...", True, (255, 255, 255))
			goat2 = fontti.render(f"Ronaldo is the Goat!", True, (255, 255, 255))
			restart = fontti.render(f"Press R to restart:", True, (255,255,255))
			win = largeFont.render(f"YOU WON!", True, (255, 255, 255))
			seewy = largeFont.render(f"SIIIII!!", True, (255, 255, 255))

			if self.counter < 100:
				naytto.blit(game_over, (leveys / 2 - (game_over.get_width()/2), korkeus / 2 + (game_over.get_height()/2 - 300)))
				naytto.blit(goat, (leveys / 2 - (goat.get_width()/2), korkeus / 2 + (goat.get_height()/2 - 100)))
				naytto.blit(currentScore, (leveys / 2 - currentScore.get_width()/2, korkeus / 2 + currentScore.get_height()/2))

			if self.counter == 100:
				naytto.blit(win, (leveys / 2 - (win.get_width()/2), 50))
				naytto.blit(goat2, (leveys / 2 - (goat2.get_width()/2), korkeus / 2 + (goat2.get_height()/2 - 100)))
				naytto.blit(seewy, (leveys / 2 - (seewy.get_width()/2), 300))
			naytto.blit(restart, (0,korkeus - restart.get_height()))

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

				if self.state == POISSA:
					if tapahtuma.key == pygame.K_7:
						self.level = 1
						self.state = KAYNNISSA
						self.kolikoita = 200
					if tapahtuma.key == pygame.K_1:
						self.level = 1
						self.state = KAYNNISSA
					if tapahtuma.key == pygame.K_2:
						self.level = 1.5
						self.state = KAYNNISSA
						self.kolikoita = 13
					if tapahtuma.key == pygame.K_3:
						self.level = 2.5
						self.state = KAYNNISSA
						self.kolikoita = 16
					if tapahtuma.key == pygame.K_4:
						self.level = 5.0
						self.kolikoita = 19
						self.state = KAYNNISSA
					

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
			kolikko.tiputa_kolikko(self.counter, self.level)

			naytto.blit(coin, (kolikko.x, kolikko.y))
			self.detect_collision_coin()

	# def make_coin_list(self):
	# 	self.kolikoita = 40
	# 	for i in range(self.kolikoita):
	# 		i = Coins()
	# 		self.kolikot.append(i)

	def tarkasta_hirvio(self):
		for monster in self.mon_list:
			monster.tiputa_hirvio(self.counter, self.level)

			naytto.blit(hirvio, (monster.x, monster.y))
			self.detect_collision_hirvio()

	def start_menu(self):
		# naytto.fill((100, 200, 100))
		naytto.fill((0, 0, 0))
		title = font.render("Grab The Ballon D'ors", True, (200, 200, 0))
		# start_button = font.render('Start', True, (255, 255, 255))
		instructions = fontti.render("Use arrows to move, dodge Messi", True, (255, 255, 255))
		info = fontti.render("Start by pressing 1 - 4", True, (255, 255, 255))
		info2 = fontti.render("1 = Easy, 2 = Medium, 3 = Hard", True, (255, 255, 255))
		info3 = fontti.render("4 = Impossible (Beware)", True, (255, 255, 255))
		info4 = fontti.render("7 = CR7GOATMODE", True, (255, 255, 255))


		naytto.blit(title, (leveys / 2 - title.get_width()/2, korkeus / 4 ))

		# naytto.blit(start_button, (leveys / 2 - start_button.get_width()/2, korkeus / 2 + start_button.get_height()/2))

		naytto.blit(instructions, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 25))
		naytto.blit(info, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 65))
		naytto.blit(info2, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 105))
		naytto.blit(info3, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 145))
		naytto.blit(info4, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 185))


		naytto.blit(iso_robo, (0, 0))
		naytto.blit(iso_hirvio, (leveys - iso_hirvio.get_width() + 80, 0))
		pygame.display.update()
	
		

	def pyorita(self):
		while (True):
			self.tapahtumat()
			if self.state == POISSA:
				self.start_menu()
				# self.make_coin_list()
			if self.state == KAYNNISSA:
				naytto.fill((50, 170, 50))
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
				naytto.blit(self.teksti, (leveys - self.teksti.get_width() - 15,korkeus - 50))
				naytto.blit(self.health, (15,korkeus - 50))
			pygame.display.flip()
			kello.tick(60)

def main():
	game = GrabtheCash()
	game.pyorita()

main()