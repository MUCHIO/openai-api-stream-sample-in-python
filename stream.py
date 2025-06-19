from openai import OpenAI
from dotenv import load_dotenv
import os

# Define schema for structured output
math_solution_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "math_solution",
        "schema": {
            "type": "object",
            "properties": {
                "equation": {
                    "type": "string",
                    "description": "The original equation to solve"
                },
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "step_number": {"type": "integer"},
                            "description": {"type": "string"},
                            "equation": {"type": "string"}
                        },
                        "required": ["step_number", "description", "equation"],
                        "additionalProperties": False
                    }
                },
                "final_answer": {
                    "type": "object",
                    "properties": {
                        "variable": {"type": "string"},
                        "value": {"type": "number"}
                    },
                    "required": ["variable", "value"],
                    "additionalProperties": False
                },
                "verification": {
                    "type": "string",
                    "description": "Verification by substituting the answer back into the original equation"
                }
            },
            "required": ["equation", "steps", "final_answer", "verification"],
            "additionalProperties": False
        },
        "strict": True
    }
}

client = OpenAI()

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
client.api_key = api_key

assistant = client.beta.assistants.create(
  name="Math Tutor",
  instructions="You are a personal math tutor. Solve math equations step by step and provide the solution in the specified structured format.",
  tools=[{"type": "code_interpreter"}],
  model="gpt-4o-mini",  # Structured outputs require specific model versions
  response_format=math_solution_schema
)
print(f"assistant.id={assistant.id}", flush=True)

thread = client.beta.threads.create()
print(f"thread.id={thread.id}", flush=True)

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me solve it step by step?"
)

from typing_extensions import override
from openai import AssistantEventHandler

# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)

# Then, we use the `stream` SDK helper
# with the `EventHandler` class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account. Provide a detailed step-by-step solution.",
    event_handler=EventHandler(),
) as stream:
    stream.until_done()
