#lets python talk to the ollama servers
import requests
#turns images to text 
import base64
#opens the image file
from PIL import Image
#temp mem storage to work with the image
from io import BytesIO
#timestamp
from datetime import datetime
#to check if the file exists. 
import os

#gets the llms to run locally. 
LLAVA_MODEL = "llava"
GEMMA_MODEL = "gemma3"
OLLAMA_URL = "http://localhost:11434/api/generate"

'''
opens the image
prepares an empty memory container
converts to a png format
turns it to a base 64 text
'''
def encode_image_base64(image_path):
    with Image.open(image_path) as img:
        buffered = BytesIO()
        img.convert("RGB").save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

'''
first function - ask llava what the image is
turns an image into base 64
model-llava prompt- what we want done. attaches image
send request to ollama ai
return the answer from llava
shows error
'''
def ask_llava(image_path, prompt):
    image_b64 = encode_image_base64(image_path)
    payload = {
        "model": LLAVA_MODEL,
        "prompt": prompt,
        "images": [image_b64],
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        raise Exception(f"LLaVA failed: {response.status_code}, {response.text}")

'''
second ask gemma to rewrite it.
'''
def ask_gemma(text_prompt):
    payload = {
        "model": GEMMA_MODEL,
        "prompt": text_prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code == 200:
        return response.json()["response"].strip()
    else:
        raise Exception(f"Gemma failed: {response.status_code}, {response.text}")

'''
saves everything
f.write(text.strip())= writes the output to a text file
'''
def save_output(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text.strip())
    print(f"Output saved to: {filename}")


'''
gives you input for the file that you want to upload
if you type in a bad name it quits
'''
def main():
    image_path = input("Enter the path to your image file (JPG/PNG): ").strip()
    if not os.path.isfile(image_path):
        print("File not found.")
        return
#gives you an option to enter the session name, if blank will add a timestamp 
    session_name = input("Session name (leave blank for timestamp): ").strip()
    if not session_name:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        session_name = f"session_{timestamp}"
    filename = f"{session_name}.txt"
#CALLS ON LLAVA TO READ THE HANDWRITTING!!!
    try:
        print("The LLaVa is flowing...")
        extracted_text = ask_llava(image_path, "What does the handwriting in this image say? Return just the raw text.")
        print("\nExtracted Text:\n")
        print(extracted_text)
#CALLS ON GEMMA TO SUMMEARIZE OR REPHRASE
        print("\nThe llama is summarizing or rephrasing...")
        gemma_prompt = f"Summarize or rephrase the following handwritten note:\n\n{extracted_text}"
        gemma_response = ask_gemma(gemma_prompt)
#prints it all out
        print("\nGemma Summary:\n")
        print(gemma_response)
#combines the two parts together. 
        full_output = (
            f"Extracted Handwritting:\n{extracted_text}\n\n"
            f"Gemma Summary:\n{gemma_response}\n"
        )
#saves everything
        save_output(full_output, filename)
#if something goes wrong.
    except Exception as e:
        print(f"Error: {e}")
#this makes things run
if __name__ == "__main__":
    main()