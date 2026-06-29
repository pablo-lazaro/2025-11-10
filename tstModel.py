from model.model import Model

myModel = Model()
myModel.creaGrafo(3, 6)
nodi, archi = myModel.getGraphDetails()
print(f"Grafo creato! Il grafo ha {nodi} nodi e {archi} archi")