from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import openai
import os
import uvicorn
from pymongo import MongoClient
from bson.objectid import ObjectId
import re



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
    chatbot_name: str

@app.get("/ask-user-name")
def ask_for_user_name():
    user_name = input("Hey! What is your name?\n ")
    return f"Nice to meet you, { user_name}"

@app.get("/ask-chatbot-name")
def ask_for_chatbot_name():
    chatbot_name = input("Chatbot: What would you like to call me?\n ")
    return f"{chatbot_name} is a nice name. Thank you!"

async def chat_with_gpt(message: str, temperature: float):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Specify the OpenAI engine
            prompt=message,
            temperature=temperature,
            max_tokens=150,  # Adjust the max tokens as per your requirement
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

async def process_user_input(message: str, user_name: str = "User", friend_name: str ="Friend"):
    # Define the triggers for different emotions
    positive_triggers = ["amazing", "happy", "good", "great", "happy", "better", "hope", "excited"]
    negative_triggers = ["sad", "lonely", "depressed", "anxious", "stressed", "I feel stuck and helpless.", "I'm such a failure."]
    neutral_triggers = ["do not belong", "kill myself", "die", "end it", "There's no point in living anymore",  "Everyone would be better off without me" , "There's no escape from this pain","I can't see any way out of this.", "I can't take it anymore",  "I wish I could just disappear."]
    topic_triggers = ["favorite color", "i want to cry", "sorry", "hello","how are you", "hi", "hey" "weather", "music","okay", "food", "hobby", "weekend plans", "movie", "book", "travel", "pet", "sport", "dream", "goal", "inspire", "family", "friend", "work", "school", "vacation"]
    greet_trigger=["hey"]+["hello"]+["hi"]+["whatsup"]+["yoo"]+["gwe"]
    friend_triggers = ["friend's name", "my friend's name","her name","his name", "friend is called"]
    sleep_triggers=["good night", 'sleep', "sleepy","good morning", "exhausted", "tired","thank"]
    if any(trigger in message.lower() for trigger in friend_triggers):
       #Extract the friend's name from the message
         friend_name = extract_friend_name(message)
    # Store the friend's name in the conversation history
         conversation_collection.insert_one({"user_name": user_name, "message": friend_name})
         return f"Nice! {friend_name} is a great name. What does {friend_name} like?"

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
    if any(trigger in message.lower() for trigger in sleep_triggers):
        if ("good night") in message.lower():
            return f"Good night {user_name}. Sleep tight!"
        
        if ("sleep") in message.lower():
            return f"Take a nap. You must be tired."
        
        if ("sleepy") in message.lower():
            return f"I think it's best you lie down and sleep"
        if ("good morning") in message.lower():
            return f"Good morning, {user_name}. How was your night?"
        if ("exhausted") in message.lower():
            return f"What have you been doing?"
        
        if ("tired") in message.lower():
            return f"What is making you tired?"
        if ("thank") in message.lower():
            return f"You're welcome, {user_name}. Is there anything else you want to share?"
# Default response for other cases# Use OpenAI API for generating responses to dynamic queries
    temperature = 0.4  # Adjust the temperature for response randomness
    response = await chat_with_gpt(message, temperature)
    return response


 
uri = "mongodb+srv://rhodzeey:12345@cluster0.tpb0e.mongodb.net/nodeMastery?retryWrites=true&w=majority"
# Create the database connection
client = MongoClient(uri)

# Create the database connection
#client = MongoClient("mongodb+srv://cyn:<lMS8DiUTpfQtW4TU>@atlascluster.w68jdko.mongodb.net/?retryWrites=true&w=majority")

# Select the database
db = client["chatbot_db"]

conversation_collection = db["conversation_history"]


# Function to extract friend's name from the message
def extract_friend_name(message: str) -> str:
    pattern = r"my friend['s]* name is ([A-Za-z]+)"
    match = re.search(pattern, message, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return ""

# Select the collection (equivalent to a table in SQL)
collection = db["names_collection"]

@app.post("/chat")
async def chat(message: Message):
  try:

         # Retrieve the stored chatbot and user names from the database
        chatbot_document = collection.find_one({"name_type": "chatbot"})
        chatbot_name = chatbot_document["name"] if chatbot_document else None
          
        user_document = collection.find_one({"name_type": "user"})
        user_name = user_document["name"] if user_document else None
           # If the user name is not set, prompt for it 
        if not message.user_name:
                user_name = input("Hey!! What is your name?\n ")
                collection.update_one({"name_type": "user"}, {"$set": {"name": user_name}})
         # If the chatbot name is not set, prompt for it 
        if not message.chatbot_name:
                 chatbot_name = input(f"Nice meeting you {user_name}, what would you like to call me?\n ")
                 collection.update_one({"name_type": "chatbot"}, {"$set": {"name": chatbot_name}})
             # Save user input to the conversation history collection
        conversation_collection.insert_one({"user_name": user_name, "message": message.message})

        
        # Extract friend's name from the message, if mentioned
        friend_name = extract_friend_name(message.message)
        if friend_name:
            # Store friend's name in the conversation history
            conversation_collection.insert_one({"user_name": user_name, "message": friend_name})

        # Retrieve the conversation history from the collection
        conversation_history = list(conversation_collection.find())
                
        # Remove ObjectId values from the conversation history
        conversation_history_cleaned = []
        for doc in conversation_history:
            doc["_id"] = str(doc["_id"])
            conversation_history_cleaned.append(doc)
     # Concatenate conversation history as a single string
        conversation = "\n".join([f"{doc['user_name']}: {doc['message']}" for doc in conversation_history_cleaned])

        # Use conversation history for generating responses
        temperature = 0.4  # Adjust the temperature for response randomness
        response = await chat_with_gpt(conversation, temperature)

        # Save chatbot response to the conversation history collection
        conversation_collection.insert_one({"user_name": chatbot_name, "message": response})

       # return {"response": response}

    
        response = await process_user_input(message.message, message.user_name)
        return  response, conversation_history_cleaned
  except Exception as e:
   raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
