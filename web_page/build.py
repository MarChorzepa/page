#!/usr/bin/env python3
"""
Build script for Moje Przestrzenie personal website.
Generates static HTML pages from Jinja2 templates and content files.
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# Try to import Jinja2, fallback to simple string replacement if not available
try:
    from jinja2 import Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("Warning: Jinja2 not available. Using simple string replacement fallback.")


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
CONTENT_DIR = BASE_DIR / "content"
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR


def get_all_images():
    """Get list of all image filenames in the images directory, excluding UI assets."""
    if not IMAGES_DIR.exists():
        return []
    images = []
    excluded = {'hitmarker.jpg'}
    for f in sorted(IMAGES_DIR.iterdir()):
        if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
            if f.name not in excluded:
                images.append(f.name)
    return images


def render_template(template_name, context):
    """Render a Jinja2 template or fallback to simple replacement."""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    if JINJA2_AVAILABLE:
        env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)
        template = env.get_template(template_name)
        return template.render(**context)
    else:
        # Simple fallback: replace variables and blocks with content
        content = template_path.read_text(encoding='utf-8')
        # Replace title
        content = content.replace('{{ title }}', context.get('title', 'Bez tytułu'))
        # Replace base_path
        content = content.replace('{{ base_path }}', context.get('base_path', ''))
        # Replace images_json
        images_json = json.dumps(context.get('images', []))
        content = content.replace('{{ images_json }}', images_json)
        # Replace content block
        page_content = context.get('content', '')
        # Simple block replacement - find {% block content %}...{% endblock %}
        block_start = content.find('{% block content %}')
        block_end = content.find('{% endblock %}')
        if block_start != -1 and block_end != -1:
            content = content[:block_start] + page_content + content[block_end + len('{% endblock %}'):]
        return content


def build_page(page_name, title, content_html, images_list, base_path=''):
    """Build a single HTML page."""
    html = render_template('base.html', {
        'title': title,
        'content': content_html,
        'images': images_list,
        'images_json': json.dumps(images_list),
        'base_path': base_path
    })
    output_path = OUTPUT_DIR / f"{page_name}.html"
    output_path.write_text(html, encoding='utf-8')
    print(f"  Built: {output_path}")


def build_content_listing(section_name, title, images_list):
    """Build a listing page for a content section."""
    section_dir = CONTENT_DIR / section_name
    items = []
    if section_dir.exists():
        for f in sorted(section_dir.iterdir()):
            if f.is_file() and f.suffix.lower() in ['.html', '.md']:
                slug = f.stem
                # Read file to extract title if possible
                file_content = f.read_text(encoding='utf-8')
                # Simple title extraction from first h1 or first line
                item_title = slug.replace('-', ' ').replace('_', ' ').title()
                if file_content.startswith('# '):
                    item_title = file_content.split('\n')[0].replace('# ', '').strip()
                elif '<h1' in file_content:
                    import re
                    match = re.search(r'<h1[^>]*>(.*?)</h1>', file_content, re.DOTALL)
                    if match:
                        item_title = re.sub(r'<[^>]+>', '', match.group(1)).strip()
                
                # Extract excerpt (first paragraph)
                excerpt = ''
                if file_content.startswith('# '):
                    lines = file_content.split('\n')[1:]
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            excerpt = line[:200] + ('...' if len(line) > 200 else '')
                            break
                
                items.append({
                    'slug': slug,
                    'title': item_title,
                    'excerpt': excerpt,
                    'date': datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d'),
                    'filename': f.name
                })
                
                # Also build individual page for this item
                item_content = f'<article class="content-card">\n'
                if f.suffix.lower() == '.md':
                    # Simple markdown to HTML conversion (very basic)
                    item_html = simple_markdown_to_html(file_content)
                else:
                    item_html = file_content
                item_content += item_html
                item_content += '\n</article>'
                build_page(f"{section_name}/{slug}", item_title, item_content, images_list, base_path='../')
    
    # Build listing page
    listing_html = f'<div class="section-header">\n'
    listing_html += f'<h1>{title}</h1>\n'
    if not items:
        listing_html += f'<p>Ta sekcja jest jeszcze pusta. Wróć później!</p>\n'
    listing_html += f'</div>\n'
    
    if items:
        listing_html += '<div class="listing-grid">\n'
        for item in items:
            listing_html += '<div class="content-card">\n'
            listing_html += f'<h2><a href="{section_name}/{item["slug"]}.html">{item["title"]}</a></h2>\n'
            listing_html += f'<div class="meta">{item["date"]}</div>\n'
            if item['excerpt']:
                listing_html += f'<p class="excerpt">{item["excerpt"]}</p>\n'
            listing_html += f'<a href="{section_name}/{item["slug"]}.html" class="btn btn-primary">Czytaj dalej</a>\n'
            listing_html += '</div>\n'
        listing_html += '</div>\n'
    else:
        listing_html += '<div class="empty-state">\n'
        listing_html += f'<h2>Brak treści</h2>\n'
        listing_html += f'<p>Dodaj pliki do folderu <code>content/{section_name}/</code>, a pojawią się tutaj.</p>\n'
        listing_html += '</div>\n'
    
    build_page(section_name, title, listing_html, images_list, base_path='')


def simple_markdown_to_html(md_text):
    """Very basic markdown to HTML converter."""
    import re
    html = md_text
    
    # Headers
    html = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
    html = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold and italic
    html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Paragraphs
    paragraphs = html.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<h') and not p.startswith('<ul') and not p.startswith('<ol'):
            p = f'<p>{p}</p>'
        new_paragraphs.append(p)
    html = '\n\n'.join(new_paragraphs)
    
    return html


def build():
    """Main build function."""
    print("=" * 50)
    print("Building: Moje Przestrzenie")
    print("=" * 50)
    
    images = get_all_images()
    print(f"\nFound {len(images)} images.")
    
    # Ensure output directories exist
    for subdir in ['teksty', 'notatki', 'galeria', 'memy', 'losowe']:
        (OUTPUT_DIR / subdir).mkdir(parents=True, exist_ok=True)
    
    print("\nBuilding pages...")
    
    # Index page
    index_content = '''<div class="section-header">
<h1>Witaj na moich stronach</h1>
<p>Tutaj dzielę się swoimi tekstami, projektami, notatkami i memami. Prywatna przestrzeń kreatywności.</p>
</div>
<div class="content-card">
<h2>O tej stronie</h2>
<p>To moje prywatne portfolio twórcze — miejsce, gdzie gromadzę teksty, projekty "vibecoded", notatki i wszystko inne, co wpadnie mi do głowy. Strona jest ciągle rozwijana, więc zaglądaj tu od czasu do czasu.</p>
<p>Tło zmienia się za każdym razem, gdy odwiedzasz stronę — zdjęcia pochodzą z mojej osobistej kolekcji. Kliknij gdziekolwiek na stronie, żeby zobaczyć małą niespodziankę.</p>
</div>
<div class="content-card">
<h2>Sekcje</h2>
<p><strong><a href="galeria.html">Galeria</a></strong> — zdjęcia i wizualne eksperymenty.</p>
<p><strong><a href="teksty.html">Teksty</a></strong> — krótkie formy, opowiadania, przemyślenia.</p>
<p><strong><a href="notatki.html">Notatki</a></strong> — luźne zapiski, obserwacje, pomysły.</p>
<p><strong><a href="memy.html">Memy</a></strong> — humor, memy, śmieszne rzeczy.</p>
<p><strong><a href="losowe.html">Losowe</a></strong> — tu pojawi się coś nieoczekiwanego. Wkrótce.</p>
</div>'''
    build_page('index', 'Witaj', index_content, images)
    
    # Galeria
    gallery_content = '<div class="section-header">\n<h1>Galeria</h1>\n<p>Zdjęcia, kadry i wizualne eksperymenty.</p>\n</div>\n'
    gallery_content += '<div class="gallery-grid">\n'
    for img in images[:20]:
        gallery_content += f'<div class="gallery-item"><img src="images/{img}" alt="Zdjęcie" loading="lazy"></div>\n'
    gallery_content += '</div>\n'
    build_page('galeria', 'Galeria', gallery_content, images)
    
    # Teksty (listing + individual pages)
    build_content_listing('teksty', 'Teksty', images)
    
    # Notatki
    build_content_listing('notatki', 'Notatki', images)
    
    # Memy
    build_content_listing('memy', 'Memy', images)
    
    # Losowe (placeholder)
    losowe_content = '''<div class="section-header">
<h1>Losowe</h1>
<p>Ta sekcja jest póki co pusta. Tu pojawi się coś nieoczekiwanego.</p>
</div>
<div class="empty-state">
<h2>Wkrótce...</h2>
<p>Pracuję nad czymś ciekawym. Wróć tu za jakiś czas!</p>
</div>'''
    build_page('losowe', 'Losowe', losowe_content, images)
    
    print("\n" + "=" * 50)
    print("Build complete! Open index.html in your browser.")
    print("=" * 50)


if __name__ == '__main__':
    build()
