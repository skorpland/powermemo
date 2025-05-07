### [0.0.32] - unreleased

**Added**

- `docs`: Locomo benchmark of Powermemo,mem0, zep, langmem
- `feat`: Update algorithms for temporal memory

**Changed**

- 

**Fixed**

- OpenAI LLM and Embedding usage logging bugs

### [0.0.31] - 2025/4/28

**Added**

- `config`: add embedding config. [doc](https://docs.powermemo.io/references/full#embedding-configuration)

- `feature`: add OpenAI embedding

- `feature`: add Jina embedding

- `feature`: add Event Search. [doc](https://docs.powermemo.io/features/event/event_search)

- `feature`: add Profile filter. [doc](https://docs.powermemo.io/features/profile/profile_filter)

  

**Changed**

- Python SDK update to date
- Add Examples Documents with Livekit, Ollama and OpenAI

**Fixed**

- Multi-replica telemetry bugs



### [0.0.30] - 2025/4/14

**Added**

- Add [profile validation](https://docs.powermemo.io/features/profile/profile_config): Powermemo will further validate the extracted profile value to remove unwant results.
- Add [Event Tags](https://docs.powermemo.io/features/event/event_tag): This feature allows you to design the attributes of each user event, like `emotion`, `goal`.
- Add summary model option for event summary tasks
- Add type validation for `config.yaml`

**Changed**

- Reorganized `docs/site` website 

**Fixed**

- Add meaningless profile slot detection.

  

### [0.0.29] - 2025/3/21

**Added**

- Add Event Summary
- Add x-code-example for APIs
- Add profile strict mode

**Changed**

- Reorganized `docs/site` website 

**Fixed**