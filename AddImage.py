import json
import time
from duckduckgo_search import DDGS

# Your list of characters
characters = [
]
# Function to fetch image URL from DuckDuckGo
def get_image_url(name, show):
    query = f"{name} {show} cartoon character"
    try:
        with DDGS() as ddgs:
            results = ddgs.images(query, max_results=1)
            if results:
                return results[0]["image"]
        print(f"No image found for {name} from {show}")
        return None
    except Exception as e:
        print(f"Error fetching image for {name} from {show}: {e}")
        return None

# Update image URLs for all characters
for i, character in enumerate(characters, 1):
    print(f"Processing character {i}/{len(characters)}: {character['name']} from {character['show']}")
    new_url = get_image_url(character["name"], character["show"])
    if new_url:
        character["image_url"] = new_url
    else:
        # Fallback to a placeholder if no image is found
        character["image_url"] = "https://via.placeholder.com/150?text=No+Image"
    time.sleep(1)  # Small delay to respect rate limits

# Save to JSON file
with open("updated_characters_duckduckgo.json", "w") as f:
    json.dump(characters, f, indent=4)

print("Image URLs updated using DuckDuckGo API. Check 'updated_characters_duckduckgo.json' for results.")