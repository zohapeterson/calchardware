from tkinter import *
from math import *
import numpy as np
from matplotlib import cm

## Relevant Variables
input_nodes = input_elasticMod = input_length = input_height = input_crossSection = input_force = input_depth = input_dia = ""
window_gap = 50

# Receive input for relevant properties
while(input_crossSection != "RECTANGULAR" and input_crossSection != "CIRCULAR"):
    input_crossSection = input("Enter the cross section of the beam [Rectangular or Circular]: ").upper()

while(not input_nodes.isdigit()):
    input_nodes = input("Enter the number of nodes for the model: ")
input_nodes = int(input_nodes)

while (not input_elasticMod.isdigit()):
    input_elasticMod = input("Enter the elastic modulus [Pa]: ")
input_elasticMod = float(input_elasticMod)

while(not input_force.isdigit()):
    input_force = input("Enter the force acted upon the beam [N]: ")
input_force = float(input_force)

while (not input_length.isdigit()):
    input_length = input("Enter the length of the model [m]: ")
input_length = float(input_length)

if(input_crossSection == "CIRCULAR"): # Circular Cross section
    while(not input_dia.isdigit()):
        input_dia = input("Enter the diameter of the model [m]: ")
    input_dia = float(input_dia)

    print("Your model has "  + str(input_nodes) + " nodes, an elastic modulus of " + str(input_elasticMod) + "Pa, an applied force of " + str(input_force) + ", a circular cross section, and a length of " + str(input_length) + "m.")

    input_height = input_width = input_dia

    height = 2 * window_gap + input_dia
else: # Rectangular Cross section
    while(not input_height.isdigit()):
        input_height = input("Enter the height of the model [m]: ")
    input_height = float(input_height)

    while(not input_depth.isdigit()):
        input_depth = input("Enter the depth of the model [m]: ")
    input_depth = float(input_depth)

    input_dia = 0

    print("Your model has "  + str(input_nodes) + " nodes, an elastic modulus of " + str(input_elasticMod) + "Pa, an applied force of " + str(input_force) + ", a rectangular cross section, a length of " + str(input_length) + "m, a height of " + str(input_height) + "m, and a depth of " + str(input_depth) + "m.")

    height = 2 * window_gap + input_height

width = 2 * window_gap + input_length

# Create Object class
class Model:
    def __init__(self, model_length, model_height, model_elasticMod, node_division, cross_section, force):
        self.model_length = model_length
        self.model_height = model_height
        self.model_elasticMod = model_elasticMod
        self.nodes = node_division
        self.cross_section = cross_section
        self.force = force
        self.BC_dim = 10
        self.modules = []
        self.entire_kMatrix = [[0] * self.nodes for i in range(self.nodes)]
        self.forceMatrixTranspose = [0] * self.nodes
        self.displacementMatrix = [0] * self.nodes

        self.createForce()
        self.createKmatrix()
        self.setForceMatrix()
        self.calcDisplacement()
        self.output()
    
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
            self.modules.append(Module(input_elasticMod, input_crossSection, input_depth, input_height, input_length, input_dia, input_nodes, i))
        self.createFixedSupport()

    def createFixedSupport(self):
        canvas.create_rectangle(window_gap + self.model_length, window_gap,window_gap + self.model_length + 10, window_gap + self.model_height, fill="black")

    def createKmatrix(self):
        temp_matrix = [[0] * self.nodes for i in range(self.nodes)]
        temp_var = 0
        for this_node in self.modules:
            for i in range(0, len(this_node.ind_kMatrix[0])):
                for j in range(0, len(this_node.ind_kMatrix[0])):
                    if((temp_var) < (len(temp_matrix[0]) - 1)):
                        temp_matrix[temp_var+i][temp_var+j] = this_node.ind_kMatrix[i][j]
            for k in range(0, len(self.entire_kMatrix)):
                for l in range(0, len(self.entire_kMatrix[k])):
                    self.entire_kMatrix[k][l] = self.entire_kMatrix[k][l] + temp_matrix[k][l]
            temp_matrix = [[0] * self.nodes for i in range(self.nodes)]
            temp_var = temp_var + 1
      
        # For now, deleting row n and column n b/c BC (fixed support is unmoving)
        self.entire_kMatrix.pop(len(self.entire_kMatrix) - 1)
        for this_node in self.entire_kMatrix:
            this_node.pop(len(this_node) - 1)

        self.forceMatrixTranspose.pop(len(self.forceMatrixTranspose) - 1)

    def setForceMatrix(self):
        self.forceMatrixTranspose[0] = self.forceMatrixTranspose[0] + self.force # For now, the force is only applied to the end of the beam. This can be changed later
    
    def calcDisplacement(self):
        inverse_kMatrix = np.linalg.inv(self.entire_kMatrix)

        for i in range(len(inverse_kMatrix)):
            for j in range(len(inverse_kMatrix[i])):
                self.displacementMatrix[i] += inverse_kMatrix[i][j] * self.forceMatrixTranspose[j]

    def output(self):
        print("The displacement of each node is as follows: ")
        for i in range(len(self.displacementMatrix)):
            print("Node " + str(i + 1) + ": " + str(self.displacementMatrix[i]) + "m")
        
        max_value = np.max(self.displacementMatrix)
        min_value = np.min(self.displacementMatrix)

        value_space = np.linspace(min_value, max_value, self.nodes) # Create equally space points between the min and max values (for normalization), create the number of nodes points
        normalize = (value_space - min_value) / (max_value - min_value) # Normalize the values
        
        color_map = cm.rainbow # Chose the turbo color map
        colors = color_map(normalize)

        self.displacementMatrix = np.sort(self.displacementMatrix) # Just for algorithmic purposes

        for i in range(self.nodes):
            r, g, b, a = colors[self.nodes - 1 - i]
            r = int(r * 255)
            g = int(g * 255)
            b = int(b * 255)
            hex_color = "#{:02X}{:02X}{:02X}".format(r, g, b)
            self.modules[i].color = hex_color
            self.modules[i].drawModule()

class Module:
    def __init__(self, elastic_mod, cross_section, depth, height, length, dia, numNodes, index):
        self.elastic_mod = elastic_mod
        self.mod_crossSection = cross_section
        self.depth = depth
        self.height = height
        self.length = length
        self.dia = dia
        self.numNodes = numNodes
        self.modLength = self.length / self.numNodes
        self.area = 0
        self.k_value = 0
        self.color = "white"
        self.index = index
        self.draw_module = None
        self.ind_kMatrix = None

        self.calcArea()
        self.calcK()
        self.setKMatrix()
    
    def drawModule(self):
        self.draw_module = canvas.create_rectangle((window_gap + (self.index * (self.length / self.numNodes))), window_gap, ((window_gap + (self.index * (self.length / self.numNodes))) + (self.length / self.numNodes)), (window_gap + self.height), fill=self.color)

    def calcArea(self):
        if(self.mod_crossSection.upper() == "RECTANGULAR"):
            self.area = self.depth * self.height
        elif(self.mod_crossSection.upper() == "CIRCULAR"):
            self.area = pi * (self.dia / 2) ** 2

    def calcK(self):
        self.k_value = (self.elastic_mod * self.area) / self.modLength

    def setKMatrix(self):
        self.ind_kMatrix = [[self.k_value, -self.k_value],[-self.k_value, self.k_value]]

## Create GUI -- window and canvas
window = Tk()
window.title("FEA")
window.geometry(str(int(width))+"x"+str(int(height)))
window.configure(background="#ffffff")
canvas = Canvas(window, width=width, height=height, bg="#ffffff", highlightthickness=1)
canvas.pack()

## Create model
model = Model(input_length, input_height, input_elasticMod, input_nodes, input_crossSection, input_force)

window.mainloop() # Starts loop and event listener