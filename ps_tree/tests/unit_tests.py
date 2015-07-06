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

    def test_move_inside(self):
        self.initialize_db()
        self.assertEqual(self.node(200).parent_id, 100)
        self._init_request('inside', 200, 1, 'pages')
        response = page_move(self.request)
        self.assertEqual(self.node(200).parent_id, 1)
        self.assertEqual(response, '')

    def test_move_after(self):
        self.initialize_db()
        self.assertEqual(self.node(500).leftsibling_in_level().id, 200)
        self._init_request('after', 200, 500, 'pages')
        response = page_move(self.request)
        self.assertEqual(self.node(200).leftsibling_in_level().id, 500)
        self.assertEqual(self.node(500).leftsibling_in_level().id, 101)
        self.assertEqual(response, '')

    def test_move_before(self):
        self.initialize_db()
        self.assertEqual(self.node(500).leftsibling_in_level().id, 200)
        self._init_request('before', 500, 200, 'pages')
        response = page_move(self.request)
        self.assertEqual(self.node(200).leftsibling_in_level().id, 500)
        self.assertEqual(self.node(500).leftsibling_in_level().id, 101)
        self.assertEqual(response, '')
