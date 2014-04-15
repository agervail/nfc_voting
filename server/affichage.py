import sys, pygame
import math
import mosquitto
from time import sleep
import requests
import json
'''
Little display of a mongodb database.
First fetching the content of the database
Then each time the database is modified displaying immediatly the changes
'''


def get_score(bd, table):
  r = requests.get('http://localhost:28017/' + bd + '/' + table + '/')
  res = json.loads(r.text)
  score = [0,0,0]
  for row in res['rows']:
    score[row['vote']] += 1
  return score

pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Vote result")
h_bas = height - 10
myfont = pygame.font.SysFont("Comic Sans MS", 80)
pink = (255, 0, 255)
blue = (0, 255, 255)
score = get_score('nfcDB', 'vote')
name = ['Pour', 'Contre', 'Neutre']

#MQTT part
def on_message(mosq, msg):
  global score
	print("one more for " + str(msg.payload) + str(score))
	score[int(msg.payload)] += 1
mqttc = mosquitto.Mosquitto("bla")
mqttc.on_message = on_message
mqttc.connect("127.0.0.1", 1883, 10000)
mqttc.subscribe("success", 0)

while 1:
	sleep(0.5)
	mqttc.loop()
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
	screen.fill((0,0,0))
	max_score = max(score)
	if max_score != 0:
		rapport = 500 / max_score
	for i, val in enumerate(score):
		xx = 200 * i
		label = myfont.render(str(val), 1, pink)
		title = myfont.render(name[i], 1, blue)
		screen.blit(pygame.transform.rotozoom(title,0,0.5), (xx + 60, 50))
		if val == 0:
			screen.blit(pygame.transform.rotozoom(label,45,0.5), (xx + 82, 550))
		else:
			hauteur = val * rapport
			rect = pygame.Rect(xx + 20, h_bas - hauteur, 160, hauteur)
			pygame.draw.rect(screen, (50,50,50), rect)
			screen.blit(pygame.transform.rotozoom(label,45,0.5), (xx + 82 - math.log(val,10)*7, min(550,h_bas - hauteur + 20)))
	pygame.display.update()
