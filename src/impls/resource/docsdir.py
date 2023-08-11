import os
import shutil

from src.models.db import database
from src.models.embed import embed
from ...models.resource import manager


class DocsDirResouceManager(manager.ResourceManager):
    
    db: database.DatabaseManager
    emb: embed.EmbeddingProvider
    
    path: str='docs'
    
    def __init__(self, db: database.DatabaseManager, emb: embed.EmbeddingProvider, path: str, **kwargs):
        self.db = db
        self.emb = emb
        self.path = path
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
            print(f'Created directory {self.path}, please put your documents in it and run again.')
        
    def run(self):
        # 读取docs目录下的所有文件
        # 对每个文件进行embedding
        # 将embedding结果存入数据库
        
        for file in os.listdir(self.path):
            
            if not file.endswith('.md'):
                continue
            
            name = file[:-3]
            
            if self.db.exists(name):
                print(f'File {file} already exists in database, skipping...')
                continue
            
            text = ""
            
            with open(os.path.join(self.path, file), 'r', encoding="utf-8") as f:
                text = f.read()
            
            emb = self.emb.get_embedding(text)
            
            doc = dict(name=name, content=text, embedding=emb)
            
            self.db.store(doc)
            print(f'File {file} stored in database.')
        
        print('All files stored in database.')
        # print(self.db.select_all()[0])
        