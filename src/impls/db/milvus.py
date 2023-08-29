import logging

from pymilvus import connections, db, CollectionSchema, FieldSchema, DataType, Collection, utility

from ...models import entities
from ...models.db import database
from ...models.embedding import embedding
from ...control import factory


@factory.component(database.DatabaseManager, "milvus")
class MilvusDB(database.DatabaseManager):
    """Milvus database manager."""

    alias: str
    user: str
    password: str
    host: str
    port: str
    dbname: str

    doc_name: FieldSchema
    doc_key: FieldSchema
    doc_embedding: FieldSchema
    doc_content: FieldSchema
    doc_digest: FieldSchema

    collection_schema: CollectionSchema

    collection: Collection

    def __init__(self, user: str, password: str, host: str, port: str, emb: embedding.EmbeddingProvider, dbname: str, **kwargs):

        self.alias = kwargs.get("alias", "default")
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname

        self.__connect()

        if dbname not in db.list_database():
            db.create_database(dbname)
        db.using_database(dbname)

        # =====================Collection Schema=====================
        doc_name = FieldSchema(name="name", dtype=DataType.VARCHAR, is_primary=True)
        doc_key = FieldSchema(name="key", dtype=DataType.VARCHAR)
        doc_embedding = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=emb.get_dim())
        doc_content = FieldSchema(name="content", dtype=DataType.VARCHAR)
        doc_digest = FieldSchema(name="digest", dtype=DataType.VARCHAR)

        collection_schema = CollectionSchema(
            fields=[doc_name, doc_key, doc_embedding, doc_content, doc_digest],
            description="Collection for documents.",
            enable_dynamic_field=False
        )
        collection_name = "docs"
        # ===========================================================

        self.doc_name = doc_name
        self.doc_key = doc_key
        self.doc_embedding = doc_embedding
        self.doc_content = doc_content
        self.doc_digest = doc_digest

        self.collection_schema = collection_schema

        self.collection = Collection(name=collection_name, schema=collection_schema, using=self.alias)

    def __connect(self):
        
        connections.connect(
            alias=self.alias,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def store(self, docs: list[entities.Document]):
        name_list = []
        key_list = []
        embedding_list = []
        content_list = []
        digest_list = []

        for doc in docs:
            name_list.append(doc.name)
            key_list.append(doc.key)
            embedding_list.append(doc.embedding.tolist())
            content_list.append(doc.content)
            digest_list.append(doc.digest)

        self.collection.insert(
            [
                name_list,
                key_list,
                embedding_list,
                content_list,
                digest_list
            ]
        )

        self.collection.flush()

    def exists(self, name: str) -> bool:
        self.collection.load()

        res = self.collection.query(
            expr="name == '{}'".format(name),
            offset=0,
            limit=1,
            output_fields=["name"]
        )

        return len(res) > 0
    
    def check(self, name: str, digest: str) -> bool:
        self.collection.load()

        res = self.collection.query(
            expr="name == '{}'".format(name),
            offset=0,
            limit=1,
            output_fields=["name", "digest"]
        )

        if len(res) == 0:
            return False
        
        return res[0].digest == digest
    
    def delete(self, name: str):
        self.collection.delete(
            expr="name == '{}'".format(name)
        )
