#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.
import unittest

from ps_tree.views import get_model


class TestCommon(unittest.TestCase):

    def test_get_tree_models(self):
        class Foo:
            __tablename__ = 'foo'

        class Bar:
            __tablename__ = 'bar'

        settings = {
            'ps_tree.models': (Foo, Bar)
        }
        self.assertEqual(get_model(settings, 'foo'), Foo)
        self.assertEqual(get_model(settings, 'bar'), Bar)
        self.assertEqual(get_model(settings, 'non'), None)
