from flask import Flask, render_template, request, jsonify
import requests
import google.generativeai as genai

FarmAssistant = Flask(__name__)

# Configure generative AI model
genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat()

# Set up the text and image recognition models
text_model = genai.GenerativeModel('gemini-pro')
image_model = genai.GenerativeModel('gemini-pro-vision')


# Placeholder function for text generation
def generate_text(input_text):
    response = text_model.start_chat().send_message(input_text)
    return response.text


# Placeholder function for image recognition
def recognize_image(image_bytes):
    response = image_model.generate_content(image_bytes)
    return response.choices[0].message.content if response.choices else "Image recognition failed."


# Function to retrieve weather updates based on the user's location

def get_weather_updates(location):
    """Retrieves current weather information using the Tomorrow.io API."""
    api_key = 'MUbsudWmUJ3kn47ush3UwLt0FXJFdBfj'
    url = f'https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-200 status codes

        weather_info = response.json()
        return weather_info
    except requests.exceptions.RequestException as e:
        # Handle request errors gracefully
        return None


def handle_weather_query(location):
    """Handles user queries about weather."""
    weather_data = get_weather_updates(location)
    if weather_data:
        # Process weather data and format the response
        formatted_data = process_weather_data(weather_data)
        return formatted_data
    else:
        return "Failed to retrieve weather updates."


def process_weather_data(weather_data):
    """Process raw weather data and format the response."""
    try:
        temperature = weather_data['data']['timelines'][0]['intervals'][0]['values']['temperature']
        description = weather_data['data']['timelines'][0]['intervals'][0]['values']['weatherCode']
        return f"Current temperature: {temperature}°C, Weather description: {description}"
    except (KeyError, IndexError):
        return "Weather information not available."
    # Example usage


location = 'New York'
print(handle_weather_query(location))


def extract_location(query):
    """Extract the location from the user query."""
    parts = query.split("weather", 1)
    if len(parts) > 1:
        location = parts[1].strip()
        print("Extracted location:", location)  # Add this line for debugging
        return location
    else:
        return None


@FarmAssistant.route('/')
def home():
    return render_template('main.html',
                           welcome_message="Welcome to FarmAssistant Vigorbot! How can I assist you today?")


@FarmAssistant.route('/get', methods=['POST'])
def get_response():
    user_message = request.form.get('userMessage', '')

    if user_message.lower().startswith("weather"):
        location = extract_location(user_message)
        if location:
            response = handle_weather_query(location)
        else:
            response = "Please specify a location for weather information."
    else:
        response = "I'm sorry, I'm not trained in that field."

    return jsonify({'response': response})


if __name__ == '__main__':
    FarmAssistant.run(debug=True)
