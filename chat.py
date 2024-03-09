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


def update_conversation(conversation, reply, model_used):
    conversation["messages"].append({"role": "assistant", "content": reply})
    conversation["last_message_time"] = datetime.datetime.now().isoformat()
    conversation["model_used"] = model_used
    try:
        with open(CONVERSATION_FILE, "w") as f:
            json.dump(conversation, f, indent=2)
    except FileNotFoundError:
        return print("Error: Could not save conversation file.")


def stream_chat_completions(conversation, question, provider, model):
    conversation["messages"].append({"role": "user", "content": question})
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]

    try:
        api_key = cfg["api_keys"][provider] if provider in cfg["api_keys"] else None
        full_model = f"{provider}/{model}"
        response = completion(model=full_model, messages=messages, stream=True, base_url=cfg["model_map"][provider]["base_url"], api_key=api_key, logger_fn=print if cfg["debug"] else None)
        if cfg["debug"]:
            print(f"Using: {full_model}")
        full_reply = handle_stream_response(response)
        update_conversation(conversation, full_reply, full_model)

    except Exception as e:
        print(f"{type(e).__name__} Error: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Use this script to interact with the OpenAI, Anthropic or Ollama models in streaming mode.")
    parser.add_argument("question", type=str, nargs="*", default=[], help="Type the question you want to ask the LLM model.")
    parser.add_argument("-p", "--provider", type=str, help="The provider to use for completion. Supported providers are: " + ", ".join(cfg["model_map"].keys()) + ".")
    parser.add_argument("-d", "--delete", action="store_true", help="If specified, the previous conversation file will be deleted before the new conversation.")

    args = parser.parse_args()

    if args.delete and os.path.exists(CONVERSATION_FILE):
        os.remove(CONVERSATION_FILE)

    if args.question:
        question = " ".join(args.question)
        conversation = load_conversation()
        provider = args.provider if args.provider else conversation["model_used"].split("/")[0] if conversation.get("model_used") else cfg["default_provider"]
        model = cfg["model_map"][provider]["model"] if args.provider else conversation["model_used"].split("/")[1] if conversation.get("model_used") else cfg["model_map"][provider]["model"]

        if provider not in cfg["model_map"]:
            print(f"Error: Unsupported provider: {provider}. Supported providers are: {', '.join(cfg['model_map'].keys())}.")
            return

        if provider in cfg["api_keys"]:
            key_env_var = f"{provider.upper()}_API_KEY"
            if not cfg["api_keys"][provider] and not os.environ.get(key_env_var):
                print(f"Error: No {provider.capitalize()} API key found. Please set the {key_env_var} environment variable.")
                return

        stream_chat_completions(conversation, question, provider, model)
    elif not args.delete:
        print("No arguments provided.")
        parser.print_help()


if __name__ == "__main__":
    main()
