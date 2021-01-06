from typing import List, Optional, Dict
from helper_classes import *
import math

MELEE = 'melee'
WORKER = 'worker'
WORKER_COST = 50
MELEE_COST = 100


class GridPlayer:

    def __init__(self):
        self.roles = []
        self.claimed_nodes = {}
        self.dup_queue = []
        self.used_resources = 0

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:

        self.used_resources = 0

        self.update_queue()
        # self.remove_dead_units(your_units)

        if not self.roles:
            self.init_roles(your_units)

        moves = []
        attacker_amount = len(your_units.get_all_unit_of_type(MELEE))
        worker_amount = len(your_units.get_all_unit_of_type(WORKER))

        print(
            f"---------------------\nRound: {200 - turns_left}\n# of Attacker: {attacker_amount}\n"
            f"# of Worker: {worker_amount}\n# of Resources: {resources}",
            flush=True)

        for unit_id in your_units.get_all_unit_ids():
            unit = your_units.get_unit(unit_id)
            role = self.get_role(unit)
            if not role:
                self.init_single_role(unit)
                role = self.get_role(unit)

            # data = self.get_data(unit)

            if role == "miner":
                moves.append(self.miner(unit, your_units, enemy_units, game_map, resources))
            elif role == "bodyguard":
                moves.append(self.bodyguard(unit, enemy_units))
            elif role == "guardian":
                moves.append(self.guardian())

        if not moves:
            return self.roles

        return [move for move in moves if move]

    def update_queue(self):
        to_remove = []

        for item in self.dup_queue:
            item[1] -= 1
            if item[1] == 0:
                to_remove.append(item)

        for item in to_remove:
            self.dup_queue.remove(item)

    def available_direction(self, position, game_map: Map, your_units: Units):
        for direction in ["UP", "LEFT", "DOWN", "RIGHT"]:
            new_pos = coordinate_from_direction(position[0], position[1],
                                                direction)
            if game_map.get_tile(new_pos[0], new_pos[1]) in [' ', 'R'] and \
                    not self.unit_on_tile(new_pos, game_map, your_units):
                return direction
        return None

    def unit_on_tile(self, position, game_map, your_units):
        for unit_id in your_units.get_all_unit_ids():
            if your_units.get_unit(unit_id).position() == position:
                return True
        return False

    def init_roles(self, your_units: Units):
        for unit_id in your_units.get_all_unit_ids():
            unit = your_units.get_unit(unit_id)
            if unit.type == "worker":
                self.roles.append([unit, "miner", 0])
            elif unit.type == "melee":
                self.roles.append([unit, "bodyguard", None])

    def init_single_role(self, unit: Unit):
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

    def num_role(self, role: str):
        num = 0
        for unit in self.roles:
            if unit[1] == role:
                num += 1
        return num

    def dup_type(self, game_map, resources):
        num_nodes = len(game_map.find_all_resources())
        num_miners = self.num_role("miner") + \
                     self.dup_queue.count("miner")
        num_bodyguards = self.num_role("bodyguard") + \
                         self.dup_queue.count("bodyguard")

        if num_bodyguards < num_miners and \
                resources - self.used_resources >= MELEE_COST:
            self.used_resources += MELEE_COST
            return MELEE
        elif num_miners < num_nodes and \
                resources - self.used_resources >= WORKER_COST:
            self.used_resources += WORKER_COST
            return WORKER
        return None

    def miner(self, unit: Unit, your_units: Units, enemy_units: Units,
              game_map: Map, resources) -> Optional[Move]:
        if unit.attr['mining_status'] > 0:
            return None

        CLONE = self.dup_type(game_map, resources)
        # For now single unit

        closest, distance = get_closest_enemy_melee(unit, enemy_units, game_map)
        if distance == 1:
            # run away
            direction_to = unit.direction_to(closest.position())
            move = unit.move(opposite_direction(direction_to))
            return move
        elif distance == 2:
            # don't move
            return None
        # If condition satisfies and we want to clone
        elif CLONE and unit.can_duplicate(resources, CLONE):
            available_dir = self.available_direction(unit.position(), game_map,
                                                     your_units)
            if available_dir:
                self.dup_queue.append([CLONE, 4])
                return unit.duplicate(available_dir, CLONE)
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

    def bodyguard(self, unit, enemy_units):
        # For now we'll check to see if neighbor has enemy so we can kill it
        # Later we'll want to add it so we move a few blocks to get advantage to kill the enemy
        to_attack = unit.can_attack(enemy_units)
        if to_attack:
            return unit.attack(to_attack[0][1])
        return None


def get_closest_enemy_melee(unit: Unit, enemy_units: Units, game_map: Map) -> (
        Unit, int):
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
    path = game_map.bfs(start, end)
    if path is None:
        return 0
    return len(path)


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

