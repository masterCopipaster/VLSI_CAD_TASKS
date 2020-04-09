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

		
def writexml(filename, gr):
	doc = minidom.parse(filename)
	net = doc.getElementsByTagName("net")[0]
	points = net.getElementsByTagName("point")
	added = []
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
		if ver(p1, p2): 
			segment.setAttribute("layer", "m3")
		if not p1 in added:
			added.append(p1)
			point = doc.createElement("point")
			point.setAttribute("x", str(p1[0]))
			point.setAttribute("y", str(p1[1]))
			if p1 in gr.pins and hor(p1, p2):
				point.setAttribute("layer", "pins_m2")
			if p1 in gr.pins and ver(p1, p2):
				point.setAttribute("layer", "pins_m2")
				apoint = doc.createElement("point")
				apoint.setAttribute("x", str(p2[0]))
				apoint.setAttribute("y", str(p2[1]))
				apoint.setAttribute("layer", "m2")
				net.appendChild(apoint)
				apoint.setAttribute("layer", "m2_m3")
				net.appendChild(apoint)
			if not p1 in gr.pins:
				point.setAttribute("layer", "m2_m3")
			net.appendChild(point)
		if not p2 in added:
			added.append(p2)
			point = doc.createElement("point")
			point.setAttribute("x", str(p2[0]))
			point.setAttribute("y", str(p2[1]))
			if p2 in gr.pins and hor(p1, p2):
				point.setAttribute("layer", "pins_m2")
			if p2 in gr.pins and ver(p1, p2):
				point.setAttribute("layer", "pins_m2")
				apoint = doc.createElement("point")
				apoint.setAttribute("x", str(p2[0]))
				apoint.setAttribute("y", str(p2[1]))
				apoint.setAttribute("layer", "m2")
				net.appendChild(apoint)
				apoint.setAttribute("layer", "m2_m3")
				net.appendChild(apoint)
			if not p2 in gr.pins:
				point.setAttribute("layer", "m2_m3")
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
gr.cleanup()

if tdot: print(gr.dotexport())
if dot: gr.dotexportpng("autopng.png", pos = True)

writexml(argv[1], gr)

print("total length", sum(ed.value for ed in gr.edges))
