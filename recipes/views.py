from pathlib import Path
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import RecipeForm
from .models import Recipe
from .utils import *

def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            if d['save_to'] == 'db':
                try:
                    Recipe.objects.create(title=d['title'], author=d['author'], category=d['category'],
                        cooking_time=d['cooking_time'], ingredients=", ".join(d['ingredients']), description=d['description'])
                    messages.success(request, 'Сохранено в БД!')
                except IntegrityError:
                    messages.error(request, 'Дубликат! Такой рецепт уже есть.')
            else:
                try:
                    save_recipe_file({'title': d['title'], 'author': d['author'], 'category': d['category'],
                        'cooking_time': d['cooking_time'], 'ingredients': d['ingredients'], 'description': d['description']}, d.get('file_format', 'json'))
                    messages.success(request, 'Сохранено в файл!')
                except Exception as e:
                    messages.error(request, f'Ошибка файла: {e}')
            return redirect('recipe_create')
    else: form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})

def upload_file(request):
    if request.method == 'POST':
        f = request.FILES.get('data_file')
        if f and Path(f.name).suffix.lower() in settings.ALLOWED_EXTENSIONS:
            name = safe_filename(Path(f.name).suffix.lower())
            path = (settings.JSON_DIR if name.endswith('.json') else settings.XML_DIR) / name
            with open(path, 'wb+') as dest:
                for chunk in f.chunks(): dest.write(chunk)
            try:
                parse_json_file(path) if name.endswith('.json') else parse_xml_file(path)
                messages.success(request, f'Файл {name} загружен.')
            except ValidationError as e:
                path.unlink(missing_ok=True)
                messages.error(request, f'Ошибка: {e}. Файл удален.')
        else: messages.error(request, 'Неверный файл.')
        return redirect('upload_file')
    return render(request, 'recipes/upload.html')

def file_list(request):
    source = request.GET.get('source', 'files')
    ctx = {'source': source, 'files': [], 'recipes': []}
    if source == 'db': ctx['recipes'] = Recipe.objects.all().order_by('-id')
    else:
        for d, fmt in ((settings.JSON_DIR, 'JSON'), (settings.XML_DIR, 'XML')):
            if d.exists():
                for p in d.iterdir():
                    if p.is_file() and not p.name.startswith('.'):
                        try: ctx['files'].append({'filename': p.name, 'format': fmt, 'data': parse_json_file(p) if p.suffix=='.json' else parse_xml_file(p), 'error': None})
                        except Exception as e: ctx['files'].append({'filename': p.name, 'format': fmt, 'error': str(e)})
    return render(request, 'recipes/list_files.html', ctx)

def search_recipes(request):
    q = request.GET.get('q', '')
    recipes = Recipe.objects.filter(title__icontains=q) | Recipe.objects.filter(author__icontains=q)
    return JsonResponse({'recipes': list(recipes.values())})

def edit_recipe(request, pk):
    r = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            r.title, r.author, r.category, r.cooking_time = d['title'], d['author'], d['category'], d['cooking_time']
            r.ingredients, r.description = ", ".join(d['ingredients']), d['description']
            try:
                r.save()
                messages.success(request, 'Обновлено!')
                return redirect('/files/?source=db')
            except IntegrityError: messages.error(request, 'Дубликат!')
    else:
        form = RecipeForm(initial={'title': r.title, 'author': r.author, 'category': r.category, 'cooking_time': r.cooking_time, 'ingredients': r.ingredients, 'description': r.description, 'save_to': 'db'})
    return render(request, 'recipes/recipe_form.html', {'form': form, 'is_edit': True})

@csrf_exempt
def delete_recipe(request, pk):
    if request.method == 'POST':
        get_object_or_404(Recipe, pk=pk).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)