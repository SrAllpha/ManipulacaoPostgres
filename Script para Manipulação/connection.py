from ast import Expression
import psycopg2 as db
import csv

# Código para Manipulação em Banco de Dados Postgres
# Para uso, é necessária a troca das informações essenciais, expostas em comentários ao longo do código
# Código por: SrAllpha


# God Bless The World




class Config:
    def __init__(self):
        self.config = {
            'postgres': {

                'user': 'postgres',     # Nome do Usuário
                'password': 'postgres', # Senha
                'host': '127.0.0.1',    # Endereço do Banco Postgres
                'port': '5432',         # Porta de Conexão
                'database': 'py.db'     # Nome do Database

            }
        }


class Connection(Config):
    def __init__(self):
        Config.__init__(self)

        try:
            self.conn = db.connect(**self.config['postgres'])
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f'Could not connect to server', e)
            exit(1)

    def _enter_(self):
        return self

    def _exit_(self, ecx_type, exc_type, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.connection.commit()

    def fetchall(self):
        return self.cursor.fetchall()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

# Classe criada a fim de alterar a tabela 'Person'
# O nome da classe pode ser alterada para fins de boas práticas
# Em caso de mais campos, ou campos diferentes a 'name':
# É necessária a troca dos valores nas querys sql's do código, demarcadas com comentário:


class Person(Connection):
    def __init__(self):
        Connection.__init__(self)

    def insert(self, *args):
        try:
            sql = 'INSERT INTO person (name) VALUES (%s)'  # Query
            self.execute(sql, args)
            self.commit()

        except Exception as e:
            print('Error Inserting', e)

    def insert_csv(self, filename):
        try:
            data = csv.DictReader(open(filename, encoding='utf-8'))

            for row in data:
                self.insert(row["name"])  # Em caso de row diferente, trocar o nome e em caso de mais de uma: row[''], row['']
            print('Inserted Successfully')

        except Exception as e:
            print('Error inserting', e)

    def delete(self, id):
        try:
            sql_search = f'SELECT * FROM person WHERE id = {id}'  # Query

            if not self.query(sql_search):
                return 'Register Not Found to Delete'

            sql_delete = f'DELETE FROM person WHERE id = {id}'   # Query

            self.execute(sql_delete)
            self.commit()
            return 'Deleted Successfully'

        except Exception as e:
            print('Error deleting', e)

    def update(self, id, *args):
        try:
            sql = f'UPDATE person SET name = %s WHERE id = {id}'   # Query
            self.execute(sql, args)
            self.commit()
            print('Updated Successfully')

        except Exception as e:
            print('Error updating', e)

    def search(self, *args, type_s='Name'):

        sql = 'SELECT * FROM person WHERE name LIKE %s'    # Query

        if type_s == 'id':
            sql = 'SELECT * FROM person WHERE id = %s'     # Query

        data = self.query(sql, args)

        if data:
            return data

        return 'Register Not Found'


if __name__ == '__main__':       # A partir dessa linha, deve ser inseridos os scripts desejados para a manipulação do db.

    x = input('Search for: ')     # Exemplo de script para pesquisa no db.
    x = f'%{x}%'

    print(person.search(x))
