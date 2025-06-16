from django.views import View
from recipes.models import Recipe
from django.http import Http404
from authors.forms.recipe_form import AuthorRecipeForm
from django.shortcuts import render, redirect 
from django.contrib import messages
from django.urls import reverse


class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.filter(is_published=False, author=request.user, id=id,).first()

        if not recipe:
            raise Http404()
        
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
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return render(request, 'authors/pages/dashboard_recipe.html', context={'form': form})