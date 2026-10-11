# Restaurant Agent

An AI-powered restaurant assistant designed to help restaurants manage reservations, answer customer questions, suggest dishes, handle order flows, and improve service efficiency across digital channels.

## Overview

Restaurant Agent is a conversational application for restaurant operations. It can assist with:

- Table reservation requests and availability checks
- Customer FAQs about menu items, hours, and policies
- Dish recommendations based on preferences and dietary needs
- Order assistance and upsell suggestions
- Staff support for service coordination and repeat guest preferences

This project is intended to be a flexible foundation for an agent that can be connected to web chat, messaging apps, a website widget, or an internal staff dashboard.

## Features

- AI-powered restaurant conversations
- Reservation and booking workflow support
- Menu and dietary recommendation logic
- Custom business rules and service policies
- Multi-channel integration support
- Extensible backend for future automation and analytics
- Simple configuration via environment variables

## Architecture

The project is structured as a service-oriented application with an AI orchestration layer and a restaurant domain layer. The agent can:

1. Receive a customer request
2. Interpret intent and context
3. Validate restaurant policy and availability
4. Respond with a helpful, human-like answer or action
5. Log the interaction for monitoring and improvement

## Tech Stack

This project is designed to be adaptable and can be implemented with common web and AI tooling, including:

- Python
- FastAPI or Flask (if exposing API endpoints)
- OpenAI or another LLM provider
- PostgreSQL, SQLite, or another database for persistence
- Redis (optional, for caching/session state)
- Docker (optional, for deployment)

## Prerequisites

Before running this project, make sure you have:

- Python 3.10 or newer
- pip or poetry
- A valid LLM API key (for example, OpenAI)
- Access to a database if persistence is enabled

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-org/restaurant-agent.git
cd restaurant-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you are using Poetry:

```bash
poetry install
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the required settings:

```env
OPENAI_API_KEY=your_api_key_here
APP_ENV=development
HOST=0.0.0.0
PORT=8000
DATABASE_URL=sqlite:///restaurant_agent.db
```

You can also copy from a sample file if provided by the project:

```bash
cp .env.example .env
```

## Running the Application

Start the application with the project default command:

```bash
python app.py
```

Or, if the project exposes a web API:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

Once the app is running, you can interact with it through your configured interface, such as:

- A web app or dashboard
- A chat widget
- A REST API endpoint
- A messaging integration

Example requests may look like:

```http
POST /chat
Content-Type: application/json

{
  "message": "I want a table for two at 7:30 PM tonight.",
  "user_id": "customer-123"
}
```

Example response:

```json
{
  "response": "I can help with that. I see tables are available at 7:30 PM for two guests. Would you like me to reserve one?",
  "status": "success"
}
```

## Project Structure

```text
restaurant-agent/
├── app/
│   ├── api/
│   ├── agents/
│   ├── core/
│   ├── models/
│   ├── services/
│   └── utils/
├── data/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── app.py
└── docker-compose.yml
```

## Configuration

Common configuration values include:

- `OPENAI_API_KEY`: API key for model access
- `APP_ENV`: application environment (`development`, `staging`, `production`)
- `HOST` and `PORT`: runtime address configuration
- `DATABASE_URL`: storage backend connection string
- `LOG_LEVEL`: logging verbosity
