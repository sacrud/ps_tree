from pyramid.httpexceptions import HTTPInternalServerError

from ps_tree.views import get_tree, page_move

from . import UnitTestBase
from .tree import base_tree


class TestGetTree(UnitTestBase):

    def test_get_empty_tree(self):
        self._init_request('foo')
        tree = get_tree(self.request)
        self.assertEqual(tree, [])

    def test_get_tree(self):
        self.initialize_db()
        self._init_config()
        self._init_request('pages')
        tree = get_tree(self.request)
        self.assertEqual(tree, base_tree)


class TestPageMove(UnitTestBase):

    def _init_request(self, method, node_id, target_id, tablename):
        super(TestPageMove, self)._init_request(tablename)
        self.request.matchdict['method'] = method
        self.request.matchdict['node_id'] = node_id
        self.request.matchdict['target_id'] = target_id

    def test_bad_move_method(self):
        self.initialize_db()
        self._init_request('foo_method', 1, 2, 'pages')
        with self.assertRaises(HTTPInternalServerError):
            page_move(self.request)
