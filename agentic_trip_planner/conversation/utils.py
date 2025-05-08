from openai import OpenAI
from yaml import safe_load

MODEL = "gpt-4.1-nano"
PROMPT_PATH = 'agentic_trip_planner/conversation/config/prompt.yaml'
PROMPT_NAME = "trip_planner"


def load_prompt(path: str, prompt_name: str):
    """Load the configuration file."""
    with open(path, 'r') as file:
        config = safe_load(file)
    
    prompt = config.get(prompt_name)

    if prompt is None:
        raise ValueError(f"Prompt '{prompt_name}' not found in the configuration file.")
    return prompt


def make_request(client: OpenAI, prompt: list[dict], previous_response: str | None = None):
    """Make a request to the OpenAI API."""
    response = client.responses.create(
        model=MODEL,
        input=prompt,
        previous_response_id=previous_response,
    )
    return response


def format_user_question(question: str):
    """Format the user question for the prompt."""
    return {"role": "user", "content": question}



if __name__ == "__main__":
    # Example usage
    system_prompt = load_prompt(PROMPT_PATH, PROMPT_NAME)
    client = OpenAI()

    user_question = "What are the best places to visit in Paris?"

    prompt = [system_prompt, {"role": "user", "content": user_question}]
    response = make_request(client, prompt)

    print(f"Response from OpenAI API: {response.output_text}")

    user_question_2 = format_user_question("Tell me who you are?")
    response2 = make_request(client, [user_question_2], response.id)
    print(response2.output_text)

