from typing import List
from helper_classes import *


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
        if turns_left == 100:
            self.init_roles()
        return []

    def init_roles(self):
        return

    def set_role(self, unit: Unit, new_role: str):
        for i in self.roles:
            if i[0] == unit:
                i[1] = new_role
