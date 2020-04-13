from graph import *

class hann_grid(graph):
	
	vertmap = None
	edgemap = None
	pins = None
	
	def __init__(self):
		super().__init__()
		self.bidir = True
		self.vertmap = {}
		self.edgemap = {}
		self.pins = []
	
	def addpin(self, p):
		self.pins.append(p)
		self.addvertex(p, name = "pin")
		
	def addvertex(self, p, name = None):
		v = vertex(name = name)
		v.value = p
		if not p in self.vertmap:
			super().addvertex(v)
			self.vertmap[v.value] = v
	
	def addedge(self, p1, p2, name = None):
		x1, y1 = p1
		x2, y2 = p2
		if not ((p1, p2) in self.edgemap or (p2, p1) in self.edgemap):
			ed = edge(self.vertmap[p1], self.vertmap[p2], value = abs(x1 - x2) + abs(y1 - y2), name = name)
			super().addedge(ed)
			self.edgemap[(p1, p2)] = ed
	
	def findedge(self, p1, p2):
		return self.edgemap[p1,p2]
	
	def full(self):
		for ed in self.edges:
			super().remedge(ed)
		self.edgemap = {}
			
		for p1 in self.vertmap.keys():
			for p2 in self.vertmap.keys():
				if p1 != p2:
					self.addedge(p1, p2)
	
	def deikstrify(self):
		super().deikstrify()
		self.edgemap = {}
		for ed in self.edges:
			self.edgemap[(ed.vertexfrom.value, ed.vertexto.value)] = ed
	
	def delvertex(self, p):
		for p1 in self.vertmap.copy().keys():
			try:
				self.deledge(p, p1)
			except:
				pass
		self.remvertex(self.vertmap[p])
		if p in self.pins: self.pins.remove[p]
		self.vertmap.pop(p, None)
	
	def deledge(self, p1, p2):
		ed = self.findedge(p1, p2)
		self.remedge(ed)
		self.edgemap.pop((p1, p2), None) 
		
	def build_hann_grid(self):
		curredges = self.edgemap.copy().keys()
		#print(self.edgemap)
		for (p1,p2) in curredges:
			x1, y1 = p1
			x2, y2 = p2
			if 1: #x1 != x2 and y1 != y2 :
				p31 = x1, y2
				p32 = x2, y1
				try:
					self.deledge(p1, p2)
				except:
					pass
				self.addvertex(p31)
				self.addedge(p1, p31)
				#print("addedge", p1, p3)
				self.addedge(p31, p2)
				#print("addedge", p3, p2)
				
				self.addvertex(p32)
				self.addedge(p1, p32)
				#print("addedge", p1, p3)
				self.addedge(p32, p2)
				#print("addedge", p3, p2)
				
	def cleanup(self):
		#print(self.pins)
		cp = self.vertmap.copy()
		self.vertmap = {}
		for p in cp.keys():
			#print("degree", cp[p], cp[p].deg(), cp[p].ins + cp[p].outs)
			#print(self.edgemap)
			if (not (p in self.pins)) and (cp[p].deg() < 2):
				try:
					self.delvertex(p)
					#print("vertex del", p)
				except:
					print("delete failure", p)
			else:
				self.vertmap[p] = cp[p]
				
			self.vertmap = {}
			self.edgemap = {}
			for ed in self.edges:
				self.edgemap[(ed.vertexfrom.value, ed.vertexto.value)] = ed
			for v in self.verts:
				self.vertmap[v.value] = v
	
	
				
	def joinify(self):
		ver = lambda ed: ed.vertexfrom.value[0] == ed.vertexto.value[0]
		
		cp = self.vertmap.copy()
		for v in self.verts:
			#print("degree", v, v.deg(), v.ins + v.outs)
			eds = v.ins + v.outs
			try:
				ed1 = eds[0]
				ed2 = eds[1]
			except:
				continue
			#print(ver(ed1))
			#print(ver(ed2))
			if v.deg() == 2 and ver(ed1) == ver(ed2) and (not v.value in self.pins):
				#print("deleted")
				self.addedge(ed1.anotherside(v).value, ed2.anotherside(v).value)
				self.delvertex(v.value)
		
