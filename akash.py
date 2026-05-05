from utils.llm_client import GroqClient
from utils.mcp_helper import build_mcp_prompt
client = GroqClient()

client = GroqClient()

topic = 'Docker'
level = 'Easy'

prompt = build_mcp_prompt(topic, level)

output = client.ask(prompt)
print(output)