#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Urls unit tests for English.

This module implements unit tests for the urls extraction functionality in English.

Todo:
    * Better testing for exact test in return sources
    * More pathological and difficult cases
"""

# Project imports
from lexnlp.extract.en.urls import get_urls
from lexnlp.tests import lexnlp_tests

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.6"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


def test_urls():
    lexnlp_tests.test_extraction_func_on_test_data(get_urls)
