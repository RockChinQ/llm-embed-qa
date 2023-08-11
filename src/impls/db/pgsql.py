import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector


from ...models.db import database


class PGSQLAdapter(database.DatabaseManager):
    
    conn = None
    
    dbname = None
    user = None
    password = None
    host = None
    port = None
    
    def __init__(self, dbname: str, user: str, password: str, host: str, port: int, **kwargs):
        
        self.conn = psycopg2.connect(
            database=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        
        register_vector(self.conn)
        
    def store(self, data: dict):
        sql = "INSERT INTO docs (name, content, embedding) VALUES (%s, %s, %s) RETURNING id"
        
        cursor = self.conn.cursor()
        
        cursor.execute(sql, (data['name'], data['content'], data['embedding']))
        
        data['id'] = cursor.fetchone()[0]
        
        self.conn.commit()
    
    def exists(self, name: str) -> bool:
        sql = "SELECT COUNT(*) as count FROM docs WHERE name = %s"
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(sql, (name,))
        
        return cursor.fetchone()['count'] > 0
    
    def select_all(self):
        sql = "SELECT id, name, content, embedding FROM docs ORDER BY id"
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(sql)
        
        return cursor.fetchall()

    def db_conn(self):
        conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            database=self.dbname,
            host=self.host,
            port=self.port
        )
        register_vector(conn)
        return conn

    def get(self, embedding: np.array) -> list:
        
        sql = "SELECT id, name, content, embedding <=> %s AS distance FROM docs ORDER BY embedding <=> %s LIMIT 3"
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        sql_stat = cursor.mogrify(sql, (embedding, embedding,))
        
        cursor.execute(sql_stat)
        
        return cursor.fetchall()
