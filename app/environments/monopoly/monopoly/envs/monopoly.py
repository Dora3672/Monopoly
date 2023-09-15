
import gym
import numpy as np

import config

from stable_baselines import logger


class Player():
    def __init__(self, id, token):
        self.id = id
        self.token = token
        

class Token():
    def __init__(self, symbol, number):
        self.number = number
        self.symbol = symbol
        
    

class MonopolyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(TicTacToeEnv, self).__init__()
        self.name = 'tictactoe'
        self.manual = manual
        
        self.n_players = 2
        self.num_squares = 40 
        self.action_space = gym.spaces.Discrete(self.num_squares)
        self.observation_space = gym.spaces.Box(-1, 1, (self.num_squares, 2))
        self.verbose = verbose

        self.current_player_num = 0
        self.players = [Player('Player 1', Token('X', 1)), Player('Player 2', Token('O', -1))]
        self.board = np.zeros(self.num_squares, dtype=int)
        self.done = False
        

    @property
    def observation(self):
    # Create an observation space representing the state of the Monopoly game
    num_property_features = 12  # Number of property-related features
    num_railroads_features = 5  # Number of features for railroads
    num_utilities_features = 4  # Number of features for utilities
    num_player_features = 13  # Number of player-related features

    num_players = len(self.players)
    num_properties = len(self.properties)
    num_railroads = len(self.railroads)
    num_utilities = len(self.utilities)

    max_price_scale = 1e6  # Choose a very large value as the max price scale

    # Create the player array with zeros
    player_array = np.zeros((num_players, num_player_features), dtype=float)
    # Update the player array for each player
    for i, player in enumerate(self.players):
        # Update player features
        player_array[i, 0] = player.playerNum/num_players
        player_array[i, 1] = ((2 * player.diceroll)/12)-1
        player_array[i, 1] = player.rollingdoubles/3
        player_array[i, 2] = player.position/40
        player_array[i, 3] = int(player.turn)
        player_array[i, 4] = ((2 * player.cash)/max_price_scale) -1
        player_array[i, 5] = int(player.jail)
        player_array[i, 6] = player.dicejail/3
        player_array[i, 7] = int(player.wasjailed)
        player_array[i, 8] = ((2 * player.houseNum)/32) -1
        player_array[i, 9] = ((player.hotelNum)/12) -1
        player_array[i, 10] = player.railroadNum/4
        player_array[i, 11] = player.utilitiesNum/2
        player_array[i, 12] = int(player.freeJail)

    # Create the property array with zeros
    property_array = np.zeros((num_properties, num_property_features), dtype=float)
    # Add property-related information
    for i, property in enumerate(self.properties):
        # Update property features
        property_array[i, 0] = property.pieceType/num_players if property.occupied == True else -1
        property_array[i, 1] = self.board.index(property)
        property_array[i, 2] = ((2 * property.color)/7) - 1
        property_array[i, 3] = ((2 * property.price) / max_price_scale) -1
        property_array[i, 4] = ((2 * property.rent) / max_price_scale) -1
        property_array[i, 5] = (2 * property.house / 4) -1
        property_array[i, 6] = property.hotel
        property_array[i, 7] = ((2 * property.househotelCosts)/max_price_scale) -1
        property_array[i, 8] = int(property.colorset)
        property_array[i, 9] = int(property.mortgaged)
        property_array[i, 10] = ((2 * property.mortgagedprice)/max_price_scale) -1
        property_array[i, 11] = ((2 * property.mortgagedPayPrice)/max_price_scale) -1

    # Create the railroad array with zeros
    railroad_array = np.zeros((num_railroads, num_railroads_features), dtype=float)
    # Add railroad-related information
    for i, railroad in enumerate(self.railroads):
        # Update railroad features
        railroad_array[i, 0] = railroad.pieceType/num_players if railroad.occupied == True else -1
        railroad_array[i, 1] = self.board.index(railroad)
        railroad_array[i, 2] = ((2 * railroad.price)/max_price_scale) -1
        railroad_array[i, 3] = ((2 * railroad.rent)/max_price_scale) -1
        railroad_array[i, 4] = ((2 * property.totalRailroad)/4) -1

    # Create the utility array with zeros
    utility_array = np.zeros((num_utilities, num_utilities_features), dtype=float)
    # Add utility-related information
    for i, utility in enumerate(self.utilities):
        # Update utility features
        utility_array[i, 0] = utility.pieceType/num_players if utility.occupied == True else -1
        utility_array[i, 1] = self.board.index(utility)
        utility_array[i, 2] = ((2 * utility.price)/max_price_scale) -1
        utility_array[i, 3] = int(property.utilities)
########### rents ok?

    # Concatenate the arrays into the observation
    observation = np.concatenate((player_array.flatten(), property_array.flatten(), railroad_array.flatten(), utility_array.flatten()))

    return observation


    @property
    def legal_actions(self):
        current_player = self.current_player
        legal_actions = []

        # Iterate through properties
        for property_index, property_info in enumerate(self.properties):
            owner = property_info.get("owner", None)
            is_mortgaged = property_info.get("mortgaged", False)
            price = property_info.get("price", 0)
            house_price = property_info.get("househotelCosts", 0)
            hotel_count = property_info.get("hotel", 0)

            # Buy the property if it's unowned and the player has enough cash
            if owner is None and current_player.cash >= price:
                legal_actions.append(1.0)  # Buy Property

            # Buy back the property if it's mortgaged and the player has enough cash
            if owner == current_player.id and is_mortgaged and current_player.cash >= price:
                legal_actions.append(0.8)  # Buy Back Property

            # Buy an additional house if the property is owned by the player and not at max houses
            if owner == current_player.id and house_price > 0 and hotel_count == 0 and current_player.cash >= house_price:
                legal_actions.append(0.6)  # Buy House on Property

            # Buy a hotel if the property is owned by the player, has 4 houses, no hotels, and enough cash
            if owner == current_player.id and hotel_count == 0 and current_player.cash >= house_price:
                legal_actions.append(0.5)  # Buy Hotel on Property

        # Append a "Do Nothing" action
        legal_actions.append(-1.0)  # Do Nothing

        return legal_actions




#     def square_is_player(self, square, player):
#         return self.board[square].number == self.players[player].token.number

#     def check_game_over(self):

#         board = self.board
#         current_player_num = self.current_player_num
#         players = self.players


#         # check game over
#         for i in range(self.grid_length):
#             # horizontals and verticals
#             if ((self.square_is_player(i*self.grid_length,current_player_num) and self.square_is_player(i*self.grid_length+1,current_player_num) and self.square_is_player(i*self.grid_length+2,current_player_num))
#                 or (self.square_is_player(i+0,current_player_num) and self.square_is_player(i+self.grid_length,current_player_num) and self.square_is_player(i+self.grid_length*2,current_player_num))):
#                 return  1, True

#         # diagonals
#         if((self.square_is_player(0,current_player_num) and self.square_is_player(4,current_player_num) and self.square_is_player(8,current_player_num))
#             or (self.square_is_player(2,current_player_num) and self.square_is_player(4,current_player_num) and self.square_is_player(6,current_player_num))):
#                 return  1, True

#         if self.turns_taken == self.num_squares:
#             logger.debug("Board full")
#             return  0, True

#         return 0, False

#     @property
#     def current_player(self):
#         return self.players[self.current_player_num]


#     def step(self, action):
        
#         reward = [0,0]
        
#         # check move legality
#         board = self.board
        
#         if (board[action].number != 0):  # not empty
#             done = True
#             reward = [1, 1]
#             reward[self.current_player_num] = -1
#         else:
#             board[action] = self.current_player.token
#             self.turns_taken += 1
#             r, done = self.check_game_over()
#             reward = [-r,-r]
#             reward[self.current_player_num] = r

#         self.done = done

#         if not done:
#             self.current_player_num = (self.current_player_num + 1) % 2

#         return self.observation, reward, done, {}

#     def reset(self):
#         self.board = [Token('.', 0)] * self.num_squares
#         self.players = [Player('1', Token('X', 1)), Player('2', Token('O', -1))]
#         self.current_player_num = 0
#         self.turns_taken = 0
#         self.done = False
#         logger.debug(f'\n\n---- NEW GAME ----')
#         return self.observation


#     def render(self, mode='human', close=False, verbose = True):
#         logger.debug('')
#         if close:
#             return
#         if self.done:
#             logger.debug(f'GAME OVER')
#         else:
#             logger.debug(f"It is Player {self.current_player.id}'s turn to move")
            
#         logger.debug(' '.join([x.symbol for x in self.board[:self.grid_length]]))
#         logger.debug(' '.join([x.symbol for x in self.board[self.grid_length:self.grid_length*2]]))
#         logger.debug(' '.join([x.symbol for x in self.board[(self.grid_length*2):(self.grid_length*3)]]))

#         if self.verbose:
#             logger.debug(f'\nObservation: \n{self.observation}')
        
#         if not self.done:
#             logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')


#     def rules_move(self):
#         if self.current_player.token.number == 1:
#             b = [x.number for x in self.board]
#         else:
#             b = [-x.number for x in self.board]

#         # Check computer win moves
#         for i in range(0, self.num_squares):
#             if b[i] == 0 and testWinMove(b, 1, i):
#                 logger.debug('Winning move')
#                 return self.create_action_probs(i)
#         # Check player win moves
#         for i in range(0, self.num_squares):
#             if b[i] == 0 and testWinMove(b, -1, i):
#                 logger.debug('Block move')
#                 return self.create_action_probs(i)
#         # Check computer fork opportunities
#         for i in range(0, self.num_squares):
#             if b[i] == 0 and testForkMove(b, 1, i):
#                 logger.debug('Create Fork')
#                 return self.create_action_probs(i)
#         # Check player fork opportunities, incl. two forks
#         playerForks = 0
#         for i in range(0, self.num_squares):
#             if b[i] == 0 and testForkMove(b, -1, i):
#                 playerForks += 1
#                 tempMove = i
#         if playerForks == 1:
#             logger.debug('Block One Fork')
#             return self.create_action_probs(tempMove)
#         elif playerForks == 2:
#             for j in [1, 3, 5, 7]:
#                 if b[j] == 0:
#                     logger.debug('Block 2 Forks')
#                     return self.create_action_probs(j)
#         # Play center
#         if b[4] == 0:
#             logger.debug('Play Centre')
#             return self.create_action_probs(4)
#         # Play a corner
#         for i in [0, 2, 6, 8]:
#             if b[i] == 0:
#                 logger.debug('Play Corner')
#                 return self.create_action_probs(i)
#         #Play a side
#         for i in [1, 3, 5, 7]:
#             if b[i] == 0:
#                 logger.debug('Play Side')
#                 return self.create_action_probs(i)


#     def create_action_probs(self, action):
#         action_probs = [0.01] * self.action_space.n
#         action_probs[action] = 0.92
#         return action_probs   


# def checkWin(b, m):
#     return ((b[0] == m and b[1] == m and b[2] == m) or  # H top
#             (b[3] == m and b[4] == m and b[5] == m) or  # H mid
#             (b[6] == m and b[7] == m and b[8] == m) or  # H bot
#             (b[0] == m and b[3] == m and b[6] == m) or  # V left
#             (b[1] == m and b[4] == m and b[7] == m) or  # V centre
#             (b[2] == m and b[5] == m and b[8] == m) or  # V right
#             (b[0] == m and b[4] == m and b[8] == m) or  # LR diag
#             (b[2] == m and b[4] == m and b[6] == m))  # RL diag


# def checkDraw(b):
#     return 0 not in b

# def getBoardCopy(b):
#     # Make a duplicate of the board. When testing moves we don't want to 
#     # change the actual board
#     dupeBoard = []
#     for j in b:
#         dupeBoard.append(j)
#     return dupeBoard

# def testWinMove(b, mark, i):
#     # b = the board
#     # mark = 0 or X
#     # i = the square to check if makes a win 
#     bCopy = getBoardCopy(b)
#     bCopy[i] = mark
#     return checkWin(bCopy, mark)


# def testForkMove(b, mark, i):
#     # Determines if a move opens up a fork
#     bCopy = getBoardCopy(b)
#     bCopy[i] = mark
#     winningMoves = 0
#     for j in range(0, 9):
#         if testWinMove(bCopy, mark, j) and bCopy[j] == 0:
#             winningMoves += 1
#     return winningMoves >= 2