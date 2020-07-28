import random

user_name = input("Enter your name: ")
print(f"Hello, {user_name}")

rating_file = open("rating.txt", "r")
ratings_dict = {}
for line in rating_file:
    ratings_dict[line.split()[0]] = int(line.split()[1])
if user_name not in ratings_dict:
    ratings_dict[user_name] = 0
rating_file.close()

game_options = input().split(',')
if game_options == [""]:
    game_options = ["rock", "paper", "scissors"]
game_win_dict = {}
for opt in game_options:
    opt_index = game_options.index(opt)
    transformed_options = game_options[opt_index + 1:] + game_options[:opt_index]
    halfway_index = len(transformed_options) / 2
    game_win_dict[opt] = transformed_options[:int(halfway_index)]


def check_win(user, comp):
    if user in game_win_dict[comp]:
        return "win"
    elif user == comp:
        return "tie"
    else:
        return "lose"


print("Okay, let's start")
while True:
    user_choice = input()
    round_score = 0
    if user_choice == "!exit":
        with open("rating.txt", "w") as rating_file:
            for key in ratings_dict:
                rating_file.write(f"{key} {ratings_dict[key]}\n")
        print("Bye!")
        break
    elif user_choice == "!rating":
        print("Your rating:", ratings_dict[user_name])
    elif user_choice in game_options:
        computer_option = random.choice(game_options)
        result = check_win(user_choice, computer_option)
        if result == "tie":
            print(f"There is a draw ({computer_option})")
            round_score += 50
        elif result == "win":
            print(f"Well done. Computer chose {computer_option} and failed")
            round_score += 100
        elif result == "lose":
            print(f"Sorry, but computer chose {computer_option}")
        ratings_dict[user_name] += round_score
    else:
        print("Invalid input")
