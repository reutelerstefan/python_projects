

def main(grid =  [n for n in range(1,10)]):
    print()
    print('-------------------------')
    print("A new game of Tic/Tac/Toe")
    print('-------------------------')
    print()
    
    player1 = "X"
    player2 = "O"
    player = player1
    while True:
        grid,player_input = player_in(player, grid)
        grid  = place_input(player_input,player, grid)
        check_game(grid,player)
        if player == player1:
            player = player2
        elif player == player2:
            player = player1
        else: print("Error")
        

def player_in(player, inital_grid):
    
    
    render_grid(inital_grid)
    
    print('You are {}, enter your input as a number 1-9'.format(player))
    player_input = input("->  ")
    return inital_grid, player_input

def place_input(player_input,player, grid):
    # print(player_input,player, grid)
   
    try:
        b=grid.index(int(player_input))
        # print(b)
        grid[b]= player
        render_grid(grid)
        return grid
    except ValueError:
        grid,player_input = player_in(player, grid)
        grid  = place_input(player_input,player, grid)
        "Valueerror"
        print('VarError')
        return grid
    else:
        "Error"
        print('Error')
        
    render_grid(grid)
    print( )
        # print("Test")
        # grid[player_input-1] = player
        # return grid
    pass

def render_grid(list_input):
    
    game_grid = "\n{0} {1} {2}\n{3} {4} {5} \n{6} {7} {8}".format(*list_input)
    print(game_grid)

def check_game(grid,player):

    victory_conditions(grid,player)
    
   
    pass

def victory_conditions(grid,player):

    list_victory = [[0, 1, 2],[3, 4, 5], [6, 7, 8], #Horizontal
                    [0, 3, 6],[1,4,7],[2,5,8],       #Vertical
                    [0,4,8],[2,4,6]]

    indices_X = [i for i, x in enumerate(grid) if x == "X"]
    indices_O = [i for i, x in enumerate(grid) if x == "O"]  
    sum_ind = len(indices_O)+len(indices_X)

    # Victory condition
    for list_vic in list_victory:
        if grid[list_vic[0]]==grid[list_vic[1]]==grid[list_vic[2]]== player:
            print('Victory for player: '+ player)
            print()
            if input('Play again ? [y]es, [n]o   ')== 'y':
                main()
            else:
                quit()
        
    if sum_ind >= 9:
            print('The game is tied')
            print()
            if input('Play again ? [y]es, [n]o')== 'y':
                main()
        
    else:
            print('Game is ongoing')
            print()
       
        
    # [print('victory: '+ str(indices_player)) for n in list_victory if list_victory.index(indices_player)]
   



if __name__ == "__main__":
    main()
    