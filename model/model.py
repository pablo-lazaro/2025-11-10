import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.DiGraph()

        # Ordini
        self.allOrders = DAO.gettAllOrdini()
        self._idMapOrdini = {}
        for order in self.allOrders:
            self._idMapOrdini[order.order_id] = order


    def getAllStores(self):
        return DAO.getAllStores()

    def getNodes(self, idOrdine):
        return DAO.getAllNodi(idOrdine)

    def creaGrafo(self, IdStore, giornoUtente):
        self.grafo.clear()
        # Nodi --> ordini che sono stati effettuati nello store selezionato
        nodi = self.getNodes(IdStore)
        self.grafo.add_nodes_from(nodi)
        print(f"Nodi: {len(self.grafo.nodes)}, Edge: {len(self.grafo.edges)}")

        # Archi
        self.addEdges(IdStore, giornoUtente)
        print(f"Nodi: {len(self.grafo.nodes)}, Edge: {len(self.grafo.edges)}")

    def addEdges(self, IdStore, giornoUtente):

        tupleEdge = DAO.getEdges(IdStore, giornoUtente)

        for tupla in tupleEdge:
            self.grafo.add_edge(self._idMapOrdini[tupla[0]], self._idMapOrdini[tupla[1]], weight = tupla[2])



    def getGraphDetails(self):
        return len(self.grafo.nodes), len(self.grafo.edges)

    def getGraphNodes(self):
        return self.grafo.nodes

    def cercaCinqueArchiPesoMaggiore(self):
        # Chiediamo gli archi passando direttamente data='weight'
        # Ogni arco nella lista sarà una tupla semplice: (u, v, peso)
        lista_archi = list(self.grafo.edges(data='weight'))

        # Ordiniamo la lista guardando l'elemento con indice 2 (il peso) in ordine decrescente
        lista_archi.sort(key=lambda x: x[2], reverse=True)

        # Restituiamo solo i primi 5
        return lista_archi[0:5]

