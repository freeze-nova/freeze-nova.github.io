import json
import os
import re
import random
from html import escape
from datetime import datetime

# Paths
BASE_DIR = r"d:\WORK\WEB-TU\new-github\stelepepe\freeze-nova.github.io"
GAMES_JSON = os.path.join(BASE_DIR, "data", "games.json")
GAMES_MINI_JSON = os.path.join(BASE_DIR, "data", "games_mini.json")
GAME_DIR = os.path.join(BASE_DIR, "game")
CATEGORY_DIR = os.path.join(BASE_DIR, "category")
TEMPLATE_FILE = os.path.join(GAME_DIR, "game39.html")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

NEW_SID = "7U7R8"

def generate_schema(game):
    schema = {
        "@context": "https://schema.org",
        "@type": "VideoGame",
        "name": game['title'],
        "description": game['description'],
        "image": game['cover'],
        "url": f"https://freeze-nova.github.io/game/{game['slug']}.html",
        "genre": game.get('category', 'Casual'),
        "operatingSystem": "Web",
        "applicationCategory": "Game",
        "author": {"@type": "Organization", "name": "Freeze-Nova"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def generate_grid_item(game, is_index=False, is_category=False):
    prefix = "./game/" if is_index else "../game/"
    if is_category: prefix = "../game/"
    return f"""        <div class="col-lg-2 col-md-4 col-6 grid-3">
          <a href="{prefix}{game['slug']}.html" title="{escape(game['title'])}">
            <div class="game-item">
              <div class="list-game">
                <div class="list-thumbnail">
                  <img
                    alt="{escape(game['title'])}"
                    class="lazyload"
                    loading="lazy"
                    src="{game['cover']}"
                  />
                </div>
              </div>
            </div>
          </a>
        </div>"""

def generate_common_styles():
    return """
    <style>
      @media (min-width: 1200px) {
        .grid-3 {
          flex: 0 0 8.333333% !important;
          max-width: 8.333333% !important;
        }
      }
      .category-bar {
        display: flex;
        flex-wrap: wrap;
        padding: 10px 0;
        margin-bottom: 20px;
        gap: 10px;
      }
      .category-item {
        padding: 5px 12px;
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        color: white;
        text-decoration: none;
        font-size: 13px;
        transition: 0.3s;
        border: 1px solid rgba(255,255,255,0.2);
      }
      .category-item:hover, .category-item.active {
        background: #ffae00;
        color: black;
        border-color: #ffae00;
      }
    </style>
    """

def generate_category_bar(categories, active_cat=None):
    html = '<div class="category-bar">'
    all_active = ' active' if active_cat == 'All' else ''
    html += f'<a href="/" class="category-item{all_active}">All</a>'
    for cat in sorted(categories):
        item_active = ' active' if active_cat == cat else ''
        html += f'<a href="/category/{cat.lower().replace(" ", "-")}.html" class="category-item{item_active}">{cat}</a>'
    html += '</div>'
    return html

def create_game_page(game, template_content, category_map, all_games):
    content = template_content
    content = re.sub(r'<title>.*?</title>', f"<title>{escape(game['title'])}</title>", content, flags=re.DOTALL)
    
    meta_desc = f'<meta name="description" content="{escape(game["description"][:160])}" />'
    if '<meta name="description"' in content:
        content = re.sub(r'<meta name="description".*?/>', meta_desc, content)
    else:
        content = content.replace('</head>', f'    {meta_desc}\n    </head>')

    seo_tags = f"""
    <meta property="og:title" content="{escape(game['title'])}" />
    <meta property="og:description" content="{escape(game['description'][:160])}" />
    <meta property="og:image" content="{game['cover']}" />
    <meta property="og:url" content="https://freeze-nova.github.io/game/{game['slug']}.html" />
    <meta name="twitter:card" content="summary_large_image" />
    {generate_schema(game)}
    """
    if seo_tags not in content:
        content = content.replace('</head>', f'{seo_tags}\n    </head>')
    
    content = re.sub(r'<h1.*?>.*?</h1>', f'<h1 style="font-weight: bolder; color: white; text-align: center">{escape(game["title"])}</h1>', content, flags=re.DOTALL)
    
    # SID Update logic
    game_url = game.get('url', '')
    if 'sid=' in game_url:
        game_url = re.sub(r'sid=[^&]*', f'sid={NEW_SID}', game_url)
    elif '?' in game_url:
        game_url += f'&sid={NEW_SID}'
    else:
        game_url += f'?sid={NEW_SID}'
        
    content = re.sub(r'<iframe.*?src=".*?".*?></iframe>', f'<iframe allowfullscreen="" border="0" class="" frameborder="0" height="100%" scrolling="no" src="{game_url}" width="100%"></iframe>', content, flags=re.DOTALL)

    category = game.get('category', 'Casual')
    related_candidates = [g for g in category_map.get(category, []) if g['slug'] != game['slug']]
    if len(related_candidates) < 12:
        others = [g for g in all_games if g['slug'] != game['slug'] and g not in related_candidates]
        related_candidates += random.sample(others, 12 - len(related_candidates))
    
    related_subset = random.sample(related_candidates, 12)
    related_grid_html = "\n".join([generate_grid_item(g, is_index=False) for g in related_subset])

    start_marker, end_marker = '<!-- GAME GRID START -->', '<!-- GAME GRID END -->'
    parts = content.split(start_marker)
    if len(parts) > 1:
        header = parts[0]
        footer_parts = parts[-1].split(end_marker)
        if len(footer_parts) > 1:
            content = header + start_marker + "\n" + related_grid_html + "\n      " + end_marker + footer_parts[1]
    
    content = content.replace('bubbleShooteonline.github.io', 'freeze-nova.github.io')
    with open(os.path.join(GAME_DIR, f"{game['slug']}.html"), 'w', encoding='utf-8') as f: f.write(content)

def update_index(games, grid_html, categories):
    with open(INDEX_FILE, 'r', encoding='utf-8') as f: content = f.read()
    content = content.replace('bubbleShooteonline.github.io', 'freeze-nova.github.io')
    
    if '</head>' in content:
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        content = content.replace('</head>', f'{generate_common_styles()}\n    </head>')
    
    cat_bar = generate_category_bar(categories, active_cat='All')
    if '<div class="category-bar">' in content:
        content = re.sub(r'<div class="category-bar">.*?</div>', cat_bar, content, flags=re.DOTALL)
    elif '<div class="row grid-container">' in content:
        content = content.replace('<div class="row grid-container">', cat_bar + '\n      <div class="row grid-container">')

    scroll_js = """
    <script>
      let allGames = [];
      let currentIndex = 300;
      const loadBatch = 24;
      let isLoading = false;

      fetch('/data/games_mini.json')
        .then(response => response.json())
        .then(data => {
          allGames = data;
          setupInfiniteScroll();
        });

      function setupInfiniteScroll() {
        const sentinel = document.createElement('div');
        sentinel.id = 'scroll-sentinel';
        document.querySelector('.container').appendChild(sentinel);

        const observer = new IntersectionObserver((entries) => {
          if (entries[0].isIntersecting && !isLoading) {
            loadMore();
          }
        }, { rootMargin: '200px' });

        observer.observe(sentinel);
      }

      function loadMore() {
        if (currentIndex >= allGames.length) return;
        isLoading = true;
        const container = document.querySelector('.grid-container');
        const nextBatch = allGames.slice(currentIndex, currentIndex + loadBatch);
        nextBatch.forEach(game => {
            const div = document.createElement('div');
            div.className = 'col-lg-2 col-md-4 col-6 grid-3';
            div.innerHTML = `<a href="/game/${game.s}.html" title="${game.t}"><div class="game-item"><div class="list-game"><div class="list-thumbnail"><img alt="${game.t}" class="lazyload" loading="lazy" src="${game.c}" /></div></div></div></a>`;
            container.appendChild(div);
        });
        currentIndex += loadBatch;
        isLoading = false;
      }
    </script>
    """
    content = re.sub(r'<script>\s*let allGames = \[\];.*?</script>', scroll_js, content, flags=re.DOTALL)
    if 'setupInfiniteScroll' not in content: content = content.replace('</body>', f'{scroll_js}\n  </body>')

    start_marker, end_marker = '<!-- GAME GRID START -->', '<!-- GAME GRID END -->'
    parts = content.split(start_marker)
    if len(parts) > 1:
        header = parts[0]
        footer_parts = parts[-1].split(end_marker)
        if len(footer_parts) > 1:
            content = header + start_marker + "\n" + grid_html + "\n      " + end_marker + footer_parts[1]
            
    with open(INDEX_FILE, 'w', encoding='utf-8') as f: f.write(content)

def generate_category_pages(categories, category_map, template_content):
    if not os.path.exists(CATEGORY_DIR): os.makedirs(CATEGORY_DIR)
    for cat in categories:
        cat_games = category_map[cat]
        cat_slug = cat.lower().replace(" ", "-")
        grid_html = "\n".join([generate_grid_item(g, is_category=True) for g in cat_games])
        
        content = template_content
        content = content.replace('</head>', f'{generate_common_styles()}\n    </head>')
        content = re.sub(r'<title>.*?</title>', f"<title>{cat} Games - Freeze-Nova</title>", content, flags=re.DOTALL)
        content = re.sub(r'<h1.*?>.*?</h1>', f'<h1 style="font-weight: bolder; color: white; text-align: center">{cat} Games</h1>', content, flags=re.DOTALL)
        
        # CLEANUP: Remove iframe/description section for categories to fix grid layout
        grid_container_start = '<div class="row grid-container">'
        if grid_container_start in content:
            # Keep only the row start and the game grid markers
            parts = content.split(grid_container_start)
            head_part = parts[0]
            tail_marker_part = content.split('<!-- GAME GRID START -->')[-1]
            content = head_part + grid_container_start + '\n      <!-- GAME GRID START -->' + tail_marker_part

        # Category Bar
        cat_bar = generate_category_bar(categories, active_cat=cat)
        if grid_container_start in content:
            content = content.replace(grid_container_start, cat_bar + '\n      ' + grid_container_start)
            
        start_marker, end_marker = '<!-- GAME GRID START -->', '<!-- GAME GRID END -->'
        parts = content.split(start_marker)
        if len(parts) > 1:
            header = parts[0]
            footer_parts = parts[-1].split(end_marker)
            if len(footer_parts) > 1:
                content = header + start_marker + "\n" + grid_html + "\n      " + end_marker + footer_parts[1]
        
        content = content.replace('bubbleShooteonline.github.io', 'freeze-nova.github.io')
        with open(os.path.join(CATEGORY_DIR, f"{cat_slug}.html"), 'w', encoding='utf-8') as f: f.write(content)

def generate_sitemap(games, categories):
    sitemap_path = os.path.join(BASE_DIR, 'sitemap.xml')
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    urls = [f'  <url><loc>https://freeze-nova.github.io/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>']
    for cat in categories:
        urls.append(f'  <url><loc>https://freeze-nova.github.io/category/{cat.lower().replace(" ", "-")}.html</loc><lastmod>{now}</lastmod><priority>0.9</priority></url>')
    for game in games:
        urls.append(f'  <url><loc>https://freeze-nova.github.io/game/{game["slug"]}.html</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>')
    
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + '\n</urlset>')

def main():
    with open(GAMES_JSON, 'r', encoding='utf-8') as f: games = json.load(f)
    category_map = {}
    for g in games:
        cat = g.get('category', 'Casual')
        if cat not in category_map: category_map[cat] = []
        category_map[cat].append(g)
    
    mini_games = [{"s": g['slug'], "t": g['title'], "c": g['cover'], "cat": g.get('category', 'Casual')} for g in games]
    with open(GAMES_MINI_JSON, 'w', encoding='utf-8') as f: json.dump(mini_games, f, separators=(',', ':'))
    
    grid_html_index = "\n".join([generate_grid_item(g, is_index=True) for g in games[:300]])
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f: template_content = f.read()
    
    # Update template for SID update (if it's ever used directly)
    template_content = re.sub(r'sid=[^&"]*', f'sid={NEW_SID}', template_content)
    with open(TEMPLATE_FILE, 'w', encoding='utf-8') as f: f.write(template_content)

    if os.path.exists(GAME_DIR):
        for file in os.listdir(GAME_DIR):
            if file.endswith(".html") and file != "game39.html":
                os.remove(os.path.join(GAME_DIR, file))
    else: os.makedirs(GAME_DIR)

    print(f"Generating site Phase 4 (SID Update: {NEW_SID})...")
    for i, game in enumerate(games):
        create_game_page(game, template_content, category_map, games)
        if (i+1) % 2000 == 0: print(f"Generated {i+1} pages...")
    
    generate_category_pages(category_map.keys(), category_map, template_content)
    update_index(games, grid_html_index, category_map.keys())
    generate_sitemap(games, category_map.keys())
    print("Done!")

if __name__ == "__main__": main()
