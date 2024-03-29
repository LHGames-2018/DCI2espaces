import math
import pickle
from helper import *
from .astar import AStar


class Bot:
    def __init__(self):
        self.astar = AStar(None)
        self.updatePrices = [10000, 15000, 25000, 50000, 100000]
        self.pos_history = []
        self.stuck_count = 0

    def before_turn(self, playerInfo):
        self.astar.home = playerInfo.HouseLocation
        self.PlayerInfo = playerInfo

    def execute_turn(self, gameMap, visiblePlayers):
        position = self.PlayerInfo.Position

        if len(self.pos_history) > 0 and (position.x != self.pos_history[-1].x or position.y != self.pos_history[-1].y):
            self.pos_history.append(position)
        else:
            self.pos_history.clear()
            self.pos_history.append(position)
        if len(self.pos_history) > 2:
            if position.x == self.pos_history[0].x and position.y == self.pos_history[0].y:
                self.stuck_count = self.stuck_count + 1
            self.pos_history.pop(0)
        if self.stuck_count > 2:
            self.astar.gotHome = False
            self.stuck_count = 0
            self.pos_history.clear()

        self.astar.update(gameMap)
        # comments are nice
        if (position.x == self.astar.home.x and position.y == self.astar.home.y):
            self.astar.gotHome = True
            if self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.AttackPower)]:
                return create_upgrade_action(UpgradeType.AttackPower)
            elif self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.MaximumHealth)]:
                return create_upgrade_action(UpgradeType.MaximumHealth)
            elif self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.Defence)]:
                return create_upgrade_action(UpgradeType.Defence)
            elif self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.CollectingSpeed)]:
                return create_upgrade_action(UpgradeType.CollectingSpeed)
            elif self.PlayerInfo.TotalResources >= self.updatePrices[self.PlayerInfo.getUpgradeLevel(UpgradeType.CarryingCapacity)]:
                return create_upgrade_action(UpgradeType.CarryingCapacity)
        # tips
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
            #ATTTACKK

            if attack != False:
                path = self.astar.find_path(
                    position.x, position.y, attack.Position.x, attack.Position.y)
            elif self.PlayerInfo.CarriedResources < self.PlayerInfo.CarryingCapacity:
                path = self.astar.find_nearest_resource(position)
            elif self.PlayerInfo.CarriedResources >= self.PlayerInfo.CarryingCapacity:
                path = self.astar.find_home(position)

        if len(path) == 0:
            self.astar.gotHome = False
            target = self.astar.get_move(
                position, self.astar.find_home(position).pop())
        else:
            target = self.astar.get_move(position, path.pop())

        print(len(path), target, self.PlayerInfo.CarriedResources,
              self.PlayerInfo.CarryingCapacity, self.PlayerInfo.UpgradeLevels)
        # HOMESWEETHOME
        if (not (position.x == self.astar.home.x and position.y == self.astar.home.y)) and math.hypot(position.x - self.astar.home.x, position.y - self.astar.home.y) > 10:
            print('going home because too far')
            self.astar.gotHome = False
            target = self.astar.get_move(
                position, self.astar.find_home(position).pop())

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
            return create_move_action(target)
        else:
            print('uh oh')

    def after_turn(self):
        pass
