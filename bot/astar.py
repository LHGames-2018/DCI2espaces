import math
from helper.tile import TileContent
from helper import *


class AStar:
    def __init__(self):
        self.grid = Grid()

    def update(self, gamemap):
        self.grid.update(gamemap.tiles)

    def get_move(self, player, node):
        return Point(node.x - player.x, node.y - player.y)

    def find_nearest_resource(self, player):
        resources = []
        path = []
        for _, v in self.grid.nodes.items():
            if (v.tile.TileContent == TileContent.Resource):
                resources.append(v)

        for res in resources:
            path.append(self.find_path(player.x, player.y, res.x, res.y))

        def shortest_path(path):
            return len(path)
        path.sort(key=shortest_path)

        if len(path) == 0:
            return None
        return path[0]

    def find_home(self, player):
        home = None
        for _, v in self.grid.nodes.items():
            if (v.tile.TileContent == TileContent.House):
                home = v
                break
        path = self.find_path(player.x, player.y, home.x, home.y)

        if len(path) == 0:
            return None
        return path

    def find_path(self, from_x, from_y, to_x, to_y):
        node_from = self.grid.get_node(from_x, from_y)
        node_to = self.grid.get_node(to_x, to_y)

        if (node_from == node_to):
            return []

        for _, node in self.grid.nodes.items():
            node.updateH(node_to)

        path = []
        if self.search(node_from, node_to):
            node = node_to
            while (node.parent != None):
                path.append(node)
                node = node.parent

        self.grid.reset()
        return path

    def search(self, node_from, node_to):
        node_from.state = 'closed'
        nodes = self.get_adj_walk_nodes(node_from)

        def takeF(node):
            return node.g + node.h
        nodes.sort(key=takeF)

        for node in nodes:
            if node.x == node_to.x and node.y == node_to.y:
                return True
            elif self.search(node, node_to):
                return True
        return False

    def get_adj_walk_nodes(self, from_node):
        nodes = []
        for node in self.get_adj_nodes(from_node):
            if node.state == 'closed':
                continue

            if node.state == 'open':
                tcost = math.hypot(
                    node.x - node.parent.x,
                    node.y - node.parent.y
                )
                gtemp = from_node.g + tcost + node.cost

                if (gtemp < node.g):
                    print('found one')
                    node.set_parent(from_node)
                    node.state = 'open'
                    nodes.append(node)
            else:
                node.set_parent(from_node)
                node.state = 'open'
                nodes.append(node)

        return nodes

    def get_adj_nodes(self, node):
        nodes = []
        if self.grid.get_node(node.x, node.y - 1) != None:
            nodes.append(self.grid.get_node(node.x, node.y - 1))
        if self.grid.get_node(node.x - 1, node.y) != None:
            nodes.append(self.grid.get_node(node.x - 1, node.y))
        if self.grid.get_node(node.x, node.y + 1) != None:
            nodes.append(self.grid.get_node(node.x, node.y + 1))
        if self.grid.get_node(node.x + 1, node.y) != None:
            nodes.append(self.grid.get_node(node.x + 1, node.y))
        return nodes


class Grid:
    def __init__(self):
        self.nodes = {}

    def update(self, tiles):
        for l in tiles:
            for t in l:
                x = t.Position.x
                y = t.Position.y
                self.set_node(x, y, t)

    def set_node(self, x, y, t):
        self.nodes[(x, y)] = Node(x, y, t)

    def get_node(self, x, y):
        try:
            return self.nodes[(x, y)]
        except:
            return None

    def reset(self):
        for _, v in self.nodes.items():
            v.reset()


class Node:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y

        self.state = 'idk'
        self.parent = None
        self.h = 9999999
        self.g = 0

        self.tile = tile
        self.cost = {
            TileContent.Empty: 0,
            TileContent.Wall: 5,
            TileContent.House: 0,
            TileContent.Lava: 5,
            TileContent.Resource: 5,
            TileContent.Shop: 5,
            TileContent.Player: 5
        }[tile.TileContent]

        self.walkable = {
            TileContent.Empty: True,
            TileContent.Wall: False,
            TileContent.House: True,
            TileContent.Lava: False,
            TileContent.Resource: False,
            TileContent.Shop: False,
            TileContent.Player: False
        }[tile.TileContent]

    def calc_traversal(self, node):
        return math.sqrt((math.pow(node.x - self.x, 2) + math.pow(node.y - self.y, 2)) + self.cost)

    def updateH(self, node_to):
        self.h = self.calc_traversal(node_to)

    def set_parent(self, node):
        self.parent = node
        self.g = node.g + self.calc_traversal(node)

    def reset(self):
        self.state = 'idk'
        self.h = 9999999
        self.g = 0
        self.parent = None
