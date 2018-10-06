import math
from helper import *
from .astar import AStar


class Bot:
    def __init__(self):
        # try:
        #    with open('/data/pickle.bin', 'rb') as file:
        #        nodes = pickle.load(file)
        # except:
        #    nodes = None
        self.astar = AStar(None)
        self.updatePrices = [10000, 15000, 25000, 50000, 100000]

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
            if self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.CollectingSpeed)]:
                return create_upgrade_action(UpgradeType.CollectingSpeed)
            elif self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.CarryingCapacity)]:
                return create_upgrade_action(UpgradeType.CarryingCapacity)

        if self.astar.gotHome == False:
            path = self.astar.find_home(position)
        else:
            attack = False
            if len(visiblePlayers) != 0:
                for player in visiblePlayers:
                    hyp = math.hypot(player.Position.x - position.x,
                                     player.Position.y - position.y)
                    print(player, hyp)
                    if hyp < 2:
                        attack = player
                        break

            if attack != False:
                path = self.astar.find_path(
                    position.x, position.y, attack.Position.x, attack.Position.y)
            elif self.PlayerInfo.CarriedResources != 0 and len(self.astar.find_home(position)) <= 3 and len(self.astar.find_nearest_resource(position)) >= 3:
                path = self.astar.find_home(position)
            elif self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
                path = self.astar.find_nearest_resource(position)
            elif self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
                path = self.astar.find_home(position)

        target = self.astar.get_move(position, path.pop())

        print(len(path), target, self.PlayerInfo.CarriedResources,
              self.PlayerInfo.CarryingCapacity, self.PlayerInfo.UpgradeLevels)

        if self.astar.gotHome == False:
            print('go home!')
            return create_move_action(target)

        if len(path) == 0 and attack != False:
            print('attack')
            return create_attack_action(target)
        elif len(path) == 0 and self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
            print('collect!')
            return create_collect_action(target)
        elif self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity or self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
            print('move!')
            return create_move_action(target)
        else:
            print('uh oh')

    def after_turn(self):
        pass
        # with open('/data/pickle.bin', mode='wb') as file:
        #    pickle.dump(self.astar.grid.nodes, file)
