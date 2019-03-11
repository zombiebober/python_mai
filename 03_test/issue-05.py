"""

    добейтесь 100% покртыия кода тестами
    используйте unittest.mock для замены реального обращения к API
    предоставьте отчет о покрытии в виде директории с html файлами
    файл README.md с описанием шагов для запуска
    файл result с командами и результатами запуска
    файл *.py с функцией и тестами
    нет замечаний от flake8
"""
from unittest.mock import patch
import  pytest
import urllib.request
import json

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock и извлекает из поля 'currentDateTime' год

    Предположим, что currentDateTime может быть в двух форматах:
      * YYYY-MM-DD - 2019-03-01
      * DD.MM.YYYY - 01.03.2019
    """
    with urllib.request.urlopen(API_URL) as resp:
        resp_json = json.load(resp)

    datetime_str = resp_json['currentDateTime']
    if datetime_str[YMD_SEP_INDEX] == YMD_SEP:
        year_str = datetime_str[YMD_YEAR_SLICE]
    elif datetime_str[DMY_SEP_INDEX] == DMY_SEP:
        year_str = datetime_str[DMY_YEAR_SLICE]
    else:
        raise ValueError('Invalid format')

    return int(year_str)


def test_get_what_is_year_now():
    exp_json = dict(currentDateTime='2018-03-30')
    exp_year = 2018
    with patch.object(json, 'load', return_value=exp_json):
        year = what_is_year_now()
    assert year == exp_year

def test_wiyn_none():
    exp_json = dict(currentDateTime='')
    with pytest.raises(IndexError):
        with patch.object(json, 'load', return_value=exp_json):
            year = what_is_year_now()

def test_get_what_is_year_now2():
    exp_json = dict(currentDateTime='2015235236')
    with pytest.raises(ValueError):
        with patch.object(json, 'load', return_value=exp_json):
            year = what_is_year_now()

def test_get_what_is_year_now3():
    exp_json = dict()
    with pytest.raises(KeyError):
        with patch.object(json, 'load', return_value=exp_json):
            year = what_is_year_now()