import google.generativeai as genai
import PIL.Image


def process_image_and_generate_content(image_file):
    try:
        genai.configure(api_key='AIzaSyB92g3rBe4oVkCKLdN3vRAC98OudYDVlaY')
        # Initialize the GenerativeModel with the correct model name
        model = genai.GenerativeModel('gemini-pro-vision')

        # Open the image using PIL
        img = PIL.Image.open(image_file)

        # Generate content based on prompts
        response = model.generate_content(["Describe the image in detail only if it is related to agriculture", img])

        # Return the generated content as a dictionary with the description
        text = {'description': response.text}
        return text
    except Exception as e:
        # In case of any error, return an error message
        return {'error': str(e)}
