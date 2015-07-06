#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.

"""
Base classes for tests
http://www.sontek.net/blog/2011/12/01/writing_tests_for_pyramid_and_sqlalchemy.html
"""
import imp
import unittest

from pyramid import testing
from sqlalchemy import Column, Integer, engine_from_config
from sqlalchemy.orm import sessionmaker

from pyramid_sacrud.security import (PYRAMID_SACRUD_DELETE,
                                     PYRAMID_SACRUD_UPDATE)
from sqlalchemy_mptt import mptt_sessionmaker
from sqlalchemy_mptt.mixins import BaseNestedSets
from webtest import TestApp

imp.load_source('ps_tree_example', 'example/ps_tree_example.py')
from ps_tree_example import Base, DBSession, Fixtures, PageTree, main  # noqa


settings = {
    'sqlalchemy.url': 'sqlite:///test.sqlite',
    'ps_tree.models': (PageTree, )
}

PREFIX = 'admin'


class Foo(Base, BaseNestedSets):

    __tablename__ = 'foo'

    id = Column(Integer, primary_key=True)


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.DBSession = mptt_sessionmaker(sessionmaker())

    def setUp(self):
        # bind an individual Session to the connection
        self.dbsession = self.DBSession(bind=self.engine)
        self.create_db()

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.drop_db()
        self.dbsession.close()

    def drop_db(self):
        Base.metadata.drop_all(bind=self.engine)
        self.dbsession.commit()

    def create_db(self):
        Base.metadata.create_all(bind=self.engine)
        self.dbsession.commit()

    def initialize_db(self):
        fixture = Fixtures(self.dbsession)
        fixture.add(PageTree, 'fixtures/pages.json')
        fixture.add(PageTree, 'fixtures/country.json')
        self.dbsession.commit()

    def node(self, id):
        return self.dbsession.query(PageTree).filter_by(id=id).one()


class UnitTestBase(BaseTestCase):

    def _init_request(self, tablename):
        self.request.matchdict['tablename'] = tablename
        self.request.registry.settings['ps_tree.models'] = (Foo, PageTree)
        self.request.dbsession = self.dbsession

    def _init_config(self):
        self.config.add_route(PYRAMID_SACRUD_DELETE,
                              PREFIX + '{table}/delete/*pk')
        self.config.add_route(PYRAMID_SACRUD_UPDATE,
                              PREFIX + '{table}/update/*pk')

    def setUp(self):
        self.request = testing.DummyRequest()
        self.config = testing.setUp(request=self.request)
        super(UnitTestBase, self).setUp()


class IntegrationTestBase(BaseTestCase):

    def setUp(self):
        self.app = TestApp(main({}, **settings))
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()
