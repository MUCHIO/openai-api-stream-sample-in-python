# openai-api-stream-sample-in-python

A sample project demonstrating streaming responses using the OpenAI Assistants API. It displays real-time streaming for mathematical problem-solving.

This sample is based on the [OpenAI Assistants API Quickstart](https://platform.openai.com/docs/assistants/quickstart?lang=python).

## Features

- Interactive chat using OpenAI Assistants API
- Real-time streaming responses
- Mathematical calculations with Code Interpreter tool
- Step-by-step response display with event handlers

## Requirements

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key

## Setup

### 1. Sync Dependencies

```bash
uv sync
```

### 2. Environment Variables Setup

Copy the template file and set your OpenAI API key:

```bash
cp .env.org .env
```

Then edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## How to Run

### Run with uv environment

```bash
uv run python stream.py
```

Or activate the uv environment and then run:

```bash
# Activate uv environment
source .venv/bin/activate

# Run the program
python stream.py
```

## Usage

1. When you run the program, a thread with OpenAI Assistant is automatically created
2. By default, the question "I need to solve the equation `3x + 11 = 14`. Can you help me?" is sent
3. The Assistant's response is displayed in real-time streaming
4. Code Interpreter executes mathematical calculations and displays the process

## Project Structure

```
.
├── stream.py          # Main program
├── pyproject.toml     # Project configuration and dependencies
├── uv.lock           # Dependencies lock file
├── README.md         # This file
├── .env.org          # Environment variables template
└── .env              # Environment variables (to be created from .env.org)
```

## Dependencies

- `openai>=1.88.0` - OpenAI Python SDK
- `python-dotenv>=1.1.0` - Environment variable management

## Notes

- Store your OpenAI API key in the `.env` file and do not commit it to Git
- Running the program will incur OpenAI API usage charges
- Change the Assistant ID to an actual existing one

## Troubleshooting

### API Key Error
```
ValueError: OPENAI_API_KEY environment variable is not set
```
→ Check if the OpenAI API key is correctly set in the `.env` file

### Assistant ID Error
→ Change the `assistant_id` in `stream.py` to a valid Assistant ID