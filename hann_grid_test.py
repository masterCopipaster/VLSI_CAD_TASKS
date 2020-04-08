from hann_grid import*
gr = hann_grid()

gr.addpin((0, 0))
#gr.addvertex((0, 1))  
#gr.addvertex((1, 0))
gr.addpin((1, 1))  
gr.addpin((0, 2)) 
#gr.addedge((0, 0), (0, 1))
#gr.findedge((0, 0), (0, 1)).name = "edge" 
gr.dotexportpng("autopng0.png")

print("building full graph")
gr.full()

#print("deikstrifying")
#gr.deikstrify()
gr.dotexportpng("autopng1.png")

print("building hann grid")
gr.build_hann_grid()
gr.dotexportpng("autopng2.png")

print("deikstrifying")
gr.deikstrify()
gr.dotexportpng("autopng3.png")
print(gr.dotexport())

print("cleaning up")
gr.cleanup()
gr.dotexportpng("autopng4.png")
