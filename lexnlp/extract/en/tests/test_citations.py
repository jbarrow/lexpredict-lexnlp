#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Citation unit tests for English.

This module implements unit tests for the citation extraction functionality in English.

Todo:
    * Better testing for exact test in return sources
    * More pathological and difficult cases
"""

# Imports

from nose.tools import assert_list_equal
from lexnlp.extract.en.citations import get_citations
from lexnlp.tests import lexnlp_tests

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.6"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


def test_get_citations():
    """
    Test default get citation behavior.
    :return:
    """
    for (_i, text, _input_args, expected) in lexnlp_tests.iter_test_data_text_and_tuple():
        expected = [(int(volume) if volume else None,
                     reporter,
                     reporter_full_name,
                     int(page) if page else None,
                     page2,
                     court,
                     int(year) if year else None,
                     source_text)
                    for volume, reporter, reporter_full_name, page, page2, court, year, source_text in expected]

        expected_without_sources = [v[:-1] for v in expected]
        expected_with_sources = expected

        lexnlp_tests.test_extraction_func(expected_without_sources, get_citations, text, return_source=False)
        lexnlp_tests.test_extraction_func(expected_with_sources, get_citations, text, return_source=True)


def test_get_citations_as_dict():
    text = 'bob lissner v. test 1 F.2d 1, 2-5 (2d Cir., 1982)'
    expected = [{'citation_str': '1 F.2d 1, 2-5 (2d Cir., 1982)',
                 'court': '2d Cir.',
                 'page': 1,
                 'page2': '2-5',
                 'reporter': 'F.2d',
                 'reporter_full_name': 'Federal Reporter',
                 'volume': 1,
                 'year': 1982}]
    assert_list_equal(
        list(lexnlp_tests.benchmark_extraction_func(get_citations, text,
                                               return_source=True,
                                               as_dict=True)),
        expected
    )
