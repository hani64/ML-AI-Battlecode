from typing import List, Optional, Dict
from helper_classes import *


class GridPlayer:
    roles = []
    claimed_nodes = {}

    def __init__(self):
        self.foo = True

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:

        print("test")

        # self.remove_dead_units(your_units)

        if not self.roles:
            self.init_roles(your_units)

        moves = []

        for unit_id in your_units.get_all_unit_ids():
            unit = your_units.get_unit(unit_id)
            role = self.get_role(unit)
            data = self.get_data(unit)

            if role == "miner":
                moves.append(self.miner(unit, enemy_units, game_map))
            elif role == "bodyguard":
                moves.append(self.bodyguard())
            elif role == "guardian":
                moves.append(self.guardian())

        if not moves:
            return self.roles

        return moves

    def init_roles(self, your_units: Units):
        for unit_id in your_units.get_all_unit_ids():
            unit = your_units.get_unit(unit_id)
            if unit.type == "worker":
                self.roles.append([unit, "miner", 0])
            elif unit.type == "melee":
                self.roles.append([unit, "bodyguard", None])

    def set_role(self, unit: Unit, role: str):
        for i in self.roles:
            if i[0].id == unit.id:
                i[1] = role
                return

    def get_role(self, unit: Unit):
        for i in self.roles:
            if i[0].id == unit.id:
                return i[1]

    def set_data(self, unit: Unit, data):
        for i in self.roles:
            if i[0].id == unit.id:
                i[2] = data
                return

    def get_data(self, unit: Unit):
        for i in self.roles:
            if i[0].id == unit.id:
                return i[2]

    def claim_node(self, unit: Unit, game_map: Map):

        closest_node = None
        distance = 9999

        for node in game_map.find_all_resources():
            if node not in self.claimed_nodes.values():
                new_distance = coordinate_distance(unit.position(), node,
                                                   game_map)
                if new_distance < distance:
                    closest_node = node
                    distance = new_distance

        if closest_node is None:
            return False
        else:
            self.claimed_nodes[unit.id] = closest_node
            return True

    def remove_dead_units(self, your_units: Units):
        remove_roles = []
        remove_claims = []

        for unit in self.roles:
            if unit[0].id not in your_units.get_all_unit_ids():
                remove_roles.append(unit)
        for unit in self.claimed_nodes:
            if unit not in your_units.get_all_unit_ids():
                remove_claims.append(unit)

        for unit in remove_roles:
            self.roles.remove(unit)
        for unit in remove_claims:
            del self.claimed_nodes[unit]

    def set_vip(self, unit: Unit, your_units: Units):
        workers = your_units.get_all_unit_of_type("worker")
        first_single = None

        for worker in workers:
            if self.get_data(worker) == 0:
                self.set_data(worker, 1)
                self.set_data(unit, worker)
                return
            elif self.get_data(worker) == 1 and first_single is None:
                first_single = worker

        if first_single is None:
            return
        self.set_data(first_single, 2)
        self.set_data(unit, first_single)

    def miner(self, unit: Unit, enemy_units: Units, game_map: Map) -> \
            Optional[Move]:
        closest, distance = get_closest_enemy_melee(unit, enemy_units, game_map)
        if distance == 1:
            # run away
            direction_to = unit.direction_to(closest.position())
            move = unit.move(opposite_direction(direction_to))
            return move
        elif distance == 2:
            # don't move
            return None
        else:
            # move towards claimed node and mine from it
            # if this unit doesn't have a claimed node, claim one
            if unit.id not in self.claimed_nodes:
                if not self.claim_node(unit, game_map):
                    # node could not be claimed, switch to another role?
                    # TODO
                    return None

            if self.claimed_nodes[unit.id] == unit.position():
                return unit.mine()
            else:
                path = game_map.bfs(unit.position(),
                                    self.claimed_nodes[unit.id])
                return unit.move_towards(path[1])


def get_closest_enemy_melee(unit: Unit, enemy_units: Units, game_map: Map) -> (Unit, int):
    closest = None
    distance = 9999

    for enemy in enemy_units.get_all_unit_of_type("melee"):
        new_distance = coordinate_distance(unit.position(), enemy.position(),
                                           game_map)
        if new_distance < distance:
            closest = enemy
            distance = new_distance

    return closest, distance


def coordinate_distance(start: (int, int), end: (int, int), game_map):
    return len(game_map.bfs(start, end))


def opposite_direction(direction: str) -> str:
    opposite = {"UP": "DOWN", "DOWN": "UP", "RIGHT": "LEFT", "LEFT": "RIGHT"}
    return opposite[direction]


def move_towards(unit: Unit, end: (int, int), game_map: Map) -> Optional[Move]:
    positions = game_map.bfs(unit.position(), end)
    if positions is None:
        return None
    else:
        direction = unit.direction_to(positions[1])
        return unit.move(direction)
