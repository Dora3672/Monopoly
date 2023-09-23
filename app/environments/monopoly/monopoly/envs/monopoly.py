
import gym
import numpy as np

import config

from stable_baselines import logger


from array import *

class Player:
  def __init__(self, symbol, name):
    self.position = 0  #position of the play on the board
    self.rollingdoubles = 0
    self.name = name
    self.playerSymbol = symbol
    self.turn = False
    self.move = False  # move to a place due to c/cc
    self.b = False  # pay for buying
    self.cash = 1500 #starting cash
    self.jail = False #whether the person is in jail or not
    self.diceJail = 0 #number of times trying to roll doubles to get out of jail free
    self.wasJailed = False #whether the person was in jail or not during the round
    #whether the player owns the property or not
    self.playerProperty = [[False, 0, 0], [False, 0, 0], #brown
                           [False, 0, 0], [False, 0, 0], [False, 0, 0], #light blue
                           [False, 0, 0], [False, 0, 0], [False, 0, 0], #purple
                           [False, 0, 0], [False, 0, 0], [False, 0, 0], #orange
                           [False, 0, 0], [False, 0, 0], [False, 0, 0], #red
                           [False, 0, 0], [False, 0, 0], [False, 0, 0], #yellow
                           [False, 0, 0], [False, 0, 0], [False, 0, 0], #green
                           [False, 0, 0], [False, 0, 0]] #dark blue
    self.houseNum = 0
    self.hotelNum = 0
    #whether the player owns the whole set or not
    self.playerSets = {'brown':False, 'light_blue':False, 'purple':False, 'orange':False, 'red':False, 'yellow':False, 'green':False, 'dark_blue':False}
    #whether the player owns the railroads
    self.playerRailroad = [False, False, False, False]
    self.railroadNum = 0
    #whether the player owns the utilities
    self.playerUtilities = [False, False]
    self.utilitiesNum = 0
    #whether the properties are mortgaged or not
    self.mortgaged = [False, False, #brown
                      False, False, False, #light blue
                      False, False, False, #purple
                      False, False, False, #orange
                      False, False, False, #red
                      False, False, False, #yellow
                      False, False, False, #green
                      False, False, #dark blue
                      False, False, False, False, #railroads (order based on the order shown in Overview)
                      False, False] #utilities (order based on the order shown in Overview)
    self.freeJail = False #free out of jail

  def getPosition(self):
    return self.position

  def checkPlayerTurn(self):
    return self.isPlayerTurn

  def getPlayerSymbol(self):
    return self.playerSymbol

  def getCash(self):
    return self.cash

  def getJail(self):
    return self.jail

  def getWasJailed(self):
    return self.wasJailed

  def getHouse(self, propertynum):
    return self.playerProperty[propertynum][1]

  def getHotel(self,propertynum):
    return self.playerProperty[propertynum][2]

  def getRailroadNum(self):
    return self.railroadNum

  def getUtilitiesNum(self):
    return self.utilitiesNum

  def getFreeJail(self):
    return self.freeJail

  def getHouseNum(self):
    return self.houseNum

  def getHotelNum(self):
    return self.hotelNum

  def getDiceJail(self):
    return self.diceJail

  def setDiceJail(self, count):
    self.diceJail = count

  def addPosition(self, movecount):
    self.position += movecount
    while self.position > 39:
      self.position -= 40
      self.passGo()

  def setPosition(self, position):
    # pass go
    if self.position > position or position == 0:
      self.passGo()
    self.position = position


  def passGo(self):
    # if was not jailed
    if self.wasJailed == False:
      print("Pass Go! Collect 200")
      self.earn(200)
    # if jailed
    else:
      self.setWasJailed()

  def setPlayerTurn(self):
    self.isPlayerTurn = not self.isPlayerTurn

  def addProperty(self, propertynum):
    self.playerProperty[propertynum][0] = True
    if self.playerProperty[0][0] == True and self.playerProperty[1][0] == True:
      self.playerSets['brown'] = True
    if self.playerProperty[2][0] == True and self.playerProperty[3][0] == True and self.playerProperty[4][0] == True:
      self.playerSets['light_blue'] = True
    if self.playerProperty[5][0] == True and self.playerProperty[6][0] == True and self.playerProperty[7][0] == True:
      self.playerSets['purple'] = True
    if self.playerProperty[8][0] == True and self.playerProperty[9][0] == True and self.playerProperty[10][0] == True:
      self.playerSets['orange'] = True
    if self.playerProperty[11][0] == True and self.playerProperty[12][0] == True and self.playerProperty[13][0] == True:
      self.playerSets['red'] = True
    if self.playerProperty[14][0] == True and self.playerProperty[15][0] == True and self.playerProperty[16][0] == True:
      self.playerSets['yellow'] = True
    if self.playerProperty[17][0] == True and self.playerProperty[18][0] == True and self.playerProperty[19][0] == True:
      self.playerSets['green'] = True
    if self.playerProperty[20][0] == True and self.playerProperty[21][0] == True:
      self.playerSets['dark_blue'] = True

  def addHouseHotel(self, propertynum):
    if self.getHouse(propertynum) == 4:
      self.playerProperty[propertynum][1] = 0
      self.addHotel(propertynum)
      self.houseNum -= 4
    else:
      self.playerProperty[propertynum][1] += 1
      self.houseNum += 1

  def addHotel(self, propertynum):
    self.playerProperty[propertynum][2] += 1
    self.hotelNum += 1

  def addRailroad(self, railroadnum):
    self.playerRailroad[railroadnum] = True
    self.railroadNum += 1

  def addUtilities(self, utilitynum):
    self.playerUtilities[utilitynum] = True
    self.utilitiesNum += 1

  def earn(self, amount):
    self.cash += amount
    print(self.name, "current cash:", self.cash)

  def setCash(self, amount):
    self.cash = amount
    print(self.name, "current cash:", self.cash)

  def setJail(self):
    self.jail = not self.jail

  def setWasJailed(self):
    self.wasJailed = not self.wasJailed

  def setMortgaged(self, propertynum):
    self.mortgaged[propertynum] = not self.mortgaged[propertynum]

  def setFreeJail(self):
    self.freeJail = not self.freeJail
    
    

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
            player_array[i, 2] = ((2 * player.position)/40)-1
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
            property_array[i, 1] = ((2 * self.board.index(property))/40 ) -1
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
            railroad_array[i, 1] = ((2 * self.board.index(railroad))/40 ) -1
            railroad_array[i, 2] = ((2 * railroad.price)/max_price_scale) -1
            railroad_array[i, 3] = ((2 * railroad.rent)/max_price_scale) -1
            railroad_array[i, 4] = ((2 * property.totalRailroad)/4) -1

        # Create the utility array with zeros
        utility_array = np.zeros((num_utilities, num_utilities_features), dtype=float)
        # Add utility-related information
        for i, utility in enumerate(self.utilities):
            # Update utility features
            utility_array[i, 0] = utility.pieceType/num_players if utility.occupied == True else -1
            utility_array[i, 1] = ((2 * self.board.index(utility))/40) -1
            utility_array[i, 2] = ((2 * utility.price)/max_price_scale) -1
            utility_array[i, 3] = int(property.utilities)

        # Concatenate the arrays into the observation
        observation = np.concatenate((player_array.flatten(), property_array.flatten(), railroad_array.flatten(), utility_array.flatten()))

        return observation


    @property
    def legal_actions(self):
        current_player = self.current_player
        legal_actions = []
        
        # Iterate through properties
        for index, tile in enumerate(self.board):
            # railroads
            tile_action = []
            if index in [10]:
                # jail
                # roll dice, pay
                legal_actions.append([1,1] if ((current_player.jail == True) and (current_player.diceJail < 3)) else [0,0])
            elif index in [5, 15, 25, 35]:
                # buy railroad
                tile_action.append(1 if tile.occupied == False else 0)
            # utilities
            elif index in [12, 28]:
                # buy utilities
                tile_action.append(1 if tile.occupied == False else 0)
            # properties
            elif index in [1,3,6,7,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                # buy property
                tile_action.append(1 if tile.occupied == False else 0)
                if tile.pieceType == current_player.playerSymbol:
                    if tile.mortgaged == False:
                        # buy house
                        tile_action.append(1 if tile.houseNum<4 else 0)
                        # buy hotel
                        tile_action.append(1 if ((tile.houseNum == 4) and (tile.hotelNum == 0)) else 0)
                        # buy back
                        tile_action.append(0)
                    else:
                        tile_action.append([0,0,1])
                else:
                    tile_action.append([0,0,0])
                ######## only land on the tile can do the action? should add that and else 0?

                legal_actions.append(tile_action)
                ####### add empty array or nothing

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

    @property
    def current_player(self):
        return self.players[self.current_player_num]


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