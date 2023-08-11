# llm-embed-qa

Question answering system built with vector dbs and LLMs.

> Part of the content is implemented with reference to [michaelliao/llm-embedding-sample](https://github.com/michaelliao/llm-embedding-sample)

## Requirements (Default Component)

- Python 3.10
- Docker

## Install

1. Clone this repo
2. Install requirements with `pip install -r requirements.txt`
3. Startup PostgreSQL with Docker

    ```bash
    docker run -d \
       --rm \
       --name pgvector \
       -p 5432:5432 \
       -e POSTGRES_PASSWORD=password \
       -e POSTGRES_USER=postgres \
       -e POSTGRES_DB=postgres \
       -e PGDATA=/var/lib/postgresql/data/pgdata \
       -v /path/to/llm-embedding-sample/pg-data:/var/lib/postgresql/data \
       -v /path/to/llm-embedding-sample/pg-init-script:/docker-entrypoint-initdb.d \
       ankane/pgvector:latest
    ```

    **NOTE: replace /path/to/... with real path.**

4. Run `python main.py`, edit `config.yaml` to set your `api_key` of OpenAI.
5. Put your `markdown` format documents in `docs` folder.
    - There are the wiki files of [QchatGPT](https://github.com/RockChinQ/QChatGPT) in `docs_examples` folder.
6. Run `python main.py` again, it will automatically build the vector database and start the server.

## Usage

`GET /ask?content=<question>`
