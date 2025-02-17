#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from unittest import TestCase

import pytest

from lexnlp import is_stanford_enabled, enable_stanford, disable_stanford
from nose.tools import assert_false, assert_true

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2019, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-lexnlp/blob/master/LICENSE"
__version__ = "0.2.6"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


class TestStanfordMissing(TestCase):
    def test_stanford_enable_disable(self):
        was_enabled = is_stanford_enabled()
        try:
            disable_stanford()
            assert_false(is_stanford_enabled())
            enable_stanford()
            assert_true(is_stanford_enabled())
        finally:
            if was_enabled:
                enable_stanford()
            else:
                disable_stanford()

    def test_stanford_method(self):
        """
        get_tokens() should throw an exception if Stanford is disabled.
        :return:
        """
        was_enabled = is_stanford_enabled()
        try:
            disable_stanford()
            from lexnlp.nlp.en.stanford import get_tokens_list
            with pytest.raises(RuntimeError):
                _ = get_tokens_list("This should throw an exception.")
        finally:
            if was_enabled:
                enable_stanford()
