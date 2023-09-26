from datetime import datetime, timedelta
import time
import traceback
import requests
import data
from operator import itemgetter
import json
import os.path
import os
from pathlib import Path
import threading
from src import resources


unit_ids = []
tool_ids = []

all_info_units = []

def items_load():
    try:
        for unit in resources.basic.game_items['units']:
            if "unit" in (str(unit['name'])).lower() or "barracks" in (str(unit['name'])).lower():
                unit_ids.append(unit['wodID'])

            if "tool" in (str(unit['name'])).lower() or "workshop" in (str(unit['name'])).lower():
                tool_ids.append(unit['wodID'])
            
        #print(unit_ids)
        #print(tool_ids)
        for unit in unit_ids:
            all_info_units.append(resources.basic.Unit(unit, 'unit'))
        for tool in tool_ids:
            all_info_units.append(resources.basic.Unit(tool, 'tool'))
    except:
        traceback.print_exc()

def get_unit(unit_id):
    for unit in all_info_units:
        if unit.id == unit_id:
            return unit
    return unit_id

class CastleData:
    def __init__(self, KID, id, name, x, y, castle_type):
        self.castle_type = castle_type #post, main, metro, etc
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.stable_id = []
        self.KID = KID
        self.loaded = False
        self.units = []
        self.tools = []
        
        self.update_date = datetime.now()
    def update(self, wood, stone, food, coal, olive, glass, aquamarine, iron, honey, mead, wall_troops, 
                     wood_storage, stone_storage, food_storage, coal_storage, olive_storage, glass_storage, iron_storage, honey_storage, mead_storage,
                     wood_production, stone_production, food_production, coal_production, olive_production, glass_production, iron_production, relative_honey_production, mead_production,
                     food_consumption, mead_consumption, food_consumption_rate, mead_consumption_rate):
            
        try:
            self.loaded = True
            self.update_date = datetime.now()
            self.wood = wood
            self.stone = stone
            self.food = food
            self.coal = coal
            self.olive = olive
            self.glass = glass
            self.aquamarine = aquamarine
            self.iron = iron
            self.honey = honey
            self.mead = mead

            self.wood_storage = wood_storage
            self.stone_storage = stone_storage
            self.food_storage = food_storage
            self.coal_storage = coal_storage
            self.olive_storage = olive_storage
            self.glass_storage = glass_storage
            self.iron_storage = iron_storage
            self.honey_storage = honey_storage
            self.mead_storage = mead_storage

            self.wood_production = wood_production/10
            self.stone_production = stone_production/10
            self.food_production = food_production/10
            self.coal_production = coal_production/10
            self.olive_production = olive_production/10
            self.glass_production = glass_production/10
            self.iron_production = iron_production/10
            self.mead_production = mead_production/10

            self.food_consumption = food_consumption/10
            self.mead_consumption = mead_consumption/10

            self.food_consumption_rate = food_consumption_rate
            self.mead_consumption_rate = mead_consumption_rate
            self.wall_troops_count_basic = wall_troops

            self.relative_honey_production = relative_honey_production/10

            self.calculate_real_consumption()
        except:
            traceback.print_exc()
    
    
    def calculate_real_consumption(self):
        self.real_food_consumption = (self.food_consumption) * (self.food_consumption_rate/100)
        self.real_mead_consumption = (self.mead_consumption) * (self.mead_consumption_rate/100)

        self.relative_food_production = (self.food_production) - self.real_food_consumption
        self.relative_mead_production = (self.mead_production) - self.real_mead_consumption
        #gui_functions.update_castle_info_stats(self)
    def update_on_grc(self, wood, stone, food, coal, olive, glass, aquamarine, iron, honey, mead):
        self.update_date = datetime.now()
        self.wood = wood
        self.stone = stone
        self.food = food
        self.coal = coal
        self.olive = olive
        self.glass = glass
        self.aquamarine = aquamarine
        self.iron = iron
        self.honey = honey
        self.mead = mead
        self.calculate_real_consumption()
    def update_on_gpa(self, food_production, food_consumption, relative_honey_production, mead_production, mead_consumption):
        self.food_production = food_production/10
        self.food_consumption = food_consumption/10
        self.relative_honey_production = relative_honey_production/10
        self.mead_production = mead_production/10
        self.mead_consumption = mead_consumption/10

        self.calculate_real_consumption()
    def update_locally(self):
        time_between_updates = (datetime.now()-self.update_date).total_seconds()
        self.wood += (self.wood_production/3600)*time_between_updates
        self.stone += (self.stone_production/3600)*time_between_updates
        self.food += (self.relative_food_production/3600)*time_between_updates
        self.coal += (self.coal_production/3600)*time_between_updates
        self.olive += (self.olive_production/3600)*time_between_updates
        self.glass += (self.glass_production/3600)*time_between_updates
        self.iron += (self.iron_production/3600)*time_between_updates
        self.honey += (self.relative_honey_production/3600)*time_between_updates
        self.mead += (self.relative_mead_production/3600)*time_between_updates
        self.calculate_real_consumption()
        self.update_date = datetime.now()

    def update_units(self, units):
        #print(self.name)
        try:
            def sort_list_by_amount(list):
                return sorted(list, key=itemgetter(1), reverse=True)
            self.units = []
            self.tools = []
            #print(unit_ids)
            for unit in units:
                #print(unit[0])
                if unit[0] in unit_ids:
                    #print(unit)
                    for class_unit in all_info_units:
                        if class_unit.id == unit[0]:
                            self.units.append([class_unit, unit[1]])
                if unit[0] in tool_ids:
                    for class_unit in all_info_units:
                        if class_unit.id == unit[0]:
                            self.tools.append([class_unit, unit[1]])
            self.units = sort_list_by_amount(self.units)
            #print(self.units)
            for i in self.units:
                pass
        except:
            traceback.print_exc()
    def as_dict(self):
        return vars(self)


class Event:
    def __init__(self, name, event_type):
        self.status = False
        self.active = False
        self.name = name
        self.event_type = event_type
        self.attacking_type = 0

        self.can_attack = True

        self.cords = []
        self.extra_cords = [] # beri 0 - red, 1 - blue
        self.target = []
        # pvp mass attack 0 - alliance, 1 - player
        self.target_type = 0  
        self.min_target_lvl = 1
        self.target_attack_once = False

        self.target_wait_list = []

        self.sender_castle_id = 0

        self.sender_castles = []
        self.helper_castle = False
        self.skip_range = 0
        self.scan_range = 5

        self.waiting_for_map_size = False
        self.map_size = 0
        self.data = []
        self.is_scanning_map = False
        self.last_map_scan = time.time()

        self.presets = [] # index of gas
        self.presets_additional = [] # for multiple types of targets like aqua
        self.fill_waves_count = -1
        self.fill_waves_count_additional = -1 # for multiple types of targets like aqua
        self.auto_fill = False
        self.fill_waves = True # if true last defined preset will fill rest of not definded waves
        self.final_wave_troop_id = -1
        self.final_wave_active = False

        self.normal_comm = True
        self.allow_vip_comm = False
        self.allow_vip_comm_rubies = False
        self.horse_type = 0
        self.EDID = 0
        self.event_difficulty = 0

        self.score_boost = False #for example heritage boosters on OR 
        self.booster_amount = 0
        self.booster_id = 0

        self.cooldown = 0

        self.flank_no_bonus_overwrite = 0 # if 0 -> skip
        self.front_no_bonus_overwrite = 0 # if 0 -> skip


        self.auto_refill_def_tools = False
        self.auto_refill_def_tools_castle = ''
        self.auto_trigger_attack = False
    def start(self, target, presets): ...
       

    def stop(self):
        self.status = False
    def clear(self):
        self.status = False
        self.target = ""
        self.presets = []
    def as_dict(self):
        return vars(self)

class Module:
    def __init__(self, name, data, args):
        self.name = name
        self.data = data
        self.args = args
        self.state = ''
    def start(self, action, data, args):
        ...

class AttackData:
    def __init__(self, level):
        self.waves = 1
        self.front = 192
        self.flank = 64
        self.front_bonus = 0
        self.flank_bonus = 0
        
        if level > 13:
            self.waves += 1
        if level > 26:
            self.waves += 1
        if level > 51:
            self.waves += 1

class PlayerData:
    def __init__(self, *args, **kwargs):
        self.reconnected = False
        self.player_id = 0
        self.player_id_main_account = 0
        self.username = ""
        self.username_main_account = ""
        self.password = ""
        self.server_type = 'normal'
        self.lvl = 1
        self.LL = 0
        self.world = ""
        self.world_main_account = ""
        self.zone = "EmpireEx"
        self.url = ""
        self.server_id = ""
        self.current_castle_id_gge_ui = 0
        self.online = False
        self.castles_green = []
        self.castles_sand = []
        self.castles_winter = []
        self.castles_peaks = []
        self.castles_aqua = []
        self.castles_berimond = []
        self.bought_researches = []
        self.relic_resources = {}
        self.crafting_data = {}
        self.crafting_queue = {}
        self.crafting_buildings_oid = []
        self.crafting_buildings_lvl = [0,0]
        #self.is_processing_craft_data = False
        self.is_in_castle = []

        self.current_KID = 0

        self.attacked_obiect = []

        self.is_processing_attack_data = False
        self.object_last_cooldown = 0
        self.object_last_cooldown_time = datetime.now()
        self.last_attack_sent_at = datetime.now() # updates at 'cra'
        self.last_cra_at = datetime.now()
        self.basic_commanders_info = []

        self.gbd = {}
        self.last_brewery_change_castle_id = []
        self.alliance_help_waiting = False
        self.gie = {} #generals
        self.gbc = {} #packages purchased 
        self.silver_tokens = 0
        self.gold_tokens = 0
        self.affluence_tickets = 0
        self.skips = {'1min':0, '5min':0, '10min':0, '30min':0, '1h':0, '5h':0, '24h':0}
        self.feathers = 0
        self.general_reset_tokens = 0
        self.vip_commanders = 0
        self.alliance_chat = []
        self.collected_KT = 0
        self.collected_KM = 0
        self.collected_ST = 0

        self.commanders_all = []
        self.castellans_all = []
        self.commanders_not_available = []
        self.commanders_excluded = []
        self.commanders_excluded_smart = []
        #self.generals_presets = {}

        self.technicus_lvl = 0

        self.nomad = Event('nomad', 'npc')
        self.khan = Event('khan', 'npc')
        self.samurai = Event('samurai', 'npc')
        self.beri = Event('beri', 'npc')
        self.crow = Event('crow', 'pvp')
        self.beri_world = Event('beri_world', 'npc')
        self.towers = Event('towers', 'npc')
        self.towers.target_attack_once = True
        self.aqua = Event('aqua', 'npc')
        self.aqua.target_attack_once = True
        self.fort = Event('fort', 'npc')
        self.fort.target_attack_once = True
        self.pvp_mass_attack = Event('pvp_mass_attack', 'pvp')
        self.or_rank_swap = Event('or_rank_swap', 'pvp')
        self.or_collector = Event('or_collector', 'pvp')
        self.bth_capitals = Event('bth_capitals', 'pvp')
        self.bth_capitals.target_attack_once = True
        # self.bth_capitals.normal_comm = False
        self.bth_capitals.allow_vip_comm = True
        self.wheel_spin = Event('wheel_spin', 'npc')
        #self.pvp = Event('pvp', 'pvp')
        self.aqua.active = True
        self.towers.active = True
        self.pvp_mass_attack.active = True
        self.towers.active = True

        
        self.sell_eq = Module('sell_eq', [0, False, False, False, False, False, False, False, False], [])
        self.sell_gems = Module('sell_gems', [0, False, False, False, False, False, False, False], [])
        self.sell_regular = Module('sell_regular', [0, False, False, False, False, False, False], [[], []])
        self.set_commander_eq = Module('set_commander_eq', [0, 0, []], [])
        self.set_castellan_eq = Module('set_castellan_eq', [0, 0, []], [])
        self.set_commander_gem = Module('set_commander_gem', [0, 0, []], [])
        self.set_castellan_gem = Module('set_castellan_gem', [0, 0, []], [])
        self.set_commander_eq_3bonus = Module('set_commander_eq_3bonus', [0, 0, []], [])
        self.set_castellan_eq_3bonus = Module('set_castellan_eq_3bonus', [0, 0, []], [])
        self.set_commander_gem_3bonus = Module('set_commander_gem_3bonus', [0, 0, []], [])
        self.set_castellan_gem_3bonus = Module('set_castellan_gem_3bonus', [0, 0, []], [])
        self.or_rank_swap_data_gathering = Module('or_rank_swap_data_gathering', [], [])
        self.or_collector_data_gathering = Module('or_collector_data_gathering', [], [])
        self.bth_capitals_data_gathering = Module('bth_capitals_data_gathering', [[],[[],[]],[],[]], [])
        


        self.pvp_attack = AttackData(70)
        self.npc_attack = AttackData(70)
    def user_create(self, username, password, world, server_type):
        print('user_create', username, password, world, server_type)
        self.server_type = server_type
        self.username = username
        self.password = password
        self.world = world
    def get_element_from_all_castles(self, element):
        all_castles = []
        castle_lists = [self.castles_green, 
                    self.castles_winter,
                    self.castles_berimond,
                    self.castles_aqua, 
                    self.castles_sand,
                    self.castles_peaks]
        for castle_list in castle_lists:
            for castle in castle_list:
                all_castles.append(castle.as_dict()[element])
        return all_castles
    def get_castle(self, KID, id, castle_type):
        """
        if you are getting the castle by id then leave castle_type as 0
        if you are getting the castle by castle_type then leave id as 0
        castle_types:
        1 - main green
        4 - outpost
        22 - metro
        12 - main kingdoms
        """
        if KID == 1:
            castles_in_kingdom = self.castles_sand
        elif KID == 2:
            castles_in_kingdom = self.castles_winter
        elif KID == 3:
            #print('peaks')
            castles_in_kingdom = self.castles_peaks
        elif KID == 4:
            castles_in_kingdom = self.castles_aqua
        elif KID == 10:
            castles_in_kingdom = self.castles_berimond
        else:
            castles_in_kingdom = self.castles_green

        #print(KID, id, castle_type) 
        if id != 0:
            for castle in castles_in_kingdom:
                #print(castle.id, id)
                if castle.id == id:
                    return castle

            return None
        elif castle_type != 0:
            #print('else')
            for castle in castles_in_kingdom:
                if castle.castle_type == castle_type:
                    #print('castle by type')
                    return castle

            return None

    def add_new_castle(self, KID, id, name, x, y, castle_type):
        exists = False
        if KID == 0:
            for castle in self.castles_green:
                if castle.id == id:
                    exists = True
            if not exists:
                self.castles_green.append(CastleData(KID, id, name, x, y, castle_type))
                #print('appended')
        if KID == 1:
            for castle in self.castles_sand:
                if castle.id == id:
                    exists = True
            if not exists:
                self.castles_sand.append(CastleData(KID, id, name, x, y, castle_type))
        if KID == 2:
            for castle in self.castles_winter:
                if castle.id == id:
                    exists = True
            if not exists:
                self.castles_winter.append(CastleData(KID, id, name, x, y, castle_type))
        if KID == 3:
            for castle in self.castles_peaks:
                if castle.id == id:
                    exists = True
            if not exists:
                self.castles_peaks.append(CastleData(KID, id, name, x, y, castle_type))
        if KID == 4:
            for castle in self.castles_aqua:
                if castle.id == id:
                    exists = True
            if not exists:
                self.castles_aqua.append(CastleData(KID, id, name, x, y, castle_type))
        if KID == 10:
            for castle in self.castles_berimond:
                if castle.id == id:
                    exists = True
            if not exists:
                self.castles_berimond.append(CastleData(KID, id, name, x, y, castle_type))
    def as_dict(self):
        return vars(self)

    

MainAccount = PlayerData()