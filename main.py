from combat.Combat import Combat
from combat.Entity import Entity
from combat.ActionQueue import ActionQueue
from utils import dice
from log import log
from utils import json_reader
from skills.SkillFactory import SkillFactory

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
combat = Combat(player_turn=True, player=player, enemy=enemy)
combat.start()

#print(player.get_attribute_skills_indices('body'))