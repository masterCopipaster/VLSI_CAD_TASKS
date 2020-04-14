import os
import xml.dom.minidom as minidom
from sys import argv

def pointcnt(filename):
	doc = minidom.parse(filename)
	net = doc.getElementsByTagName("net")[0]
	points = net.getElementsByTagName("point")
	return len(points)
	
filename = argv[1]
pc = pointcnt(filename)

print("pins in file:", pc)

if pointcnt(filename) > 50:  
	print("running fast mode")	
	os.system("python3 main.py " + filename + " -fm &")	

print("running slow mode")	
os.system("python3 main.py " + filename)
