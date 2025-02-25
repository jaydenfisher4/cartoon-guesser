import os
import sys
import json
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cartoon_guesser.settings')
django.setup()

from game.models import CartoonCharacter

def remove_characters(names):
    """Remove multiple characters from the database by name."""
    for name in names:
        try:
            character = CartoonCharacter.objects.get(name__iexact=name)
            character.delete()
            print(f"Successfully removed '{name}' from the database.")
        except CartoonCharacter.DoesNotExist:
            print(f"Character '{name}' not found in the database.")

def add_characters(characters_data):
    """Add multiple characters to the database from a list of JSON-like dictionaries."""
    for character_data in characters_data:
        try:
            required_fields = ['name', 'show', 'network', 'is_main', 'release_year', 'still_airing', 'gender']
            for field in required_fields:
                if field not in character_data:
                    raise ValueError(f"Missing required field: {field}")
            
            image_url = character_data.get('image_url', None)
            
            character, created = CartoonCharacter.objects.get_or_create(
                name=character_data['name'],
                defaults={
                    'show': character_data['show'],
                    'network': character_data['network'],
                    'is_main': character_data['is_main'],
                    'release_year': character_data['release_year'],
                    'still_airing': character_data['still_airing'],
                    'gender': character_data['gender'],
                    'image_url': image_url
                }
            )
            if created:
                print(f"Successfully added '{character_data['name']}' to the database.")
            else:
                character.show = character_data['show']
                character.network = character_data['network']
                character.is_main = character_data['is_main']
                character.release_year = character_data['release_year']
                character.still_airing = character_data['still_airing']
                character.gender = character_data['gender']
                character.image_url = image_url
                character.save()
                print(f"Updated existing character '{character_data['name']}' in the database.")
        except ValueError as e:
            print(f"Error adding character '{character_data.get('name', 'Unknown')}': {e}")
        except Exception as e:
            print(f"Unexpected error adding character '{character_data.get('name', 'Unknown')}': {e}")

def update_character_images(characters_data):
    """Update the image URLs for existing characters in the database."""
    for character_data in characters_data:
        try:
            if 'name' not in character_data or 'image_url' not in character_data:
                raise ValueError("Each character must have 'name' and 'image_url'")
            
            name = character_data['name']
            new_image_url = character_data['image_url']
            
            character = CartoonCharacter.objects.get(name__iexact=name)
            character.image_url = new_image_url
            character.save()
            print(f"Updated image for '{name}' to '{new_image_url}'.")
        except CartoonCharacter.DoesNotExist:
            print(f"Character '{name}' not found in the database.")
        except ValueError as e:
            print(f"Error updating character '{character_data.get('name', 'Unknown')}': {e}")
        except Exception as e:
            print(f"Unexpected error updating character '{character_data.get('name', 'Unknown')}': {e}")

def export_characters_to_json(output_file):
    """Export all CartoonCharacter data from the database to a JSON file in the specified format."""
    try:
        # Fetch all characters from the database
        characters = CartoonCharacter.objects.all()
        
        # Prepare data in the requested format
        export_data = [
            {
                "name": character.name,
                "show": character.show,
                "network": character.network,
                "is_main": character.is_main,
                "release_year": character.release_year,
                "still_airing": character.still_airing,
                "gender": character.gender,
                "image_url": character.image_url
            }
            for character in characters
        ]
        
        # Write to file with pretty printing
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2, separators=(',', ': '))
        
        print(f"Successfully exported {len(export_data)} characters to '{output_file}'.")
    except Exception as e:
        print(f"Error exporting data to '{output_file}': {e}")

def main():
    print("Cartoon Character Manager")
    print("1. Remove characters")
    print("2. Add characters")
    print("3. Update character images")
    print("4. Export all characters to JSON")
    choice = input("Enter choice (1, 2, 3, or 4): ").strip()
    
    if choice == '1':
        print("Enter character names as a JSON list (e.g., ['SpongeBob SquarePants', 'Patrick Star']) or 'file' to load from a JSON file:")
        names_input = input("Names: ").strip()
        if names_input.lower() == 'file':
            file_path = input("Enter the path to the JSON file: ").strip()
            try:
                with open(file_path, 'r') as f:
                    names = json.load(f)
                if not isinstance(names, list):
                    raise ValueError("File must contain a JSON list of names")
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        else:
            try:
                names = json.loads(names_input)
                if not isinstance(names, list):
                    raise ValueError("Input must be a JSON list of names")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                return
        remove_characters(names)
    
    elif choice == '2':
        print("Enter character data as a JSON list (e.g., [{'name': 'New Char', ...}, ...]) or 'file' to load from a JSON file:")
        json_input = input("JSON data: ").strip()
        if json_input.lower() == 'file':
            file_path = input("Enter the path to the JSON file: ").strip()
            try:
                with open(file_path, 'r') as f:
                    characters_data = json.load(f)
                if not isinstance(characters_data, list):
                    raise ValueError("File must contain a JSON list of character objects")
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        else:
            try:
                characters_data = json.loads(json_input)
                if not isinstance(characters_data, list):
                    raise ValueError("Input must be a JSON list of character objects")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                return
        add_characters(characters_data)
    
    elif choice == '3':
        print("Enter character image updates as a JSON list (e.g., [{'name': 'SpongeBob', 'image_url': 'new_url'}, ...]) or 'file' to load from a JSON file:")
        json_input = input("JSON data: ").strip()
        if json_input.lower() == 'file':
            file_path = input("Enter the path to the JSON file: ").strip()
            try:
                with open(file_path, 'r') as f:
                    characters_data = json.load(f)
                if not isinstance(characters_data, list):
                    raise ValueError("File must contain a JSON list of character objects")
            except Exception as e:
                print(f"Error reading file: {e}")
                return
        else:
            try:
                characters_data = json.loads(json_input)
                if not isinstance(characters_data, list):
                    raise ValueError("Input must be a JSON list of character objects")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON: {e}")
                return
        update_character_images(characters_data)
    
    elif choice == '4':
        output_file = input("Enter the path for the output JSON file (e.g., 'characters.json'): ").strip()
        if not output_file:
            output_file = 'characters.json'  # Default filename if none provided
        export_characters_to_json(output_file)
    
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()