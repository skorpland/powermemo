<div align="center">
    <a href="https://powermemo.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://assets.memodb.io/powermemo-dark.svg">
      <img alt="Shows the Powermemo logo" src="https://assets.memodb.io/powermemo-light.svg" width="424">
    </picture>
  </a>
  <p><strong>The server-side of Powermemo</strong></p>
  <p>
    <img src="https://img.shields.io/github/v/tag/skorpland/powermemo">
  </p>
</div>




## Get started

### Setup

[**config.yaml**](https://docs.powermemo.io/references/full)

Powermemo uses a single  `config.yaml` to initialize the server. It contains the configs of:

- LLM: `llm_base_url`, `llm_api_key`, `best_llm_model`,...
- Embedding: `enable_event_embedding`, `embedding_api_key`...
- Memory: `max_pre_profile_token_size`, `max_profile_subtopics`, `additional_user_profiles`...

By default, Powermemo enables user profile and event memory with filter ability. That means running a Powermemo server requires you to have below things:

- **LLM API**: You must fill the OpenAI API Key in `llm_api_key` of `config.yaml`.Or you can change `llm_base_url` to any OpenAI-SDK-Compatible service(via [vllm](https://github.com/vllm-project/vllm), [Ollama](../../assets/tutorials/ollama+powermemo/readme.md),...). Alternatively, you can set `llm_api_key` and `llm_base_url` using environment variables `POWERMEMO_LLM_API_KEY` and `POWERMEMO_LLM_BASE_URL`
- **Embedding API**: Powermemo supports OpenAI-Compatible SDK and [Jina Embedding](https://jina.ai/models/jina-embeddings-v3/). Powermemo uses embedding API to retrieve related user events. If you don't have a embedding API, you can set `enable_event_embedding: false` in `config.yaml`

We have some example `config.yaml` in `examplel_config`:

- [`profile_for_assistant`](./api/example_config/profile_for_education),  [`profile_for_education`](./api/example_config/profile_for_education),  [`profile_for_companion`](./api/example_config/profile_for_companion)  are three similar configs in term of structure, but for different user cases.
- [`event_tag`](./api/example_config/event_tag) is a feature to tracking temporal attributes of users. [doc](https://docs.powermemo.io/features/event/event_tag)
- [`only_strict_profile`](./api/example_config/only_strict_profile): disable all other features, only collect the profiles you design.
- [`jina_embedding`](./api/example_config/jina_embedding) uses Jina exmbedding for event search.



**environment variables**

Check `./.env.example` for necessary vars. You can configure the running port and access token in here.  Also, anything in `config.yaml` can be override in env([doc](https://docs.powermemo.io/references/full#environment-variable-overrides)), just starts with `POWERMEMO_`

### Launch

1. Make sure you have [docker-compose](https://docs.docker.com/compose/install/) installed.

2. Prepare the configs:

   ```bash
   cd src/server
   cp .env.example .env
   cp ./api/config.yaml.example ./api/config.yaml
   ```

   1. `.env` contains the service configs, like running port, secret token...
   2. `config.yaml` contains the Powermemo configs, like LLM model, profile slots. [docs](https://docs.powermemo.io/references/full)

3. Run `docker-compose build && docker-compose up` to start the services.

Check out the [docs](https://docs.powermemo.io/quickstart) of how to use Powermemo client or APIs.



## Use Powermemo core only

1. If you have existing postgres and reids, you can only launch the Powermemo core

2. Find and download the docker image of Powermemo:

   ```bash
   docker pull ghcr.io/skorpland/powermemo:latest
   ```

3. Setup your `config.yaml` and an `env.list` file, the `env.list` should look like [this](./api/.env.example):

4. Run the service:
   ```bash
   docker run --env-file env.list -v ./api/config.yaml:/app/config.yaml -p 8019:8000 ghcr.io/skorpland/powermemo:main
   ```



## Development

1. Start a local DB first by `sh script/up-dev.sh`
2. Open a new terminal window and `cd ./api`
3. Install python deps: `pip install -r requirements.txt`
4. To test if you got everything right, run `pytest` to see if all the tests are passed.
5. Launch Powermemo Server in dev mode: `fastapi dev --port 8019`

> `fastapi dev` has hot-reload, so you can just modify the code and test it without relaunch the service.



## Migrations

Powermemo may introduce breaking changes in DB schema, here is a guideline of how to migrate your data to latest Powermemo:

1. Install `alembic`: `pip install alembic`

2. Modify `./api/alembic.ini`. Find the field called `sqlalchemy.url` in `alembbic.ini`, change it to your Postgres DB of Powermemo

3. Run below commands to prepare the migration plan:

   ```bash
   cd api
   mkdir migrations/versions
   alembic upgrade head
   alembic revision --autogenerate -m "powermemo changes"
   ```

4. ⚠️ Run the command `alembic upgrade head` again to migrate your current Powermemo DB to the latest one.
