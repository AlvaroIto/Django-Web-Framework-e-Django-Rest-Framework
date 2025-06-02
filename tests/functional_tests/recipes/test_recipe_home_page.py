from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipleBaseFuncionalTest
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageTest(RecipleBaseFuncionalTest):
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here', body.text)
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needle = 'Recipe 1'
        
        recipes[0].title = title_needle
        recipes[0].save()
        

        # Usuário abre a página inicial do site	
        self.browser.get(self.live_server_url)

        # Ve um campo de busca "Search for recipes..."
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for recipes..."]')

        # clica no campo de busca e digita "recipe"
        search_input.send_keys(title_needle)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            title_needle,
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
        

        self.sleep(6)
        