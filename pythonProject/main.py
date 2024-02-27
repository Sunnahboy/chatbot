from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import spacy
import random
import markdown
import textwrap

from testimage import process_image_and_generate_content

import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GENAI_API_KEY')

# Configure GenAI with the API key
genai.configure(api_key=api_key)


app = Flask(__name__)

# Initialize the GenerativeModel with 'gemini-pro'
model = genai.GenerativeModel('gemini-pro')

# Load the English language model for spaCy
nlp = spacy.load("en_core_web_sm")

# Define welcome messages with variations
welcome_messages = [
    "Hi there! Welcome to FarmAssistant Vigorbot. How can I assist you today?",
    "Hello! I'm FarmAssistant Vigorbot. How can I help you with farming and agriculture?",
    "Hey! Welcome to FarmAssistant Vigorbot. What can I do for you today?"
]

# Define a list of conversational fillers for more natural responses
fillers = ["Um", "Well", "Let me think", "Hmm"]

# Define suggestions for related topics with more variation
suggestions = {
    "crop management": ["How can we improve soil fertility?", "What are some effective weed control methods?"],
    "weather updates": ["How can we interpret weather forecasts better?",
                        "What preparations should we make for extreme weather?"],
    "livestock management": ["What are the common diseases in poultry?", "How can we optimize dairy cow feed?"],
    "disease and pest identification": ["What are the signs of common tomato diseases?",
                                        "How can we control aphids in crops?"]
}

# Define a dictionary to store user feedback
user_feedback = {}


def extract_key_information(response_text):
    # Process the response using spaCy
    doc = nlp(response_text)

    # Extract key sentences based on sentence length
    key_sentences = [sent.text for sent in doc.sents if len(sent) > 20]

    # Return the extracted key sentences as the chatbot's response
    return " ".join(key_sentences)


@app.route('/')
def home():
    return render_template('test.html')


@app.route('/get', methods=['GET'])
def get_message():
    user_message = request.args.get('userMessage', '')

    # Check if the user message is a greeting
    if user_message.lower() in ['hi', 'hello', 'hey']:
        response_text = random.choice(welcome_messages)
    else:
        # Check if the message is a general inquiry
        if is_general_inquiry(user_message):
            response_text = "I am FarmAssistant Vigorbot, your advanced agricultural assistant. I am here to assist you with various aspects of farming and agriculture."
        else:
            # Check if the message is related to agriculture
            if is_agriculture_related(user_message):
                # Append the user message to chat history
                global chat_history
                chat_history.append({'role': 'user', 'parts': [{'text': user_message}]})

                # Generate content based on chat history
                response = model.generate_content(chat_history)

                # Check if the response is outside the scope of agriculture
                if "not trained in that field" in response.text.lower():
                    response_text = "I'm sorry, I'm not trained in that field."
                else:
                    # Extract key information from the response
                    response_text = extract_key_information(response.text)

                # Provide suggestions for related topics based on the user query
                for topic, related_questions in suggestions.items():
                    if topic.lower() in user_message.lower():
                        response_text += "\n\nRelated topics you might be interested in:\n"
                        response_text += "\n".join("- " + question for question in
                                                   random.sample(related_questions, min(2, len(related_questions))))
                        break

                # Append the chatbot response to chat history
                chat_history.append({'role': 'model', 'parts': [{'text': response_text}]})
            else:
                # If the message is not related to agriculture, provide a default response
                response_text = "I'm sorry, I'm not trained in that field."

    # Add conversational fillers for natural responses
    if random.random() < 0.3:  # Add fillers with 30% probability
        response_text = f"{random.choice(fillers)}, {response_text}"

    # Convert response text to Markdown format
    response_text = to_markdown(response_text)

    return jsonify({'response': response_text})


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image_file = request.files['image']

        # Process the image file and generate content
        result = process_image_and_generate_content(image_file)

        # Check if there was an error processing the image
        if 'error' in result:
            return jsonify({'response': result['error']}), 400

        # Extract the description from the result
        image_description = result.get('description', 'No description available')

        # Convert description to Markdown format
        markdown_description = f"**Description:**\n{image_description}"

        # Convert Markdown to HTML for better rendering
        html_description = markdown.markdown(markdown_description)

        return jsonify({'response': html_description})
    else:
        return jsonify({'response': 'No image file provided'}), 400

def is_agriculture_related(user_message):
    # Process the user's message using spaCy
    doc = nlp(user_message)

    # Check for entities related to agriculture
    agriculture_entities = ["FARM", "FARMING", "CROP", "LIVESTOCK", "WEATHER", "DISEASE", "PEST"]

    for entity in doc.ents:
        if entity.text.upper() in agriculture_entities:
            return True

    # Check for keywords related to agriculture
    agriculture_keywords = ["farm", "farming", "crop", "livestock", "weather", "disease", "pest"]
    for token in doc:
        if token.text.lower() in agriculture_keywords:
            return True

    return False


def is_general_inquiry(user_message):
    # Define keywords for general inquiries
    general_inquiry_keywords = ["what do you do", "what's your name", "Your name"]

    # Check if the user's message contains any of the general inquiry keywords
    for keyword in general_inquiry_keywords:
        if keyword.lower() in user_message.lower():
            return True

    return False


def to_markdown(text):
    # Convert plain text to Markdown format
    text = text.replace('•', '  *')
    return markdown.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


if __name__ == '__main__':
    # Define chat history as a global variable
    chat_history = []
    app.run(debug=True)
