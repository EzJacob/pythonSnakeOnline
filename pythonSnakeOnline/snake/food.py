import random


class Food:
    def __init__(self):
        self.pos_list_taken = []
        self.spawned = False
        self.pos = []

    def set_pos_list_taken(self, player, other_player=None):
        if other_player is None:
            self.pos_list_taken = player.get_list_of_nodes_pos()
        else:
            self.pos_list_taken = player.get_list_of_nodes_pos() + other_player.get_list_of_nodes_pos()

    def set_spawn_food_pos(self, width, height):
        if self.spawned:
            return

        mat = []
        for j in range(0, width, 50):
            for k in range(0, height, 50):
                mat.append([j, k])

        # Remove elements from list1 that are in list2
        available_positions = [x for x in mat if x not in self.pos_list_taken]

        random_element = random.choice(available_positions)
        self.spawned = True
        self.pos = random_element
