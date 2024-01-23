from tkinter import *
from math import *
import numpy as np

## Relevant Variables
input_nodes = input_elasticMod = input_length = input_height = input_crossSection = input_force = input_depth = input_dia = None
window_gap = 50

# Receive input for relevant properties
#while (not input_elasticMod.isdigit()):
input_elasticMod = 200000#input("Enter the elastic modulus [Pa]: ")

#while (not input_length.isdigit()):
input_length = 500#input("Enter the length of the model [m]: ")

#while(not input_height.isdigit()):
input_height = 200#input("Enter the height of the model [m]: ")

#while(not input_depth.isdigit()):
input_depth = 10#input("Enter the depth of the model [m]: ")

#while(not input_dia.isdigit()):
input_dia = 10#input("Enter the diameter of the model [m]: ")

#while(not input_nodes.isdigit()):
input_nodes = 10#input("Enter the number of nodes for the model: ")

#while(not input_force.isdigit()):
input_force = 1000000#input("Enter the force acted upon the beam [N]: ")

#while(cross_section.toUpper() != "RECTANGULAR" or cross_section.toUpper() != "CIRCULAR"):
input_crossSection = "Rectangular"#input("Enter the cross section of the beam [Rectangular or Circular]: ")

# print("Your model has "  + str(input_nodes) + " nodes, an elastic modulus of " + str(input_elasticMod) + "Pa, a length of " + str(input_length) + "m, and a height of " + str(input_height) + "m.")

width = 2 * window_gap + input_length
height = 2 * window_gap + input_height

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
        
        for node in self.modules:
            node.drawModule()
        

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
        self.draw_module = None#canvas.create_rectangle((window_gap + (index * (self.length / self.numNodes))), window_gap, ((window_gap + (index * (self.length / self.numNodes))) + (self.length / self.numNodes)), (window_gap + self.height), fill=self.color)
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
window.geometry(str(width)+"x"+str(height))
window.configure(background="#ffffff")
canvas = Canvas(window, width=width, height=height, bg="#ffffff", highlightthickness=1)
canvas.pack()

## Create model
model = Model(input_length, input_height, input_elasticMod, input_nodes, input_crossSection, input_force)

window.mainloop() # Starts loop and event listener