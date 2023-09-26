from typing import Optional, List, Union
from .basic import game_items

CHEST = 1
WEAPON = 2
HELMET = 3
ARTEFACT = 4
SKIN = 5
HERO = 6



class Commander:
    commanders: List
    id: int
    wid: int
    vis: int
    licid: Optional[int]
    n: str
    gid: int
    w: int
    d: int
    spr: int
    eq: List[List[Union[List[Union[List[Union[List[Union[List[Union[List[float], int]], float]], int]], int]], int]]]
    l: Optional[int]
    st: Optional[int]

    def __init__(self, id: int, wid: int, vis: int, licid: Optional[int], n: str, gid: int, w: int, d: int, spr: int, eq: List[List[Union[List[Union[List[Union[List[Union[List[Union[List[float], int]], float]], int]], int]], int]]], l: Optional[int], st: Optional[int]) -> None:
        self.id = id # LORD_ID
        self.wid = wid # WEARER_ID
        self.vis = vis # LORD_LOOK
        self.licid = licid # LOCKED_CASTLE_ID
        self.n = n # LORD_NAME
        self.gid = gid # GENERAL_ID
        self.w = w # WINS
        self.d = d # DEFEATS
        self.spr = spr # WINNING_SPREE
        self.eq = eq # EQUIPMENT
        self.l = l # LORDS
        self.st = st # STAR_TIER
        self.picID = 0
    def createEquipment(self, equipment):
        if len(equipment) >= 12 and equipment[11] == 3:
            #i = RelicEquipmentVO
            ...
        else:
            if equipment[1] == HERO:
                #i = CastleHeroVO
                ...
            else:
                #i = BasicEquipmentVO
                ...
            return i.parseEquipFromArray(equipment)
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
                            self.armorSlotVO.equipmentVO = s
                        elif (equipment[1]) == ARTEFACT:
                            self.artifactSlotVO.equipmentVO = s
                        elif (equipment[1]) == HELMET:
                            self.helmetSlotVO.equipmentVO = s
                        elif (equipment[1]) == SKIN:
                            self.skinSlotVO.equipmentVO = s
                        elif (equipment[1]) == WEAPON:
                            self.weaponSlotVO.equipmentVO = s
                        elif (equipment[1]) == HERO:
                            self.heroSlotVO.equipmentVO = s

            self._picID = int(data['VIS'])
            self._name = data['N']
            self.parseGeneral(data, None)
            
    def parseGeneral(self, data, t):
        if t is None:
            t = False
        i = data['GID']
        if i > 0 and t:
            self.assignedGeneralVO = General(i)
            self.assignedGeneralVO.parseData(data)
        else: ...
            # self.assignedGeneralVO = h.CastleModel.generalsData.playerGenerals.get(i)

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
    b: List[Commander]
    c: List[Commander]

    def __init__(self, b: List[dict], c: List[dict]) -> None:
        self.b = [Commander(tuple(commander.values())) for commander in b]
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