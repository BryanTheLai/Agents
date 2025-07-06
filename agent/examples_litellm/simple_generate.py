from litellm import completion, stream_chunk_builder
from dotenv import load_dotenv

load_dotenv()

messages = [{"role": "user", "content": "Hey, how's it going?"}]

response = completion(
  model="gemini/gemini-2.5-flash-lite-preview-06-17",
  messages=messages, 
  stream=True
  )

chunks = []
for chunk in response: 
  print(chunk.choices[0].delta.content or "")
  chunks.append(chunk)

print(stream_chunk_builder(chunks, messages=messages))