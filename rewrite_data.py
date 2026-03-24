import json
import random
import os

BASE_DIR = r"d:\WORK\WEB-TU\new-github\stelepepe\freeze-nova.github.io"
GAMES_JSON = os.path.join(BASE_DIR, "data", "games.json")

# Category-specific keywords for SEO richness
CATEGORY_KEYWORDS = {
    "action": ["fast-paced combat", "intense missions", "epic battles", "skillful maneuvers"],
    "zombie": ["undead survival", "zombie apocalypse", "horde defense", "post-apocalyptic world"],
    "racing": ["high-speed tracks", "powerful vehicles", "racing championships", "precision steering"],
    "driving": ["vehicle simulation", "road challenges", "driving physics", "open-road exploration"],
    "puzzle": ["brain-teasing logic", "matching challenges", "strategic thinking", "complex puzzles"],
    "casual": ["relaxing gameplay", "simple mechanics", "addictive fun", "easy-to-play"],
    "multiplayer": ["online competition", "PvP battles", "cooperative play", "global leaderboards"],
    "arcade": ["classic gaming", "retro style", "fast reflexes", "high-score chasing"],
}

def get_category_keywords(category):
    cat_lower = category.lower()
    for key, words in CATEGORY_KEYWORDS.items():
        if key in cat_lower:
            return words
    return ["exciting gameplay", "unblocked fun", "browser-based gaming", "high-quality graphics"]

def rewrite_content(games):
    generic_intros = [
        "Welcome to {title}, the premier {category} game on Freeze-Nova.",
        "Experience the excitement of {title}, a top-rated {category} title available for free.",
        "{title} is one of our most popular {category} games, offering endless unblocked fun.",
        "Step into the world of {title}, where {category} action meets high-quality gameplay.",
        "Looking for the best {category} games? {title} is a must-play experience on our site.",
    ]
    
    generic_middles = [
        "This unblocked {title} experience delivers thrilling challenges and smooth controls.",
        "In {title}, you'll find addictive {category} elements that keep you coming back for more.",
        "Master the skills required for {title} and show off your expertise in our {category} collection.",
        "Whether you're a casual player or a pro, {title} offers a perfect balance of fun and difficulty.",
        "Dive deep into the mechanics of {title} and discover why players love this {category} masterpiece.",
    ]
    
    generic_closers = [
        "Play {title} for free today and join the community of winners on Freeze-Nova!",
        "Don't wait—start your {title} adventure now and explore more {category} games here.",
        "{title} is fully unblocked and ready for immediate play in your browser.",
        "Join the action in {title} and see if you can top the leaderboards in our {category} section.",
        "Experience {title} now and bookmark Freeze-Nova for the best unblocked {category} content.",
    ]

    extra_sentences = [
        "The {keyword} elements in {title} make it stand out among other browser games.",
        "You will love the way {title} combines {category} mechanics with {keyword}.",
        "If you enjoy {keyword}, then {title} is definitely the right choice for your next session.",
        "Our team at Freeze-Nova highly recommends {title} for anyone seeking high-quality {category} entertainment.",
        "Unlock new achievements in {title} as you progress through different {category} levels.",
    ]

    title_templates = [
        "Play {title} Unblocked - {category} Games",
        "{title} - Online {category} Game on Freeze-Nova",
        "{title} Game - Free Unblocked {category} Fun",
        "Master {title} | Best {category} Titles Online",
        "{title} - Experience the Best {category} Action",
    ]

    print(f"Rewriting {len(games)} games with HIGH-QUALITY SEO policy...")
    
    for game in games:
        title = game.get('title', 'Unknown Game')
        # Clean up previous rewrite if any
        if " - " in title: title = title.split(" - ")[0]
        if " | " in title: title = title.split(" | ")[0]
            
        category = game.get('category', 'Casual')
        keywords = get_category_keywords(category)
        
        # New Title
        new_title = random.choice(title_templates).format(title=title, category=category)
        game['title'] = new_title
        
        # Build High-Density Description (5-6 sentences)
        intro = random.choice(generic_intros).format(title=title, category=category)
        middle = random.choice(generic_middles).format(title=title, category=category)
        
        # Add 2-3 extra keyword-rich sentences
        shuffled_extras = random.sample(extra_sentences, 3)
        extra1 = shuffled_extras[0].format(title=title, category=category, keyword=random.choice(keywords))
        extra2 = shuffled_extras[1].format(title=title, category=category, keyword=random.choice(keywords))
        
        closing = random.choice(generic_closers).format(title=title, category=category)
        
        new_desc = f"{intro} {extra1} {middle} {extra2} {closing}"
        game['description'] = new_desc

    return games

def main():
    if not os.path.exists(GAMES_JSON):
        print(f"Error: {GAMES_JSON} not found.")
        return

    with open(GAMES_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        data = rewrite_content(data)
    elif isinstance(data, dict) and 'games' in data:
        data['games'] = rewrite_content(data['games'])

    with open(GAMES_JSON, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Successfully updated games.json with high-density, keyword-rich content.")

if __name__ == "__main__":
    main()
