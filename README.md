# quick-ai-chat-cli

This script enables CLI interaction with language models like GPT or Ollama though [LiteLLM](https://litellm.ai/). It supports conversational queries and maintains a history for context-aware responses.

### Requirements

-   [OpenAI API Key](https://platform.openai.com/account/api-keys): Set in `config.yaml` or as `OPENAI_API_KEY` environment variable.
-   [Ollama](https://ollama.ai): Install and configure if using Ollama models, specified under `model_map` in `config.yaml`.

### Setup

1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create an alias in `.bashrc`: `alias gpt="python ~/path/to/chat.py"`.
4. Source `.bashrc`: `source ~/.bashrc`.

## Configuration

-   `openai_api_key`: Your OpenAI API key. If not provided here, it must be set as an environment variable `OPENAI_API_KEY`.
-   `conversation_file`: Filename for storing the conversation history.
-   `conversation_expiry_hours`: The number of hours after which the conversation history is considered expired and will be reset.
-   `system_prompt`: Initial message from the system to start the conversation.
-   `model_map`: A mapping between short names and model identifiers. Include identifiers for OpenAI and any Ollama models you want to use.

## Usage

Use the `gpt` command followed by your question to activate the chat assistant. The `--engine` flag selects the model (default: OpenAI), and `--remove` clears history.

Examples:

```bash
gpt --engine ollama What is the theory of relativity?
```

```bash
gpt --remove Who discovered penicillin?
```

```bash
gpt What is the capital of Italy?
```

### Flags

-   `--engine`: Choose the language model (default `openai`).
-   `--remove`: Clear conversation history.

## Troubleshooting

-   If you installed the script in a virtual environment (venv), but the alias doesn't seem to work correctly, it might be due to the shell not having access to the virtual environment's libraries. To solve this, you can modify the alias to activate the virtual environment before running the script:
    ```bash
    alias gpt='source ~/path/to/venv/bin/activate && python ~/path/to/repo/chat.py'
    ```
-   You may encounter a warning about protected namespaces due to the pydantic dependency. This warning can safely be ignored. Alternatively, you can eliminate the warning by downgrading the pydantic version using the following command:
    ```bash
    pip install pydantic==1.10.13
    ```
