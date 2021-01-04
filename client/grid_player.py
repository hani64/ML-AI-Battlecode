class GridPlayer:

    def __init__(self):
        self.foo = True

    # game_map is the grid which represents the current map.
    # your_units is the list of every unit that belongs to you.
    # enemy_units is the list of every unit that your units can see (fog of war) that belong to the enemy.
    # resources is the number of resources that you currently possess.
    # turns_left is the number of turns that remain until the game ends.


    def tick(self, game_map, your_units, enemy_units, resources, turns_left):
        move_list = []
        # Want to try and gather as many resources as possible
        # Melees will want to try and kill as many of opponent as possible while guarding
        # Per every move, we need to check if valid

        # Check scoring system per each player
        # Like what if melee moves 1 direction from here, will it benefit to kill 
        attackers = your_units.get_all_unit_of_type("melle")
        workers = your_units.get_all_unit_of_type("worker")
        # for worker in workers:
        #     game_map.
        return move_list



# Worker
# 	- Mine resources at a resource node, locked into position
# 		- Requires 5 turns
# 	- Duplicate themselves into melee and worker unit
# 		- Requires 4 turns
# 	- Move to another block

# Melee
# 	- Attack player (free)
# 	- Stun player at max 2 blocks away (50 resources)
# 	- Move to another block
	
	
# Common
# 	- Each move is 1 turn
	
	

# Beginning
# - We want worker to gather as many resources as possible
# - while some of our melee will defend and some will go in offensive
