import pygame

pygame.init()

from pygame.locals import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

DX = 20
DY = 20

import xml.dom.minidom as minidom
from sys import argv
import sys

def readxml(filename, m):
	doc = minidom.parse(filename)
	net = doc.getElementsByTagName("net")[0]
	points = net.getElementsByTagName("point")
	for point in points:
		x = 0
		y = 0
		layer = None
		for name, value in point.attributes.items():
			if name == "x": x = m * int(value) + DX
			if name == "y": y = m * int(value) + DY
			if name == "layer": layer = value
		if layer == "pins":
			pygame.draw.circle(sc, WHITE, (x, y), 10, 1)
		if layer == "m2_m3":
			pygame.draw.circle(sc, PINK, (x, y), 4, 1)
		if layer == "pins_m2":
			pygame.draw.circle(sc, LIGHT_BLUE, (x, y), 8, 1)
		if layer == "m2":
			pygame.draw.circle(sc, YELLOW, (x, y), 6, 1)
		if layer == "m3":
			pygame.draw.circle(sc, GREEN, (x, y), 2, 1)
	
	segments = net.getElementsByTagName("segment")
	for segment in segments:
		x1 = 0
		y1 = 0
		x2 = 0
		y2 = 0
		layer = None
		for name, value in segment.attributes.items():
			if name == "x1": x1 = m * int(value) + DX
			if name == "y1": y1 = m * int(value) + DY
			if name == "x2": x2 = m * int(value) + DX
			if name == "y2": y2 = m * int(value) + DY
			if name == "layer": layer = value
		if layer == "m2":
			pygame.draw.line(sc, YELLOW, (x1, y1), (x2, y2), 1)
		if layer == "m3":
			pygame.draw.line(sc, GREEN, (x1, y1), (x2, y2), 1)

sc = pygame.display.set_mode((150 * int(argv[2]) + 2 * DX, 150 * int(argv[2]) + 2 * DY))
readxml(argv[1], int(argv[2]))
pygame.display.update()
print("ready")

import time
while 1:
	time.sleep(1)
	sc.fill((0, 0, 0))
	readxml(argv[1], int(argv[2]))
	pygame.display.update()
	for i in pygame.event.get():
		if i.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
