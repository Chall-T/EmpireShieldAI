from __future__ import annotations
from typing import Optional, List, Union
from .basic import game_items

CHEST = 1
WEAPON = 2
HELMET = 3
ARTEFACT = 4
SKIN = 5
HERO = 6

MELEE_MAX = 140
MELEE_GEMS_MAX = 50
MELEE_LORD_MAX = 50
RANGE_MAX = 140
RANGE_GEMS_MAX = 50
RANGE_LORD_MAX = 50
COURTYARD_MAX = 100
COURTYARD_GEMS_MAX = 60
COURTYARD_LORD_MAX = 60
FLANK_MAX = 50
FLANK_GEMS_MAX = 40
FLANK_LORD_MAX = 40
WALL_MAX = 160
WALL_GEMS_MAX = 60
WALL_LORD_MAX = 60
GATE_MAX = 160
GATE_GEMS_MAX = 60
GATE_LORD_MAX = 60
MOAT_MAX = 120
MOAT_GEMS_MAX = 30
MOAT_LORD_MAX = 30
UNITS_ON_WALL_MAX = 50
UNITS_ON_WALL_GEMS_MAX = 40
UNITS_ON_WALL_LORD_MAX = 40
class LordEffects:
    melee = 0.0
    melee_gems = 0.0
    melee_lord = 0.0
    range = 0.0
    range_gems = 0.0
    range_lord = 0.0
    courtyard = 0.0
    courtyard_gems = 0.0
    courtyard_lord = 0.0
    wall = 0.0
    wall_gems = 0.0
    wall_lord = 0.0
    gate = 0.0
    gate_gems = 0.0
    gate_lord = 0.0
    moat = 0.0
    moat_gems = 0.0
    moat_lord = 0.0
    flank = 0.0
    flank_gems = 0.0
    flank_lord = 0.0
    front = 0.0
    front_gems = 0.0
    front_lord = 0.0
    unit_bonus_ids = []
    unit_bonus_count = 0
    waves = 0
    waves_flank = 0
    waves_front = 0
    units_on_wall = 0.0
    units_on_wall_gems = 0.0
    units_on_wall_lord = 0.0
    def add_equipment_bonuses(self, equipment: 'Equipment'):
        self.melee += equipment.melee
        self.melee_gems += equipment.melee_gems
        self.melee_lord += equipment.melee_lord
        self.range += equipment.range
        self.range_gems += equipment.range_gems
        self.range_lord += equipment.range_lord
        self.courtyard += equipment.courtyard
        self.courtyard_gems += equipment.courtyard_gems
        self.courtyard_lord += equipment.courtyard_lord
        self.wall += equipment.wall
        self.wall_gems += equipment.wall_gems
        self.wall_lord += equipment.wall_lord
        self.gate += equipment.gate
        self.gate_gems += equipment.gate_gems
        self.gate_lord += equipment.gate_lord
        self.moat += equipment.moat
        self.moat_gems += equipment.moat_gems
        self.moat_lord += equipment.moat_lord
        self.flank += equipment.flank
        self.flank_gems += equipment.flank_gems
        self.flank_lord += equipment.flank_lord
        self.front += equipment.front
        self.front_gems += equipment.front_gems
        self.front_lord += equipment.front_lord
        self.unit_bonus_ids =equipment.unit_bonus_ids
        self.unit_bonus_count =equipment.unit_bonus_count
        self.waves += equipment.waves
        self.waves_flank += equipment.waves_flank
        self.waves_front += equipment.waves_front
        self.units_on_wall += equipment.units_on_wall
        self.units_on_wall_gems += equipment.units_on_wall_gems
        self.units_on_wall_lord += equipment.units_on_wall_lord
        
        if self.melee >= MELEE_MAX: self.melee = MELEE_MAX
        if self.melee_gems >= MELEE_GEMS_MAX: self.melee_gems = MELEE_GEMS_MAX
        if self.melee_lord >= MELEE_LORD_MAX: self.melee_lord = MELEE_LORD_MAX
        if self.range >= RANGE_MAX: self.range = RANGE_MAX
        if self.range_gems >= RANGE_GEMS_MAX: self.range_gems = RANGE_GEMS_MAX
        if self.range_lord >= RANGE_LORD_MAX: self.range_lord = RANGE_LORD_MAX
        if self.courtyard >= COURTYARD_MAX: self.courtyard = COURTYARD_MAX
        if self.courtyard_gems >= COURTYARD_GEMS_MAX: self.courtyard_gems = COURTYARD_GEMS_MAX
        if self.courtyard_lord >= COURTYARD_LORD_MAX: self.courtyard_lord = COURTYARD_LORD_MAX
        if self.wall >= WALL_MAX: self.wall = WALL_MAX
        if self.wall_gems >= WALL_GEMS_MAX: self.wall_gems = WALL_GEMS_MAX
        if self.wall_lord >= WALL_LORD_MAX: self.wall_lord = WALL_LORD_MAX
        if self.gate >= GATE_MAX: self.gate = GATE_MAX
        if self.gate_gems >= GATE_GEMS_MAX: self.gate_gems = GATE_GEMS_MAX
        if self.gate_lord >= GATE_LORD_MAX: self.gate_lord = GATE_LORD_MAX
        if self.moat >= MOAT_MAX: self.moat = MOAT_MAX
        if self.moat_gems >= MOAT_GEMS_MAX: self.moat_gems = MOAT_GEMS_MAX
        if self.moat_lord >= MOAT_LORD_MAX: self.moat_lord = MOAT_LORD_MAX
        if self.flank >= FLANK_MAX: self.flank = FLANK_MAX
        if self.flank_gems >= FLANK_GEMS_MAX: self.flank_gems = FLANK_GEMS_MAX
        if self.flank_lord >= FLANK_LORD_MAX: self.flank_lord = FLANK_LORD_MAX
        if self.front >= FLANK_MAX: self.front = FLANK_MAX
        if self.front_gems >= FLANK_GEMS_MAX: self.front_gems = FLANK_GEMS_MAX
        if self.front_lord >= FLANK_LORD_MAX: self.front_lord = FLANK_LORD_MAX
        if self.units_on_wall >= UNITS_ON_WALL_MAX: self.units_on_wall = UNITS_ON_WALL_MAX
        if self.units_on_wall_gems >= UNITS_ON_WALL_GEMS_MAX: self.units_on_wall_gems = UNITS_ON_WALL_GEMS_MAX
        if self.units_on_wall_lord >= UNITS_ON_WALL_LORD_MAX: self.units_on_wall_lord = UNITS_ON_WALL_LORD_MAX
class Equipment(LordEffects):
    def __init__(self, element, element_type) -> None:
        if len(element) == 0:
            return None
        equipment = element[5]
        gem = []

        if element_type not in [SKIN, HERO]:
            gem = element[-1][-1][4]

        self.add_bonuses(equipment, element_type)
        if len(gem) > 0:
            self.add_bonuses(gem, element_type)

    def add_bonuses(self, element, element_type):
        print(element)
        for effect in element:
            if element_type == SKIN:
                if effect[0] == 21:
                    self.waves += effect[-1][0]
                if effect[0] == 19:
                    self.waves_flank += effect[-1][0]
                if effect[0] == 20:
                    self.waves_front += effect[-1][0]

            if effect[0] == [20018]: self.waves +=1

            if effect[0] in [10113, 10301]: self.units_on_wall += effect[-1][0]
            if effect[0] in [10201, 10313]: self.units_on_wall_gems += effect[-1][0]
            if effect[0] in [10515]: self.units_on_wall_lord += effect[-1][0]

            if effect[0] in [115, 201, 301]: self.flank += effect[-1][0]
            if effect[0] in [313, 307]: self.flank_gems += effect[-1][0]
            if effect[0] in [811]: self.flank_lord += effect[-1][0]

            if effect[0] in [117]: self.front += effect[-1][0]
            if effect[0] in [315]: self.front_gems += effect[-1][0]
            if effect[0] in [812]: self.front_lord += effect[-1][0]

            if effect[0] in [1, 108, 10005, 10111]: self.melee += effect[-1][0]
            if effect[0] in [305, 311, 10305, 10311]: self.melee_gems += effect[-1][0]
            if effect[0] in [813, 10513]: self.melee_lord += effect[-1][0]

            if effect[0] in [2, 109, 10006, 10112]: self.range += effect[-1][0]
            if effect[0] in [306, 312, 10306, 10312]: self.range_gems += effect[-1][0]
            if effect[0] in [814, 10514]: self.range_lord += effect[-1][0]

            if effect[0] in [116, 10114, 302]: self.courtyard += effect[-1][0]
            if effect[0] in [308, 314, 10314, 10202, 10302]: self.courtyard_gems += effect[-1][0]
            if effect[0] in [805, 810, 10516]: self.courtyard_lord += effect[-1][0]

            if effect[0] in [3, 103, 110, 10002, 10102]: self.wall += effect[-1][0]
            if effect[0] in [303, 309, 10303, 10309]: self.wall_gems += effect[-1][0]
            if effect[0] in [803, 808, 10511]: self.wall_lord += effect[-1][0]

            if effect[0] in [4, 104, 111, 10003, 10103]: self.gate += effect[-1][0]
            if effect[0] in [304, 310, 10304, 10309]: self.gate_gems += effect[-1][0]
            if effect[0] in [804, 809, 10506,  10512]: self.gate_lord += effect[-1][0]

            if effect[0] in [5, 105, 112, 10004, 10104]: self.moat += effect[-1][0]
            if effect[0] in [305, 317, 10305, 10310]: self.moat_gems += effect[-1][0]
            if effect[0] in [802, 807, 10504, 10511]: self.moat_lord += effect[-1][0]


            # if effect[0] in [20017, 20004, 20005]:
                
            #     for value in range(len(effect[-1][0])):
            #         if value % 2 == 0:
            #             self.unit_bonus_ids.append(effect[-1][0][value])
            #         else:
            #             self.unit_bonus_count = effect[-1][0][value]
class Commander:
    commanders: List
    id: int
    wid: int
    vis: int
    n: str
    gid: int
    w: int
    d: int
    spr: int
    eq: List
    l: Optional[int]
    st: Optional[int]
    armor_equipment = Equipment([], CHEST)
    artifact_equipment = Equipment([], ARTEFACT)
    helmet_equipment = Equipment([], HELMET)
    skin_equipment = Equipment([], SKIN)
    weapon_equipment = Equipment([], WEAPON)
    hero_equipment = Equipment([], HERO)
    def __init__(self, data) -> None:
        self.id = data['ID'] # LORD_ID
        self.wid = data['WID'] # WEARER_ID
        self.vis = data['VIS'] # LORD_LOOK
        self.n = data['N'] # LORD_NAME
        self.gid = data['GID'] # GENERAL_ID
        self.w = data['W'] # WINS
        self.d = data['D'] # DEFEATS
        self.spr = data['SPR'] # WINNING_SPREE
        self.eq = data['EQ'] # EQUIPMENT
        self.l = data.setdefault('L', -1) # LORDS
        self.st = data.setdefault('ST', -1) # STAR_TIER
        self.picID = 0
        self.parseLord(data)
    def createEquipment(self, equipment):
        if len(equipment) >= 12 and equipment[11] == 3:
            #RelicEquipment
            return Equipment(equipment, equipment[1])
        else:
            if equipment[1] == HERO:
                #CastleHero
                return Equipment(equipment, equipment[1])
            else:
                #BasicEquipment
                return Equipment(equipment, equipment[1])
    def parseLord(self, data):
        if data != None:
            self.id = int(data['ID']),
            self.equipmentSlots = {}
            self.equipmentSlots['helmet'] = {}
            self.equipmentSlots['chest'] = {}
            self.equipmentSlots['weapon'] = {}
            self.equipmentSlots['artefact'] = {}
            self.equipmentSlots['skin'] = {}
            self.equipmentSlots['hero'] = {}
            #self.hardModeEffects = self.parseRawEffects(e.HME),
            #self.rawLordEffects = self.parseRawEffects(e.E),
            #self.areaEffects = self.parseRawEffects(e.AE),
            self.wins = int(data['W'])
            self.defeats = int(data['D'])
            self.winSpree = int(data['SPR'])
            if (data['EQ'] and len(data['EQ']) > 0):
                #for (var n = 0, o = data['EQ']; n < o.length; n++) {
                for n in range(len(data['EQ'])):
                    equipment = data['EQ'][n]
                    if (len(equipment) > 0):
                        s = self.createEquipment(equipment)
                        if (equipment[1]) == CHEST:
                            self.armor_equipment = s
                        elif (equipment[1]) == ARTEFACT:
                            self.artifact_equipment = s
                        elif (equipment[1]) == HELMET:
                            self.helmet_equipment = s
                        elif (equipment[1]) == SKIN:
                            self.skin_equipment = s
                        elif (equipment[1]) == WEAPON:
                            self.weapon_equipment = s
                        elif (equipment[1]) == HERO:
                            self.hero_equipment = s

            self._picID = int(data['VIS'])
            self._name = data['N']
            self.parseGeneral(data, None)
    def get_effects(self):
        lord_effects = LordEffects()
        equipment_set = [self.armor_equipment, self.artifact_equipment, self.skin_equipment, self.helmet_equipment, self.hero_equipment, self.weapon_equipment]
        for equipment in equipment_set:
            lord_effects.add_equipment_bonuses(equipment)
        return vars(lord_effects)
    def parseGeneral(self, data, t):
        if t is None:
            t = False
        i = data['GID']
        if i > 0 and t:
            self.assignedGeneralVO = General(i)
            self.assignedGeneralVO.parseData(data)
        else: ...
            # self.assignedGeneralVO = h.CastleModel.generalsData.playerGenerals.get(i)

class Castellan_temp:
    commanders: List
    id: int
    wid: int
    vis: int
    licid: int
    n: str
    gid: int
    w: int
    d: int
    spr: int
    eq: List
    l: Optional[int]
    st: Optional[int]
    armor_equipment = Equipment([], CHEST)
    artifact_equipment = Equipment([], ARTEFACT)
    helmet_equipment = Equipment([], HELMET)
    skin_equipment = Equipment([], SKIN)
    weapon_equipment = Equipment([], WEAPON)
    hero_equipment = Equipment([], HERO)
    def __init__(self, data) -> None:
        self.id = data["ID"] # LORD_ID
        self.wid = data["WID"] # WEARER_ID
        self.vis = data["VIS"] # LORD_LOOK
        self.licid = data["LICID"] # LOCKED_CASTLE_ID
        self.n = data["N"] # LORD_NAME
        self.gid = data["GID"] # GENERAL_ID
        self.w = data["W"] # WINS
        self.d = data["D"] # DEFEATS
        self.spr = data["SPR"] # WINNING_SPREE
        self.eq = data["EQ"] # EQUIPMENT
        self.l = data.setdefault('L', -1) # LORDS
        self.st = self.l = data.setdefault('ST', -1) # STAR_TIER
        self.picID = 0
    def createEquipment(self, equipment):
        if len(equipment) >= 12 and equipment[11] == 3:
            #RelicEquipment
            return Equipment(equipment, equipment[1])
        else:
            if equipment[1] == HERO:
                #CastleHero
                return Equipment(equipment, equipment[1])
            else:
                #BasicEquipment
                return Equipment(equipment, equipment[1])
    def parseLord(self, data):
        if data != None:
            self.id = int(data['ID']),
            self.equipmentSlots = {}
            self.equipmentSlots['helmet'] = {}
            self.equipmentSlots['chest'] = {}
            self.equipmentSlots['weapon'] = {}
            self.equipmentSlots['artefact'] = {}
            self.equipmentSlots['skin'] = {}
            self.equipmentSlots['hero'] = {}
            #self.hardModeEffects = self.parseRawEffects(e.HME),
            #self.rawLordEffects = self.parseRawEffects(e.E),
            #self.areaEffects = self.parseRawEffects(e.AE),
            self.wins = int(data['W'])
            self.defeats = int(data['D'])
            self.winSpree = int(data['SPR'])
            if (data['EQ'] and len(data['EQ']) > 0):
                #for (var n = 0, o = data['EQ']; n < o.length; n++) {
                for n in range(len(data['EQ'])):
                    equipment = data['EQ'][n]
                    if (len(equipment) > 0):
                        s = self.createEquipment(equipment)
                        if (equipment[1]) == CHEST:
                            self.armor_equipment = s
                        elif (equipment[1]) == ARTEFACT:
                            self.artifact_equipment = s
                        elif (equipment[1]) == HELMET:
                            self.helmet_equipment = s
                        elif (equipment[1]) == SKIN:
                            self.skin_equipment = s
                        elif (equipment[1]) == WEAPON:
                            self.weapon_equipment = s
                        elif (equipment[1]) == HERO:
                            self.hero_equipment = s

            self._picID = int(data['VIS'])
            self._name = data['N']
            self.parseGeneral(data, None)
    def get_effects(self):
        lord_effects = LordEffects()
        equipment_set = [self.armor_equipment, self.artifact_equipment, self.skin_equipment, self.helmet_equipment, self.hero_equipment, self.weapon_equipment]
        for equipment in equipment_set:
            lord_effects.add_equipment_bonuses(equipment)
    def parseGeneral(self, data, t):
        if t is None:
            t = False
        i = data['GID']
        if i > 0 and t:
            self.assignedGeneralVO = General(i)
            self.assignedGeneralVO.parseData(data)
        else: ...

class Castellan:
    lockedInCastleID: int
    baronOrderPosition: int
    isDummyBaron: int
    picID = int
    PIC_ID_ORDER = [0, 6, 7, 8, 1, 13, 2, 3, 4, 10, 11, 12, 9, 5]
    def parseLord(self, data):
        self.picID = data['VIS']
        self.lockedInCastleID = data['LICID']
        self.baronOrderPosition = int(self.PIC_ID_ORDER.index(self.picID))



class Welcome1:
    b: 'Commander'
    c: 'Commander'

    def __init__(self, b: List[dict], c: List[dict]) -> None:
        print('a')
        print(b)
        
        self.b = [Commander(tuple(commander.values()) for commander in b)]
        self.c = c

    def parse_GLI(self, e):
        if e:
            self._barons = []
            self._commanders = []
            for n in e["B"]: # Castellan
                if n is not None:
                    o = Castellan()
                    o.parseLord(n)
                    self._barons.append(o)
            for c in e["C"]:
                if c is not None:
                    u = _.CommanderVO()
                    u.parseLord(c)
                    if self.isLordLocked(u.id):
                        u.lock()
                    self._commanders.append(u)
            self._barons.sort(self.bindFunction(self.onSortBaron))
            self._commanders.sort(self.bindFunction(self.onSortLord))
            for d in range(len(self._commanders)):
                self._commanders[d].playerIndex = d + 1
            p.CastleModel.generalsData.updateAssignedLords()
            self.dispatchEvent(l.CastleEquipmentEvent(l.CastleEquipmentEvent.LORDS_UPDATED))

class General:
    
    def __init__(self, id):
        self.currentXP = 0
        self.currentStarLevel = 0
        self.isUnlocked = False
        self.hasLevelUp = False
        self.isNew = False
        self.kills = 0
        self.might = 0
        self.won = 0
        self.lost = 0
        self.unlockedSkillIDs = []
        self.selectedAbilities = []
        self.fixedLevel = -1
        self.oldXP = 0

    def parseData(self, data):
        self.currentXPAll = data['XP']  or 0
        self.currentStarLevel = data['ST'] or 0
        self.isNew = data['IN'] or False
        self.hasLevelUp = data['LU'] or False
        self.unlockedSkillIDs = data['SIDS'] or []
        self.selectedAbilities = data['GASAIDS'] or []
        self.fixedLevel = data['L'] or -1
        if not data['ST'] and self.fixedLevel > 0:
            self.currentStarLevel = (self.fixedLevel - 1) // 10 if self.fixedLevel % 10 == 0 else self.fixedLevel // 10
        self.oldXP = data['OXP'] or 0
        self.won = data['W'] or 0
        self.lost = data['D'] or 0
        self.isUnlocked = True

    def from_items(self, id):
        for general in game_items['generals']:
            if int(general['generalID']) == id:
                self.generalID = int(general['generalID'] or "0")
                self.maxLevel = int(general['maxLevel'] or "0")
                self.maxStarLevel = int(general['maxStarLevel'] or "0")
                self.upgradeCurrencyIDs = (general['upgradeCurrencyIDs'] or "0").split(",")
                self.attackSlots = (general['attackSlots'] or "").split(",")
                self.defenseSlots = (general['defenseSlots'] or "").split(",")
                self.generalRarityID = int(general['generalRarityID'] or "2")
                self.unlockCurrencyID = int(general['unlockCurrencyID'] or "0")
                self.isImplemented = 0 == int(general['isPreview'] or "0")
                self.isNPCGeneral = 1 == int(general['isNPCGeneral'] or "0")