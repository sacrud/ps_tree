from sqlalchemy import Column, Integer

from ps_tree.views import get_tree
from sqlalchemy_mptt.mixins import BaseNestedSets

from . import Base, UnitTestBase


class Foo(Base, BaseNestedSets):

    __tablename__ = 'foo'

    id = Column(Integer, primary_key=True)


class TestGetTree(UnitTestBase):

    def test_get_empty_tree(self):
        self.request.matchdict['tablename'] = 'foo'
        self.request.registry.settings['ps_tree.models'] = (Foo, )
        self.request.dbsession = self.dbsession
        tree = get_tree(self.request)
        self.assertEqual(tree, [])
