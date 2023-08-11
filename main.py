import os
import yaml
import shutil
import threading

import flask, flask_cors
import openai

from src.impls.db import pgsql
from src.impls.llm import openaigpt
from src.impls.embed import openaiemb
from src.impls.resource import docsdir


def main():
    # 检查config.yaml是否存在
    if not os.path.exists('config.yaml'):
        shutil.copy('config-template.yaml', 'config.yaml')
        print('config.yaml created, please edit it before running again')
        return
    
    cfg: dict = {}
    
    # 读取config.yaml
    with open('config.yaml', 'r', encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        
    openai.api_key = cfg['openai']['api_key']

    pgsqldb = pgsql.PGSQLAdapter(
        **cfg['database'][0]
    )
    
    emb = openaiemb.OpenAIEmbedding(
        **cfg['embedding'][0]
    )
    
    llm = openaigpt.OpenAIGPT(
        **cfg['llm'][0]
    )

    resource = docsdir.DocsDirResouceManager(
        db=pgsqldb,
        emb=emb,
        **cfg['resource'][0]
    )
    
    thread = threading.Thread(target=resource.run)
    thread.start()
    
    app = flask.Flask(__name__)
    flask_cors.CORS(app)
    
    @app.route("/ask")
    def ask():
        content = flask.request.args.get('content')
        
        prompt_string = cfg['prompt']
        embedding = emb.get_embedding(content)
        
        docs = pgsqldb.get(embedding)
        
        if len(docs) > 1:
            
            docstring = "\n\n".join([doc['content'] for doc in docs])
            
            prompt_string += cfg['guide'] % docstring
        else:
            print('No docs found, skipping...')
        
        messages = [
            {
                "role": "system",
                "content": prompt_string
            },
            {
                "role": "user",
                "content": content
            }
        ]
        
        resp = llm.ask(messages)
        
        return flask.jsonify(
            {
                'message': resp,
            }
        )
    
    app.run(
        **cfg['server']
    )
    
if __name__ == '__main__':
    main()