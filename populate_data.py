import os
import sys
import json
import django
from django.conf import settings

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cartoon_guesser.settings')
django.setup()

from game.models import CartoonCharacter

def reset_database():
    """Delete the existing SQLite database and recreate it with migrations."""
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
    
    # Delete the existing database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Deleted existing database.")
    
    # Run migrations to recreate the database
    from django.core.management import call_command
    call_command('migrate', interactive=False)
    print("Database recreated with migrations.")

def populate_database(json_file_path):
    """Populate the database with data from a JSON file."""
    try:
        with open(json_file_path, 'r') as f:
            characters_data = json.load(f)
        
        if not isinstance(characters_data, list):
            raise ValueError("JSON file must contain a list of character objects")
        
        for character_data in characters_data:
            try:
                # Required fields check
                required_fields = ['name', 'show', 'network', 'is_main', 'release_year', 'still_airing', 'gender']
                for field in required_fields:
                    if field not in character_data:
                        raise ValueError(f"Missing required field: {field} for character {character_data.get('name', 'Unknown')}")

                # Optional image_url field
                image_url = character_data.get('image_url', None)
                
                # Create or update the character in the database
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
                    print(f"Added new character: {character_data['name']}")
                else:
                    # Update existing character
                    character.show = character_data['show']
                    character.network = character_data['network']
                    character.is_main = character_data['is_main']
                    character.release_year = character_data['release_year']
                    character.still_airing = character_data['still_airing']
                    character.gender = character_data['gender']
                    character.image_url = image_url
                    character.save()
                    print(f"Updated existing character: {character_data['name']}")
                    
            except ValueError as e:
                print(f"Error processing character {character_data.get('name', 'Unknown')}: {e}")
            except Exception as e:
                print(f"Unexpected error processing character {character_data.get('name', 'Unknown')}: {e}")
                
        print(f"Successfully populated database with {len(characters_data)} characters.")
        
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{json_file_path}' contains invalid JSON.")
    except Exception as e:
        print(f"Error loading JSON file: {e}")

def main():
    print("Cartoon Character Database Reset and Repopulation Tool")
    
    # Confirm reset
    confirm = input("This will delete the existing database and repopulate it. Are you sure? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Operation cancelled.")
        return
    
    # Reset the database
    reset_database()
    
    # Get JSON file path
    json_file_path = input("Enter the path to your new JSON file: ").strip()
    if not json_file_path:
        print("No file path provided. Operation cancelled.")
        return
    
    # Populate the database with new data
    populate_database(json_file_path)

if __name__ == "__main__":
    main()