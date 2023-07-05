from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from textblob import TextBlob
from dotenv import load_dotenv
import os
import openai

load_dotenv()
api_key = os.environ['API_KEY']
base_url = os.getenv("BASE_URL")

app = FastAPI()

# Set your OpenAI API key
openai.api_key = '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'


class Message(BaseModel):
    message: str
    user_name: str
    is_questionnaire: bool = False
    questionnaire: dict = {}


async def chat_with_gpt(message: str, temperature: float):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Specify the OpenAI engine
            prompt=message,
            temperature=temperature,
            max_tokens=100,  # Adjust the max tokens as per your requirement
        )
        return response.choices[0].text.strip()

    except Exception as exc:
        error_message = f"Failed to communicate with the OpenAI API: {str(exc)}"
        raise HTTPException(status_code=500, detail=error_message)


async def process_user_input(message: str, user_name: str = "User"):
    # Provide friendly replies and emotional support based on user input
    positive_triggers = ["thank", "happy", "good", "great"]
    negative_triggers = ["sad", "lonely", "depressed", "anxious"]

    if any(trigger in message.lower() for trigger in positive_triggers):
        # User expressed positive emotions
        return f"I'm glad to hear that, {user_name}! Is there anything specific you'd like to talk about?"

    if any(trigger in message.lower() for trigger in negative_triggers):
        # User expressed negative emotions
        return f"I'm here to listen and support you, {user_name}. Remember, you're not alone in this. Would you like to share more about what you're going through?"

    # Default friendly response
    return f"I'm here to chat and support you, {user_name}. Feel free to share anything on your mind."


@app.post("/chat")
async def chat(message: Message):
    if message.is_questionnaire:
        response = await process_questionnaire(message.message)
    else:
        response = await process_user_input(message.message, message.user_name)

    return {"response": response}


async def process_questionnaire(message: str):
    # Define the questionnaire questions and options
    questionnaire = {
        "depression": {
            "questions": [
                "Have you been feeling sad, down, or hopeless?",
                "Have you lost interest or pleasure in activities you used to enjoy?",
                "Have you been experiencing changes in appetite or weight?",
            ],
            "options": ["Yes", "No"],
        },
        "anxiety": {
            "questions": [
                "Have you been feeling excessively worried or anxious?",
                "Have you been experiencing restlessness or irritability?",
                "Have you been having trouble sleeping or staying asleep?",
            ],
            "options": ["Yes", "No"],
        },
        "ptsd": {
            "questions": [
                "Have you been having distressing thoughts or memories about a past traumatic event?",
                "Have you been avoiding situations or activities that remind you of the trauma?",
                "Have you been experiencing heightened arousal, such as being easily startled or having difficulty concentrating?",
            ],
            "options": ["Yes", "No"],
        },
    }

    # Process the questionnaire responses
    response = message.lower().strip()
    if response in ["yes", "no"]:
        if response == "yes":
            # User answered "Yes" to at least one question
            return "Based on your responses, it's important to seek professional help. We recommend contacting a mental health professional for further assistance."
        else:
            # User answered "No" to all questions
            return "It seems like you are not currently experiencing significant symptoms. However, if you have any concerns, it's always a good idea to reach out to a mental health professional for support."
    else:
        # Invalid response
        return "Please respond with 'Yes' or 'No' to the questionnaire."


def analyze_sentiment(message: str):
    blob = TextBlob(message)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score


@app.post("/feedback")
async def submit_feedback(feedback: str):
    # Store feedback in a database or log file
    # You can also perform sentiment analysis on the feedback
    # and use it to improve the chatbot

    # Return a success message
    return {"message": "Feedback submitted successfully."}

@app.route("/")
def main():
    return "Hello World!"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
