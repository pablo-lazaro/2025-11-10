from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodi(IdStore):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                    from orders o 
                    where o.store_id = %s"""

        cursor.execute(query, (IdStore,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getMappaOrdineQuantita(idMapOrdini):
        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = """select oi.order_id as IDOrdine, sum(oi.quantity) as quantita
                    from order_items oi 
                    group by idordine"""

        cursor.execute(query)

        for row in cursor:
            results[idMapOrdini[row["IDOrdine"]]] = row["quantita"]

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def gettAllOrdini():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                   from orders o"""

        cursor.execute(query)

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results # Lista di ordini

    @staticmethod
    def getEdges(idStore, giornoUtente):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)

        # Usiamo DATEDIFF(data_successiva, data_precedente) per calcolare i giorni reali
        query = """SELECT o.order_id                                                                    AS ID1, \
                          o2.order_id                                                                   AS ID2,
                          (SUM(i1.quantity) + SUM(i2.quantity)) / DATEDIFF(o2.order_date, o.order_date) AS peso
                   FROM orders o, \
                        orders o2, \
                        order_items i1, \
                        order_items i2
                   WHERE o.store_id = %s
                     AND o.store_id = o2.store_id
                     AND i1.order_id = o.order_id
                     AND i2.order_id = o2.order_id
                     AND DATEDIFF(o2.order_date, o.order_date) >= 1
                     AND DATEDIFF(o2.order_date, o.order_date) <= %s
                   GROUP BY o.order_id, o2.order_id, o.order_date, o2.order_date"""

        cursor.execute(query, (idStore, giornoUtente,))

        for row in cursor:
            results.append((row["ID1"], row["ID2"], row["peso"]))

        cursor.close()
        conn.close()
        return results  # lista di Tuple (IdNodoA, IdNodoB, peso)