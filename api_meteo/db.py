import sqlite3

class Connection_bdd():
    def __init__(self,bdd):
        self.bdd = bdd
        self.connection = None
        self.cursor = None
        self.connecter_bdd(bdd)
        pass

    def connecter_bdd(self,bdd):
        # with open(bdd, 'r') as sql_file:
        #     sql_script = sql_file.read()
        self.connection = sqlite3.connect(bdd)
        self.cursor = self.connection.cursor()

    def execute_requete(self,requete):
        results = []
        if type(requete) == tuple:
            for row in self.cursor.execute(requete[0],requete[1]):
                results.append(row)
        # return results
        else:
            for row in self.cursor.execute(requete):
                results.append(row)
        return results

    def execute_script(self,script):
        try:
            self.cursor.executescript(script)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print(e)
            print(dir(e))

    def executer_transaction(
        self, requetes: list[str], fermer_connection: bool = False
    ) -> bool:
        try:
            for requete in requetes:
                print(requete)
                res = self.execute_requete(requete)
                print(res)

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            self.connection.rollback()
            print(
                f"Erreur lors de l'execution de la transaction. "
                f"Celle-ci est annulée. "
                f"Erreur : {e}"
            )
            return False
        finally:
            if fermer_connection:
                self.connection.close()
        # return self.connection
