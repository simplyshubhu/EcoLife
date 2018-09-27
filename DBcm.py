import mysql.connector as connector


class ConnectionError(Exception):
    pass


class CredentialError(Exception):
    pass


class SQLError(Exception):
    pass


class UseDatabase:
    def __init__(self, config: dict)-> None:
        self.configuration = config

    def __enter__(self):
        try:
            self.con = connector.connect(**self.configuration)
            self.cursor = self.con.cursor()
            return self.cursor
        except connector.errors.InterfaceError as err:
            raise(ConnectionError(err))
        except connector.errors.ProgrammingError as err:
            raise(CredentialError(err))

    def __exit__(self, exc_type, exc_val, exc_tb)-> None:
        self.con.commit()
        self.cursor.close()
        self.con.close()
        if exc_type is connector.errors.ProgrammingError:
            raise SQLError(exc_val)
        elif exc_type:
            raise exc_type(exc_val)
