from . import IntegrationTestBase


class TestTree(IntegrationTestBase):

    def test_get_root_page(self):
        self.app.get('/', status=200)

    def test_get_tree_page(self):
        self.app.get('/admin/pages/', status=200)

    def test_move_inside(self):
        self.assertEqual(self.node(200).parent_id, 100)
        response = self.app.get(
            'http://localhost:6543/ps_tree/pages/move/200/inside/1/',
            status=200
        )
        self.assertEqual(self.node(200).parent_id, 1)
        self.assertEqual(response.json, '')

    def test_move_after(self):
        self.assertEqual(self.node(500).leftsibling_in_level().id, 200)
        response = self.app.get(
            'http://localhost:6543/ps_tree/pages/move/200/after/500/',
            status=200
        )
        self.assertEqual(response.json, '')
        self.assertEqual(self.node(200).leftsibling_in_level().id, 500)
        self.assertEqual(self.node(500).leftsibling_in_level().id, 101)

    def test_move_before(self):
        self.assertEqual(self.node(500).leftsibling_in_level().id, 200)
        response = self.app.get(
            'http://localhost:6543/ps_tree/pages/move/500/before/200/',
            status=200
        )
        self.assertEqual(self.node(200).leftsibling_in_level().id, 500)
        self.assertEqual(self.node(500).leftsibling_in_level().id, 101)
        self.assertEqual(response.json, '')
