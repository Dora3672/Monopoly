
import gym
import numpy as np

import config

from stable_baselines import logger

import random

from array import *

class Dice:
  def __init__(self):
    self.min=1
    self.max=6
    self.currentnum=random.randint(self.min,self.max)

  def randomnum(self):
    self.currentnum=random.randint(self.min,self.max)
    return self.currentnum

  def __str__(self):
    return str(self.currentnum)

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


class Tile:
  def __init__(self):
    self.hasPiece = False
    # player number
    self.pieceType = 0

## Getter Functions
  def getPieceType(self):
    return self.pieceType

  def checkHasPiece(self):
    return self.hasPiece

## Setter Function
  def setPiece(self, newPiece):
    self.hasPiece = True
    self.pieceType = newPiece  


class PropertyTile(Tile):
  #color = number starts from 1
  def __init__(self, color, pprice, position):
    self.position = position
    self.once = False #whether the if statement in the sent rent function is called or not
    self.occupied = False #whether the property is occupied or not
    self.color = color
    self.price = pprice #the cost to buy the property
    self.rent = (pprice/10) - 4
    self.rentWOneHouse = (pprice/2) - 20 #rent with one house
    self.house = 0 #number of house
    self.hotel = 0 #number of hotel
    self.hhcosts = [50, 100, 100, 150, 150, 150, 200, 200]
    self.househotelCosts = self.hhcosts[color] #costs for houses and hotels
    self.colorset = False #whether the colorset is full or not
    self.mortgaged = False
    self.mortgageprice = pprice/2
    self.mortgagedPayPrice = 1.1 * self.mortgageprice #price to get back the mortgaged property
    self.diceroll = 0
    super().__init__()

  def getOccupied(self):
    return self.occupied

  def getColor(self):
    return self.color

  def getPrice(self):
    return self.price

  def getOwner(self):
    return self.pieceType

  def getRent(self):
    self.setRent()
    if self.mortgaged == True:
      return 0
    return self.rent

  def getHouse(self):
    return self.house

  def getHotel(self):
    return self.hotel

  def getColorSet(self):
    return self.colorset

  def getOccupied(self):
    return self.occupied

  def getMortgagePrice(self):
    return self.mortgageprice

  def getMortgaged(self):
    return self.mortgaged

  def getMortgagedPayPrice(self):
    return self.mortgagedPayPrice

  def getHouseHotelPrice(self):
    return self.househotelCosts

  def setOccupied(self):
    self.occupied = not self.occupied

  def setOwner(self, pieceType):
    self.pieceType = pieceType
    self.setOccupied()

  def setPrice(self, price):
    self.price = price

  def setRent(self):
    if self.colorset == True and self.once == False:
      self.rent = self.rent*2
      self.once = True
    else:
      if self.house == 1:
        self.rent = self.rentWOneHouse
      elif self.house == 2:
        self.rent = 3 * self.rentWOneHouse
      elif self.house == 3:
        self.rent = 50 * round((140 + (6 * self.rentWOneHouse)) / 50)
      elif self.house == 4:
        self.rent = 25 * round((210 + (7 * self.rentWOneHouse)) / 25)
      elif self.hotel == 1:
        self.rent = 25 * round((600 + (5 * self.rentWOneHouse)) / 25)

  def setHouse(self):
    if self.house == 4:
      self.house = 0
      self.setHotel() ##house max, then call set hotel
    elif self.house < 4 and self.house == 0:
      self.house += 1

  def setHotel(self):
    if self.hotel == 0:
      self.hotel += 1

  def setColorSet(self):
    self.colorset = not self.colorset ##owner needs to be the same (in main, if the user has all set, colorset is true)

  def setMortgaged(self):
    self.mortgaged = not self.mortgaged


class RailroadTile(Tile):
  def __init__(self, position):
    self.position = position
    self.occupied = False #whether the property is occupied or not
    self.price = 200 #the cost to buy the property
    self.rent = 25
    self.totalRailroad = 0 #number of total railroads
    super().__init__()

  def getOccupied(self):
    return self.occupied

  def getPrice(self):
    return self.price

  def getOwner(self):
    return self.pieceType

  def getRent(self):
    self.setRent()
    return self.rent

  def getNumberRailroads(self):
    return self.totalRailroad

  def setOccupied(self):
    self.occupied = not self.occupied

  def setOwner(self, pieceType):
    self.pieceType = pieceType
    self.setOccupied()
    self.setRailroadNum()

  def setRent(self):
    self.rent = 25 * (2 ** (self.totalRailroad - 1))

  def setRailroadNum(self):
    self.totalRailroad += 1


class UtilityTile(Tile):
  def __init__(self, position):
    self.position = position
    self.occupied = False #whether the property is occupied or not
    self.price = 150 #the cost to buy the property
    self.utilities = False #whether the player owns the two utilities or not
    super().__init__()

  def getOccupied(self):
    return self.occupied

  def getPrice(self):
    return self.price

  def getOwner(self):
    return self.pieceType

  def getRent(self, diceroll):
    if self.utilities == False:
      return 4 * diceroll
    else:
      return 10 * diceroll

  def getUtilities(self):
    return self.utilities

  def setOccupied(self):
    self.occupied = not self.occupied

  def setOwner(self, pieceType):
    self.pieceType = pieceType
    self.setOccupied()

  def setUtilities(self):
    self.utilities = not self.utilities


import pandas as pd
import random

class CChestTile(Tile):
  def __init__(self):
    super().__init__()
    self.ccnum = 0 #random cc index
    self.communityChest = {
        "Text":{
            0:"You set aside time every week to hang out with your elderly neighbor – you’ve heard some amazing stories! COLLECT $100.",
            1:"You organize a group to clean up your town’s footpaths. COLLECT $50.",
            2:"You volunteered at a blood donation. There were free cookies! COLLECT $10.",
            3:"You buy a few bags of cookies from that school bake sale. Yum! PAY $50.",
            4:"You rescue a puppy – and you feel rescued, too! GET OUT OF JAIL FREE. Keep this card until needed, traded, or sold.",
            5:"You organize a street party so people on your road can get to know each other. COLLECT $10 FROM EACH PLAYER.",
            6:"Blasting music late at night? Your neighbors do not approve. GO TO JAIL. DO NOT PASS GO. DO NOT COLLECT $200.",
            7:"You help your neighbor bring in her groceries. She makes you lunch to say thanks! COLLECT $20.",
            8:"You help build a new school playground – then you get to test the slide! COLLECT $100.",
            9:"You spend the day playing games with kids at a local children’s hospital. COLLECT $100.",
            10:"You go to the local school’s car wash fundraiser – but you forget to close your windows! PAY $100.",
            11:"Just when you think you can’t go another step, you finish that foot race – and raise money for your local hospital! ADVANCE TO GO. COLLECT $200.",
            12:"You help your neighbors clean up their Gardens after a big storm. COLLECT $200.",
            13:"Your fuzzy friends at the animal shelter will be thankful for your donation. PAY $50.",
            14:"You should have volunteered for that home improvement project – you would have learned valuable skills! FOR EACH HOUSE YOU OWN, PAY $40. FOR EACH HOTEL YOU OWN, PAY $115.",
            15:"You organize a bake sale for your local school. COLLECT $25."
        },

        "PlayerEarn":{
            0:100,
            1:50,
            2:10,
            3:-50,
            4:0,
            5:10,
            6:0,
            7:20,
            8:100,
            9:100,
            10:-100,
            11:0,
            12:0,
            13:-50,
            14:0,
            15:25
        },

        "OtherEachEarn":{
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:0,
            6:-10,
            7:0,
            8:0,
            9:0,
            10:0,
            11:0,
            12:0,
            13:0,
            14:0,
            15:0,
        }
    }

  def landCC(self):
    self.cc = pd.DataFrame(self.communityChest)
    self.ccnum = random.randint(0, 15)
    return (
        self.ccnum,
        self.cc.loc[self.ccnum, 'Text'],
        self.cc.loc[self.ccnum, 'PlayerEarn'],
        self.cc.loc[self.ccnum, 'OtherEachEarn']
    )


import pandas as pd
import random

class chanceTile(Tile):
  def __init__(self):
    super().__init__()
    self.cnum = 0 #random chance index
    self.chance = {
        "Text":{
            0:"Advance to 'Go'.",
            1:"Advance to Illinois Ave. If you pass Go, collect $200.",
            2:"Advance to St. Charles Place. If you pass Go, collect $200.",
            3:"Advance token to the nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total 10 (ten) times the amount thrown.",
            4:"Advance to the nearest Railroad. If unowned, you may buy it from the Bank. If owned, pay owner twice the retal to which they are otherwise entitled. If Railroad is unowned, you may buy it from the Bank.",
            5:"Bank pays you dividend of $50.",
            6:"Get out of Jail Free. This card may be kept until needed, or traded/sold.",
            7:"Go Back Three Spaces.",
            8:"Go to Jail. Go directly to Jail. Do not pass GO, do not collect $200. ",
            9:"Make general repairs on all your property: For each house pay $25, For each hotel {pay} $100.",
            10:"Take a trip to Reading Railroad. If you pass Go, collect $200.",
            11:"Take a walk on the Boardwalk. Advance token to Boardwalk.",
            12:"You have been elected Chairman of the Board. Pay each player $50.",
            13:"Your building loan matures. Receive $150.",
        },

        "Earn":{
            0:0,
            1:0,
            2:0,
            3:0,
            4:0,
            5:50,
            6:0,
            7:0,
            8:0,
            9:0,
            10:0,
            11:0,
            12:0,
            13:150,
        },

        "Position":{
            0:0,
            1:24,
            2:16,
            3:[12, 28],
            4:[5, 15, 25, 35],
            5:'',
            6:'',
            7:'',
            8:30,
            9:'',
            10:5,
            11:39,
            12:'',
            13:''
        }
    }

  def landC(self):
    self.c = pd.DataFrame(self.chance)
    self.cnum = random.randint(0, 13)
    return (
        self.cnum,
        self.c.loc[self.cnum, 'Text'],
        self.c.loc[self.cnum, 'Earn'],
        self.c.loc[self.cnum, 'Position']
    )


class MonopolyEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(TicTacToeEnv, self).__init__()
        self.name = 'tictactoe'
        self.manual = manual
        
        self.n_players = 2
        self.num_squares = 40 
        ########
        #self.action_space = gym.spaces.Discrete(self.num_squares)
        # each element is thenum of possible action for that tile
        self.possible_actions = [0,8,0,8,0,2,8,0,8,8,2,8,2,8,8,2,8,0,8,8,0,8,0,8,8,2,8,8,2,8,0,8,8,0,8,2,0,8,0,8]
        self.action_space = spaces.MultiDiscrete(self.possible_actions)
        ########
        #self.observation_space = gym.spaces.Box(-1, 1, (self.num_squares, 2))
        self.num_property_features = 12  # Number of property-related features
        self.num_railroads_features = 5  # Number of features for railroads
        self.num_utilities_features = 4  # Number of features for utilities
        self.num_player_features = 13  # Number of player-related features

        self.num_players = len(self.players)
        self.num_properties = len(self.properties)
        self.num_railroads = len(self.railroads)
        self.num_utilities = len(self.utilities)
        self.total_elements = (self.num_players * self.num_player_features) + (self.num_properties * self.num_property_features) + (self.num_railroads * self.num_railroads_features) + (self.num_utilities * self.num_utilities_features)
        self.observation_shape = (self.total_elements,)
        self.observation_space = spaces.Box(low=-1, high=1, shape=self.observation_shape)
        
        self.verbose = verbose

        #board
        self.mAvenue = PropertyTile(0, 60, 1)
        self.bAvenue = PropertyTile(0, 60, 3)
        self.oAvenue = PropertyTile(1, 100, 6)
        self.verAvenue = PropertyTile(1, 100, 8)
        self.cAvenue = PropertyTile(1, 120, 9)
        self.sCPlace = PropertyTile(2, 140, 11)
        self.sAvenue = PropertyTile(2, 140, 13)
        self.viAvenue = PropertyTile(2, 160, 14)
        self.sJPlace = PropertyTile(3, 180, 16)
        self.tAvenue = PropertyTile(3, 180,18)
        self.nYAvenue = PropertyTile(3, 200,19)
        self.kAvenue = PropertyTile(4, 220,21)
        self.inAvenue = PropertyTile(4, 220,23)
        self.ilAvenue = PropertyTile(4, 240,24)
        self.aAvenue = PropertyTile(5, 260,26)
        self.venAvenue = PropertyTile(5, 260,27)
        self.mGardens = PropertyTile(5, 280,29)
        self.paAvenue = PropertyTile(6, 300,31)
        self.nCAvenue = PropertyTile(6, 300,32)
        self.peAvenue = PropertyTile(6, 320,34)
        self.pPlace = PropertyTile(7, 350,37)
        self.bw = PropertyTile(7, 400,39)
        self.properties = [self.mAvenue, self.bAvenue,
                        self.oAvenue, self.verAvenue, self.cAvenue,
                        self.sCPlace, self.sAvenue, self.viAvenue,
                        self.sJPlace, self.tAvenue, self.nYAvenue,
                        self.kAvenue, self.inAvenue, self.ilAvenue,
                        self.aAvenue, self.venAvenue, self.mGardens,
                        self.paAvenue, self.nCAvenue, self.peAvenue,
                        self.pPlace, self.bw]
        self.boardnames = ['Pass Go! Collect 200', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 'Income Tax', 'Reading Railroad', 'Oriental Avenue', 'Chance', 'Vermont Avenue', 'Connecticut Avenue',
                        'Just Visiting', 'St. Charles Place', 'Electric Company', 'States Avenue', 'Virginia Avenue', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 'Tennessee Avenue', 'New York Avenue',
                        'Free Parking', 'Kentucky Avenue', 'Chance', 'Indiana Avenue', 'Illinois Avenue', 'B&O Railroad', 'Atlantic Avenue', 'Ventor Avenue', 'Water Works', 'Marvin Gardens',
                        'Go to Jail!', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue', 'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk']
        self.propertynames = ["Mediterranean Avenue", "Baltic Avenue",
                            "Oriental Avenue", "Vermont Avenue", "Connecticut Avenue",
                            "St. Charles Place", "States Avenue", "Virginia Avenue",
                            "St. James Place", "Tennessee Avenue", "New York Avenue",
                            "Kentucky Avenue", "Indiana Avenue", "Illinois Avenue",
                            "Atlantic Avenue", "Ventnor Avenue", "Marvin Gardens",
                            "Pacific Avenue", "North Carolina Avenue", "Pennsylvania Avenue",
                            "Park Place", "Boardwalk"]
        self.colors = ['brown', 'light_blue', 'purple', 'orange', 'red', 'yellow', 'green', 'dark_blue']
        self.sets = [[self.mAvenue, self.bAvenue],
                    [self.oAvenue, self.verAvenue, self.cAvenue],
                    [self.sCPlace, self.sAvenue, self.viAvenue],
                    [self.sJPlace, self.tAvenue, self.nYAvenue],
                    [self.kAvenue, self.inAvenue, self.ilAvenue],
                    [self.aAvenue, self.venAvenue, self.mGardens],
                    [self.paAvenue, self.nCAvenue, self.peAvenue],
                    [self.pPlace, self.bw]]

        self.communityChest=CChestTile()
        self.chance = chanceTile()
        self.electricCompany = UtilityTile(12)
        self.waterWorks = UtilityTile(28)
        self.utilities = [self.electricCompany, self.waterWorks]
        self.utilitynames = ["Electric Company", "Water Works"]
        self.rRailroad = RailroadTile(5)
        self.pRailroad = RailroadTile(15)
        self.bRailroad = RailroadTile(25)
        self.sLine = RailroadTile(35)
        self.railroads = [self.rRailroad, self.pRailroad, self.bRailroad, self.sLine]
        self.railroadnames = ["Reading Railroad", "Pennsylvania Railroad", "B&O Railroad", "Short Line"]

        self.board = [Tile(), self.mAvenue, self.communityChest, self.bAvenue, Tile(), self.rRailroad, self.oAvenue, self.chance, self.verAvenue, self.cAvenue,
                    Tile(), self.sCPlace, self.electricCompany, self.sAvenue, self.viAvenue, self.pRailroad, self.sJPlace, self.communityChest, self.tAvenue, self.nYAvenue,
                    Tile(), self.kAvenue, self.chance, self.inAvenue, self.ilAvenue, self.bRailroad, self.aAvenue, self.venAvenue, self.waterWorks, self.mGardens,
                    Tile(), self.paAvenue, self.nCAvenue, self.communityChest, self.peAvenue, self.sLine, self.chance, self.pPlace, Tile(), self.bw]



        self.current_player_num = 0
        self.players = Player(0, '1'), Player(1, '-1')


        self.done = False
        self.next = False   # will have a next round (False no)
        self.roll = True   # next round roll? (False no)
        

    @property
    def observation(self):
        # if game continues, do the actions to go to the next round
        index, worth = self.calculateWorth()        
        if worth <= 0:
          self.turn()


        max_price_scale = 1e6  # Choose a very large value as the max price scale

        # Create the player array with zeros
        player_array = np.zeros((self.num_players, self.num_player_features), dtype=float)
        # Update the player array for each player
        for i, player in enumerate(self.players):
            # Update player features
            player_array[i, 0] = player.playerNum/self.num_players
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
        property_array = np.zeros((self.num_properties, self.num_property_features), dtype=float)
        # Add property-related information
        for i, property in enumerate(self.properties):
            # Update property features
            property_array[i, 0] = property.pieceType/self.num_players if property.occupied == True else -1
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
        railroad_array = np.zeros((self.num_railroads, self.num_railroads_features), dtype=float)
        # Add railroad-related information
        for i, railroad in enumerate(self.railroads):
            # Update railroad features
            railroad_array[i, 0] = railroad.pieceType/self.num_players if railroad.occupied == True else -1
            railroad_array[i, 1] = ((2 * self.board.index(railroad))/40 ) -1
            railroad_array[i, 2] = ((2 * railroad.price)/max_price_scale) -1
            railroad_array[i, 3] = ((2 * railroad.rent)/max_price_scale) -1
            railroad_array[i, 4] = ((2 * property.totalRailroad)/4) -1

        # Create the utility array with zeros
        utility_array = np.zeros((self.num_utilities, self.num_utilities_features), dtype=float)
        # Add utility-related information
        for i, utility in enumerate(self.utilities):
            # Update utility features
            utility_array[i, 0] = utility.pieceType/self.num_players if utility.occupied == True else -1
            utility_array[i, 1] = ((2 * self.board.index(utility))/40) -1
            utility_array[i, 2] = ((2 * utility.price)/max_price_scale) -1
            utility_array[i, 3] = int(property.utilities)

        # Concatenate the arrays into the observation
        observation = np.concatenate((player_array.flatten(), property_array.flatten(), railroad_array.flatten(), utility_array.flatten()))
      
        return observation


  def turn(self, playern):
    player=self.players[playern]
    self.current_player = player
    self.next = False

    # if in jail and still can try to get out of jail free
    if player.getJail() == True and player.diceJail < 3:
      # if have free jail card
      if player.getFreeJail() == True:
        player.setFreeJail()
      # player make decision about paying or rolling
    # if in jail and cannot get out of jail free
    elif player.jail == True and player.diceJail == 3:
      self.end = self.bankrupt(-50, playern)
      player.diceJail = 0
      # player do nothing
    # not in jail
    else:
      # did not move there because of chance/community chest, roll dice
      if self.roll == True:

        # roll the dice
        self.d1.randomnum()
        self.d2.randomnum()
        self.dice_roll = self.d1.currentnum + self.d2.currentnum
        player.diceroll = self.dice_roll

        # rolling doubles
        if self.d1.currentnum == self.d2.currentnum:
          self.next = True
          player.rollingdoubles += 1
        else:
          player.rollingdoubles = 0
        if player.rollingdoubles == 3:
          player.wasJailed = True
          player.setPosition(10)
          player.wasJailed = True
          player.jail = True
          player.rollingdoubles = 0

      # move the player
      if self.roll == True:
        player.addPosition(self.dice_roll)
      self.roll = True
      position = player.getPosition()

      if position == 0:
        pass
      # community chest
      elif position in [2, 17, 33]:
        ccnum, text, selfEarn, otherEarn = self.communityChest.landCC()
        if ccnum == 5:
          self.bankrupt(selfEarn * (self.playerNum-1), playern)
        else:
          if selfEarn != 0:
            self.bankrupt(selfEarn, playern)
        if otherEarn != 0:
          for p in range(self.playerNum):
            if p != playern:
              e = self.end
              self.bankrupt(otherEarn, p)

        # free jail card
        if ccnum == 4:
          player.freeJail = True
        # go to jail
        elif ccnum == 6:
          player.wasJailed = True
          player.setPosition(10)
          player.wasJailed = True
          player.jail = True
        # go to Go
        elif ccnum == 11:
          player.setPosition(0)
          self.next = True
          self.roll = False
          self.turns_taken -=1
        # pay for houses and hotels
        elif ccnum == 14:
          if player.houseNum != 0 and player.hotelNum != 0:
            self.bankrupt(-(player.getHouseNum() * 40 + player.getHotelNum() * 115), playern)

      # chance
      elif position in [7, 22, 36]:
        cnum, text, earning, newposition = self.chance.landC()

        # moves
        # if advance to a specific property
        if cnum in [0, 1, 2, 10, 11]:
          player.setPosition(newposition)
          self.next = True
          self.roll = False
          self.turns_taken -=1
        # if advance to the nearest something
        elif cnum in [3, 4]:
          # utilities
          if cnum == 3:
            self.closest([12, 28], position, playern)
            newposition = player.position
            utility = self.electricCompany if newposition == 12 else self.waterWorks
            if utility.occupied == False or ((player.playerUtilities[0] == True if newposition == 12 else player.playerUtilities[1] == True)):
              self.next = True
              self.turns_taken -= 1
            elif utility.mortgaged == True:
              pass
            else:
              self.d1.randomnum()
              self.d2.randomnum()
              self.dice_roll = self.d1.currentnum + self.d2.currentnum
              player.diceroll = self.d1.currentnum + self.d2.currentnum
              self.bankrupt(-(10 * self.dice_roll), playern)
              self.bankrupt((10 * self.dice_roll), int(utility.pieceType))
          # railroad
          else:
            self.closest([5, 15, 25, 35], position, playern)
            newposition = player.position
            railroad = self.railroads[[5, 15, 25, 35].index(newposition)]
            if railroad.occupied == False or (player.playerRailroad[[5, 15, 25, 35].index(newposition)] == True):
              self.next = True
              self.turns_taken -= 1
            elif railroad.mortgaged == True:
              pass
            else:
              self.bankrupt(-(railroad.rent * 2), playern)
              self.bankrupt((railroad.rent * 2), int(railroad.pieceType))

        # if advance to jail
        elif cnum == 8:
          player.wasJailed = True
          player.setPosition(10)
          player.wasJailed = True
          player.jail = True
        # move back three spaces
        elif cnum == 7:
          player.addPosition(-3)
          self.next = True
          self.roll = False
          self.turns_taken -=1


        # change in money
        # earn money
        if cnum in [5, 13]:
          self.bankrupt(earning, playern)
        # pay by house num and hotel num
        elif cnum == 9:
          if player.houseNum != 0 or player.hotelNum != 0:
            self.bankrupt(-(player.getHouseNum() * 25 + player.getHotelNum() * 100), playern)
        # pay to each player
        elif cnum == 12:
           self.bankrupt(- (50 * (self.playerNum-1)), playern)
          for p in range(self.playerNum):
            if p != playern:
              self.bankrupt(50, p)

      # tax
      elif position in [4, 38]:
        tax = 200 if position == 4 else 100
        self.bankrupt(-tax, playern)

      # railroads
      elif position in [5, 15, 25, 35]:
        railroad = self.railroads[[5, 15, 25, 35].index(position)]
        if railroad.occupied == True and player.playerRailroad[[5, 15, 25, 35].index(position)] == False:
          self.bankrupt(-(railroad.getRent()), playern)
          self.bankrupt((railroad.getRent()), int(railroad.pieceType))
          # player makes decision about buying

      # utilities
      elif position in [12, 28]:
        utility = self.utilities[[12, 28].index(position)]
        if utility.occupied == True and player.playerUtilities[[12, 28].index(position)] == False:
          self.bankrupt(-(utility.getRent(self.dice_roll)), playern)
          self.bankrupt((utility.getRent(self.dice_roll)), int(utility.pieceType))
        # player makes decision about buying

      # do nothing
      elif position in [10, 20]:
        pass

      # prison
      elif position == 30:
        player.wasJailed = True
        player.setPosition(10)
        player.wasJailed = True
        player.jail = True

      # properties
      else:
        prop = self.board[position]
        # property already being bought, player not the owner, not mortaged
        if prop.occupied == True and self.board[position].pieceType != playern and prop.mortgaged == False:
          self.bankrupt(-(prop.getRent()), playern)
          self.bankrupt((prop.getRent()), int(prop.pieceType))
        # player make choices about buying properties, houses/hotels and buy back mortgage


  def closest(self, newposition, position, playern):
    player = self.players[playern]
    # find the place that is closest to the player
    finalposition = newposition[0]
    for place in newposition:
      if (place - position) < (finalposition - position):
        finalposition = place
    if finalposition < position:
      player.setWasJailed()
    player.setPosition(finalposition)


  def bankrupt(self, moneyneed, playern):
    player = self.players[playern]
    if moneyneed > 0:
      player.earn(moneyneed)
    else:
      if player.cash > -(moneyneed):
        player.earn(moneyneed)
      else:
        moneyneed += player.cash
        player.setCash(0)
        totalmortgage = []
        indices = []
        for i in range(22):
          if player.playerProperty[i][0] == True and player.mortgaged[i] == False:
            totalmortgage.append(self.properties[i].mortgageprice)
            indices.append(i)
        combination = self.find_combination(totalmortgage, -(moneyneed))
        for mprice in combination:
          for i in indices:
            if self.properties[i].mortgageprice == mprice and self.properties[i].mortgaged == False:
              player.earn(mprice)
              player.playerProperty[i][0] = False
              player.houseNum -= player.playerProperty[i][1]
              player.hotelNum -= player.playerProperty[i][2]
              self.properties[i].mortgaged = True
              player.setMortgaged(i)
              break
        player.earn(moneyneed)


    # first one yes, second one no
    @property
    def legal_actions(self):
        current_player = self.current_player
        legal_actions = []
        # buy MA (0), not buy MA (1), buy house (2), not buy house (3), buy hotel (4), not buy hotel (5), buy back (6), not buy back (7),
        # buy BA (8), not buy BA (9), buy house (10), not buy house (11), buy hotel (12), not buy hotel (13), buy back (14), not buy back (15),
        # buy RR (16), not buy RR (17),
        # buy OA (18), not buy OA (19), buy house (20), not buy house (21), buy hotel (22), not buy hotel (23), buy back (24), not buy back (25),
        # buy VerA (26), not buy (27), buy house (28), not buy house (29), buy hotel (30), not buy hotel (31), buy back (32), not buy back (33),
        # buy SA (34), not buy (35), buy house (36), not buy house (37), buy hotel (38), not buy hotel (39), buy back (40), not buy back (41),
        # roll dice free jail (42), pay jail (43),
        # buy SCP (44), not buy (45), buy house (46), not buy house (47), buy hotel (48), not buy hotel (49), buy back (50), not buy back (51),
        # buy EC (52), not buy (53),
        # buy SA (54), not buy (55), buy house (56), not buy house (57), buy hotel (58), not buy hotel (59), buy back (60), not buy back (61),
        # buy ViA (62), not buy (63), buy house (64), not buy house (65), buy hotel (66), not buy hotel (67), buy back (68), not buy back (69),
        # buy PR (70), not buy (71),
        # buy SJP (72), not buy (73), buy house (74), not buy house (75), buy hotel (76), not buy hotel (77), buy back (78), not buy back (79),
        # buy TA (80), not buy (81), buy house (82), not buy house (83), buy hotel (84), not buy hotel (85), buy back (86), not buy back (87),
        # buy NYA (88), not buy (89), buy house (90), not buy house (91), buy hotel (92), not buy hotel (93), buy back (94), not buy back (95),
        # buy KA (96), not buy (97), buy house (98), not buy house (99), buy hotel (100), not buy hotel (101), buy back (102), not buy back (103),
        # buy InA (104), not buy (105), buy house (106), not buy house (107), buy hotel (108), not buy hotel (109), buy back (110), not buy back (111),
        # buy IlA (112), not buy (113), buy house (114), not buy house (115), buy hotel (116), not buy hotel (117), buy back (118), not buy back (119),
        # buy BOR (120), not buy (121),
        # buy AA (122), not buy (123), buy house (124), not buy house (125), buy hotel (126), not buy hotel (127), buy back (128), not buy back (129),
        # buy VenA (130), not buy (131), buy house (132), not buy house (133), buy hotel (134), not buy hotel (135), buy back (136), not buy back (137),
        # buy WW (138), not buy (139),
        # buy MG (140), not buy (141), buy house (142), not buy house (143), buy hotel (144), not buy hotel (145), buy back (146), not buy back (147),
        # buy PaA (148), not buy (149), buy house (150), not buy house (151), buy hotel (152), not buy hotel (153), buy back (154), not buy back (155),
        # buy NCA (156), not buy (157), buy house (158), not buy house (159), buy hotel (160), not buy hotel (161), buy back (162), not buy back (163),
        # buy PeA (164), not buy (165), buy house (166), not buy house (167), buy hotel (168), not buy hotel (169), buy back (170), not buy back (171),
        # buy SLR (172), not buy (173),
        # buy PP (174), not buy (175), buy house (176), not buy house (177), buy hotel (178), not buy hotel (179), buy back (180), not buy back (181),
        # buy B (182), not buy (183), buy house (184), not buy house (185), buy hotel (186), not buy hotel (187), buy back (188), not buy back (189),
        # nothing (190)

        


        # Iterate through properties
        for index, tile in enumerate(self.board):
            # railroads
            tile_action = []
            if index in [10]:
                # jail
                # roll dice, pay
                tile_action.append(1 if ((current_player.jail == True) and (current_player.diceJail < 3) and (current_player.position == 10)) else 0)
                tile_action.append(1 if ((current_player.jail == True) and (current_player.diceJail < 3) and (current_player.position == 10)) else 0)
            elif index in [5, 15, 25, 35] :
                # buy railroad
                tile_action.append(1 if (tile.occupied == False and current_player.position in [5,15,25,35]) else 0)
                tile_action.append(1 if (tile.occupied == False and current_player.position in [5,15,25,35]) else 0)
            # utilities
            elif index in [12, 28]:
                # buy utilities
                tile_action.append(1 if (tile.occupied == False and current_player.position in [12, 28]) else 0)
                tile_action.append(1 if (tile.occupied == False and current_player.position in [12, 28]) else 0)
            # properties
            elif index in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]:
                # buy property
                tile_action.append(1 if tile.occupied == False else 0)
                tile_action.append(1 if tile.occupied == False else 0)
                if tile.pieceType == current_player.playerSymbol and current_player.position == index:
                    if tile.mortgaged == False:
                        # buy house
                        tile_action.append(1 if tile.houseNum<4 else 0)
                        tile_action.append(1 if tile.houseNum<4 else 0)
                        # buy hotel
                        tile_action.append(1 if ((tile.houseNum == 4) and (tile.hotelNum == 0)) else 0)
                        tile_action.append(1 if ((tile.houseNum == 4) and (tile.hotelNum == 0)) else 0)
                        # buy back
                        tile_action.append(0)
                        tile_action.append(0)
                    else:
                        tile_action.append(0)
                        tile_action.append(0)
                        tile_action.append(0)
                        tile_action.append(0)
                        tile_action.append(1)
                        tile_action.append(1)
                else:
                    tile_action.append(0)
                    tile_action.append(0)
                    tile_action.append(0)
                    tile_action.append(0)
                    tile_action.append(0)
                    tile_action.append(0)

                legal_actions.append(tile_action)
        
        nothing = True
        for sub_array in legal_actions:
          if ((not all(item == 0 for item in sub_array)) or sub_array != [])):
            nothing = False
        
        legal_actions.append([0] if nothing == False else [1])

        legal_actions.flatten()

        return legal_actions


    def square_is_player(self, tile, player):
        return self.board[tile].pieceType == self.players[player].playerSymbol


    def calculateWorth(self):
      winindex = [0]
      winworth = [1]
      for i in range(self.playerNum):
        player = self.players[i]
        ca = player.cash
        for ii in range(len(self.properties)):
          if player.mortgaged[ii] == False and player.playerProperty[ii][0] == True:
            ca += self.properties[ii].price
            if player.playerProperty[ii][1] != 0:
              ca += (player.playerProperty[ii][1] + player.playerProperty[ii][2]) * self.properties[ii].househotelCosts
        for ii in range(len(self.railroads)):
          if player.playerRailroad[ii] == True:
            ca += 200
        for ii in range(len(self.utilities)):
          if player.playerUtilities[ii] == True:
            ca += 150
        if winworth[0] < ca:
          winindex = [i]
          winworth = [ca]
        elif winworth[0] == ca:
          winindex.append(i)
          winworth.append(ca)
        return winindex, winworth


    def check_game_over(self):
      winindex, winworth = self.calculateWorth()
      winworthsorted = sorted(winworth)
      if winworthsorted[0] <= 0 and len(winworth) == 1:
        if self.players[winindex[0]] == 1:
          return 1, True
        else:
          return 0, True
      return 0, False


    @property
    def current_player(self):
        return self.players[self.current_player_num]


    def step(self, action):
        
        reward = [0,0]
        
        # check move legality
        board = self.legal_actions()
        
        if (board[action[0]][action[1]] == 0) :  # not legal
            done = True
            reward = [1, 1]
            reward[self.current_player_num] = -1
        else:
            # railroad
            if action[1] == 0 and action[0] in [5,15,25,35]:
              railroad = self.board[action[0]]
              self.bankrupt(railroad.price, self.current_player.playerSymbol)
              railroad.setOwner(self.current_player.playerSymbol)
              self.current_player.addRailroad([5, 15, 25, 35].index(action[0]))
            # utilities
            if action[1] == 0 and action[0] in [12.28]:
              utility = self.board[action[0]]
              self.bankrupt(utility.price, self.current_player.playerSymbol)
              utility.setOwner(self.current_player.playerSymbol)
              self.current_player.addUtilities([12, 28].index(action[0]))
              if self.current_player.playerUtilities == [True, True]:
                utility.setUtilities()
            elif action[0] == 10 and action[1] == 0:
              # roll dice
              self.d1.randomnum()
              self.d2.randomnum()
              self.current_player.diceroll = self.d1.currentnum + self.d2.currentnum
              if self.d1.currentnum != self.d2.currentnum:
                self.current_player.diceJail += 1
              else:
                self.current_player.setJail()
                self.current_player.setDiceJail(0)
            elif action[0] == 10 and action[1] == 1:
              # pay out of jail
              self.bankrupt(-50, self.current_player.playerSymbol)
              self.current_player.diceJail = 0
            elif action[0] in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]:
              prop = self.board[action[0]]
              # buy property
              if action[1] == 0:
                self.bankrupt(-(prop.getPrice()), self.current_player.playerSymbol)
                prop.setOwner(self.current_player.playerSymbol)
                self.current_player.addProperty(self.properties.index(self.board[action[0]]))
                for s, owned in self.current_player.playerSets.items():
                  if owned == True:
                    for p in self.sets[self.colors.index(s)]:
                      p.setColorSet()
              if action[1] in [2,4]:
                prop.setHouse()
                self.current_player.earn(-(prop.househotelCosts))
                self.current_player.addHouseHotel(self.properties.index(self.board[action[0]]))
              elif action[1] == 6:
                self.bankrupt(-self.board[action[0]].mortgagedPayPrice, self.current_player.playerSymbol)
                self.current_player.setMortgaged(self.properties.index(self.board[action[0]]))
                self.current_player.playerProperty[(self.properties.index(self.board[action[0]])][0] = False
                self.current_player.houseNum += self.current_player.playerProperty[(self.properties.index(self.board[action[0]]))][1]
                self.current_player.hotelNum += self.current_player.playerProperty[(self.properties.index(self.board[action[0]]))][2]
                self.board[action[0]].mortgaged = False

            self.turns_taken += 1
            r, done = self.check_game_over()
            reward = [-r,-r]
            reward[self.current_player_num] = r

        self.done = done

        if not done and self.next == False:
            self.current_player_num = (self.current_player_num + 1) % 2

        return self.observation, reward, done, {}


    def reset(self):
        # reset board
        self.mAvenue = PropertyTile(0, 60, 1)
        self.bAvenue = PropertyTile(0, 60, 3)
        self.oAvenue = PropertyTile(1, 100, 6)
        self.verAvenue = PropertyTile(1, 100, 8)
        self.cAvenue = PropertyTile(1, 120, 9)
        self.sCPlace = PropertyTile(2, 140, 11)
        self.sAvenue = PropertyTile(2, 140, 13)
        self.viAvenue = PropertyTile(2, 160, 14)
        self.sJPlace = PropertyTile(3, 180, 16)
        self.tAvenue = PropertyTile(3, 180,18)
        self.nYAvenue = PropertyTile(3, 200,19)
        self.kAvenue = PropertyTile(4, 220,21)
        self.inAvenue = PropertyTile(4, 220,23)
        self.ilAvenue = PropertyTile(4, 240,24)
        self.aAvenue = PropertyTile(5, 260,26)
        self.venAvenue = PropertyTile(5, 260,27)
        self.mGardens = PropertyTile(5, 280,29)
        self.paAvenue = PropertyTile(6, 300,31)
        self.nCAvenue = PropertyTile(6, 300,32)
        self.peAvenue = PropertyTile(6, 320,34)
        self.pPlace = PropertyTile(7, 350,37)
        self.bw = PropertyTile(7, 400,39)
        self.properties = [self.mAvenue, self.bAvenue,
                        self.oAvenue, self.verAvenue, self.cAvenue,
                        self.sCPlace, self.sAvenue, self.viAvenue,
                        self.sJPlace, self.tAvenue, self.nYAvenue,
                        self.kAvenue, self.inAvenue, self.ilAvenue,
                        self.aAvenue, self.venAvenue, self.mGardens,
                        self.paAvenue, self.nCAvenue, self.peAvenue,
                        self.pPlace, self.bw]
        self.boardnames = ['Pass Go! Collect 200', 'Mediterranean Avenue', 'Community Chest', 'Baltic Avenue', 'Income Tax', 'Reading Railroad', 'Oriental Avenue', 'Chance', 'Vermont Avenue', 'Connecticut Avenue',
                        'Just Visiting', 'St. Charles Place', 'Electric Company', 'States Avenue', 'Virginia Avenue', 'Pennsylvania Railroad', 'St. James Place', 'Community Chest', 'Tennessee Avenue', 'New York Avenue',
                        'Free Parking', 'Kentucky Avenue', 'Chance', 'Indiana Avenue', 'Illinois Avenue', 'B&O Railroad', 'Atlantic Avenue', 'Ventor Avenue', 'Water Works', 'Marvin Gardens',
                        'Go to Jail!', 'Pacific Avenue', 'North Carolina Avenue', 'Community Chest', 'Pennsylvania Avenue', 'Short Line', 'Chance', 'Park Place', 'Luxury Tax', 'Boardwalk']
        self.propertynames = ["Mediterranean Avenue", "Baltic Avenue",
                            "Oriental Avenue", "Vermont Avenue", "Connecticut Avenue",
                            "St. Charles Place", "States Avenue", "Virginia Avenue",
                            "St. James Place", "Tennessee Avenue", "New York Avenue",
                            "Kentucky Avenue", "Indiana Avenue", "Illinois Avenue",
                            "Atlantic Avenue", "Ventnor Avenue", "Marvin Gardens",
                            "Pacific Avenue", "North Carolina Avenue", "Pennsylvania Avenue",
                            "Park Place", "Boardwalk"]
        self.colors = ['brown', 'light_blue', 'purple', 'orange', 'red', 'yellow', 'green', 'dark_blue']
        self.sets = [[self.mAvenue, self.bAvenue],
                    [self.oAvenue, self.verAvenue, self.cAvenue],
                    [self.sCPlace, self.sAvenue, self.viAvenue],
                    [self.sJPlace, self.tAvenue, self.nYAvenue],
                    [self.kAvenue, self.inAvenue, self.ilAvenue],
                    [self.aAvenue, self.venAvenue, self.mGardens],
                    [self.paAvenue, self.nCAvenue, self.peAvenue],
                    [self.pPlace, self.bw]]

        self.communityChest=CChestTile()
        self.chance = chanceTile()
        self.electricCompany = UtilityTile(12)
        self.waterWorks = UtilityTile(28)
        self.utilities = [self.electricCompany, self.waterWorks]
        self.utilitynames = ["Electric Company", "Water Works"]
        self.rRailroad = RailroadTile(5)
        self.pRailroad = RailroadTile(15)
        self.bRailroad = RailroadTile(25)
        self.sLine = RailroadTile(35)
        self.railroads = [self.rRailroad, self.pRailroad, self.bRailroad, self.sLine]
        self.railroadnames = ["Reading Railroad", "Pennsylvania Railroad", "B&O Railroad", "Short Line"]

        self.board = [Tile(), self.mAvenue, self.communityChest, self.bAvenue, Tile(), self.rRailroad, self.oAvenue, self.chance, self.verAvenue, self.cAvenue,
                    Tile(), self.sCPlace, self.electricCompany, self.sAvenue, self.viAvenue, self.pRailroad, self.sJPlace, self.communityChest, self.tAvenue, self.nYAvenue,
                    Tile(), self.kAvenue, self.chance, self.inAvenue, self.ilAvenue, self.bRailroad, self.aAvenue, self.venAvenue, self.waterWorks, self.mGardens,
                    Tile(), self.paAvenue, self.nCAvenue, self.communityChest, self.peAvenue, self.sLine, self.chance, self.pPlace, Tile(), self.bw]


        # players
        self.players = [Player(0, '1'), Player(1, '-1')]

        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        return self.observation



    def render(self, mode='human', close=False, verbose = True):
        logger.debug('')
        if close:
            return
        if self.done:
            logger.debug(f'GAME OVER')
        else:
            logger.debug(f"It is Player {self.current_player.playerSymbol}'s turn to move")

        if self.verbose:
            logger.debug(f'\nObservation: \n{self.observation}')
        
        if not self.done:
            logger.debug(f'\nLegal actions: {[i for i,o in enumerate(self.legal_actions) if o != 0]}')


##### test move for win, how to change
# def rules_move(self):
#     # Check computer win moves
#     for i in range(0, self.num_squares):
#         if b[i] == 0 and testWinMove(b, 1, i):
#             logger.debug('Winning move')
#             return self.create_action_probs(i)
#     # Check player win moves
#     for i in range(0, self.num_squares):
#         if b[i] == 0 and testWinMove(b, -1, i):
#             logger.debug('Block move')
#             return self.create_action_probs(i)
def rules_move(self):
  #for all tiles in the board
  #check computer win
    # use the function previously made for creating legal actions, go through and test for win

  # check player win
    #use the function previously made for creating legal actions, go through and test for win
    # if player can win, block move


 def create_action_probs(self, action):
        action_probs = [0.01] * self.action_space.n
        action_probs[action] = 0.92
        return action_probs


### b = board, mark = player
def checkWin(b, m):
  # worth of the other player (see if the other player bankrupts)
  worth = self.checkworth(b,m)
  if worth < 0:
    return True
  return False

def checkworth(self, b, playern):
  player = self.players[(0 if playern == 1 else 1)]
  ca = player.cash
  for ii in range(22):
    if ii in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]:
      l = [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]
      if player.mortgaged[l.index(ii)] == False and player.playerProperty[l.index(ii)][0] == True:
        ca += b[ii].price
        if player.playerProperty[l.index(ii)][1] != 0:
          ca += (player.playerProperty[l.index(ii)][1] + player.playerProperty[l.index(ii)][2]) * b[ii].househotelCosts
    if ii in [5,15,25,35]
      l = [5,15,25,35]
      if player.playerRailroad[l.index(ii)] == True:
        ca += 200
    if ii in [12,28]:
      l = [12,28]
      if player.playerUtilities[l.index(ii)] == True:
        ca += 150
  return ca

def getBoardCopy(b):
    # Make a duplicate of the board. When testing moves we don't want to 
    # change the actual board
    bmAvenue = self.copyproperty(1,b)
    bbAvenue = self.copyproperty(3,b)
    boAvenue = self.copyproperty(6,b)
    bverAvenue = self.copyproperty(8,b)
    bcAvenue = self.copyproperty(9,b)
    bsCPlace = self.copyproperty(11,b)
    bsAvenue = self.copyproperty(13,b)
    bviAvenue = self.copyproperty(14,b)
    bsJPlace = self.copyproperty(16,b)
    btAvenue = self.copyproperty(18,b)
    bnYAvenue = self.copyproperty(19,b)
    bkAvenue = self.copyproperty(21,b)
    binAvenue = self.copyproperty(23,b)
    bilAvenue = self.copyproperty(24,b)
    baAvenue = self.copyproperty(26,b)
    bvenAvenue = self.copyproperty(27,b)
    bmGardens = self.copyproperty(29,b)
    bpaAvenue = self.copyproperty(31,b)
    bnCAvenue = self.copyproperty(32,b)
    bpeAvenue = self.copyproperty(34,b)
    bpPlace = self.copyproperty(37,b)
    bbw = self.copyproperty(39,b)

    belectricCompany = self.copyutility(12,b)
    bwaterWorks = self.copyproperty(28,b)
    brRailroad = self.copyrailroad(5,b)
    bpRailroad = self.copyrailroad(15,b)
    bbRailroad = self.copyrailroad(25,b)
    bsLine = self.copyrailroad(35,b)

    dupeBoard = [Tile(), bmAvenue, self.communityChest, bbAvenue, Tile(), brRailroad, boAvenue, self.chance, bverAvenue, bcAvenue,
                Tile(), bsCPlace, belectricCompany, bsAvenue, bviAvenue, bpRailroad, bsJPlace, self.communityChest, btAvenue, bnYAvenue,
                Tile(), bkAvenue, self.chance, binAvenue, bilAvenue, bbRailroad, baAvenue, bvenAvenue, bwaterWorks, bmGardens,
                Tile(), bpaAvenue, bnCAvenue, self.communityChest, bpeAvenue, bsLine, self.chance, bpPlace, Tile(), bbw]

    return dupeBoard

###############
# def testWinMove(b, mark, i):
    # # b = the board
    # # mark = number of the player
    # # i = the square to check if makes a win 
    # bCopy = getBoardCopy(b)
    # bCopy[i] = mark
    # return checkWin(bCopy, mark)
############## should the indexes stay the same? include no in the index?
# action = 1 number -> legal action flattened array (include not moving)
def testWinMove(b, mark, action):
  # b = the board
  # mark = number of the player
  # action = the square to check if makes a win 
  bCopy = getBoardCopy(b)
  player = self.copyplayer(mark)

  bproperties = [bCopy[x] for x in [1,3,6,8,9,11,13,14,16,18,19,21,23,24,26,27,29,31,32,34,37,39]]
  bsets = [[bCopy[1], bCopy[3]],
          [bCopy[6], bCopy[8], bCopy[9]],
          [bCopy[11], bCopy[13], bCopy[14]],
          [bCopy[16], bCopy[18], bCopy[19]],
          [bCopy[21], bCopy[23], bCopy[24]],
          [bCopy[26], bCopy[27], bCopy[29]],
          [bCopy[31], bCopy[32], bCopy[34]],
          [bCopy[37], bCopy[39]]]

  butilities = [bCopy[12], bCopy[28]]
  brailroads = [bCopy[x] for x in [5,15,25,35]]
       
  # railroad
  if action == 190:
    pass
  elif action == 42:
    # roll dice
    self.d1.randomnum()
    self.d2.randomnum()
    player.diceroll = self.d1.currentnum + self.d2.currentnum
    if self.d1.currentnum != self.d2.currentnum:
      player.diceJail += 1
    else:
      player.setJail()
      player.setDiceJail(0)
  elif action == 43: 
    # pay out of jail
    self.bankrupt(-50, player.playerSymbol)
    player.diceJail = 0
  elif action in [16,70,120,172]:
    # railroad
    railroad = brailroads[[16,70,120,172].index(action)]
    self.bankrupt(railroad.price, player.playerSymbol)
    railroad.setOwner(player.playerSymbol)
    player.addRailroad([16,70,120,172].index(action))
  elif action in [52,138]:
    # utility
    utility = butilities[[52,138].index(action)]
    self.bankrupt(utility.price, player.playerSymbol)
    utility.setOwner(player.playerSymbol)
    player.addUtilities([52,138].index(action))
    if player.playerUtilities == [True, True]:
      utility.setUtilities()
  elif action in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]
    # buy property
    prop = bproperties[[0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182].index(action)]
    self.bankrupt(-(prop.getPrice()), player.playerSymbol)
    prop.setOwner(player.playerSymbol)
    player.addProperty([0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182].index(action))
    for s, owned in player.playerSets.items():
      if owned == True:
        for p in bsets[self.colors.index(s)]:
          p.setColorSet()
  elif action in [x+2 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]]:
    prop = bproperties[[x+2 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]].index(action)]
    prop.setHouse()
    player.earn(-(prop.househotelCosts))
    player.addHouseHotel([x+2 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]].index(action))
  elif action in [x+4 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]]
    prop = bproperties[[x+4 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]].index(action)]
    prop.setHouse()
     player.earn(-(prop.househotelCosts))
    player.addHouseHotel([x+4 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]].index(action))
  elif action in [x+6 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]]
    index = [x+6 for x in [0,8,18,26,34,44,54,62,72,80,88,96,104,112,122,130,140,148,156,164,174,182]].index(action)
    prop = bproperties[index]
    self.bankrupt(-prop.mortgagedPayPrice, player.playerSymbol)
    player.setMortgaged(index)
    player.playerProperty[index][0] = False
    player.houseNum += player.playerProperty[index][1]
    player.hotelNum += player.playerProperty[index][2]
    prop.mortgaged = False

    return checkWin(bCopy, mark)


def copyplayer(self, playern):
  player = self.players[playern]
  bplayer = Player(player.playerSymbol, plauer.name)
  bplayer.position = player.position
  bplayer.rollingdoubles = player.rollingdoubles
  bplayer.turn = player.turn
  bplayer.move = player.move
  bplayer.b = player.b
  bplayer.cash = player.cash
  bplayer.jail = player.jail
  bplayer.diceJail = player.diceJail
  bplayer.wasJailed = player.wasJailed
  bplayer.playerProperty = player.playerProperty
  bplayer.houseNum = player.houseNu
  bplayer.hotelNum = player.hotelNum
  bplayer.playerSets = player.playerSets
  bplayer.playerRailroad = player.playerRailroad
  bplayer.railroadNum = player.railroadNum
  bplayer.playerUtilities = player.playerUtilities
  bplayer.utilitiesNum = player.utilitiesNum
  bplayer.mortgaged = player.mortgaged
  bplayer.freeJail = player.freeJail
  return bplayer

def copyproperty(self, tilen, b):
  prop = b[tilen]
  bprop = PropertyTile(prop.color, prop.price, prop.position)
  bprop.hasPiece = prop.hasPiece
  bprop.pieceType = prop.pieceType
  bprop.once = prop.once
  bprop.occupied = prop.occupied
  bprop.rent = prop.rent
  bprop.rentWOneHouse = prop.rentWOneHouse
  bprop.house = prop.house
  bprop.hotel = prop.hotel
  bprop.hhcosts = prop.hhcosts
  bprop.househotelCosts = prop.househotelCosts
  bprop.colorset = prop.colorset
  bprop.mortgaged = prop.mortgaged
  bprop.mortgageprice = prop.mortgageprice
  bprop.mortgagedPayPrice = prop.mortgagedPayPrice
  bprop.diceroll = prop.diceroll
  return bprop

def copyrailroad(self, tilen, b):
  railroad = b[tilen]
  brailroad = RailroadTile(tilen)
  brailroad.hasPiece = railroad.hasPiece
  brailroad.pieceType = railroad.pieceType
  brailroad.occupied = railroad.occupied
  brailroad.price = railroad.price
  brailroad.rent = railroad.rent
  brailroad.totalRailroad = railroad.totalRailroad
  return brailroad

def copyutility(self, tilen, b):
  utility = b[tilen]
  butility = UtilityTile(tilen)
  butility.hasPiece = utility.hasPiece
  butility.pieceType = utility.pieceType
  butility.occupied = utility.occupied
  butility.price = utility.price
  butility.utilities = utility.utilities