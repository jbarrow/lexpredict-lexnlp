import os
from unittest import TestCase
import codecs
import time
from typing import Callable, Dict
from lexnlp.extract.en.acts import get_acts
from lexnlp.extract.en.amounts import get_amounts
from lexnlp.extract.en.citations import get_citations
from lexnlp.extract.en.conditions import get_conditions
from lexnlp.extract.en.constraints import get_constraints
from lexnlp.extract.en.copyright import get_copyright
from lexnlp.extract.en.courts import _get_courts
from lexnlp.extract.en.cusip import get_cusip
from lexnlp.extract.en.dates import get_dates
from lexnlp.extract.en.definitions import get_definitions
from lexnlp.extract.en.distances import get_distances
from lexnlp.extract.en.durations import get_durations
from lexnlp.extract.en.geoentities import get_geoentities, load_entities_dict_by_path
from lexnlp.extract.en.money import get_money
from lexnlp.extract.en.percents import get_percents
from lexnlp.extract.en.pii import get_pii
from lexnlp.extract.en.ratios import get_ratios
from lexnlp.extract.en.regulations import get_regulations
from lexnlp.extract.en.trademarks import get_trademarks
from lexnlp.extract.en.urls import get_urls

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.6"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class TestParsingSpeed(TestCase):
    """
    This method is not named as test_XXX
    because it is not intended for (automatic) regression tests
    """
    def en_parsers_speed(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = dir_path + '/../../../../test_data/long_parsed_text.txt'
        with codecs.open(file_path, 'r', encoding='utf-8') as fr:
            text = fr.read()

        ge_path = dir_path + '/../../../../test_data/lexnlp/extract/en/tests/test_geoentities/'
        entities_fn = ge_path + 'geoentities.csv'
        aliases_fn = ge_path + 'geoaliases.csv'
        geo_config = list(load_entities_dict_by_path(entities_fn, aliases_fn))

        times = {}  # type: Dict[str, float]
        self.check_time(text, lambda s: list(get_amounts(s)), 'get_amounts', times)
        self.check_time(text, lambda s: list(get_acts(s)), 'get_acts', times)
        self.check_time(text, lambda s: list(get_citations(s)), 'get_citations', times)
        self.check_time(text, lambda s: list(get_conditions(s)), 'get_conditions', times)
        self.check_time(text, lambda s: list(get_constraints(s)), 'get_constraints', times)
        self.check_time(text, lambda s: list(get_copyright(s)), 'get_copyright', times)
        self.check_time(text, lambda s: list(_get_courts(s)), 'get_courts', times)
        self.check_time(text, lambda s: list(get_cusip(s)), 'get_cusip', times)
        self.check_time(text, lambda s: list(get_dates(s)), 'get_dates', times)
        self.check_time(text, lambda s: list(get_definitions(s)), 'get_definitions', times)
        self.check_time(text, lambda s: list(get_distances(s)), 'get_distances', times)
        self.check_time(text, lambda s: list(get_durations(s)), 'get_durations', times)
        self.check_time(text, lambda s: list(get_geoentities(s, geo_config)), 'get_geoentities', times)
        self.check_time(text, lambda s: list(get_money(s)), 'get_money', times)
        self.check_time(text, lambda s: list(get_percents(s)), 'get_percents', times)
        self.check_time(text, lambda s: list(get_pii(s)), 'get_pii', times)
        self.check_time(text, lambda s: list(get_ratios(s)), 'get_ratios', times)
        self.check_time(text, lambda s: list(get_regulations(s)), 'get_regulations', times)
        self.check_time(text, lambda s: list(get_trademarks(s)), 'get_trademarks', times)
        self.check_time(text, lambda s: list(get_urls(s)), 'get_urls', times)

        self.assertTrue('get_amounts' in times)

    def check_time(self, text: str, func: Callable, func_name: str, times: Dict[str, float]) -> None:
        start = time.time()
        func(text)
        end = time.time()
        times[func_name] = end - start



