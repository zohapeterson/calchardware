from tkinter import *
from math import *

## Relevant Variables
input_nodes = input_elasticMod = input_length = input_height = input_crossSection = input_force = input_depth = input_dia = None
window_gap = 50

# Receive input for relevant properties, set height and width of the window
#while (not input_elasticMod.isdigit()):
input_elasticMod = 100000#input("Enter the elastic modulus [Pa]: ")

#while (not input_length.isdigit()):
input_length = 500#input("Enter the width of the model [m]: ")

#while(not input_height.isdigit()):
input_height = 200#input("Enter the height of the model [m]: ")

#while(not input_depth.isdigit()):
input_depth = 10#input("Enter the depth of the model [m]: ")

#while(not input_dia.isdigit()):
input_dia = 10#input("Enter the diameter of the model [m]: ")

#while(not input_nodes.isdigit()):
input_nodes = 10#input("Enter the number of nodes for the model: ")

#while(not input_force.isdigit()):
input_force = 100#input("Enter the force acted upon the beam [N]: ")

#while(cross_section.toUpper() != "RECTANGULAR" or cross_section.toUpper() != "CIRCULAR"):
input_crossSection = "Rectangular"#input("Enter the cross section of the beam [Rectangular or Circular]: ")

print("Your model has "  + str(input_nodes) + " nodes, an elastic modulus of " + str(input_elasticMod) + "Pa, a width of " + str(input_length) + "m, and a height of " + str(input_height) + "m.")

width = 2 * window_gap + input_length
height = 2 * window_gap + input_height

# Create Object class
class Model:
    def __init__(self, model_width, model_height, model_elasticMod, node_division, cross_section, force):
        self.model_width = model_width
        self.model_height = model_height
        self.model_elasticMod = model_elasticMod
        self.nodes = node_division
        self.cross_section = cross_section
        self.force = force
        self.BC_dim = 10
        self.modules = []


        self.createForce()
    
    def createForce(self):
        if(self.force > 0):
            canvas.create_rectangle(3 * self.BC_dim, window_gap + (self.model_height / 2) - (self.BC_dim / 2), window_gap, window_gap + (self.model_height / 2) + (self.BC_dim / 2), fill="red", width = 0)
            canvas.create_polygon(3 * self.BC_dim, window_gap + (self.model_height / 2) - self.BC_dim, 3 * self.BC_dim, window_gap + (self.model_height / 2) + self.BC_dim, 2 * self.BC_dim, window_gap + self.model_height / 2, fill="red")
        else:
            canvas.create_rectangle(2 * self.BC_dim, window_gap + (self.model_height / 2) - (self.BC_dim / 2), window_gap - self.BC_dim, window_gap + (self.model_height / 2) + (self.BC_dim / 2), fill="red", width = 0)
            canvas.create_polygon(window_gap - self.BC_dim, window_gap + (self.model_height / 2) - self.BC_dim, window_gap - self.BC_dim, window_gap + (self.model_height / 2) + self.BC_dim, window_gap, window_gap + (self.model_height / 2), fill="red")

        self.createNodes()

    def createNodes(self):
        for i in range(0, self.nodes):
            self.modules.append(Module(input_elasticMod, input_crossSection, input_depth, input_height, input_length, input_dia, input_nodes))
            #self.modules.append(canvas.create_rectangle((window_gap + (i * (self.model_width / self.nodes))), window_gap, ((window_gap + (i * (self.model_width / self.nodes))) + (self.model_width / self.nodes)), (window_gap + self.model_height)))

        self.createFixedSupport()

    def createFixedSupport(self):
        canvas.create_rectangle(window_gap + self.model_width, window_gap,window_gap + self.model_width + 10, window_gap + self.model_height, fill="black")

class Module:
    def __init__(self, elastic_mod, cross_section, depth, height, length, dia, numNodes):
        self.elastic_mod = elastic_mod
        self.mod_crossSection = cross_section
        self.depth = depth
        self.height = height
        self.dia = dia
        self.modLength = self.length / self.numNodes
        self.area = 0
        self.k_value = 0
        self.k_matrix = []
    
    def calcArea(self):
        if(self.mod_crossSection.toUpper() == "RECTANGULAR"):
            self.area = self.depth * self.height
        elif(self.mod_crossSection.toUpper() == "CIRCULAR"):
            self.area = pi * (self.dia / 2) ** 2

    def calcK(self):
        self.k_value = (self.elastic_mod * self.area) / self.modLength

    def setKMatrix(self):
        self.k_matrix.append([[self.k_value, -self.k_value],[-self.k_value, self.k_value]])
        


## Create GUI -- window and canvas
window = Tk()
window.title("FEA")
window.geometry(str(width)+"x"+str(height))
window.configure(background="#ffffff")
canvas = Canvas(window, width=width, height=height, bg="#ffffff", highlightthickness=1)
canvas.pack()

## Create model
model = Model(input_length, input_height, input_elasticMod, input_nodes, input_crossSection, input_force)

window.mainloop() # Starts loop and event listener
