import pygame
import random
import time

pygame.init()
#window
win = pygame.display.set_mode ((1000, 600))
pygame.display.set_caption('Typing Speed Test')
win.fill((255,255,255))

#fonts
TITLE = pygame.font.SysFont('comicsans', 70)
TEXT = pygame.font.SysFont('arial', 30)

app_title = pygame.font.SysFont('comicsans', 70).render('Typing Speedooo Test', 1, (pygame.Color("#00e6e6")))
win.blit(app_title, (1000//2 - app_title.get_width()//2, 50))

count = 0


def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    co = 0
    for line in words:
        c = co
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            if count == c:
            	pygame.draw.line(win, (pygame.Color("#00ff99")), (x - 2, y + word_height - 3), (x + word_width, y + word_height - 3), (3))
            c += 1 
            x += word_width + space
        
        co += len(line) - 1
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def examples():
	example = ["Sometimes life is like a dark tunnel. You can't always see \nthe light at the end of the tunnel, but if you keep moving, \nyou will come to a better place.", 
	"At my age, there is only one big surprise left, and I would just \nas soon leave it a mystery.",
	"Pride is not the opposite of shame, but its source. True humility \nis the only antidote to shame.",
	"You must never give in to despair. Allow yourself to slip down that \nroad and you surrender to your lowest instincts. In the \ndarkest times, hope is something you give yourself. That is the \nmeaning of inner strength."]
	choic = random.choice(example)
	return choic


def choose_random():
	choi = examples()
	choice = ''.join(choi)
	return choice, choi


cho, choi = choose_random()

blit_text(win, choi, (150,175), TEXT)

user_words = []
user_text = ''

input_rect = pygame.draw.rect(win, (0,0,0), (100, 425, 800, 50),2)
win.blit(TEXT.render('Click here to start. Press Space when you are done.',1,(pygame.Color("#80ffaa"))), (input_rect.x+10, input_rect.y+5))

active = False
error = 0


def find_errors(temp_input):
	errors = error
	j = cho.split()
	indice = len(temp_input) - 1

	for i in range(len(temp_input)):
		if temp_input[i] != j[i]:
			errors += 1

	return errors


def accuracy(temp_input):
	try:
		acc = (len(temp_input) - find_errors(temp_input))/ len(temp_input) * 100
	except:
		acc = 0
	return int(acc)


def speed(temp_input, start_time):
	new_time = time.time() - start_time 
	try:
		WPM = (len(temp_input) - find_errors(temp_input))//(new_time/60)
	except:
		WPM = 0
	return int(WPM) 


def check_word(user, text):
	i = cho.split()
	index = len(user) - 1
	if user[index] != i[index]:
		return False
	else:
		return True


mode = True


def draw():
	if mode:
		win.fill((255,255,255))
		win.blit(app_title, (1000//2 - app_title.get_width()//2, 50))
		blit_text(win, choi, (150,175), TEXT)
		pygame.draw.rect(win, (0,0,0), (100, 425, 800, 50),2)
		output = TEXT.render(user_text, 1, (0,0,0))
		win.blit(output, (input_rect.x+10, input_rect.y+5))
	else:
		win.fill((255,255,255))
		win.blit(app_title, (1000//2 - app_title.get_width()//2, 50))
		blit_text(win, choi, (150,175), TEXT)
		pygame.draw.rect(win, (0,0,0), (100, 425, 800, 50),2)
		pygame.draw.rect(win, (pygame.Color('pink')), (input_rect.x+5, input_rect.y+5, 790, 40))
		output = TEXT.render(user_text, 1, (0,0,0))
		win.blit(output, (input_rect.x+10, input_rect.y+5))


def stats(active, start):
	if active:
		win.blit(TEXT.render('Accuracy: ' + str(accuracy(user_words)) + '%',1,(pygame.Color("#00ff99"))), (700, 300))
		win.blit(TEXT.render('Speed: ' + str(speed(user_words,start)) + ' WPM',1,(pygame.Color("#00ff99"))), (700, 350))
	
	pygame.display.update()

run = True


while run:

	pygame.time.delay(100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			if input_rect.collidepoint(pos) and not active:
				active = True
				start_time = time.time()
				draw()
				win.blit(TEXT.render('Accuracy: 0%',1,(pygame.Color("#00ff99"))), (700, 300))
				win.blit(TEXT.render('Speed: 0 WPM',1,(pygame.Color("#00ff99"))), (700, 350))	
		

		if event.type == pygame.KEYDOWN and active == True:
				
			if event.key == pygame.K_SPACE:
				user_words.append(user_text)
				if check_word(user_words, user_text):
					user_text = ''
					count += 1
					if not mode:
						mode = True
				else:
					mode = False
					draw()
					user_words.pop(-1)
					error += 1
					
				try:
					if user_words[-1] == cho.split()[-1]:
						win.fill((255,255,255))
						win.blit(TITLE.render('Accuracy: ' + str(accuracy(user_words)) + '%',1,(pygame.Color("#00e6e6"))), (310, 200))
						win.blit(TITLE.render('Speed: ' + str(speed(user_words,start_time)) + ' WPM',1,(pygame.Color("#00e6e6"))), (305, 350))
						pygame.display.update()
						pygame.time.delay(2000)
						cho, choi = choose_random()
						user_text = ''
						active = False
						count = 0
						error = 0
						user_words = []
						draw()
						
						win.blit(TEXT.render('Click here to start. Press Space when you are done.',1,(pygame.Color("#80ffaa"))), (input_rect.x+10, input_rect.y+5))
						pygame.display.update()

					else:
						draw()
						stats(active, start_time)
				except:
					pass

			elif event.key == pygame.K_BACKSPACE:
				user_text = user_text[:-1]
				draw()
				stats(active, start_time)
			else:
				user_text += event.unicode
				draw()
				stats(active, start_time)
			

	pygame.display.update()

pygame.quit()