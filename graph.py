class vertex :
	name = None
	value = None
	ins = None
	outs = None
	def __init__(self, name = None, value = None):
		self.name = name
		self.value = value
		self.ins = []
		self.outs = []
		self.name = name
	def __str__(self):
		return "<vertex " + str(id(self)) + " name: " + str(self.name) + " value: " + str(self.value) + ">"
	def __repr__(self):
		return "<vertex " + str(id(self)) + " name: " + str(self.name) + " value: " + str(self.value) + ">"
		
	def deg(self, ind = True, outd = True):
		d = 0
		#print("measure deg")
		if ind: 
			d += len(self.ins)
		#	print(self.ins)
		if outd: 
			d+= len(self.outs)
		#	print(self.outs) 
		return d
		
class edge :
	name = None
	value = None
	vertexfrom = None
	vertexto = None

	def __init__ (self, frm, to, name = None, value = None):
		self.name = name
		self.value = value
		self.vertexfrom = frm
		self.vertexto = to
		to.ins.append(self)
		frm.outs.append(self)
		
	def __del__(self):
		try:
			self.vertexto.ins.remove(self)
			self.vertexfrom.outs.remove(self)
		except:
			pass
			
	def anotherside(self, v):
		if v == self.vertexfrom:
			return self.vertexto
		if v == self.vertexto:
			return self.vertexfrom
		
	def __str__(self):
		return "<edge " + str(id(self)) + " name: " + str(self.name) + " value: " + str(self.value) + " from: " + str(self.vertexfrom) + " to: " + str(self.vertexto) + ">"
	def __repr__(self):
		return "<edge " + str(id(self)) + " name: " + str(self.name) + " value: " + str(self.value) + " from: " + str(self.vertexfrom) + " to: " + str(self.vertexto) + ">"
		
import os
	
class graph:
	edges = None
	verts = None
	unvisited = None
	bidir = False
	
	
	def __init__(self):
		self.edges = []
		self.verts = []
		
	def addvertex(self, ver):
		self.verts.append(ver)
	
	def addedge(self, ed):
		self.edges.append(ed)
	
	def remedge(self, ed, destructor = True):
		#d1 = self.deg()
		self.edges.remove(ed)
		if destructor:
			ed.vertexto.ins.remove(ed)
			ed.vertexfrom.outs.remove(ed)
			del ed
		else:
			ed.vertexto.ins.remove(ed)
			ed.vertexfrom.outs.remove(ed)
		#d2 = self.deg()
		#print(d1, d2)
			
	def deg(self):
		return sum(v.deg() for v in self.verts)
	
	def rem2vertsedge(self, ver1, ver2):
		removable = set({})
		removable |= set(ver1.outs) & set(ver2.ins)
		if self.bidir: 
			removable |= set(ver2.outs) & set(ver1.ins)
		for ed in removable:
			self.remedge(ed);
		
	
	def remvertex(self, ver, destructor = True):
		self.verts.remove(ver)
		for ed in set(ver.ins) | set(ver.outs):
			self.remedge(ed)
		if destructor: 
			del ver
		
	
	def dfs(self, frm = None, runfunc = None, arg = None, bidir = None):
		if bidir == None: 
			bidir = self.bidir
		if(frm == None) :
			self.unvisited = self.verts.copy()
			while len(self.unvisited) > 0:
				self.dfs(self.unvisited[0], runfunc, bidir)
		else:
			try:
				self.unvisited.remove(frm)
			except: 
				return
			if runfunc:
				runfunc(frm, arg)
			for ed in frm.outs:
				self.dfs(ed.vertexto, runfunc, bidir)
			if bidir: 
				for ed in frm.ins:
					self.dfs(ed.vertexfrom, runfunc, bidir)

		
	def dotexport(self, pos = True):
		s = ""
		if self.bidir:
			s += "graph{\n"
			arrow = " -- "
		else :
			s += "digraph{\n"
			arrow = " -> "
		#s += "graph [pad=\"0.212,0.055\" bgcolor=lightgray]"
		idf = lambda v:"\"" + (str(v.name) if v.name else "") + (str(v.value) if v.value else str(id(v))) + "\""	
		for v in self.verts:
			s += idf(v)
			if pos:
				s += " [pos=\"" + str(v.value[0]*0.4) + "," + str(v.value[1]*0.4) + "!\"]"
			s += ";\n"
			
		s += "\n"
		
		for ed in self.edges:
			label = "\""
			label += "name: " + str(ed.name) + "\n" if ed.name else ""
			label += "value: " + str(ed.value) if ed.value else ""
			label += "\""
			s += idf(ed.vertexfrom) + arrow + idf(ed.vertexto) + (" [label = " + label + "]" if label != "\"\"" else "" )+ "\n"
		s += "}"
		return s

	def dotexportpng(self, filename, pos = True):
		f = open("__tmpfile__.tmp", "w")
		f.write(self.dotexport(pos = pos))
		f.close()
		ret = os.system("neato -Tpng -o " + filename + " __tmpfile__.tmp")
		os.system("rm __tmpfile__.tmp")
		return ret
		
	def deikstrify(self, start = None):
		if not start: start = self.verts[0]
		
		val = lambda v: v.value
		vouts = lambda v: v.outs if not self.bidir else v.outs + v.ins
		vins = lambda v: v.ins if not self.bidir else v.outs + v.ins
		 
		self.unvisited = self.verts.copy()
		appended = start
		deikedges = []
		avedges = []
		
		goedge = None
		
		while len(self.unvisited) > 0:
			#print("-----------------------" )
			#print("appended initial", appended)
			#avedges += vouts(appended)
			for ed in vouts(appended):
				if (ed.vertexfrom in self.unvisited) or (ed.vertexto in self.unvisited):
					avedges.append(ed)
			try:
				while 1:
					avedges.remove(goedge)
			except:
				pass
			#print("avedges", avedges)
			avedges.sort(key = val)
			if not len(avedges):
				break
			goedge = avedges[0]
			#print(goedge)
			appendedl = [goedge.vertexto, goedge.vertexfrom]
			
			#print("unvisited", self.unvisited)
			if appended in self.unvisited: 
				self.unvisited.remove(appended)
			#print("unvisited", self.unvisited)
			#print("appendedl", appendedl)
			
			if appendedl[0] in self.unvisited:
				appended = appendedl[0]
				deikedges.append(goedge)
			if appendedl[1] in self.unvisited:
				appended = appendedl[1]
				deikedges.append(goedge)
			#print(appended)
				
		#print(deikedges)
		for ed in set(self.edges) - set(deikedges):
			self.remedge(ed)
			#print("ooops")
		
			
		
		
		
		
		
