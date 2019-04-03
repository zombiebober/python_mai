from issue_01 import Advert
import json


class ColorizeMixin:
    repr_color_code = 0

    def __repr__(self):
        return f"\033[1;{self.repr_color_code};40m" + super().__repr__()


class AdvertColor(ColorizeMixin, Advert):
    def __init__(self, json: dict, repr_color):
        super().__init__(json)
        ColorizeMixin.repr_color_code = repr_color


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
    lesson_ad = AdvertColor(lesson, 32)
    lesson_ad.repr_color_code = 37
    assert lesson_ad.__repr__() == "\033[1;37;40mpython | 0 ₽"
