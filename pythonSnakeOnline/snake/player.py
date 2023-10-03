import pygame

from snake.food import Food


class Player:
    def __init__(self):
        self.movement = {'up': False, 'down': False, 'right': False, 'left': False}
        self.pos = [600, 400]
        self.next_node = None
        self.prev_node = None
        self.len = 1
        self.player_number = 0
        self.connected = False
        self.ready = False
        self.lost = False

    def __str__(self):
        return f"player num: {self.player_number}"

    def move(self, direction):
        self.move_nodes()
        for key in self.movement:
            self.movement[key] = False
        self.movement[direction] = True
        self.pos[1] += (self.movement['down'] - self.movement['up']) * 50
        self.pos[0] += (self.movement['right'] - self.movement['left']) * 50

    def move_nodes(self):
        p = self
        while p.next_node is not None:
            p = p.next_node
        while p.prev_node is not None:
            p.movement = p.prev_node.movement.copy()
            p.pos = list(p.prev_node.pos)
            p = p.prev_node

    def add_node(self):
        p = self
        while p.next_node is not None:
            p = p.next_node
        p.next_node = Player()
        p.next_node.movement = p.movement.copy()
        p.next_node.pos = list(p.pos)
        p.next_node.prev_node = p
        p.set_next_node_pos()
        self.len += 1

    def set_next_node_pos(self):
        if self.next_node.movement['up']:
            self.next_node.pos[1] += 50
        if self.next_node.movement['down']:
            self.next_node.pos[1] -= 50
        if self.next_node.movement['right']:
            self.next_node.pos[0] -= 50
        if self.next_node.movement['left']:
            self.next_node.pos[0] += 50

    def check_collision(self, width, height, other=None):
        if self.pos[0] < 0 or self.pos[0] >= width:
            return True
        if self.pos[1] < 0 or self.pos[1] >= height:
            return True

        p = self
        while p.next_node is not None:
            p = p.next_node
            if self.pos == p.pos:
                return True

        if other is not None and self.check_collision_with_other_player(other) is True:
            return True

        return False

    def get_list_of_nodes_pos(self):
        pos_list = []
        p = self
        while p:
            pos_list += p.pos
            p = p.next_node

        return pos_list

    def draw(self, win):
        p = self
        while p:
            player_rect = pygame.Rect(*p.pos, 50, 50)
            pygame.draw.rect(win, (64, 130, 64), player_rect)
            pygame.draw.rect(win, (255, 255, 255), player_rect, 1)
            p = p.next_node

    def reset_player(self):
        self.movement = {'up': False, 'down': False, 'right': False, 'left': False}
        self.pos = [600, 400]
        self.next_node = None
        self.prev_node = None
        self.len = 1
        self.ready = False
        self.lost = False

    def check_collision_with_other_player(self, other):
        p = other
        if self.pos == other.pos and self.len <= other.pos:
            return True
        while p.next_node is not None:
            p = p.next_node
            if self.pos == p.pos:
                return True
        return False
