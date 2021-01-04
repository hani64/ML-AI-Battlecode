from typing import List, Optional, Dict
from helper_classes import *

REVERSE_DIR = {"UP": "DOWN", "DOWN": "UP", "RIGHT": "LEFT", "LEFT": "RIGHT"}
claimed_nodes = {}


class GridPlayer:
    roles: List[List]

    """
    This list contains one element for each friendly unit in play.
    The element corresponding to any given friendly unit is a list:
    [this_unit, role, other_unit]

    this_unit: a Unit object corresponding to the given friendly unit
    role: a string representing this unit's role. Depending on what the unit's
          role is, it will use different behavior when determining its move.
    other_unit: an optional argument corresponding to another unit in the game.
                most roles require this argument as additional specification.


    Unit Roles:

    miner - Seeks the nearest unoccupied mining node and mines from it.
            This unit will not move into the range of an enemy melee unit.

    bodyguard - Attempts to stay ahead of the specified miner unit by predicting
                its movement. If an enemy unit is detected nearby, or if the
                miner unit has reached its mining destination, this unit will
                switch to a different role based on various cases.

    grenadier - Stuns the specified enemy unit, then switches
                its role back to bodyguard.

    sprinter - Must be used in conjunction with a grenadier. Moves into melee
               range of the specified enemy unit, then switches its role to
               guardian.

    guardian - When an enemy unit is detected in vision of the specified
               miner unit, this unit will move in front of the miner unit to
               protect it. If an enemy unit moves into melee range of this
               unit, kill it

    duplicator - Stays in a safe location and may generate new units over
                 time based on various parameters including remaining turns,
                 resource count, and unit numbers.

    berserker - Fuck it, just go on a killing spree
    """

    def __init__(self):
        self.foo = True

    def tick(self, game_map: Map, your_units: Units, enemy_units: Units,
             resources: int, turns_left: int) -> [Move]:

        game_data = (game_map, your_units, enemy_units, resources, turns_left)
        moves = []

        if turns_left == 100:
            self.init_roles(*game_data)
        for unit_id in your_units.get_all_unit_ids():
            unit = your_units.get_unit(unit_id)
            role = self.get_unit_role(unit)

            if role == "":
                # self.determine_role(unit)
                pass

            role_method = getattr(GridPlayer, role, "choose_role")
            move = role_method(*game_data)
            if move is not None:
                moves.append(move)

        return moves

    def init_roles(self, game_map: Map, your_units: Units, enemy_units: Units,
                   resources: int, turns_left: int) -> None:
        return

    def set_role(self, unit: Unit, new_role: str) -> None:
        for i in self.roles:
            if i[0] == unit:
                i[1] = new_role

    def get_unit_role(self, unit: Unit) -> str:
        for i in self.roles:
            if i[0] == unit:
                return i[1]
        return ""

    def get_role_data(self, unit: Unit) -> Optional[Unit]:
        for i in self.roles:
            if i[0] == unit:
                if len(i) == 3:
                    return i[2]
                return None

    def choose_role(self, unit: Unit, game_map: Map, your_units: Units,
                    enemy_units: Units, resources: int, turns_left: int):
        pass

    def miner(self, unit: Unit, game_map: Map, your_units: Units,
              enemy_units: Units, resources: int, turns_left: int) -> Optional[Move]:

        closest = unit.nearby_enemies_by_distance(enemy_units)[0]

        if closest[1] == 1:
            # run away
            enemy_unit = enemy_units.get_unit(closest[0])
            direction = unit.direction_to(enemy_unit.position())
            reverse = REVERSE_DIR[direction]
            return unit.move(reverse)
        elif closest[1] == 2:
            # don't move
            return None
        else:
            # move towards claimed resource node
            # if this unit has not claimed a resource node, claim one
            if unit in claimed_nodes:
                return unit.move_towards(claimed_nodes[unit])
            else:
                for resource in game_map.find_all_resources():
                    if resource not in claimed_nodes.values():
                        claimed_nodes[unit] = resource
                        return unit.move_towards(resource)

    def bodyguard(self, unit: Unit, game_map: Map, your_units: Units,
                  enemy_units: Units, resources: int, turns_left: int) -> Optional[Move]:
        pass

    def grenadier(self, unit: Unit, game_map: Map, your_units: Units,
                  enemy_units: Units, resources: int, turns_left: int) -> Optional[Move]:
        pass

    def sprinter(self, unit: Unit, game_map: Map, your_units: Units,
                 enemy_units: Units, resources: int, turns_left: int) -> Optional[Move]:
        pass

    def guardian(self, unit: Unit, game_map: Map, your_units: Units,
                 enemy_units: Units, resources: int, turns_left: int) -> Optional[Move]:
        pass
