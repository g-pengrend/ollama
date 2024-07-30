from ollama import Client

client = Client(host="http://localhost:11434")
prompt = "why is the sky blue"

output = client.generate(model="llama2", prompt=prompt)

print(output['response'])
