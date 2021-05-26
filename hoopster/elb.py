import hoopster.client as client
import hoopster.utils as utils
import hoopster.decorators as dec
from lxml import etree
from dataclasses import dataclass


@dataclass(frozen=True)
class Venue:
    code: str
    name: str = None
    capacity: int = None
    address: str = None
    images: dict = None
    active: bool = None,
    notes: str = None


@dataclass(frozen=True)
class Country:
    """Object for defining a country."""

    code: str
    name: str = None


@dec.nested_dataclass(frozen=True)
class Referee:
    """Object for defining a referee."""

    code: str
    name: str = None
    alias: str = None
    nationality: str = None
    country: Country = None
    images: dict = None
    active: bool = None

    # def __post_init__(self, nationality, country):
    #     if nationality is None and country is not None:
    #         self.nationality = self.country.code
    #     elif nationality is not None and country is None:
    #         self.country = Country(code=self.nationality)


@dec.nested_dataclass(frozen=True)
class Person:
    """Object for defining a person."""

    code: str
    name: str = None
    alias: str = None
    alias_raw: str = None
    passport_name: str = None
    passport_surname: str = None
    jersey_name: str = None
    abbreviated_name: str = None
    country: Country = None
    height: int = None
    weight: int = None
    birth_date: str = None
    birth_country: Country = None
    twitter_account: str = None
    images: dict = None


def _parse_referees(xml_data):
    root = etree.fromstring(bytes(xml_data, encoding='utf-8'))
    referees = [Referee(**dict(r.items())) for r in root.findall('referee')]
    return referees


def referees_1():
    """Finds all
    """
    params = {'version': 1.0, }
    url = client.build_url('referees', **params)
    res = client.get(url)

    return _parse_referees(utils.remove_invalid_characters(res.text))
    # print(res)


def referees(offset=0, limit=500):
    """Finds all referees
    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('referees', **params)
    res = client.get(url)
    return [Referee(**r) for r in res.json()]


def referee(referee_code):
    """Get one referee
    """
    params = {'version': 2.0}
    url = client.build_url('referees', referee_code, **params)
    res = client.get(url)
    return Referee(**res.json())


def venues(offset=0, limit=500):
    """Finds all referees
    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('venues', **params)
    res = client.get(url)
    return [Venue(**r) for r in res.json()]


def venue(venue_code):
    """Get one referee
    """
    params = {'version': 2.0}
    url = client.build_url('venues', venue_code, **params)
    res = client.get(url)
    return Venue(**res.json())


def people(offset=0, limit=500):  # 13336 persons on May 26.
    """Get one referee
    """
    params = {'version': 2.0, 'offset': offset, 'limit': limit}
    url = client.build_url('people', **params)
    res = client.get(url)
    # import ipdb; ipdb.set_trace()
    return [Person(**utils.normalize_keys(r)) for r in res.json()]


def person(person_code):
    """Get one referee
    """
    params = {'version': 2.0}
    url = client.build_url('people', person_code, **params)
    res = client.get(url)
    return Person(**utils.normalize_keys(res.json()))
