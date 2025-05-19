# from nlp_parser import parse_command
# from command_mapper import handle_command

# if __name__ == "__main__":
#     print("Welcome to Android Controller via USB (Natural Language Interface)")
#     while True:
#         user_input = input("\nEnter command (or 'exit'): ")
#         if user_input.lower() in ["exit", "quit"]:
#             break
#         command = parse_command(user_input)
#         handle_command(command)


from nlp_parser import parse_command
from command_mapper import handle_command

if __name__ == "__main__":
    print("Welcome to Android Controller via USB (Natural Language Interface)")
    while True:
        user_input = input("\nEnter command (or 'exit'): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print(f"🗣 Original Command: {user_input}")
        command = parse_command(user_input)
        print(f"🔎 Interpreted NLP Command: {command}")
        handle_command(command)
