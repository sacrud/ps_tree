from sqlalchemy import Column, Integer

from ps_tree.views import get_tree
from pyramid_sacrud.security import (PYRAMID_SACRUD_DELETE,
                                     PYRAMID_SACRUD_UPDATE)
from sqlalchemy_mptt.mixins import BaseNestedSets

from . import Base, PageTree, UnitTestBase
from .tree import base_tree

prefix = 'admin'


class Foo(Base, BaseNestedSets):

    __tablename__ = 'foo'

    id = Column(Integer, primary_key=True)


class TestGetTree(UnitTestBase):

    def _init_request(self, tablename='foo'):
        self.request.matchdict['tablename'] = tablename
        self.request.registry.settings['ps_tree.models'] = (Foo, PageTree)
        self.request.dbsession = self.dbsession

    def _init_config(self):
        self.config.add_route(PYRAMID_SACRUD_DELETE,
                              prefix + '{table}/delete/*pk')
        self.config.add_route(PYRAMID_SACRUD_UPDATE,
                              prefix + '{table}/update/*pk')

    def test_get_empty_tree(self):
        self._init_request()
        tree = get_tree(self.request)
        self.assertEqual(tree, [])

    def test_get_tree(self):
        self.initialize_db()
        self._init_config()
        self._init_request('pages')
        tree = get_tree(self.request)
        self.assertEqual(tree, base_tree)
