import pytest
import urllib.request
import json
from unittest.mock import patch, MagicMock

API_URL = 'http://worldclockapi.com/api/json/utc/now'

YMD_SEP = '-'
YMD_SEP_INDEX = 4
YMD_YEAR_SLICE = slice(None, YMD_SEP_INDEX)

DMY_SEP = '.'
DMY_SEP_INDEX = 5
DMY_YEAR_SLICE = slice(DMY_SEP_INDEX + 1, DMY_SEP_INDEX + 5)


def what_is_year_now() -> int:
    """
    Получает текущее время из API-worldclock
    и извлекает из поля 'currentDateTime' год

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
    exp_json = dict(currentDateTime='2018-01-01')
    exp_json = json.dumps(exp_json)
    exp_year = 2018
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value =  exp_json
        year = what_is_year_now()
    assert exp_year == year


def test_what_is_year_now_valuee_error():
    exp_json = dict(currentDateTime='2015235236')
    exp_json = json.dumps(exp_json)
    with pytest.raises(ValueError):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value.read.return_value = exp_json
            what_is_year_now()


def test_get_what_is_year_now_r():
    exp_json = dict(currentDateTime='21.03.2017')
    exp_json = json.dumps(exp_json)
    exp_year = 2017
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_urlopen.return_value.__enter__.return_value.read.return_value = exp_json
        year = what_is_year_now()
    assert year == exp_year
