# imports and Global variables
import random

USER_CHOISES = ["rock", "paper", "scissors"]


# create a function to get User's input
def get_user_input():
    choise = input("pick your choice ['rock','paper','scissors']: ")
    while choise not in USER_CHOISES:
        choise = input("pick your choice ['rock','paper','scissors']: ")
    return choise


# create a function to get Pc's input
def get_pc_input():
    pc_choice = random.choice(USER_CHOISES)
    print("the PC choice:", pc_choice)
    return pc_choice


# compare and determine which one is the winner
def determine_winner(user_input, pc_input):
    if user_input == pc_input:
        print("Draw!")
    elif (
        (user_input == "rock" and pc_input == "scissors")
        or (user_input == "scissors" and pc_input == "paper")
        or (user_input == "scissors" and pc_input == "paper")
    ):
        print("User Won!")
    else:
        print("PC Won!")


# create a main function as the runner
def main():
    user_input = get_user_input()
    pc_input = get_pc_input()
    determine_winner(user_input, pc_input)
    print("end of the game!")


# make a itteration for doing the game as much as we need
answer = "y"
while answer == "y":
    main()
    answer = input("do you want to continue? [y/n ?]:")
