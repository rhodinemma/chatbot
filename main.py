from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
import uvicorn


load_dotenv()
api_key = os.environ['API_KEY']
base_url = os.getenv("BASE_URL")

app = FastAPI()
@app.get("/")
def read_root():
    return "Hello, am your virtual friend"

# Set your OpenAI API key
openai.api_key = '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'


class Message(BaseModel):
    message: str
    user_name: str
    is_questionnaire: bool = False

@app.get("/ask-user-name")
def ask_for_user_name():
    user_name = input("Hey!! What is your name?\n ")
    return f"Nice to meet you, { user_name}"

@app.get("/ask-chatbot-name")
def ask_for_chatbot_name():
    chatbot_name = input("What would you like to call me?\n ")
    return f"{chatbot_name} is a nice name. Thank you!"
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
        error_message = f"Failed to communicate with chatbot: {str(exc)}"
        raise HTTPException(status_code=500, detail=error_message)

# Uganda Mental Health Hotlines
mental_health_hotlines = {
    "Uganda Helpline": "+256 200 110200",
    "Mental Health Uganda": "+256 775 951543",
    "Butabika National Referral Hospital": "+256 414 505 000"
}

async def process_user_input(message: str, user_name: str = "User"):
    # Define the triggers for different emotions
    positive_triggers = ["amazing", "happy", "good", "great", "happy", "better", "hope", "excited"]
    negative_triggers = ["sad", "lonely", "depressed", "anxious", "stressed", "I feel stuck and helpless.", "I'm such a failure."]
    neutral_triggers = ["do not belong", "kill myself", "die", "end it", "There's no point in living anymore",  "Everyone would be better off without me" , "There's no escape from this pain","I can't see any way out of this.", "I can't take it anymore",  "I wish I could just disappear."]
    topic_triggers = ["favorite color", "i want to cry", "sorry", "hello","how are you", "hi", "hey" "weather", "music","okay", "food", "hobby", "weekend plans", "movie", "book", "travel", "pet", "sport", "dream", "goal", "inspire", "family", "friend", "work", "school", "vacation"]
    greet_trigger=["hey"]+["hello"]+["hi"]+["whatsup"]+["yoo"]+["gwe"]
    if any(trigger in message.lower() for trigger in positive_triggers):
        # User expressed positive emotions
        return f"I'm glad to hear that, {user_name}! Is there anything else i can help you with?"

    if any(trigger in message.lower() for trigger in neutral_triggers):
        # User expressed negative emotions
        response = f"I'm here to listen and support you, {user_name}. If you need immediate assistance, you can reach out to the following mental health hotlines in Uganda:\n\n"
        
        for contact, phone_number in mental_health_hotlines.items():
            response += f"{contact}: {phone_number}\n"
        
        response += "\nAdditionally, here are some useful mental health resources and organizations:\n"
        response += "- Mental Health Uganda: [Website](https://www.mentalhealthuganda.org/)\n"
        response += "- Butabika National Referral Hospital: [Website](https://www.butabikahospital.com/)\n"

        response += "\nIf you have any specific concerns or questions, feel free to ask."
        return response
    if any(trigger in message.lower() for trigger in greet_trigger):
        return f"Hi! Whatsup,{user_name}?"

    if any(trigger in message.lower() for trigger in negative_triggers):
        # User expressed neutral emotions
        return f"Feel free to share, {user_name}. Am a good listener"

    if any(trigger in message.lower() for trigger in topic_triggers):
        # Respond to specific topic-related triggers
        if "favorite color" in message.lower():
            return f"My favorite color is blue."
        if "i want to cry" in message.lower():
            return f"Oh sorry {user_name}, what's wrong?"
        
        if "sorry" in message.lower():
            return f"No problem, it's ok."
             
        #if ("hello"| "hey") in message.lower():
        #    return f"Hello, how are you,{user_name}?"
        
        if "weather" in message.lower():
            return f"I am not sure! What's the weather like where you are, {user_name}?"
   
        
        if"how are you" in message.lower():
            return f"Am fine, you?"
        
        if "music" in message.lower():
            return f"I love listening to music! What's your favorite genre of music, {user_name}?"
        
        if "okay" in message.lower():
            return f"What are you doing?"
        
        if "food" in message.lower():
            return f"I enjoy trying different cuisines. What's your favorite dish, {user_name}?"

        if "hobby" in message.lower():
            return f"I have many hobbies, but one of my favorites is reading. What's your favorite hobby, {user_name}?"

        if "weekend plans" in message.lower():
            return f"I'm looking forward to relaxing over the weekend. Do you have any exciting plans, {user_name}?"

        if "movie" in message.lower():
            return f"I enjoy watching movies! What's your favorite movie, {user_name}?"

        if "book" in message.lower():
            return f"I'm an avid reader. Do you have a favorite book, {user_name}?"

        if "travel" in message.lower():
            return f"I love learning about new places! Where is your dream travel destination, {user_name}?"

        if "pet" in message.lower():
            return f"Pets are wonderful companions! Do you have a pet, {user_name}?"

        if "sport" in message.lower():
            return f"I enjoy playing and watching sports! What's your favorite sport,{user_name}?"

        if "dream" in message.lower():
            return f"Dreams are powerful! What is your biggest dream, {user_name}?"

        if "goal" in message.lower():
            return f"Setting goals can help you achieve great things! What is one of your current goals, {user_name}?"

        if "inspire" in message.lower():
            return f"Inspiration is everywhere! Is there someone or something that inspires you, {user_name}?"

        if "family" in message.lower():
            return f"Family is important. Tell me something about your family, {user_name}."

        if "friend" in message.lower():
            return f"Friends make life more meaningful. Do you have a close friend you would like to share about, {user_name}?"

        if "work" in message.lower():
            return f"Work is a significant part of our lives. What do you do for work, {user_name}?"

        if "school" in message.lower():
            return f"Education is valuable. Are you currently studying or have any memorable school experiences, {user_name}?"

        if "vacation" in message.lower():
            return f"Vacations are a great way to relax and explore. Do you have a favorite vacation destination, {user_name}?"
   
# Default response for other cases# Use OpenAI API for generating responses to dynamic queries
    temperature = 0.8  # Adjust the temperature for response randomness
    response = await chat_with_gpt(message, temperature)
    return response

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
""""   
from pymongo import MongoClient

# Create the database connection
client = MongoClient("mongodb+srv://cyn:<lMS8DiUTpfQtW4TU>@atlascluster.w68jdko.mongodb.net/?retryWrites=true&w=majority")

# Select the database
db = client["User_chats"]

# Select the collection (equivalent to table in SQL)
collection = db["feedback_collection"]    

class FeedbackRequest(BaseModel):
    content: str
    
@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    try:
        # Create a new document (equivalent to a row in SQL)
        document = {"content": feedback.content}

        # Insert the document into the collection
        collection.insert_one(document)

        return {"message": "Feedback submitted successfully."}

    except Exception as e:
        # Handle any errors
        return {"message": "Failed to submit feedback."}

"""
@app.post("/chat")
async def chat(message: Message):
    if message.is_questionnaire:
        response = await process_questionnaire(message.message)
    else:
        response = await process_user_input(message.message, message.user_name)

    return {"response": response}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
