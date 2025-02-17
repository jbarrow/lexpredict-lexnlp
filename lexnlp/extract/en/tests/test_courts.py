#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Court/jurisdiction unit tests for English.

This module implements unit tests for the court/jurisdiction extraction functionality in English.

Todo:
    * Re-introduce known bad cases with better master data or more flexible approach
    * More pathological and difficult cases
"""
import csv
import os
from unittest import TestCase
from nose.tools import assert_equals
from lexnlp.extract.en.courts import get_courts, \
    _get_court_list, _get_courts
from lexnlp.extract.en.dict_entities import entity_config, add_alias_to_entity
from lexnlp.tests import lexnlp_tests

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.6"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


BAD_EXAMPLES = ["""13.  Governing Law;  Submissions to  Jurisdiction.  This Agreement shall be
deemed to be a contract made under the laws of the State of New York and for all
purposes  shall be  construed  in  accordance  with those laws.  The Company and
Employee  unconditionally consent to submit to the exclusive jurisdiction of the
New York State Supreme Court,  County of New York or the United States  District
Court for Southern  District of New York for any actions,  suits or  proceedings
arising  out of or relating  to this  letter and the  transactions  contemplated
hereby  (and agree not to  commence  any  action,  suit or  proceeding  relating
thereto  except in such courts),  and further agree that service of any process,
summons,  notice or document by  registered  mail to the address set forth above
shall be effective service of process for any action, suit or proceeding brought
against the Company or the Employee, as the case may be, in any such court.""",
                """THE  GUARANTOR HEREBY  IRREVOCABLY  SUBMITS  ITSELF TO THE EXCLUSIVE  JURISDICTION  OF BOTH THE
SUPREME  COURT OF THE STATE OF NEW YORK,  NEW YORK COUNTY AND THE UNITED  STATES
DISTRICT COURT FOR THE SOUTHERN  DISTRICT OF NEW YORK, AND ANY APPEAL THEREFROM,
FOR THE  PURPOSE  OF ANY SUIT,  ACTION  OR OTHER  PROCEEDING  ARISING  OUT OF OR
RELATING TO THIS GUARANTY,  AND HEREBY WAIVES,  AND AGREES NOT TO ASSERT, BY WAY
OF MOTION,  AS A DEFENSE OR OTHERWISE,  IN ANY SUIT,  ACTION OR PROCEEDING,  ANY
CLAIM THAT IT IS NOT PERSONALLY  SUBJECT TO THE  JURISDICTION OF THE ABOVE-NAMED
COURTS  FOR ANY  REASON  WHATSOEVER,  THAT SUCH SUIT,  ACTION OR  PROCEEDING  IS
BROUGHT IN AN INCONVENIENT FORUM OR THAT THIS GUARANTY MAY NOT BE ENFORCED IN OR
BY SUCH COURTS.""",

                ]


class TestParseEnCourts(TestCase):

    def test_parse_empty_text(self):
        ret = _get_court_list('')
        self.assertEqual(0, len(ret))
        ret = _get_court_list("""

         """)
        #self.assertEqual(0, len(ret))

    def test_parse_simply_text(self):
        text = "A recent decision by a United States Supreme Court in Alabama v. Ballyshear LLC confirms that a key factor is the location of the impact of the alleged discriminatory conduct."
        ret = _get_court_list(text)
        self.assertEqual(1, len(ret))
        self.assertEqual("en", ret[0].locale)

        ret = _get_court_list(text, "z")
        self.assertEqual("z", ret[0].locale)

        items = list(_get_courts(text))
        court_name = items[0]["tags"]["Extracted Entity Court Name"]
        self.assertEqual('United States Supreme Court', court_name)


def test_courts():
    """
    Test court extraction.
    :return:
    """

    # Read master data
    import pandas

    # Load court data
    court_df = pandas \
        .read_csv("https://raw.githubusercontent.com/LexPredict/lexpredict-legal-dictionary/1.0.2/en/legal/us_courts"
                  ".csv")

    # Create config objects
    court_config_list = []
    for _, row in court_df.iterrows():
        c = entity_config(row["Court ID"], row["Court Name"], 0,
                          row["Alias"].split(";") if not pandas.isnull(row["Alias"]) else [])
        court_config_list.append(c)

    lexnlp_tests.test_extraction_func_on_test_data(get_courts, court_config_list=court_config_list,
                                                   actual_data_converter=lambda actual:
                                                   [cc[0][1] for cc in actual])


def test_courts_rs():
    """
    Test court extraction with return sources.
    :return:
    """

    # Read master data
    import pandas

    # Load court data
    court_df = pandas \
        .read_csv("https://raw.githubusercontent.com/LexPredict/lexpredict-legal-dictionary/1.0.2/en/legal/us_courts"
                  ".csv")

    # Create config objects
    court_config_list = []
    for _, row in court_df.iterrows():
        c = entity_config(row["Court ID"], row["Court Name"], 0,
                          row["Alias"].split(";") if not pandas.isnull(row["Alias"]) else [])
        court_config_list.append(c)

    lexnlp_tests.test_extraction_func_on_test_data(get_courts,
                                                   court_config_list=court_config_list,
                                                   actual_data_converter=lambda actual: [cc[0][1] for cc in actual])


def test_court_config_setup():
    """
    Test setup of CourtConfig object.
    :return:
    """
    # Test setup 1
    cc = entity_config(0, 'Test Court', 0, ['Alias'])
    assert_equals(str(cc), "(0, 'Test Court', 0, [('Test Court', None, False, None), ('Alias', None, False, None)])")

    # Test setup 2
    cc = entity_config(0, 'Test Court', 0)
    assert_equals(str(cc), "(0, 'Test Court', 0, [('Test Court', None, False, None)])")


def test_courts_longest_match():
    """
    Tests the case when there are courts having names/aliases being one a substring of another.
    In such case the court having longest alias should be returned for each conflicting matching.
    But for the case when there is another match of the court having shorter alias in that conflict,
    they both should be returned.
    :return:
    """
    courts_config_fn = os.path.join(os.path.dirname(lexnlp_tests.this_test_data_path()), 'us_courts.csv')
    courts_config_list = []
    with open(courts_config_fn, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cc = entity_config(row['Court ID'], row['Court Type'] + '|' + row['Court Name'], 0,
                               row['Alias'].split(';') if row['Alias'] else [],
                               name_is_alias=False)
            add_alias_to_entity(cc, row['Court Name'])

            courts_config_list.append(cc)
    lexnlp_tests.test_extraction_func_on_test_data(get_courts, court_config_list=courts_config_list,
                                                   actual_data_converter=lambda actual:
                                                   [tuple(c[0][1].split('|')) for c in actual],
                                                   debug_print=True)
