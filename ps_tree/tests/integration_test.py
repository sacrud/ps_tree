from . import IntegrationTestBase


class TestTree(IntegrationTestBase):

    def test_get_root_page(self):
        self.app.get('/', status=200)
