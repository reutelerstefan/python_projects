

def main():
    print("Test")
    grid =  [1 , 2 ,3 ,4 ,5 ,6, 7,8, 9]
    player = "X"
    grid,player_input = player_in(player, grid)


    grid  = place_input(player_input,player, grid)


def player_in(player, inital_grid):
    
    
    render_grid(inital_grid)
    print('You are {}, enter your input as a number 1-9'.format(player))
    player_input = input("->  ")
    return inital_grid, player_input

def place_input(player_input,player, grid):
    print(player_input,player, grid)
    index = [int(player_input)-1]
    if set(1,2,3,4,5,6,7,8,9) >= index:
        grid[index]= player
    render_grid(grid)
    print( )
        # print("Test")
        # grid[player_input-1] = player
        # return grid
    pass

def render_grid(list_input):

    game_grid = "{0} {1} {2}\n{3} {4} {5} \n{6} {7} {8}".format(*list_input)
    print(game_grid)

if __name__ == "__main__":
    main()
    