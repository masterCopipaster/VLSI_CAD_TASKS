from graph import*

def printfunc(ver, arg):
	print(ver.name)
	
gr = graph()
gr.bidir = True
gr.addvertex(vertex("vert1"))
gr.addvertex(vertex("vert2"))
gr.addvertex(vertex("vert3"))
gr.addvertex(vertex("vert4"))
gr.addedge(edge(gr.verts[0], gr.verts[1], value = 10))
gr.addedge(edge(gr.verts[0], gr.verts[2], value = 20))
gr.addedge(edge(gr.verts[0], gr.verts[3], value = 30))
gr.addedge(edge(gr.verts[1], gr.verts[3], value = 40))


gr.dotexportpng("autopng0.png")
#gr.remvertex(gr.verts[0])
#gr.remedge(gr.edges[0])
#gr.rem2vertsedge(gr.verts[0], gr.verts[1])
#gr.addedge(edge(gr.verts[1], gr.verts[3]))
gr.deikstrify2(start = gr.verts[2])
gr.dotexportpng("autopng1.png")
