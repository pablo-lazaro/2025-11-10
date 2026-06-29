import flet as ft

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        # Stores
        self.allStores = self._model.getAllStores()
        self._coiceStore = None

        self._coiceNodo = None
    def fillDDStore(self):

        for store in self.allStores:
            self._view._ddStore.options.append(
                ft.dropdown.Option(
                    data=store,  # Oggetto
                    key=store.store_name,  # Stringa che verrà visualizzata
                    on_click=self._choiceDdStore  # Dove viene salvato
                )
            )

    def _choiceDdStore(self, e):
        self._coiceStore = e.control.data
        print(f"Hai selezionato come store --> {self._coiceStore}")

    def handleCreaGrafo(self, e):

        valoreNumUtente = self._view._txtIntK.value

        if valoreNumUtente == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore numetico per numero minimo compagnie", color="red"))
            self._view.update_page()
            return

        try:
            numeroFinale = int(valoreNumUtente)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserire un valore intero per numero minimo compagnie", color="red"))
            self._view.update_page()
            return

        self._model.creaGrafo(self._coiceStore.store_id, numeroFinale)

        numNodes, numEdges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {numNodes} nodi e {numEdges} archi", color="green"))
        self._view.update_page()

        cinqueArchiPesoMaggiore = self._model.cercaCinqueArchiPesoMaggiore()
        for arco in cinqueArchiPesoMaggiore:
            self._view.txt_result.controls.append(ft.Text(f"Arco {arco[0]} --> {arco[1]} - Peso: {arco[2]}"))


        nodi = self._model.getGraphNodes()

        for nodo in nodi:
            self._view._ddNode.options.append(
                ft.dropdown.Option(
                    data=nodo,  # Oggetto
                    key=nodo.order_id,  # Stringa che verrà visualizzata
                    on_click=self._choiceDdNodo  # Dove viene salvato
                )
            )

        self._view.update_page()

    def _choiceDdNodo(self, e):
        self._coiceNodo = e.control.data
        print(f"Hai selezionato come nodo {self._coiceNodo}")

    def handleCerca(self, e):

        if self._coiceNodo is None:
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un nodo dal dropdown", color="red"))
            self._view.update_page()
            return



    def handleRicorsione(self, e):
        pass