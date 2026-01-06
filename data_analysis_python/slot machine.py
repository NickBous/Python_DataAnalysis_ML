import random
ROWS=5
COLS=3
slot_options=['$','#','7','@','%']
slot_choice1=random.randint(0,4)
slot_choice2=random.randint(0,4)
slot_choice3=random.randint(0,4)
slot_choice4=random.randint(0,4)
slot_choice5=random.randint(0,4)
def give_start_amount():
    global starting_amount
    starting_amount=input("Deposit the starting amount of money you have on you\n")
    if starting_amount.isdigit:
        starting_amount=int(starting_amount)
        
        return starting_amount
    else:
        print("Input an integer please!\n")
def instructions():
    print('Welcome to the slot machine. You win if you have three same type of chatacters on the same row\n')
    print("If you win you 4x your deposited money\n")
    print("If you have all 7's on the same row you 10x your deposited money\n")
def bet():
    betting=int(input("Select the amount to bet on:\n"))
    if betting>starting_amount:
        print("The amount you bet on has to be smaller than your starting amount")
    return betting
    
def play():
    slot=[[slot_options[slot_choice1],slot_options[slot_choice2],slot_options[slot_choice3]],
        [slot_options[slot_choice4],slot_options[slot_choice5],slot_options[slot_choice1]],
        [slot_options[slot_choice2],slot_options[slot_choice3],slot_options[slot_choice4]],
        [slot_options[slot_choice5],slot_options[slot_choice1],slot_options[slot_choice2]],
        [slot_options[slot_choice3],slot_options[slot_choice4],slot_options[slot_choice5]]]
    print("|",slot[0][0],"|",slot[0][1],"|",slot[0][2],"|","\n")
    print("|",slot[1][0],"|",slot[1][1],"|",slot[1][2],"|","\n")
    print("|",slot[2][0],"|",slot[2][1],"|",slot[2][2],"|","\n")
    print("|",slot[3][0],"|",slot[3][1],"|",slot[3][2],"|","\n")
    print("|",slot[4][0],"|",slot[4][1],"|",slot[4][2],"|","\n")
    for i in range(ROWS):
        for j in range(COLS):
            if slot[i][0]==slot[i][1]==slot[i][2]!='7':
                print("You win\n")
                earnings=bet()*4
                total_amount=starting_amount-bet()+earnings
                print("You have a total amount of:", total_amount)
            elif slot[i][0]==slot[i][1]==slot[i][2]=='7':
                print("You win\n")
                earnings=bet()*10
                total_amount=starting_amount-bet()+earnings
                print("You have a total amount of:", total_amount)
            else:
                print("Better luck next time\n")
                total_amount=starting_amount-bet()
                print("You have a total amount of:", total_amount)

instructions()
give_start_amount()
bet()
play()



