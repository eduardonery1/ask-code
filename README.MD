# Debug Helper Chatbot

This project is a chatbot that assists in debugging by leveraging answers from Stack Overflow. It uses a FastAPI backend with BigQuery for retrieving relevant answers and Google Vertex AI's Gemini model to generate responses. The frontend is built using Next.js.

## Features
- Retrieves relevant Stack Overflow answers for a given question.
- Uses Gemini AI to generate concise and informative responses.
- FastAPI backend with BigQuery integration.
- Next.js frontend for user interaction.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Node.js 18+
- Google Cloud SDK (for BigQuery access)
- Virtual environment (recommended)

### Backend Setup
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
   ```sh
   GEMINI_API_KEY=<path-to-your-gcp-credentials.json>
   DEBUG=True  # Set to False in production
   ```

5. Run the backend:
   ```sh
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

### Frontend Setup
1. Navigate to the frontend folder:
   ```sh
   cd frontend
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the development server:
   ```sh
   npm run dev
   ```

The frontend should now be accessible at `http://localhost:3000`.

## Running Tests
To run backend tests:
```sh
pytest test_main.py
```

## API Endpoints
### `POST /ask`
**Description:** Takes a programming-related question and returns a response based on Stack Overflow answers.

**Request Body:**
```json
{
  "question": "How to install numpy?"
}
```

**Response:**
```json
{
  "answer": "You can install numpy using pip: pip install numpy."
}
```

## Contributing
Feel free to submit issues or pull requests to improve this chatbot!

## License
MIT License


