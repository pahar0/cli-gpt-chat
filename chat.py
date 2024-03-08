import os
import argparse
import json
import datetime
import yaml
from litellm import completion

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.safe_load(ymlfile)

CONVERSATION_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), cfg["conversation_file"])


def load_conversation():
    try:
        with open(CONVERSATION_FILE, "r") as f:
            conversation = json.load(f)
            last_message_time = conversation.get("last_message_time")
            if last_message_time:
                last_message_datetime = datetime.datetime.fromisoformat(last_message_time)
                if datetime.datetime.now() - last_message_datetime >= datetime.timedelta(hours=cfg["conversation_expiry_hours"]):
                    return {"messages": [{"role": "system", "content": cfg["system_prompt"]}]}
            return conversation
    except FileNotFoundError:
        return {"messages": [{"role": "system", "content": cfg["system_prompt"]}]}


def handle_stream_response(response):
    full_reply = ""
    for chunk in response:
        new_content = ""
        if hasattr(chunk, "choices") and chunk.choices:
            new_content = chunk.choices[0].delta.content if chunk.choices[0].delta else ""
        elif isinstance(chunk, dict) and "choices" in chunk and chunk["choices"][0]["delta"]:
            new_content = chunk["choices"][0]["delta"]["content"]

        if new_content:
            print(f"\033[1m\033[93m{new_content}\033[0m", end="", flush=True)
            full_reply += new_content

    print()
    return full_reply


def update_conversation(conversation, reply):
    conversation["messages"].append({"role": "assistant", "content": reply})
    conversation["last_message_time"] = datetime.datetime.now().isoformat()
    try:
        with open(CONVERSATION_FILE, "w") as f:
            json.dump(conversation, f, indent=2)
    except FileNotFoundError:
        return print("Error: Could not save conversation file.")


def stream_chat_completions(question, engine="openai"):
    if engine in ["anthropic", "openai"]:
        key_env_var = f"{engine.upper()}_API_KEY"
        if not cfg.get(f"{engine}_api_key") and not os.getenv(key_env_var):
            print(f"Error: No {engine.capitalize()} API key found. Please set the {key_env_var} environment variable.")
            return

    conversation = load_conversation()
    conversation["messages"].append({"role": "user", "content": question})
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]

    try:
        if engine in cfg["model_map"]:
            model = f"{engine}/{cfg['model_map'][engine]['model']}" if engine == "ollama" else cfg["model_map"][engine]["model"]
            api_key = cfg["openai_api_key"] if engine == "openai" else cfg["anthropic_api_key"] if engine == "anthropic" else None
            response = completion(model=model, messages=messages, stream=True, base_url=cfg["model_map"][engine]["base_url"], api_key=api_key)
            full_reply = handle_stream_response(response)
            update_conversation(conversation, full_reply)
        else:
            print("Unsupported engine.")

    except Exception as e:
        print(f"{type(e).__name__} Error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Use this script to interact with the OpenAI GPT model or any Ollama model in streaming mode. You can ask a question or remove the conversation file.")
    parser.add_argument("question", type=str, nargs="*", default=[], help="Type the question you want to ask the LLM model.")
    parser.add_argument("--engine", type=str, default="openai", choices=[model for model in cfg["model_map"]], help="The engine to use for the conversation.")
    parser.add_argument("--remove", action="store_true", help="If specified, the previous conversation file will be removed before the new conversation.")

    args = parser.parse_args()

    if args.remove and os.path.exists(CONVERSATION_FILE):
        os.remove(CONVERSATION_FILE)

    if args.question:
        question = " ".join(args.question)
        stream_chat_completions(question, engine=args.engine)
    elif not args.remove:
        print("No arguments provided.")
        parser.print_help()


if __name__ == "__main__":
    main()
