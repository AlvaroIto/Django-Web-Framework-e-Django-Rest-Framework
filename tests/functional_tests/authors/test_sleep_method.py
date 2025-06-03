from tests.functional_tests.authors.base import AuthorsBaseTest

class TestSleep(AuthorsBaseTest):
    def test_sleep_method(self):
        self.sleep(0)  # Passe 0 ou um número pequeno para não atrasar os testes
