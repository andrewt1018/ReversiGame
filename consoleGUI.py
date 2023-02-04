from env import Reversi
import sys

if __name__ == "__main__":
    print("Welcome to Reversi!")
    print("What would you like to do?")
    print("1. Start a new game.")
    print("2. Exit")
    while True:
        try:
            choice = int(input())
            if choice == 1:
                print("What size do you want the board to be? \nEnter a positive even integer greater than 2.")
                while True:
                    try:
                        choice = int(input())
                        board = Reversi(choice)
                        break
                    except:
                        print("Please enter a positive even integer greater than 2!")

                end = False
                while not end:
                    if board.white_move:
                        print()
                        print("White's turn to play!")
                    else:
                        print()
                        print("Black's turn to play!")
                    board.rendor()
                    print(f"Action space: {board.action_space}")
                    print("Type 'Exit' to return to the main menu at any time.")
                    print("Where would you like to place your piece? Enter a coordinate in the form (x,y)")
                    coordinate = (-1, -1)
                    while True:
                        try:
                            check_exit = input()
                            if check_exit == "Exit" or check_exit == "exit":
                                break
                            choice = tuple(check_exit.split(','))
                            coordinate = (int(choice[0].replace('(', '')), int(choice[1].replace(')', '')))

                            if coordinate not in board.action_space:
                                raise ValueError
                            break
                        except ValueError:
                            print("Please enter a valid coordinate!")
                    win = board.step(coordinate)
                    if win != 0:
                        end = True
            elif choice == 2:
                print("Bye!")
                sys.exit()
            else:
                print("Please enter a valid choice!")
            print("What would you like to do?")
            print("1. Start a new game.")
            print("2. Exit")
        except ValueError:
            print("Please enter a valid choice!")
