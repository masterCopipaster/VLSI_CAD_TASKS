import xml.dom.minidom as minidom
from hann_grid import*
from sys import argv

gr = hann_grid()

def readxml(filename, gr):
	doc = minidom.parse(filename)
	net = doc.getElementsByTagName("net")[0]
	points = net.getElementsByTagName("point")
	for point in points:
		x = 0
		y = 0
		layer = None
		for name, value in point.attributes.items():
			if name == "x": x = int(value) 
			if name == "y": y = int(value)
			if name == "layer": layer = value
		if layer == "pins":
			gr.addpin((x, y))

def generate_layermap(gr):
	lmap = {}
	ver = lambda ed: ed.vertexfrom.value[0] == ed.vertexto.value[0]
	for p in gr.vertmap.keys():
		layers = {"pins" : False, "m2" : False, "m3" : False, "pins_m2" : False, "m2_m3" : False}
		v = gr.vertmap[p]
		if p in gr.pins:
			layers["pins"] = True
		eds = v.ins + v.outs
		for ed in eds:
			if ver(ed):
				layers["m3"] = True
			else:
				layers["m2"] = True
				
		if layers["m2"] and layers["m3"]:
			layers["m2_m3"] = True
		if layers["pins"] and layers["m2"]:
			layers["pins_m2"] = True
		m2 = layers["m2"]
		layers["m2"] = False
		if layers["pins"] and layers["m3"]:
			layers["pins_m2"] = True
			layers["m2_m3"] = True
			layers["m2"] = not m2
		lmap[p] = layers
	return lmap
		
		
def writexml(filename, gr):
	doc = minidom.parse(filename)
	net = doc.getElementsByTagName("net")[0]
	points = net.getElementsByTagName("point")
	added = []
	lmap = generate_layermap(gr)
	ver = lambda p1, p2: p1[0] == p2[0]
	hor = lambda p1, p2: p1[1] == p2[1]
	for p1, p2 in gr.edgemap.keys():
		segment = doc.createElement("segment")
		segment.setAttribute("x1", str(p1[0]))
		segment.setAttribute("y1", str(p1[1]))
		segment.setAttribute("x2", str(p2[0]))
		segment.setAttribute("y2", str(p2[1]))
		net.appendChild(segment)
		if hor(p1, p2): 
			segment.setAttribute("layer", "m2")
		elif ver(p1, p2): 
			segment.setAttribute("layer", "m3")
		else:
			segment.setAttribute("layer", "m3")
	for p in lmap.keys():
		point = doc.createElement("point")
		point.setAttribute("x", str(p[0]))
		point.setAttribute("y", str(p[1]))
		if lmap[p]["pins_m2"]:
			point.setAttribute("layer", "pins_m2")
			net.appendChild(point)
			
		point = doc.createElement("point")
		point.setAttribute("x", str(p[0]))
		point.setAttribute("y", str(p[1]))
		if lmap[p]["m2_m3"]:
			point.setAttribute("layer", "m2_m3")
			net.appendChild(point)
			
		point = doc.createElement("point")
		point.setAttribute("x", str(p[0]))
		point.setAttribute("y", str(p[1]))
		if lmap[p]["m2"]:
			point.setAttribute("layer", "m2")
			net.appendChild(point)
			
	l = filename.split(".")
	l[len(l) - 2] += "_out"
	outname = "."
	outname = outname.join(l)
	f = open(outname, "w")
	f.write(doc.toprettyxml())
	f.close()
	
readxml(argv[1], gr)

fastmode = False
tdot = False
dot = False

for arg in argv:
	if arg == "-fm": fastmode = True
	if arg == "-tdot": tdot = True
	if arg == "-dot": dot = True
print("building full graph")
gr.full()

print("deikstrifying")
gr.deikstrify()

print("building hann grid")
gr.build_hann_grid()

if not fastmode:
	print("building full graph")
	gr.full()

	print("deikstrifying")
	gr.deikstrify()

	print("building hann grid")
	gr.build_hann_grid()

print("deikstrifying")
gr.deikstrify()

print("cleaning up")
gr.joinify()
gr.cleanup()
gr.joinify()
gr.cleanup()

if tdot: print(gr.dotexport())
if dot: gr.dotexportpng("autopng.png", pos = True)

writexml(argv[1], gr)

print("total length", sum(ed.value for ed in gr.edges))
