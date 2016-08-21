__author__ = 'RiteshReddy'
import json
from flaskappbase import app

class BhajanModel():
    FILLER_SLIDE = {
        "id" : -1,
        "name" : "Sai Center",
        "bhajan" : "",
        "meaning" : ""
    }

    @staticmethod
    def __read_bhajans_file(filename=app.config['BHAJAN_SOURCE_FILE']):
        """
        Structure of file:
        Json Dict {
            next_id : <int>,
            bhajans : list of Json Dict [
                    Json Dict { id: int
                                name: string
                                bhajan: string
                                meaning: string (optional)
                            }
                    ]
                  }
        :param filename: - name of file defaults to bhajans.json
        :return: tuple: next_id, bhajan list
        """
        try:
            with open(filename) as bhajans_json:
                json_data = json.load(bhajans_json)
                next_id = json_data['next_id']
                bhajans = json_data['bhajans']
                return next_id, bhajans
        except IOError,e:
            print e
            return 1, list()
        except ValueError,e:
            print e
            return 1, list()


    @staticmethod
    def __write_bhajans_file(next_id, bhajans, filename=app.config['BHAJAN_SOURCE_FILE']):
        """
        Structure of file:
        Json Dict {
            next_id : <int>,
            bhajans : list of Json Dict [
                    Json Dict { id: int
                                name: string
                                bhajan: string
                                meaning: string (optional)
                            }
                    ]
                  }
        :param next_id: - next_id
        :param bhajans: - bhajan_list
        :param filename: - name of file defaults to bhajans.json
        """
        with open(filename, 'w') as bhajans_json:
            json_data = {"next_id" : next_id, "bhajans" : bhajans}
            json.dump(json_data, bhajans_json)


    @staticmethod
    def get_all_bhajans():
        next_id, bhajans = BhajanModel.__read_bhajans_file()
        return bhajans

    @staticmethod
    def get_bhajan(bhajan_id):
        bhajans = BhajanModel.get_all_bhajans()
        bhajan_id = int(bhajan_id)
        for bhajan in bhajans:
            if bhajan['id'] == bhajan_id:
                return bhajan
        return None


    @staticmethod
    def delete_bhajan(bhajan_id):
        next_id, bhajans = BhajanModel.__read_bhajans_file()
        bhajan_id = int(bhajan_id)
        for i, bhajan in enumerate(bhajans):
            if bhajan['id'] == bhajan_id:
                bhajans.pop(i)
                break
        BhajanModel.__write_bhajans_file(next_id, bhajans)


    @staticmethod
    def edit_bhajan(bhajan_id, name, bhajan_text):
        next_id, bhajans = BhajanModel.__read_bhajans_file()
        bhajan_id = int(bhajan_id)
        for bhajan in bhajans:
            if bhajan['id'] == bhajan_id:
                bhajan['name'] = name
                bhajan['bhajan'] = bhajan_text
                break
        BhajanModel.__write_bhajans_file(next_id, bhajans)

    @staticmethod
    def add_bhajan(name, bhajan, meaning = ""):
        next_id, bhajans = BhajanModel.__read_bhajans_file()
        bhajan_dict = {"id":next_id, "name":name, "bhajan":bhajan, "meaning":meaning}
        next_id += 1
        bhajans.append(bhajan_dict)
        BhajanModel.__write_bhajans_file(next_id, bhajans)
        return bhajan_dict['id']

    @staticmethod
    def get_bhajans_if_they_exist(bhajan_list):
        """
        :param bhajan_list: bhajan ids
        :return: list of bhajans with id and text
        """
        bhajans = list()
        for id in bhajan_list:
            if int(id) == -1: # filler slide id
                bhajans.append(BhajanModel.FILLER_SLIDE)
                continue
            bhajan = BhajanModel.get_bhajan(id)
            if not bhajan is None:
                bhajans.append(bhajan)
        return bhajans

    @staticmethod
    def import_bhajans(filename):
        try:
            _, new_bhajans = BhajanModel.__read_bhajans_file(filename)
            if len(new_bhajans) == 0:
                return False
            next_id, current_bhajans = BhajanModel.__read_bhajans_file()
            for bhajan in new_bhajans:
                bhajan_dict = {
                    "id" : next_id,
                    "name" : bhajan['name'],
                    "bhajan" : bhajan['bhajan'],
                    "meaning" : bhajan['meaning']
                }
                current_bhajans.append(bhajan_dict)
                next_id += 1
            BhajanModel.__write_bhajans_file(next_id, current_bhajans)
        except Exception,e:
            return False
        return True