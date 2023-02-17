#OPTIONS
BOARD_SIZE = 3 # max 9 (due to current moves loading), check if >= CONNECTED_TO_WIN needed
CONNECTED_TO_WIN = 3

# To-do:
# add pygame and made graphic
# check controls
# add single player

def check_win(num, x, y, board):

    #Check row x
    in_row = max_in_row = 0
    for i in range(BOARD_SIZE):
        if board[x][i] == num:
            in_row += 1
        else:
            if in_row >= max_in_row:
                max_in_row = in_row
            in_row = 0

    if in_row >= max_in_row:
        max_in_row = in_row
    if max_in_row >= CONNECTED_TO_WIN:
        return True

    #Check col y
    in_col = max_in_col = 0
    for i in range(BOARD_SIZE):
        if board[i][y] == num:
            in_col += 1
        else:
            if in_col >= max_in_col:
                max_in_col = in_col
            in_col = 0

    if in_col >= max_in_col:
        max_in_col = in_col
    if max_in_col >= CONNECTED_TO_WIN:
        return True

    #Check left diagonal
    l_diag = max_l_diag = 0
    diag_x = x - y
    if diag_x >= 0:
        diag_y = 0
    else:
        diag_y = diag_x * (-1)
        diag_x = 0

    while diag_x < BOARD_SIZE and diag_y < BOARD_SIZE:
        if board[diag_x][diag_y] == num:
            l_diag += 1
        else:
            if l_diag >= max_l_diag:
                max_l_diag = l_diag
            l_diag = 0
        
        diag_x += 1
        diag_y += 1

    if l_diag >= max_l_diag:
        max_l_diag = l_diag
    if max_l_diag >= CONNECTED_TO_WIN:
        return True

    #Check right diagonal
    r_diag = max_r_diag = 0
    diag_x = x + y
    if diag_x < BOARD_SIZE:
        diag_y = 0
    else:
        diag_y = diag_x - BOARD_SIZE + 1
        diag_x = BOARD_SIZE - 1

    while diag_x >= 0 and diag_y < BOARD_SIZE:
        if board[diag_x][diag_y] == num:
            r_diag += 1
        else:
            if r_diag >= max_r_diag:
                max_r_diag = r_diag
            r_diag = 0
        
        diag_x -= 1
        diag_y += 1

    if r_diag >= max_r_diag:
        max_r_diag = r_diag
    if max_r_diag >= CONNECTED_TO_WIN:
        return True

    return False
    
def valid_move(x, y, board):
    if board[x][y] == 0:
        return True

    return False

def pvp():
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    run = True

    while run:
        #player 1 turn 
        good_move = False
        while not good_move:
            move = int(input("Ruch pierwszego gracza: "))
            r, c = move//10, move%10
            if valid_move(r, c, board):
                board[r][c] = 1
                good_move = True

        if check_win(1, r, c, board):
            print("Player 1 wins!")
            run = False
            break

        good_move = False
        while not good_move:
            move = int(input("Ruch drugiego gracza: "))
            r, c = move//10, move%10
            if valid_move(r, c, board):
                board[r][c] = 2
                good_move = True

        if check_win(2, r, c, board):
            print("Player 2 wins!")
            run = False
            break

        print(board)
    
    quit()

def sp():
    pass

def main():
    mode = int(input("Tryb gry \n 1) Single Player \n 2) Player vs Player \n"))
    mode = 2 #To usunac jak bedzie sp
    if mode == 1:
        sp()
    else:
        pvp()
    quit()
  
if __name__ == "__main__":
    main()
