# cli-gpt-chat

This script enables CLI interaction with language models through LiteLLM. It supports conversational queries and maintains a history for context-aware responses.

### Requirements

-   An API key for language model providers like [OpenAI](https://platform.openai.com/account/api-keys) or [Anthropic](https://console.anthropic.com/settings/keys), set in `config.yaml` or as respective environment variables (e.g., `OPENAI_API_KEY`).
-   If using [Ollama](https://ollama.ai) models, ensure they are installed and configured as specified under `model_map` in `config.yaml`.

### Setup

1. Clone the repo: `git clone git@github.com:pahar0/cli-gpt-chat.git`.
2. Install dependencies: `pip install -r path/to/repo/cli-gpt-chat/requirements.txt`.
3. Make `gpt.py` executable: `chmod +x path/to/repo/cli-gpt-chat/gpt.py`.
4. Create a symlink: `sudo ln -sf path/to/repo/cli-gpt-chat/gpt.py /usr/local/bin/gpt`.
5. Refresh environment: `source ~/.bashrc`.
6. Use the command: `gpt <arguments>` anywhere in your terminal.

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

-   You may encounter a warning about protected namespaces due to the pydantic dependency. This warning can safely be ignored. Alternatively, you can eliminate the warning by downgrading the pydantic version using the following command:
    ```bash
    pip install pydantic==1.10.13
    ```
