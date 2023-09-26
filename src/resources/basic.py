
import json
import os
import requests
import traceback
gge_language_json = {}


with open('items.json') as f:
    game_items = json.load(f)

game_units = game_items['units']


def get_gge_language_json(LANG) -> bool:
    global gge_language_json
    #print(settings)

    try:
        if os.path.isfile('src/translations/'+str(LANG)+'12@3443.json'):
            with open('src/translations/'+str(LANG)+'12@3443.json', 'r', encoding='utf-8') as translation_file:
                gge_language_json = json.load(translation_file)
            return True
        else:
            try:
                URL = 'https://langserv.public.ggs-ep.com/12@3443/'+str(LANG)+'/*?nodecode=1'
            except:
                URL = 'https://langserv.public.ggs-ep.com/12@3443/en/*?nodecode=1'
            request = requests.get(url = URL)
            node = request.json()
            gge_language_json = node
            with open('src/translations/'+str(LANG)+'12@3443.json', 'w', encoding='utf-8') as f:
                json.dump(node, f, ensure_ascii=False)
            return True
    except Exception as e:
        print(e)
        return False
    
class Unit:
    def __init__(self, id, unit_type):
        self.id = id
        self.unit_type = unit_type
        self.name = 'None'
        self.name_lang = 'None'
        self.role = ''
        self.loot = 0
        self.speed = 0
        self.origin = ''
        self.lvl = 0
        if self.id != -1:
            self.get_unit_info()
    def get_unit_info(self):
        if self.unit_type == 'unit':
            self.melee_attack = 0
            self.range_attack = 0
            self.melee_defence = 0
            self.range_defence = 0
            self.fight_type = ''
        try:
            for unit in game_units:
                    
                if self.id == unit['wodID']:
                    if "comment2" in unit:
                        #print(unit['comment2']+'_name')
                        self.name = unit['comment2']
                        if 'level' in unit:
                            lvl_written = ' ('+gge_language_json['upgrade_buildingLevel'].format('', str(unit['level']))[1:]+')'
                        try:
                            self.name_lang = gge_language_json[unit['type'].replace(' ', '')[0].lower()+unit['type'].replace(' ', '')[1:]+'_name']
                            if 'level' in unit:
                                self.name_lang += lvl_written
                        except:
                            try:
                                self.name_lang = gge_language_json[unit['type'].replace(' ', '')+'_name']
                                if 'level' in unit:
                                    self.name_lang += lvl_written
                            except:
                                try:
                                    self.name_lang = gge_language_json[unit['type'].replace(' ', '').lower()+'_name']
                                    if 'level' in unit:
                                        self.name_lang += lvl_written
                                except:
                                    #print(unit['type'])
                                    self.name_lang = unit['comment2']
                                    if 'level' in unit:
                                        self.name_lang += lvl_written
                    else:
                        self.name = unit['comment1']
                        self.name_lang = unit['comment1']
                    if "lootValue" in unit:
                        self.loot = int(unit['lootValue'])
                    if "speed" in unit:
                        self.speed = int(unit['speed'])
                    if "role" in unit:
                        self.role = unit['role']
                    if "name" in unit:
                        self.origin = unit['name']
                    if "meleeAttack" in unit:
                        self.melee_attack = int(unit['meleeAttack'])
                    if "rangeAttack" in unit:
                        self.range_attack = int(unit['rangeAttack'])
                    if "meleeDefence" in unit:
                        self.melee_defence = int(unit['meleeDefence'])
                    if "rangeDefence" in unit:
                        self.range_defence = int(unit['rangeDefence'])
                    if self.unit_type == 'unit' and 'fameAsDef' in unit and 'fameAsOff' in unit:
                        #print(float(unit['fameAsDef']) > float(unit['fameAsOff']))
                        #print(float(unit['fameAsDef']), float(unit['fameAsOff']))
                        #print(self.name_lang, self.id, unit['fameAsDef'], unit['fameAsOff'])
                        self.fameAsDef = float(unit['fameAsDef'])
                        self.fameAsOff = float(unit['fameAsOff'])
                        if float(unit['fameAsDef']) > float(unit['fameAsOff']):
                            self.fight_type = 'def'
                        else:
                            self.fight_type = 'off'
                    if 'level' in unit:
                        self.lvl = int(unit['level'])
        except:
            traceback.print_exc()
    
    def as_dict(self):
        return vars(self)