# import os
# import openai




# def parse_command(text):
#     text = text.strip()
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Convert natural language Android control commands into structured JSON. Supported actions: scroll, swipe, click, type, back, home, lock, unlock."},
#                 {"role": "user", "content": text}
#             ]
#         )
#         json_str = response["choices"][0]["message"]["content"]
#         return eval(json_str)  # Expecting a dict-like string
#     except Exception as e:
#         print(f"Error using OpenAI: {e}")
#         return {"action": "unknown", "text": text}



import openai
import os



def parse_command(text):
    try:
        # Call OpenAI with few-shot examples
        prompt = f"""You are a helpful assistant that converts user commands into structured JSON.
Examples:
User: scroll down
Output: {{"action": "scroll", "direction": "down"}}

User: scroll up please
Output: {{"action": "scroll", "direction": "up"}}

User: swipe left
Output: {{"action": "swipe", "direction": "left"}}

User: type hello world
Output: {{"action": "type", "text": "hello world"}}

User: click on YouTube
Output: {{"action": "click", "target": "YouTube"}}

User: I want to open WhatsApp
Output: {{"action": "click", "target": "WhatsApp"}}

User: go back
Output: {{"action": "back"}}

User: go home
Output: {{"action": "home"}}

User: {text}
Output:
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        output = response['choices'][0]['message']['content']
        print(f"🧠 GPT Parsed Output: {output}")
        import json
        return json.loads(output)

    except Exception as e:
        print(f"⚠️ Error using OpenAI: {e}")
        return {"action": "unknown", "text": text}
