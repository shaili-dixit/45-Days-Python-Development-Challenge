"""
Dictionary-Driven Text Adventure Game Engine with Inventory System
Rooms, items, NPCs defined via dicts; move/pick up/interact; win/lose conditions.
"""

import random

WORLD = {
    'rooms': {
        'entrance': {
            'name': 'Castle Entrance',
            'description': 'A grand archway leads into a crumbling castle. Torches flicker along the walls.',
            'exits': {'north': 'great_hall', 'east': 'garden'},
            'items': ['rusty_key'],
            'npcs': [],
        },
        'great_hall': {
            'name': 'Great Hall',
            'description': 'A vast hall with a long table. Dusty portraits line the walls. A locked door is to the north.',
            'exits': {'south': 'entrance', 'east': 'kitchen', 'north': 'tower'},
            'items': ['old_map', 'coin'],
            'npcs': ['guard'],
            'locked': True,
            'lock_key': 'rusty_key',
        },
        'garden': {
            'name': 'Overgrown Garden',
            'description': 'A once-beautiful garden now overrun by weeds. A glimmer catches your eye.',
            'exits': {'west': 'entrance', 'north': 'kitchen'},
            'items': ['healing_potion', 'shovel'],
            'npcs': [],
        },
        'kitchen': {
            'name': 'Kitchen',
            'description': 'Pots and pans hang everywhere. A fire crackles. Someone was here recently.',
            'exits': {'west': 'great_hall', 'south': 'garden'},
            'items': ['bread', 'knife'],
            'npcs': ['cook'],
        },
        'tower': {
            'name': 'Tower Dungeon',
            'description': 'A dark spiral staircase leads up. At the top, the ancient artifact glows.',
            'exits': {'south': 'great_hall'},
            'items': ['ancient_artifact'],
            'npcs': ['dark_wizard'],
        },
    },
    'items': {
        'rusty_key':       {'name': 'Rusty Key',       'description': 'An old key, likely opens something nearby.', 'weight': 1},
        'old_map':         {'name': 'Old Map',         'description': 'A map of the castle with a marked chamber.', 'weight': 1},
        'coin':            {'name': 'Gold Coin',       'description': 'A gleaming gold coin worth keeping.',        'weight': 1},
        'healing_potion':  {'name': 'Healing Potion',  'description': 'Restores 30 HP when consumed.',             'weight': 1, 'usable': True, 'heal': 30},
        'shovel':          {'name': 'Shovel',          'description': 'Useful for digging.',                       'weight': 3},
        'bread':           {'name': 'Bread Loaf',      'description': 'Restores 10 HP when consumed.',             'weight': 1, 'usable': True, 'heal': 10},
        'knife':           {'name': 'Knife',           'description': 'A sharp kitchen knife. Useful in combat.',  'weight': 1, 'weapon': True, 'damage': 10},
        'ancient_artifact':{'name': 'Ancient Artifact','description': 'The goal of your quest! It radiates power.','weight': 5, 'quest_item': True},
    },
    'npcs': {
        'guard': {
            'name': 'Gruff Guard',
            'dialogue': ['Who goes there?', 'Move along.', 'The tower is dangerous.'],
            'hostile': False,
        },
        'cook': {
            'name': 'Friendly Cook',
            'dialogue': ['Help yourself to some bread!', 'Careful in the tower.', 'The wizard is powerful!'],
            'hostile': False,
            'gives': 'bread',
        },
        'dark_wizard': {
            'name': 'Dark Wizard',
            'dialogue': ['You dare enter my tower?', 'Begone!'],
            'hostile': True,
            'hp': 50,
            'damage': 20,
        },
    },
}


class Player:
    def __init__(self, name="Hero"):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.inventory = []
        self.current_room = 'entrance'
        self.score = 0
        self.visited = set()

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def has_item(self, item_id):
        return item_id in self.inventory

    def status(self):
        bar = '█' * int(self.hp / 10) + '░' * (10 - int(self.hp / 10))
        print(f"  HP: [{bar}] {self.hp}/{self.max_hp}  Score: {self.score}  Items: {len(self.inventory)}")


class GameEngine:
    def __init__(self):
        import copy
        self.world = copy.deepcopy(WORLD)
        self.player = None
        self.game_over = False
        self.won = False

    def start(self, player_name):
        self.player = Player(player_name)
        print(f"\n  Welcome, {player_name}! Find the Ancient Artifact and escape the castle.")
        print("  Commands: go <dir> | take <item> | use <item> | look | talk | inventory | status | quit\n")
        self.look()

    def look(self):
        p = self.player
        room = self.world['rooms'][p.current_room]
        p.visited.add(p.current_room)
        print(f"\n  📍 {room['name']}")
        print(f"  {room['description']}")
        exits = ', '.join(f"{d.upper()}" for d in room['exits'])
        print(f"  Exits: {exits}")
        if room['items']:
            items = ', '.join(self.world['items'][i]['name'] for i in room['items'])
            print(f"  Items: {items}")
        if room['npcs']:
            npcs = ', '.join(self.world['npcs'][n]['name'] for n in room['npcs'])
            print(f"  People: {npcs}")

    def go(self, direction):
        p = self.player
        room = self.world['rooms'][p.current_room]
        if direction not in room['exits']:
            print(f"  ✗ You can't go {direction} from here.")
            return
        dest = room['exits'][direction]
        dest_room = self.world['rooms'][dest]

        # Check locked
        if dest_room.get('locked'):
            key = dest_room.get('lock_key')
            if key and not p.has_item(key):
                print(f"  🔒 The door is locked. You need the {self.world['items'][key]['name']}.")
                return
            else:
                dest_room['locked'] = False
                print(f"  🔓 You unlocked the door with the {self.world['items'][key]['name']}!")

        # Check hostile NPCs
        for npc_id in room['npcs']:
            npc = self.world['npcs'][npc_id]
            if npc.get('hostile') and npc.get('hp', 0) > 0:
                self.combat(npc_id)
                if not p.is_alive():
                    return

        p.current_room = dest
        p.score += 5
        self.look()

    def take(self, item_name):
        p = self.player
        room = self.world['rooms'][p.current_room]
        # Find item by name or partial match
        found = None
        for item_id in room['items']:
            if item_name.lower() in self.world['items'][item_id]['name'].lower():
                found = item_id
                break
        if not found:
            print(f"  ✗ No '{item_name}' here to take.")
            return
        room['items'].remove(found)
        p.inventory.append(found)
        p.score += 10
        item = self.world['items'][found]
        print(f"  ✓ Picked up: {item['name']}. {item['description']}")
        if item.get('quest_item'):
            print(f"\n  🏆 You found the Ancient Artifact! Head to the entrance to win!")
            self.won = p.current_room == 'entrance'

    def use(self, item_name):
        p = self.player
        found = None
        for item_id in p.inventory:
            if item_name.lower() in self.world['items'][item_id]['name'].lower():
                found = item_id
                break
        if not found:
            print(f"  ✗ You don't have '{item_name}'.")
            return
        item = self.world['items'][found]
        if item.get('usable'):
            heal = item.get('heal', 0)
            p.heal(heal)
            p.inventory.remove(found)
            print(f"  ✓ Used {item['name']}. Restored {heal} HP.")
            p.status()
        else:
            print(f"  ✗ You can't use {item['name']} that way.")

    def talk(self):
        p = self.player
        room = self.world['rooms'][p.current_room]
        if not room['npcs']:
            print("  There's no one here to talk to.")
            return
        for npc_id in room['npcs']:
            npc = self.world['npcs'][npc_id]
            if npc.get('hostile') and npc.get('hp', 0) > 0:
                print(f"  {npc['name']}: \"{random.choice(npc['dialogue'])}\"")
                print(f"  They look hostile! Type 'fight' to engage.")
            else:
                print(f"  {npc['name']}: \"{random.choice(npc['dialogue'])}\"")
                if npc.get('gives') and npc['gives'] not in p.inventory:
                    gives = npc['gives']
                    p.inventory.append(gives)
                    print(f"  {npc['name']} gives you the {self.world['items'][gives]['name']}!")
                    npc.pop('gives')

    def combat(self, npc_id):
        p = self.player
        npc = self.world['npcs'][npc_id]
        print(f"\n  ⚔  COMBAT with {npc['name']}!")
        weapon = next((self.world['items'][i] for i in p.inventory
                       if self.world['items'][i].get('weapon')), None)
        p_damage = weapon['damage'] if weapon else 5

        while npc['hp'] > 0 and p.is_alive():
            action = input(f"  {npc['name']} HP:{npc['hp']}  Your HP:{p.hp} — [a]ttack/[r]un: ").strip().lower()
            if action == 'r':
                print("  You fled!")
                return
            if action == 'a':
                npc['hp'] -= p_damage
                print(f"  You deal {p_damage} damage. {npc['name']} has {max(0,npc['hp'])} HP.")
                if npc['hp'] > 0:
                    p.take_damage(npc['damage'])
                    print(f"  {npc['name']} hits you for {npc['damage']} damage. Your HP: {p.hp}")
                    if not p.is_alive():
                        print(f"  💀 You were defeated by {npc['name']}!")
                        self.game_over = True
                        return

        if npc['hp'] <= 0:
            print(f"  ✓ Defeated {npc['name']}! +50 score")
            p.score += 50
            npc['hostile'] = False

    def inventory(self):
        p = self.player
        if not p.inventory:
            print("  Inventory is empty.")
        else:
            print("  Your inventory:")
            for item_id in p.inventory:
                item = self.world['items'][item_id]
                print(f"    • {item['name']} — {item['description']}")

    def check_win(self):
        p = self.player
        if p.has_item('ancient_artifact') and p.current_room == 'entrance':
            print(f"\n  🎉 CONGRATULATIONS, {p.name}! You retrieved the Ancient Artifact and escaped!")
            print(f"  Final Score: {p.score + 200}")
            self.game_over = True
            self.won = True

    def play(self, player_name="Hero"):
        self.start(player_name)
        while not self.game_over:
            self.check_win()
            if self.game_over:
                break
            cmd = input("\n  > ").strip().lower().split()
            if not cmd:
                continue
            action = cmd[0]
            arg = ' '.join(cmd[1:]) if len(cmd) > 1 else ''

            if action in ('go', 'move', 'walk'):
                self.go(arg)
            elif action in ('take', 'pick', 'get'):
                self.take(arg)
            elif action == 'use':
                self.use(arg)
            elif action in ('look', 'l'):
                self.look()
            elif action == 'talk':
                self.talk()
            elif action in ('inventory', 'inv', 'i'):
                self.inventory()
            elif action == 'status':
                self.player.status()
            elif action in ('quit', 'exit', 'q'):
                print("  Thanks for playing!")
                break
            else:
                print(f"  ✗ Unknown command: '{action}'. Try: go, take, use, look, talk, inventory, status, quit")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Text Adventure Game Engine v1.0       ║")
    print("╚══════════════════════════════════════════╝")
    name = input("\n  Enter your character's name: ").strip() or "Hero"
    game = GameEngine()
    game.play(name)


if __name__ == "__main__":
    main()
