import google.generativeai as genai
import PIL.Image
import tkinter as tk
from tkinter import filedialog

# Initialize the GenerativeAI API with your API key
"""def process_image_and_generate_content(image_file):
    genai.configure(api_key='AIzaSyB92g3rBe4oVkCKLdN3vRAC98OudYDVlaY')

    # Initialize the GenerativeModel with the correct model name
    model = genai.GenerativeModel('gemini-pro-vision')

    # Create a Tkinter root window (hidden)
    root = tk.Tk()
    root.withdraw()

    # Prompt the user to select an image file
    image_path = filedialog.askopenfilename(title="Select an image file", filetypes=[("Image files", "*.jpg *.jpeg *.png")])

    # Open the image using PIL
    img = PIL.Image.open(image_path)

    # Generate content based on prompts
    response = model.generate_content(["Describe the image  in detail only if it is related to agriculture  ", img])

    # Print the generated content
    print(response.text)"""

def process_image_and_generate_content(image_file):
    genai.configure(api_key='AIzaSyB92g3rBe4oVkCKLdN3vRAC98OudYDVlaY')

    # Initialize the GenerativeModel with the correct model name
    model = genai.GenerativeModel('gemini-pro-vision')

    # Open the image using PIL
    img = PIL.Image.open(image_file)

    # Generate content based on prompts
    response = model.generate_content(["Describe the image in detail only if it is related to agriculture", img])

    # Return the generated content as a dictionary with the description
    return {'description': response.text}



