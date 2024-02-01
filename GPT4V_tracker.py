import os
import requests
import base64
import time

# Configuration
GPT4V_KEY = os.getenv("GPT4V_KEY")  # Your GPT4V key
GPT4V_ENDPOINT = os.getenv("GPT4V_ENDPOINT")  # The API endpoint for your GPT4V instance

#replace with the name of the image you want to use, exclude the file extension
image_name = 'torn'

#replace with the path to the image you want to use
IMAGE_PATH = "C:\\Users\\wnwanne\\Python\\damaged_package_tracker\\images\\{}.jpg".format(image_name)

system_message = '"You are a damaged package detection AI assistant that spots damages only in packages as quickly as possible. \
         If you spot damage in packagaing in the photo, please identify the extent of the damage and where it is in the following format. \
        \n{item: \"type of item\",\ndamage_extent: \"scale of 1-10, 1 being barely damaged 10 being completely destroyed\" \
        ,\ndamage_description: \"describe the damage and location of the damage\"} \n\nIf there is no damage, simply return \"no damage\".\
            remeber to only focus on the damage to the packaging and not the item inside. \n\nIf you are unsure, please return \"unsure\"'

encoded_image = base64.b64encode(open(IMAGE_PATH, 'rb').read()).decode('ascii')
headers = {
    "Content-Type": "application/json",
    "api-key": GPT4V_KEY,
}

# Payload for the request
payload = {
  "enhancements": { 
    "ocr": { 
      "enabled": True #enabling OCR to extract text from the image using AI vision services
    },
    "grounding": {
      "enabled": True #enabling grounding to extract the context of the image using AI vision services
    }
  },
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": system_message 
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{encoded_image}"
          }
        }
      ]
    }
  ],
  "temperature": 0.5,
  "top_p": 0.95,
  "max_tokens": 800
}
# Send request
try:
    start_time = time.time()
    response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
#time taken to get response
print("--- %s seconds ---" % (time.time() - start_time)) 

# Print the response
print(response.json()['choices'][0]['message']['content'])
print("\n \n")

# Print the tokens used 
print(response.json()['usage'])