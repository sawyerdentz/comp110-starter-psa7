"""
Module: game_of_sticks

Implementation of the Game of Sticks, including an AI that learns the game,
either by playing against a human, or by pre-training against another AI.

Authors:
1) Sawyer Dentz - sdentz@sandiego.edu
2) Matt Oderlin - moderlin@sandiego.edu
"""

import random

def get_player_selection(player_number, sticks_left):
    """
    Asks the user to select an amount of sticks to take and returns the validated amount

    Parameters:
    player_number (type: int) - The players number. Either 1 or 2
    sticks_left (type: int) - the number of sticks remaining

    Returns:
    (type: int) - the validated input from the user

    """
    max_selection = 3
    if sticks_left < max_selection:
        max_selection = sticks_left

    selection = int(input(f"Player {player_number}: How many sticks do you take (1-{max_selection})? "))
    while not (1 <= selection <= max_selection):
        print(f"Please enter a number between 1 and {max_selection}")
        selection = int(input(f"Player {player_number}: How many sticks do you take (1-{max_selection})? "))
    return selection

def player_vs_player(num_sticks):
    """
    Takes in the number of sticks to start with and alternates turns between two players

    Parameters:
    num_sticks (type: int) - the number of sticks to start with

    Returns:
    None
    """

    turn = 1
    sticks_remaining = num_sticks
    while sticks_remaining > 0:
        print()
        if sticks_remaining > 1:
            print(f"There are {sticks_remaining} sticks on the board.")
        else:
            print("There is 1 stick on the board.")
        selection = get_player_selection(turn, sticks_remaining)
        sticks_remaining -= selection
        if sticks_remaining > 0:
            if turn == 1:
                turn = 2
            else:
                turn = 1
    
    print(f"Player {turn}, you lose.")

def initialize_hats(num_sticks):
    """
    Takes in the number of sticks and initializes an amount of hats according to that number

    Parameters:
    num_sticks (type: int) - the number of sticks to start with

    Returns:
    (type: dict) - the dictionary containing hats
    """
    dict = {}
    for i in range(num_sticks):
        i += 1
        if i == 1:
            dict[i] = [1]
        elif i == 2:
            dict[i] = [1,2]
        else:
            dict[i] = [1,2,3]
    return dict

def update_hats(hat_dict, besides_dict, ai_won):
    """
    Updates the hat contents based on whether the ai won or lost.

    Parameters:
    hat_dict (type: dictionary) - the dictionary containing hats
    besides_dict (type: dictionary) - the dictionary containing balls besides the hats
    ai_won (type: boolean) - a boolean of whether or not the ai won

    Returns:
    None
    """
    for hat in besides_dict:
        if ai_won:
            hat_dict[hat].append(besides_dict[hat])
            hat_dict[hat].append(besides_dict[hat])
        else:
            largest_ball = 3
            if hat < largest_ball:
                largest_ball = hat
            for i in range(1, largest_ball + 1):
                if i not in hat_dict[hat]:
                    hat_dict[hat].append(i)

def get_ai_selection(sticks_left, hat_dict, besides_dict):
    """
    Randomly picks and removes a ball from a hat. Adds it to a besides hat dictionary and returns the ball chosen

    Parameters:
    sticks_left (type: int) - the number of sticks remaining on the board
    hat_dict (type: dictionary) - the dictionary containing hats
    besides_dict (type: dictionary) - the dictionary containing balls besides the hats

    Returns
    (type: int) - the number of the ball chosen from the hat
    """
    ball = hat_dict[sticks_left].pop(hat_dict[sticks_left].index(random.choice(hat_dict[sticks_left])))
    besides_dict[sticks_left] = ball
    return ball

def player_vs_ai(num_sticks, training_rounds):
    """
    Takes in the number of sticks to start with and alternates turns between a player and an ai

    Parameters:
    num_sticks (type: int) - the number of sticks to start with

    Returns:
    None
    """
    turn = 1
    sticks_remaining = num_sticks
    hat_dict = pretrain_ai(num_sticks, training_rounds)
    write_hat_contents(hat_dict, "hat-contents.txt")
    besides_dict = {}
    repeat = "1"
    while repeat == "1":
        while sticks_remaining > 0:
            print()
            if sticks_remaining > 1:
                print(f"There are {sticks_remaining} sticks on the board.")
            else:
                print("There is 1 stick on the board.")
            if turn == 1:
                selection = get_player_selection(turn, sticks_remaining)
            else:
                selection = get_ai_selection(sticks_remaining, hat_dict, besides_dict)
                print(f"AI selects {selection}")
            sticks_remaining -= selection
            if sticks_remaining > 0:
                if turn == 1:
                    turn = 2
                else:
                    turn = 1

        if turn == 1:
            print("You lose.")
            ai_won = True
        else:
            print("AI loses.")
            ai_won = False
    
        repeat = input("Play again (1 = yes, 0 = no)? ")
        while repeat not in ["1","0"]:
            print("Input invalid. Please enter 1 or 2.")
            repeat = input("Play again (1 = yes, 0 = no)? ")
        sticks_remaining = num_sticks
        turn = 1
        update_hats(hat_dict, besides_dict, ai_won)
        besides_dict = {}

def pretrain_ai(num_sticks, training_rounds):
    """
    Trains ai by playing a certain amount of games against another ai

    Parameters:
    num_sticks (type: int) - the number of sticks that the game starts with
    training rounds (type: int) - the number of games that should be played to train the ai

    Returns:
    (type: dict) - the dictionary containing hats after training the ai
    """
    hat_dict_1 = initialize_hats(num_sticks)
    besides_dict_1 = {}
    hat_dict_2 = initialize_hats(num_sticks)
    besides_dict_2 = {}
    for _ in range(training_rounds):
        turn = 1
        sticks_remaining = num_sticks
        while sticks_remaining > 0:
            if turn == 1:
                selection = get_ai_selection(sticks_remaining, hat_dict_1, besides_dict_1)
            else:
                selection = get_ai_selection(sticks_remaining, hat_dict_2, besides_dict_2)
            sticks_remaining -= selection
            if sticks_remaining > 0:
                if turn == 1:
                    turn = 2
                else:
                    turn = 1
        if turn == 2:
            update_hats(hat_dict_1, besides_dict_1, True)
            update_hats(hat_dict_2, besides_dict_2, False)
        else:
            update_hats(hat_dict_2, besides_dict_2, True)
            update_hats(hat_dict_1, besides_dict_1, False)
        besides_dict_1 = {}
        besides_dict_2 = {}
    return hat_dict_2

def write_hat_contents(hats, filename):
    """
    writes the contents of the hats to a file

    Parameters:
    hats (type: dictionary) - the dictionary containing hats
    filename (type: string) - the name of the file to write to

    Returns:
    None
    """
    out_file = open(filename, "w")
    out_file.write("Hat Number: (1's, 2's, 3's)\n")

    
    for hat in hats:
        num_one = 0
        num_two = 0
        num_three = 0
        for i in hats[hat]:
            if i == 1:
                num_one += 1
            elif i == 2:
                num_two += 1
            else:
                num_three += 1
        out_file.write(f"{hat}: ({num_one}, {num_two}, {num_three})\n")
    out_file.close()

def main():
    """
    main function - starts the game and asks user what type of game they would like to play
    """
    print("Welcome to the Game of Sticks!")
    num_sticks = int(input("How many sticks are there on the table initially (10-100)? "))
    while not (10 <= num_sticks <= 100):
        print("Please enter a number between 10 and 100")
        num_sticks = int(input("How many sticks are there on the table initially (10-100)? "))

    print("Options:\n Play against a friend (1)\n Play against the computer (2)\n Play against the trained computer (3)")

    option = input("Which option do you take (1-3)? ")
    while option not in ["1","2", "3"]:
        print("Input invalid. Please enter 1, 2, or 3.")
        option = input("Which option do you take (1-3)? ")
    if option == "1":
        player_vs_player(num_sticks)
    elif option == "2":
        player_vs_ai(num_sticks, 0)
    else:
        print("Training AI, please wait...")
        player_vs_ai(num_sticks, 1000)

if __name__ == "__main__":
    main()

