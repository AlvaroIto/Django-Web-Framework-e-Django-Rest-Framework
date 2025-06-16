from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from recipes.models import Recipe
from django.http import Http404, HttpRequest
from authors.forms.recipe_form import AuthorRecipeForm
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class DashboardRecipe(View):         
    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.filter(is_published=False, author=self.request.user, id=id,).first()

            if not recipe:
                raise Http404()
            
        return recipe
    
    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', context={'form': form})

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)        
        form = AuthorRecipeForm(data=request.POST or None, files=request.FILES or None, instance=recipe)

        if form.is_valid():
            # Agora o form já está validado, podemos salvar a receita
            recipe = form.save(commit=False)
            # Define o autor da receita
            recipe.author = request.user  
            # Garante que os passos de preparação não serão salvos como HTML
            recipe.preparation_steps_is_html = False  
            # Garante que a receita não será publicada ainda
            recipe.is_published = False  
            # Salva a receita no banco de dados
            recipe.save()

            messages.success(request, 'Recipe updated successfully!')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

        return self.render_recipe(form)


@method_decorator(login_required(login_url='authors:login', redirect_field_name='next'), name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Recipe deleted successfully!')
        return redirect(reverse('authors:dashboard'))

    