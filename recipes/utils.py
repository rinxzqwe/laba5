import json, uuid, xml.etree.ElementTree as ET
from pathlib import Path
from django.conf import settings

class ValidationError(Exception): pass
def dict_to_json(recipe): return json.dumps(recipe, ensure_ascii=False, indent=2)
def dict_to_xml(recipe):
    root = ET.Element('recipe')
    for k in ['title', 'author', 'category', 'cooking_time', 'description']:
        ET.SubElement(root, k).text = str(recipe.get(k, ''))
    ingr = ET.SubElement(root, 'ingredients')
    for i in recipe['ingredients']: ET.SubElement(ingr, 'ingredient').text = i
    return ET.tostring(root, encoding='unicode')
def validate_recipe_dict(data):
    if not isinstance(data.get('cooking_time'), int) or not (1 <= data['cooking_time'] <= 1440):
        raise ValidationError('Неверное время готовки.')
    if not data.get('ingredients') or not isinstance(data['ingredients'], list):
        raise ValidationError('Нет ингредиентов.')
def parse_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: data = json.load(f)
        validate_recipe_dict(data); return data
    except Exception as e: raise ValidationError(f'Ошибка JSON: {e}')
def parse_xml_file(path):
    try:
        root = ET.parse(path).getroot()
        if root.tag != 'recipe': raise ValidationError('Нет тега recipe')
        data = {tag: root.findtext(tag) or '' for tag in ['title', 'author', 'category', 'description']}
        data['cooking_time'] = int(root.findtext('cooking_time') or 0)
        data['ingredients'] = [i.text for i in root.find('ingredients')]
        validate_recipe_dict(data); return data
    except Exception as e: raise ValidationError(f'Ошибка XML: {e}')
def safe_filename(ext): return f"{uuid.uuid4().hex}{ext}"
def save_recipe_file(recipe, fmt):
    directory = settings.JSON_DIR if fmt == 'json' else settings.XML_DIR
    content = dict_to_json(recipe) if fmt == 'json' else dict_to_xml(recipe)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / safe_filename(f'.{fmt}')
    path.write_text(content, encoding='utf-8')
    return path