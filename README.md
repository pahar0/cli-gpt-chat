# cli-gpt-chat

This script enables CLI interaction with language models through LiteLLM. It supports conversational queries and maintains a history for context-aware responses.

### Requirements

-   An API key for language model providers like [OpenAI](https://platform.openai.com/account/api-keys) or [Anthropic](https://console.anthropic.com/settings/keys), set in `config.yaml` or as respective environment variables (e.g., `OPENAI_API_KEY`).
-   If using [Ollama](https://ollama.ai) models, ensure they are installed and configured as specified under `model_map` in `config.yaml`.

### Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Create an alias in `.bashrc`: `alias gpt="python ~/path/to/chat.py"`.
4. Source `.bashrc`: `source ~/.bashrc`.

## Configuration

-   `api_keys`: Specify your API keys for providers like OpenAI and Anthropic. If not directly provided, set them as environment variables.
-   `conversation_file`: Designate a file to save conversation history, aiding in context awareness.
-   `conversation_expiry_hours`: Set the duration after which the conversation history expires and resets.
-   `system_prompt`: Define the initial system message to start conversations.
-   `model_map`: Map provider names to their respective models and base URLs for API requests.
-   `default_provider`: Set your default language model provider.
-   `debug`: Enable or disable debug mode for additional log information.

## Usage

Use the `gpt` command followed by your question to activate the chat assistant. The `-p` or `--provider` flag selects the provider (default: OpenAI), and `-d` or `--delete` clears conversational history.

Examples:

```bash
gpt -p ollama What is the theory of relativity?
```

```bash
gpt -d Who discovered penicillin?
```

```bash
gpt What is the capital of Italy?
```

### Flags

-   `-p` or `--provider`: Choose the provider. (default `openai`).
-   `-d` or `--delete`: Clear conversation history.

## Troubleshooting

-   If you installed the script in a virtual environment (venv), but the alias doesn't seem to work correctly, it might be due to the shell not having access to the virtual environment's libraries. To solve this, you can modify the alias to activate the virtual environment before running the script:
    ```bash
    alias gpt='source ~/path/to/venv/bin/activate && python ~/path/to/repo/chat.py'
    ```
-   You may encounter a warning about protected namespaces due to the pydantic dependency. This warning can safely be ignored. Alternatively, you can eliminate the warning by downgrading the pydantic version using the following command:
    ```bash
    pip install pydantic==1.10.13
    ```
