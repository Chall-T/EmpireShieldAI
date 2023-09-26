from src import *
import storage
import data


if __name__ == "__main__":
    result = basic.get_gge_language_json('en')
    print(result)
    print('Loading...')
    storage.items_load()
    print('Loaded')

    # CASTLE DATA START
    castle_data = data.gcl
    for kingdom in data.gcl['C']:
        for castle_data in kingdom['AI']:
            try:
                storage.MainAccount.add_new_castle(kingdom['AI'], castle_data['AI'][3], castle_data['AI'][10], castle_data['AI'][1], castle_data['AI'][2], castle_data['AI'][0])
            except Exception as e:
                traceback.print_exc()
    resources.castle.update_castles_to_account(data.dcl, storage.MainAccount)
    # CASTLE DATA END



    # CASTELLAN/GENERAL DEFENCE DATA START
    characters_old.Welcome1(data.gli['B'], data.gli['C'])
    # CASTELLAN/GENERAL DEFENCE DATA END



    # COMMANDER/GENERAL ATTACK DATA START

    # COMMANDER/GENERAL ATTACK DATA END
    hall_of_fame_attack_on = {
        "melee": 21.0,
        "range": 25.0,
        "flank": 30.0,
        "front": 25,
        "courtyard": 10,
        "moat": 30
    }
    hall_of_fame_defence_on = {
        "melee": 25.0,
        "range": 31.0,
        "units_on_wall": 25.0,
        "courtyard": 9.0,
        "slot": 1,
        "moat": 30
    }

    # CASTLE DEFENCE DATA START
    keep = resources.castle.DefenceSettingsKeep().set_by_dict(data.dfk)
    print(keep.get_as_dict())
    wall = resources.castle.DefenceSettingsWall().set_by_dict(data.dfw)
    print(wall.get_as_dict())
    moat = resources.castle.DefenceSettingsMoat().set_by_dict(data.dfm)
    print(moat.get_as_dict())
    # CASTLE DEFENCE DATA END
