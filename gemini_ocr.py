from google import genai
import base64
client = genai.Client(api_key="...")


# your interactions.create call here



def imageto64(image):
    with open(image,"rb") as f:
            image_bytes=base64.b64encode(f.read()).decode("utf-8")
            return image_bytes
    
def extractcode(image):    
   
    interaction = client.interactions.create(
    model="gemini-2.5-flash",
    input=
    [
        {"type": "text", "text": """Extract the programming code from this image.


            Return the output in the following format:

            Language: <programming language>

            Code:
            <exact code from the image>

            Rules:
            - Preserve exact indentation
            - Preserve line breaks
            - Do not explain anything
            - Do not modify the code
            """},
            {"type": "image",
            "data": imageto64(image),
            "mime_type": "image/png"
        }
    ]
)
  
    return interaction.outputs[-1].text
