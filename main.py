from combat.Combat import Combat
from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from utils import dice
from log import Log
from utils import json_reader
from combat.ArtFactory import ArtFactory

'''entity = Entity(is_player=True, identifier=0)

action_queue = ActionQueue(entity=entity)

print(action_queue)

action_queue.shift()
print(action_queue)
action_queue.shift()
print(action_queue)
action_queue.shift()
print(action_queue)
action_queue.shift()
print(action_queue)
action_queue.shift()

print(action_queue)'''
player = Entity(True, 0)
enemy = Entity(False, 0)
combat = Combat(player=player, enemy=enemy, player_turn=True)
combat.start()

#print(player.get_attribute_skills_indices('body'))