# from issue_01 import Advert
# import json
# class ColorizeMixin:
#     repr_color_code = 0
#     def __repr__(self):
#         return f"\033[1;{self.repr_color_code};40m" + super().__repr__()
#
# class Advert(ColorizeMixin, Advert):
#     pass


import keyword
import json


class ColorizeMixin:
    repr_color_code = 0

    def __repr__(self):
        return f"\033[1;{self.repr_color_code};40m"


class Advert(ColorizeMixin):
    def __init__(self, json: dict):
        for key, value in json.items():
            if keyword.iskeyword(key):
                self.__dict__[key + '_'] = value
            if (isinstance(value, dict)):
                self.__dict__[key] = Advert(value)
                setattr(self.__dict__[key], 'settlement',
                        settlement(value["address"], 0))
            else:
                if key == "price" and value < 0:
                    raise ValueError
                self.__dict__[key] = value

    def __getattr__(self, item):
        if item == 'price':
            return 0
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        if key == 'price' and value < 0:
            raise ValueError
        else:
            super().__setattr__(key, value)

    def __repr__(self):
        return super().__repr__() + f'{self.title} | {self.price} ₽'


def settlement(address: str, ind: int) -> str:
    address_spl = address.split(',')
    return address_spl[ind]


def test_mixin_repr():
    lesson_str = """{
    "title": "python",
    "class" : "2",
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
        }
    }"""
    lesson = json.loads(lesson_str)
    lesson_ad = Advert(lesson)
    lesson_ad.repr_color_code = 37
    assert lesson_ad.__repr__() == "\033[1;37;40mpython | 0 ₽"
