from helper import *
from .astar import AStar


class Bot:
    def __init__(self):
        self.astar = AStar()
        pass

    def before_turn(self, playerInfo):
        """
        Gets called before ExecuteTurn. This is where you get your bot's state.
            :param playerInfo: Your bot's current state.
        """
        self.astar.home = playerInfo.HouseLocation
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        position = self.PlayerInfo.Position
        self.astar.update(gameMap)

        if (position.x == self.astar.home.x and position.y == self.astar.home.y):
            self.astar.gotHome = True
        if self.astar.gotHome == False:
            path = self.astar.find_home(position)
        elif self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
            path = self.astar.find_nearest_resource(position)
        elif self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
            path = self.astar.find_home(position)

        target = self.astar.get_move(position, path.pop())

        print(len(path), self.PlayerInfo.CarriedResources,
              self.PlayerInfo.CarryingCapacity)

        if self.astar.gotHome == False:
            print('go home!')
            return create_move_action(target)
        if len(path) == 0 and self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
            print('collect!')
            return create_collect_action(target)
        elif self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity or self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
            print('move!')
            return create_move_action(target)
        else:
            print('uh oh')

    def after_turn(self):
        """
        Gets called after executeTurn
        """
        pass
