
from typing import List
import json
from . basic import Unit
import storage
import traceback
MAX_SLOTSIZE = 999
MAX_SUPPORT_TOOLS_SLOTSIZE = 1
TOOL_TYPE_WALL = 1
TOOL_TYPE_GATE = 2
TOOL_TYPE_FIELD = 3
TOOL_TYPE_MOAT = 4
TOOL_TYPE_KEEP = 5
TOOL_TYPE_KEEP_DEFENSE_SUPPORT_TOOLS = 6
DEFENCE_CATEGORY_MOAT = 2
SIDE_LEFT = 0
SIDE_MIDDLE = 1
SIDE_RIGHT = 2
MAX_SUPPORT_TOOL_TRIGGER_LIMIT = 2e3

class DefenceSettings:
    CX: int
    CY: int
    AID: int
    def __init__(self, CX: int, CY: int, AID: int) -> None:
        self.CX = CX
        self.CY = CY
        self.AID = AID

class DefenceSettingsSlot(Unit):
    amount: int
    slot_name: str
    def __init__(self, id = -1, unit_type = "None", amount = 0):
        id, unit_type, amount = self.check_if_valid(id, unit_type, amount)
        self.amount = amount
        Unit.__init__(self, id, unit_type)

    def check_if_valid(self, id, unit_type, amount):
        if amount > MAX_SLOTSIZE:
            amount = MAX_SLOTSIZE
        elif amount <= 0:
            id = -1
            unit_type = 'None'
            amount = 0
        return id, unit_type, amount
    
    def update_slot(self, id=-1, unit_type="None", amount=0):
        id, unit_type, amount = self.check_if_valid(id, unit_type, amount)
        
        self.id = id
        self.unit_type = unit_type
        self.amount = amount
        self.get_unit_info()

    def get_slot(self):
        return [self.id, self.amount]
        

class DefenceSettingsKeep(DefenceSettings):  
    MAUCT: int # minimum_attack_units_to_consume_tools
    UC: int # unit_composition (melee)
    S:List[DefenceSettingsSlot] = [DefenceSettingsSlot(), DefenceSettingsSlot(), DefenceSettingsSlot()] # slot
    STS:List[DefenceSettingsSlot] = [DefenceSettingsSlot(), DefenceSettingsSlot(), DefenceSettingsSlot()] # STS support_tool_slots

    def __init__(self, CX: int=0, CY: int=0, AID: int=0, MAUCT:int=0, UC:int=50) -> None:
        super().__init__(CX, CY, AID)
        self.MAUCT = MAUCT
        self.UC = UC
    def set_slot(self, slot_index: int, unit_id:int=-1, unit_type:str="None", amount:int=0):
        self.S[slot_index].update_slot(unit_id, unit_type, amount)
    def get_slot_as_dict(self, slot_group:List[DefenceSettingsSlot]):
        slot_list = []
        for slot in slot_group:
            slot_list.append([slot.id, slot.amount])
        return slot_list
    def set_support_tool_slots(self, slot_index: int, unit_id:int=-1, unit_type:str="None", amount:int=0):
        self.STS[slot_index].update_slot(unit_id, unit_type, amount)
    
    def set_by_dict(self, dfk):
        self.CX = dfk['CX']
        self.CY = dfk['CY']
        self.AID = dfk['AID']
        self.MAUCT = dfk['MAUCT']
        self.UC = dfk['UC']
        self.set_slot(SIDE_LEFT, dfk['S'][SIDE_LEFT][0], "tool", dfk['S'][SIDE_LEFT][1])
        self.set_slot(SIDE_MIDDLE, dfk['S'][SIDE_MIDDLE][0], "tool", dfk['S'][SIDE_MIDDLE][1])
        self.set_slot(SIDE_RIGHT, dfk['S'][SIDE_RIGHT][0], "tool", dfk['S'][SIDE_RIGHT][1])
        self.set_support_tool_slots(SIDE_LEFT, dfk['STS'][SIDE_LEFT][0], "tool", dfk['STS'][SIDE_LEFT][1])
        self.set_support_tool_slots(SIDE_MIDDLE, dfk['STS'][SIDE_MIDDLE][0], "tool", dfk['STS'][SIDE_MIDDLE][1])
        self.set_support_tool_slots(SIDE_RIGHT, dfk['STS'][SIDE_RIGHT][0], "tool", dfk['STS'][SIDE_RIGHT][1])
        return self
    def get_as_dict(self):
        dfk:dict = vars(self)
        dfk['S'] = self.get_slot_as_dict(self.S)
        dfk['STS'] = self.get_slot_as_dict(self.STS)
        return dfk
    
class DefenceSettingsWallSide:
    S:List[DefenceSettingsSlot]=[]
    UC: int =0# unit_composition (melee)
    UP: int =0# UNIT_DISTRIBUTION_PERCENTAGE
    def __init__(self, slots:int=5):
        self.S = []
        self.UC = 0
        self.UP = 0
        for i in range(slots):
            slot = DefenceSettingsSlot()
            self.S.append(slot)

    
class DefenceSettingsWall(DefenceSettings): 
    MAUCT: int # minimum_attack_units_to_consume_tools
    UC: int # unit_composition (melee)
    L:DefenceSettingsWallSide
    M:DefenceSettingsWallSide
    R:DefenceSettingsWallSide
    
    def __init__(self, CX: int=0, CY: int=0, AID: int=0) -> None:
        super().__init__(CX, CY, AID)
        self.L = DefenceSettingsWallSide()
        self.M = DefenceSettingsWallSide(slots=6)
        self.R = DefenceSettingsWallSide()
    def get_side(self, side):
        if side == SIDE_LEFT:
            side_class = self.L
        if side == SIDE_MIDDLE:
            side_class = self.M
        if side == SIDE_RIGHT:
            side_class = self.R
        return side_class
    
    def set_slot(self, side, slot_index: int, unit_id:int=-1, unit_type:str="None", amount:int=0):
        side_class = self.get_side(side)
        side_class.S[slot_index].update_slot(unit_id, unit_type, amount)

    def get_side_as_dict(self, side):
        side_class = self.get_side(side)

        side_dict = {}
        side_dict['S'] = self.get_slot_as_dict(side_class.S)
        side_dict['UP'] = side_class.UP
        side_dict['UC'] = side_class.UC
        return side_dict
    
    def get_slot_as_dict(self, slot_group:List[DefenceSettingsSlot]):
        slot_list = []
        for slot in slot_group:
            slot_list.append([slot.id, slot.amount])
        return slot_list
    

    def set_side_slots(self, side, side_index):
        for slot in range(len(side['S'])):
            self.set_slot(side_index, slot, side['S'][slot][0], "tool", side['S'][slot][1])
        side_class = self.get_side(side_index)
        side_class.UP = side['UP']
        side_class.UC = side['UC']
        

    def set_by_dict(self, dfw):
        self.CX = dfw['CX']
        self.CY = dfw['CY']
        self.AID = dfw['AID']
        self.set_side_slots(dfw['L'], SIDE_LEFT)
        self.set_side_slots(dfw['M'], SIDE_MIDDLE)
        self.set_side_slots(dfw['R'], SIDE_RIGHT)
        return self
    def get_as_dict(self):
        dfw:dict = vars(self)
        dfw['L'] = self.get_side_as_dict(SIDE_LEFT)
        dfw['M'] = self.get_side_as_dict(SIDE_MIDDLE)
        dfw['R'] = self.get_side_as_dict(SIDE_RIGHT)
        return dfw
    


    
class DefenceSettingsMoat(DefenceSettings): 
    LS:List[DefenceSettingsSlot] = [DefenceSettingsSlot()]
    MS:List[DefenceSettingsSlot] = [DefenceSettingsSlot()]
    RS:List[DefenceSettingsSlot] = [DefenceSettingsSlot()]

    def __init__(self, CX: int=0, CY: int=0, AID: int=0):
        super().__init__(CX, CY, AID)
    def get_side(self, side):
        if side == SIDE_LEFT:
            side_class = self.LS
        if side == SIDE_MIDDLE:
            side_class = self.MS
        if side == SIDE_RIGHT:
            side_class = self.RS
        return side_class
    
    def set_slot(self, side, slot_index: int, unit_id:int=-1, unit_type:str="None", amount:int=0):
        side_class = self.get_side(side)
        side_class[slot_index].update_slot(unit_id, unit_type, amount)

    def set_side_slots(self, side, side_index):
        for slot in range(len(side)):
            self.set_slot(side_index, slot, side[slot][0], "tool", side[slot][1])

    def get_slot_as_dict(self, slot_group:List[DefenceSettingsSlot]):
        slot_list = []
        for slot in slot_group:
            slot_list.append([slot.id, slot.amount])
        return slot_list


    def set_by_dict(self, dfm):
        self.CX = dfm['CX']
        self.CY = dfm['CY']
        self.AID = dfm['AID']
        self.set_side_slots(dfm['LS'], SIDE_LEFT)
        self.set_side_slots(dfm['MS'], SIDE_MIDDLE)
        self.set_side_slots(dfm['RS'], SIDE_RIGHT)
        return self
    def get_as_dict(self) -> dict:
        dfm:dict = vars(self)
        dfm['LS'] = self.get_slot_as_dict(self.LS)
        dfm['MS'] = self.get_slot_as_dict(self.MS)
        dfm['RS'] = self.get_slot_as_dict(self.RS)
        return dfm

class Defence:
    ...
def update_castles_to_account(payload, account:storage.PlayerData):
    try:
        if payload['PID'] == account.player_id:
            print("Updating castles")
            def update_castle(account_kingdom:List[storage.CastleData], castle, account, KID):
                try:
                    for element in account_kingdom:
                        if element.id == castle['AID']:
                            # update
                            element.update(castle['W'], castle['S'], castle['F'], castle['C'], castle['O'], castle['G'], castle['A'], castle['I'], castle['HONEY'], castle['MEAD'], castle['D'], 
                            castle['gpa']['MRW'], castle['gpa']['MRS'], castle['gpa']['MRF'], castle['gpa']['MRC'], castle['gpa']['MRO'], castle['gpa']['MRG'], castle['gpa']['MRI'], castle['gpa']['MRHONEY'], castle['gpa']['MRMEAD'],
                            castle['gpa']['DW'], castle['gpa']['DS'], castle['gpa']['DF'], castle['gpa']['DC'], castle['gpa']['DO'], castle['gpa']['DC'], castle['gpa']['DI'], castle['gpa']['DHONEY'], castle['gpa']['DMEAD'],
                            castle['gpa']['DFC'], castle['gpa']['DMEADC'], castle['gpa']['FCR'], castle['gpa']['MEADCR'])
                            # end

                            
                            
                            print('units_castle_update')
                            element.update_units(castle['AC'])
                            return 0
                except Exception as e:
                    traceback.print_exc()
                


            for kingdom in payload['C']:
                for castle in kingdom['AI']:
                    if kingdom["KID"] == 0:
                        updated_element = account.castles_green
                    elif kingdom["KID"] == 1:
                        updated_element = account.castles_sand
                    elif kingdom["KID"] == 2:
                        updated_element = account.castles_winter
                    elif kingdom["KID"] == 3:
                        updated_element = account.castles_peaks
                    elif kingdom["KID"] == 4:
                        updated_element = account.castles_aqua
                    elif kingdom["KID"] == 10:
                        updated_element = account.castles_berimond
                    else:
                        continue
                    try:
                        update_castle(updated_element, castle, account, kingdom["KID"])
                    except Exception as e:
                        traceback.print_exc()
    except Exception as e:
        traceback.print_exc()