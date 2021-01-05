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
    data: an optional argument corresponding to additional info about this unit.
          if this argument is not required for a given role, it will be None.


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

        self.remove_dead_units(your_units)
        game_data = (game_map, your_units, enemy_units, resources, turns_left)
        moves = []

        if turns_left == 100:
            self.init_roles(*game_data)
        for unit_id in your_units.get_all_unit_ids():
            unit = your_units.get_unit(unit_id)
            role = self.get_unit_role(unit)

            if role == "":
                self.determine_role(unit, *game_data)
                pass

            role_method = getattr(GridPlayer, role, "choose_role")
            move = role_method(*game_data)
            if move is not None:
                moves.append(move)

        return moves

    def init_roles(self, game_map: Map, your_units: Units, enemy_units: Units,
                   resources: int, turns_left: int) -> None:
        return

    def get_unit_role(self, unit: Unit) -> str:
        for i in self.roles:
            if i[0] == unit:
                return i[1]
        return ""

    def set_unit_role(self, unit: Unit, new_role: str) -> None:
        for i in self.roles:
            if i[0] == unit:
                i[1] = new_role

    def get_role_data(self, unit: Unit):
        for i in self.roles:
            if i[0] == unit:
                return i[2]

    def set_role_data(self, unit: Unit, new_data):
        for i in self.roles:
            if i[0] == unit:
                i[2] = new_data

    def determine_role(self, unit: Unit, game_map: Map, your_units: Units,
                       enemy_units: Units, resources: int, turns_left: int):
        pass

    def remove_dead_units(self, your_units: Units):

        to_remove = []

        for unit in self.roles:
            if unit[0].id not in your_units.get_all_unit_ids():
                to_remove.append(unit)

        for unit in to_remove:
            self.roles.remove(unit)

    def miner(self, unit: Unit, game_map: Map, your_units: Units,
              enemy_units: Units, resources: int, turns_left: int) -> \
            Optional[Move]:

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
            if unit not in claimed_nodes:
                for resource in game_map.find_all_resources():
                    if resource not in claimed_nodes.values():
                        claimed_nodes[unit] = resource
                for resource in game_map.find_all_resources():
                    if resource not in claimed_nodes.values():
                        claimed_nodes[unit] = resource

            if unit.position() == claimed_nodes[unit]:
                return unit.mine()
            else:
                end = claimed_nodes[unit]
                return unit.move_towards(game_map.bfs(unit.position(), end)[0])

    def bodyguard(self, unit: Unit, game_map: Map, your_units: Units,
                  enemy_units: Units, resources: int, turns_left: int) -> \
            Optional[Move]:

        unit_data = self.get_role_data(unit)
        closest = unit.nearby_enemies_by_distance(enemy_units)[0]

        if closest[1] == 1:
            # attack the unit
            enemy_unit = enemy_units.get_unit(closest[0])
            direction = unit.direction_to(enemy_unit.position())
            return unit.attack(direction)
        # TODO: add this branch after grenadier and sprinter are done
        # elif closest[1] == 2:
        # if there is another melee at a distance of 2 to the enemy,
        # one switches to grenadier and the other to sprinter
        # otherwise, switch to guardian
        elif closest[1] <= 4:
            # switch role to guardian
            self.set_unit_role(unit, "guardian")
            return self.guardian(unit, game_map, your_units,
                                 enemy_units, resources, turns_left)
        else:
            # move towards the friendly worker stored in this unit's data
            # if the specified unit does not exist, switch to the closest
            # friendly worker unit with less than 2 bodyguards
            if unit_data not in your_units.get_all_unit_ids():
                for other_id in unit.nearby_enemies_by_distance(your_units):
                    other_unit = your_units.get_unit(other_id[0])
                    if other_unit.type == "worker":
                        other_data = self.get_role_data(other_unit)
                        if other_data < 2:
                            self.set_role_data(unit, other_unit)
                            self.set_role_data(other_unit, other_data + 1)

            end = self.get_role_data(unit).position()
            return unit.move_towards(game_map.bfs(unit.position(), end))

    def grenadier(self, unit: Unit, game_map: Map, your_units: Units,
                  enemy_units: Units, resources: int, turns_left: int) -> \
            Optional[Move]:
        pass

    def sprinter(self, unit: Unit, game_map: Map, your_units: Units,
                 enemy_units: Units, resources: int, turns_left: int) -> \
            Optional[Move]:
        pass

    def guardian(self, unit: Unit, game_map: Map, your_units: Units,
                 enemy_units: Units, resources: int, turns_left: int) -> \
            Optional[Move]:

        unit_data = self.get_role_data(unit)
        closest = unit.nearby_enemies_by_distance(enemy_units)[0]

        if closest[1] == 1:
            enemy_unit = enemy_units.get_unit(closest[0])
            direction = unit.direction_to(enemy_unit.position())
            return unit.attack(direction)
        # TODO: add this branch after grenadier and sprinter are done
        # elif closest[1] == 2:
        # if there is another melee at a distance of 2 to the enemy,
        # one switches to grenadier and the other to sprinter
        # otherwise, switch to guardian
        elif closest[1] <= 4:
            enemy_id = unit.nearby_enemies_by_distance(enemy_units)[0]
            enemy_unit = enemy_units.get_unit(enemy_id[0])
            end = enemy_unit.position()
            return unit.move_towards(game_map.bfs(unit.position(), end))
        else:
            # switch role to bodyguard
            self.set_unit_role(unit, "bodyguard")
            return self.bodyguard(unit, game_map, your_units,
                                  enemy_units, resources, turns_left)
