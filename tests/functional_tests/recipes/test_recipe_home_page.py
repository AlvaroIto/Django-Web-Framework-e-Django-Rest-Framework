from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipleBaseFuncionalTest
from unittest.mock import patch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.functional_test
class RecipeHomePageTest(RecipleBaseFuncionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'

        recipes[0].title = title_needed
        recipes[0].is_published = True
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê um campo de busca com o texto "Search for a recipe"
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for recipes..."]'
        )

        # Clica neste input e digita o termo de busca
        # para encontrar a receita o título desejado
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # Aguarda a página atualizar e o conteúdo ser renderizado de novo
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'main-content-list'))
        )

        # Rebusca o elemento após a atualização do DOM
        main_content = self.browser.find_element(By.CLASS_NAME, 'main-content-list')


        # O usuário vê o que estava procurando na página
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text,
        )
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        recipes = self.make_recipe_in_batch()

        # Usuário abre a página inicial do site
        self.browser.get(self.live_server_url)
        
        # Ve que tem uma paginação e clica na segunda página
        page2 = self.browser.find_element(By.XPATH, '//a[@aria-label="Go to page 2"]')

        page2.click()

        # ve que tem mais 2 receitas na segunda página
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)

        self.sleep(5)

    