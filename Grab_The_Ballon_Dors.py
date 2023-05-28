import pygame
from pygame import mixer
from random import *

	# For music in Ballon d'or version
mixer.init()
pygame.init()

	# Choose 1 for Grab_The_Ca$h version
	# Choose 2 for Grab_The_Ballon D'ors version
choose_game = 1

if choose_game == 2:
	mixer.music.load('seewy.mp3')
	mixer.music.set_volume(0.2)
	mixer.music.play()

leveys = 700
korkeus = 520
naytto = pygame.display.set_mode((leveys, korkeus))

	#Original Version
if choose_game == 1:
	robo = pygame.image.load("robo.png")
	coin = pygame.image.load("kolikko.png")
	hirvio = pygame.image.load("hirvio.png")
	iso_robo = pygame.image.load("robo.png")
	iso_robo = pygame.transform.scale(robo, (100, 150))
	iso_hirvio = pygame.image.load("hirvio.png")
	iso_hirvio = pygame.transform.scale(robo, (200, 150))
	# iso_robo = pygame.transform.scale(iso_robo, (iso_hirvio.get_width() - 120, iso_hirvio.get_height()))
	boxers = pygame.image.load("ruuvi.png")
	boxers = pygame.transform.scale(boxers, (30, 30))
	shoes = pygame.image.load("nappikset.png")
	shoes = pygame.transform.scale(shoes, (30, 30))

	#Football one
if choose_game == 2:
	robo = pygame.image.load("ronaldo.png")
	robo = pygame.transform.scale(robo, (60, 110))

	iso_robo = pygame.image.load("ronaldo.png")
	iso_hirvio = pygame.image.load("messi.png")
	iso_robo = pygame.transform.scale(iso_robo, (iso_hirvio.get_width() - 120, iso_hirvio.get_height()))

	coin = pygame.image.load("bdor.png")
	coin = pygame.transform.scale(coin, (40, 40))

	hirvio = pygame.image.load("messi.png")
	hirvio = pygame.transform.scale(hirvio, (80, 90))

		#Power_Ups
	boxers = pygame.image.load("boxer.png")
	boxers = pygame.transform.scale(boxers, (30, 30))

	shoes = pygame.image.load("nappikset.png")
	shoes = pygame.transform.scale(shoes, (30, 30))

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

	# PowerUp class has shoes and boxers that make player faster and smaller.
class PowerUp:
	def __init__(self):
		self.valinta = randint(1, 2)
		self.x = randint(0, leveys - 50)
		self.y = randint(-1500, -300)
		self.velocity = 2
		self.finished = False

	def tiputa_power_up(self, counter :int, level :float):
		if counter >= 10:
			self.velocity += counter / 5000

		if self.y < korkeus + 100:
			self.y += self.velocity 
		if self.y > (korkeus - 50) or self.y > korkeus:
			self.finished = True

	# Hirvio / Monster class is the enemy the player has to dodge or loses lives.
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

	# Coins / Ballon D'ors class is the collectibles the player has to get to increase counter
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

	# Robootti / Robot class is the player character 
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
			self.x += 3 * self.velocity
		if self.vasemmalle and self.x >= 0:
			self.x -= 3 * self.velocity
		if self.ylos and self.y >= 0:
			self.y -= 3 * self.velocity
		if self.alas and self.y < korkeus - robo_korkeus:
			self.y += 3 * self.velocity

	# Game class with all the information that is needed to keep during the game.
class GrabtheCash:
	def __init__(self):
		pygame.display.set_caption("Grab The Ca$h")

		self.state = POISSA
		self.robo_health = 5
		self.p1 = Robootti(leveys / 2, korkeus / 2)
		self.counter = 0
		self.level = 0
		self.cr7_mode = False
		self.r_leveys = robo_leveys
		self.r_korkeus = robo_korkeus
		self.robo = pygame.transform.scale(robo, (self.r_leveys, self.r_korkeus))

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

			#Viholliset
		self.monsters = 5
		self.mon_list = []
		for mon in range(self.monsters):
			mon = Hirvio()
			self.mon_list.append(mon)

			#Power_upit
		self.power_upit = 3
		self.power_up_lista = []
		for p in range(self.power_upit):
			p = PowerUp()
			self.power_up_lista.append(p)

	# Detects if player collides with a coin icon and increases counter if that happens.
	# If the item is finished or is collected we remove it from the list and add a new one.
	def detect_collision_coin(self):
		while self.coins_made < self.kolikoita:
			c = Coins()
			self.kolikot.append(c)
			self.coins_made += 1
		for c in self.kolikot:
			if self.p1.x < c.x + coin.get_width() and c.x < self.p1.x + self.r_leveys and \
				self.p1.y < c.y + coin.get_height() and c.y < self.p1.y + self.r_korkeus:
					self.kolikot.remove(c)
					self.counter += 1
					self.coins_made -= 1
			if c.finished:
				self.kolikot.remove(c)
				self.coins_made -= 1
		
	# Detects if player collides with a monster icon and reduces health if that happens.
	# If the item is finished or is collected we remove it from the list and add a new one.
	def detect_collision_hirvio(self):
		for mon in self.mon_list:
			if self.p1.x + self.r_leveys > mon.x + (h_w / 4) and self.p1.x < mon.x + h_w - (h_w / 3) and \
				self.p1.y + self.r_korkeus > mon.y + (h_h / 5) and self.p1.y < mon.y + h_h - (h_h / 5):
					self.mon_list.remove(mon)
					mon = Hirvio()
					self.mon_list.append(mon)
					self.robo_health -= 1
			if mon.finished:
				self.mon_list.remove(mon)
				mon = Hirvio()
				self.mon_list.append(mon)

	# Detects if player collides with a powerup icon and acts accordingly.
	# If the item is finished or is collected we remove it from the list and add a new one.
	def detect_collision_power(self):
		for p_up in self.power_up_lista:
			if self.p1.x + self.r_leveys > p_up.x + (shoes.get_width() / 4) and self.p1.x < p_up.x + shoes.get_width() - (shoes.get_width() / 3) and \
				self.p1.y + self.r_korkeus > p_up.y + (shoes.get_height() / 5) and self.p1.y < p_up.y + shoes.get_height()- (shoes.get_height() / 3):
					if (p_up.valinta == 1):
						self.p1.velocity += 0.2
					if p_up.valinta == 2:
						self.r_leveys /= 1.1
						self.r_korkeus /= 1.1
						self.robo = pygame.transform.scale(robo, (self.r_leveys, self.r_korkeus))


					self.power_up_lista.remove(p_up)
					p_up = PowerUp()
					self.power_up_lista.append(p_up)
			if p_up.finished:
				self.power_up_lista.remove(p_up)
				p_up = PowerUp()
				self.power_up_lista.append(p_up)

	# If the the player has no health left of counter is 100 game ends.
	# The player gets shown an end screen dependinp of the outcome.
	def endScreen(self):
		run = True
		while run:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						main()
			naytto.fill((0, 0, 0))
			currentScore = fontti.render(f"Final Score: {self.counter}", True, (255, 255, 255))
			game_over = largeFont.render(f"GAME OVER", True, (255, 255, 255))
			if choose_game == 2:
				goat = fontti.render(f"Messi is the Goat...", True, (255, 255, 255))
				goat2 = fontti.render(f"Ronaldo is the Goat!", True, (255, 255, 255))
			else:
				goat = fontti.render(f"Better luck next time!", True, (255, 255, 255))
				goat2 = fontti.render(f"You are a master gamer!", True, (255, 255, 255))

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
		
	# Keybinding for movement and difficulty selection.
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
	# Checking the coin icon, dropping it, and checking for collision.
	def tarkasta_kolikko(self):
		for kolikko in self.kolikot:
			kolikko.tiputa_kolikko(self.counter, self.level)

			naytto.blit(coin, (kolikko.x, kolikko.y))
			self.detect_collision_coin()

	# Checking the power-up icons, dropping them, and checking for collision.
	def tarkasta_power_up(self):
		for p_up in self.power_up_lista:
			p_up.tiputa_power_up(self.counter, self.level)
			if (p_up.valinta == 1 and self.counter > 30):
				naytto.blit(shoes, (p_up.x, p_up.y))
			if (p_up.valinta == 2 and self.counter > 50):
				naytto.blit(boxers, (p_up.x, p_up.y))
			self.detect_collision_power()

	# Checking the monster icons, dropping them, and checking for collision.
	def tarkasta_hirvio(self):
		for monster in self.mon_list:
			monster.tiputa_hirvio(self.counter, self.level)
			naytto.blit(hirvio, (monster.x, monster.y))
			self.detect_collision_hirvio()

	# When the game opens player reseves teh start menu with info and
	# a possibility to choose difficulty
	def start_menu(self):
		naytto.fill((0, 0, 0))
		if (choose_game == 2):
			title = font.render("Grab The Ballon D'ors", True, (200, 200, 0))
		else:
			title = font.render("Grab The Ca$h", True, (200, 200, 0))
		instructions = fontti.render("Use arrows to move, dodge Messi", True, (255, 255, 255))
		info = fontti.render("Start by pressing 1 - 4", True, (255, 255, 255))
		info2 = fontti.render("1 = Easy, 2 = Medium, 3 = Hard", True, (255, 255, 255))
		info3 = fontti.render("4 = Impossible (Beware)", True, (255, 255, 255))
		if (choose_game == 2):
			info4 = fontti.render("7 = CR7GOATMODE", True, (255, 255, 255))
		else:
			info4 = fontti.render("7 = Pass the game", True, (255, 255, 255))

		naytto.blit(title, (leveys / 2 - title.get_width()/2, korkeus / 4 ))
		naytto.blit(instructions, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 25))
		naytto.blit(info, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 65))
		naytto.blit(info2, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 105))
		naytto.blit(info3, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 145))
		naytto.blit(info4, (leveys / 2 - instructions.get_width()/2, korkeus / 2 - (instructions.get_height()/2)+ 185))
		naytto.blit(iso_robo, (0, 0))
		if (choose_game == 2):
			naytto.blit(iso_hirvio, (leveys - iso_hirvio.get_width() + 80, 0))
		else:
			naytto.blit(iso_robo, (leveys - iso_robo.get_width(), 0))
		pygame.display.update()
	
	# Game loop, checks keyboard info first, then opens start menu, fills board
	# Moves robot, checks all collectables and their collisins.
	# If game ends enters EndScreen
	def pyorita(self):
		while (True):
			self.tapahtumat()
			if self.state == POISSA:
				self.start_menu()
			if self.state == KAYNNISSA:
				naytto.fill((50, 170, 50))
				self.p1.liikuta_roboa(self)
				self.tarkasta_hirvio()
				self.tarkasta_kolikko()
				self.tarkasta_power_up()
				self.detect_collision_power()
				self.detect_collision_hirvio()
				self.detect_collision_coin()

				if self.robo_health == 0:
					self.endScreen()
				if self.counter == 100:
					self.endScreen()

				self.teksti = fontti.render(f"Counter: {self.counter}", True, (0, 0, 0))
				self.health = fontti.render(f"Health: {self.robo_health}", True, (0, 0, 0))

				naytto.blit(self.robo, (self.p1.x, self.p1.y))
				naytto.blit(self.teksti, (leveys - self.teksti.get_width() - 15,korkeus - 50))
				naytto.blit(self.health, (15,korkeus - 50))
			pygame.display.flip()
			kello.tick(60)

def main():
	game = GrabtheCash()
	game.pyorita()

main()