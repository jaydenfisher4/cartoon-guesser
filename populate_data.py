import os
import sys
import django
from django.conf import settings
import requests
from bs4 import BeautifulSoup

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cartoon_guesser.settings')
django.setup()

from game.models import CartoonCharacter

def get_wikipedia_image(character_name, show_name):
    try:
        url = f"https://en.wikipedia.org/wiki/{character_name.replace(' ', '_')}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        infobox = soup.find('table', class_='infobox')
        if infobox:
            img = infobox.find('img')
            if img and 'src' in img.attrs:
                return f"https:{img['src']}"
        return None
    except Exception as e:
        print(f"Error scraping image for {character_name}: {e}")
        return None

def populate_cartoon_data():
    Cdata = [
  {
    "name": "Peppa Pig",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": True,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "George Pig",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Mummy Pig",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Daddy Pig",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Suzy Sheep",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Rebecca Rabbit",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Richard Rabbit",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Candy Cat",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Danny Dog",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Pedro Pony",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Emily Elephant",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Madame Gazelle",
    "show": "Peppa Pig",
    "network": "Channel 5",
    "is_main": False,
    "release_year": 2004,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Pablo",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Tyrone",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Tasha",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Austin",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sammy Squirrel",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ricky Raccoon",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Lulu Lamb",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Danny Duck",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Bobby Bear",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Molly Mole",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Harry Hamster",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Lucy Ladybug",
    "show": "The Backyardigans",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Max",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ruby",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Mother Rabbit",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Father Rabbit",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Grandma Rabbit",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Grandpa Rabbit",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Trixie Cat",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Emily Elephant",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ginger Giraffe",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Bobby Bear",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sammy Squirrel",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Cody Koala",
    "show": "Max & Ruby",
    "network": "Nick Jr.",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dora",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Boots",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Diego",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Swiper",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Tico",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Isa Iguana",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Benny the Bull",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mami",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Juan",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Pedro",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Elena",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Roberto",
    "show": "Dora the Explorer",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2000,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mickey Mouse",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": True,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Minnie Mouse",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": True,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Donald Duck",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Goofy",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Pluto",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Daisy Duck",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Clarabelle Cow",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Horace Horsecollar",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Chip",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dale",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Huey",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Louie",
    "show": "Mickey Mouse Clubhouse",
    "network": "Disney Junior",
    "is_main": False,
    "release_year": 2006,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Peter Griffin",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": True,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Lois Griffin",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": True,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Stewie Griffin",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Brian Griffin",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Meg Griffin",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Chris Griffin",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Glenn Quagmire",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Cleveland Brown",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Joe Swanson",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Bonnie Swanson",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Tom Tucker",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Death",
    "show": "Family Guy",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Stan Marsh",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": True,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Kyle Broflovski",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": True,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Kenny McCormick",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": True,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Eric Cartman",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": True,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Butters Stotch",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Wendy Testaburger",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Mr. Garrison",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Chef",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Token Black",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Randy Marsh",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Sheila Broflovski",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Towelie",
    "show": "South Park",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 1997,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Homer Simpson",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": True,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Marge Simpson",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": True,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Bart Simpson",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": True,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Lisa Simpson",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": True,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Maggie Simpson",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": True,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Mr. Burns",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Waylon Smithers",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Ned Flanders",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Moe Szyslak",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Barney Gumble",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Krusty the Clown",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Apu Nahasapeemapetilon",
    "show": "The Simpsons",
    "network": "Fox",
    "is_main": False,
    "release_year": 1989,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Philip J. Fry",
    "show": "Futurama",
    "network": "Fox",
    "is_main": True,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Leela",
    "show": "Futurama",
    "network": "Fox",
    "is_main": True,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Bender",
    "show": "Futurama",
    "network": "Fox",
    "is_main": True,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Professor Farnsworth",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dr. Zoidberg",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Amy Wong",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Hermes Conrad",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Nibbler",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Calculon",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mom",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Scruffy",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "URL",
    "show": "Futurama",
    "network": "Fox",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Rick Sanchez",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": True,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Morty Smith",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": True,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Summer Smith",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Beth Smith",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Jerry Smith",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Mr. Meeseeks",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Squanchy",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Birdperson",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Tammy",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Evil Morty",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Unity",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Mr. Poopybutthole",
    "show": "Rick and Morty",
    "network": "Adult Swim",
    "is_main": False,
    "release_year": 2013,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Stan Smith",
    "show": "American Dad",
    "network": "Fox",
    "is_main": True,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Francine Smith",
    "show": "American Dad",
    "network": "Fox",
    "is_main": True,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Roger",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Klaus",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Steve Smith",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Hayley Smith",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Jeff Fischer",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Avery Bullock",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Terry Bates",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Duncan",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Linda",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Barry",
    "show": "American Dad",
    "network": "Fox",
    "is_main": False,
    "release_year": 2005,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Timmy Turner",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Cosmo",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Wanda",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Vicky",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Poof",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Chester McBadbat",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "AJ",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Tootie",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Mr. Crocker",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jorgen Von Strangle",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Foop",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mr. Turner",
    "show": "The Fairly OddParents",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Finn",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jake",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Princess Bubblegum",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Marceline the Vampire Queen",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ice King",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "BMO",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Lumpy Space Princess",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Flame Princess",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Lady Rainicorn",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Tree Trunks",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Cinnamon Bun",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Peppermint Butler",
    "show": "Adventure Time",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mordecai",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Rigby",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Benson",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Pops",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Skips",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Muscle Man",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Hi-Five Ghost",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Margaret",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Eileen",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Thomas",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "CJ",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Mr. Maellard",
    "show": "Regular Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mac",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Bloo",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Wilt",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Eduardo",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Coco",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Madame Foster",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Frankie",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Cheese",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mr. Herriman",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Goo",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Duchess",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Buddy",
    "show": "Foster's Home for Imaginary Friends",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Nigel Uno (Numbuh 1)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Hoagie P. Gilligan, Jr. (Numbuh 2)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Kuki Sanban (Numbuh 3)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Wallabee Beatles (Numbuh 4)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Abigail Lincoln (Numbuh 5)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Adam (Numbuh 6)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Zara (Numbuh 0)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Xander (Numbuh X)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Zelda (Numbuh Z)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Simon (Numbuh 7)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Olivia (Numbuh 8)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Jordan (Numbuh 9)",
    "show": "Codename Kids Next Door",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Bob Belcher",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": True,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Linda Belcher",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": True,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Tina Belcher",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Gene Belcher",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Louise Belcher",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Teddy",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Mort",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Jimmy Pesto",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Mr. Fischoeder",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Andy",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Ollie",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Marcus",
    "show": "Bob's Burgers",
    "network": "Fox",
    "is_main": False,
    "release_year": 2011,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Dexter",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dee Dee",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Mandark",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mom",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Dad",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Koosland Guide",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Security Guard",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Robot Assistant",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Professor Von Quack",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Emily",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Sally",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Leo",
    "show": "Dexter's Laboratory",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1996,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "SpongeBob SquarePants",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Patrick Star",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Squidward Tentacles",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Mr. Krabs",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Sandy Cheeks",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Plankton",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Gary",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Pearl Krabs",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Mrs. Puff",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Larry the Lobster",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Mermaid Man",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Barnacle Boy",
    "show": "SpongeBob SquarPants",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1999,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Ed",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Edd (Double D)",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Eddy",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Kevin",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Rolf",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Nazz",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Sarah",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Jimmy",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Plank",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jonny 2x4",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Lee Kanker",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Stella",
    "show": "Ed Edd n Eddy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1999,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Gumball Watterson",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Darwin Watterson",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Anais Watterson",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Nicole Watterson",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Richard Watterson",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Banana Joe",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Carrie",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Tobias Wilson",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Alan",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Tara",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Bobert",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Pencil Head",
    "show": "The Amazing World of Gumball",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Blossom",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Bubbles",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Buttercup",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Professor Utonium",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mojo Jojo",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "HIM",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Fuzzy Lumpkins",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ace",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sedusa",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Princess Morbucks",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ms. Bellum",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Brick",
    "show": "The Powepuff Girls",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 1998,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jimmy Neutron",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Carl Wheezer",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sheen Estevez",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Libby Folfax",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Cindy Vortex",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Hugh Neutron",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Judy Neutron",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ooblar",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jorgen Von Strangle",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Nick Dean",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Gretchen",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Max",
    "show": "Jimmy Neutron Boy Genius",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Robin",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Starfire",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Raven",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Beast Boy",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Cyborg",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Terra",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Slade",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jinx",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Gizmo",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Control Freak",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Blackfire",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Red Star",
    "show": "Teen Titans",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Fred Flintstone",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": True,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Wilma Flintstone",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": True,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Barney Rubble",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Betty Rubble",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Pebbles Flintstone",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Bamm-Bamm Rubble",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dino",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mr. Slate",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Hoppy",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mr. Granite",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mrs. Granite",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Mona",
    "show": "The Flintstones",
    "network": "ABC",
    "is_main": False,
    "release_year": 1960,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Aang",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Katara",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Sokka",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Toph",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Zuko",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Uncle Iroh",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Azula",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Suki",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Jet",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mai",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ty Lee",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Hakoda",
    "show": "Avatar The Last Airbender",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dipper Pines",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": True,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mabel Pines",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": True,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Grunkle Stan",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Soos",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Wendy Corduroy",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ford Pines",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Pacifica Northwest",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Bill Cipher",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Robbie Valentino",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sheriff Blubs",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Deputy Durland",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Old Man McGucket",
    "show": "Gravity Falls",
    "network": "Disney XD",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ben Tennyson",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Gwen Tennyson",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Grandpa Max",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Vilgax",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Kevin Levin",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Four Arms",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Heatblast",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Diamondhead",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "XLR8",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Stinkfly",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Upgrade",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Wildvine",
    "show": "Ben 10",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2005,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Kim Possible",
    "show": "Kim Possible",
    "network": "Disney Channel",
    "is_main": True,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Ron Stoppable",
    "show": "Kim Possible",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Rufus",
    "show": "Kim Possible",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Dr. Drakken",
    "show": "Kim Possible",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Shego",
    "show": "Kim Possible",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2002,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Tommy Pickles",
    "show": "Rugrats",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 1991,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Chuckie Finster",
    "show": "Rugrats",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 1991,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Phil Pickles",
    "show": "Rugrats",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1991,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Lil Pickles",
    "show": "Rugrats",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1991,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Angelica Pickles",
    "show": "Rugrats",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1991,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Susie Carmichael",
    "show": "Rugrats",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1991,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Billy",
    "show": "The Grim Adventures of Billy & Mandy",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mandy",
    "show": "The Grim Adventures of Billy & Mandy",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Grim",
    "show": "The Grim Adventures of Billy & Mandy",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Irwin",
    "show": "The Grim Adventures of Billy & Mandy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Nergal",
    "show": "The Grim Adventures of Billy & Mandy",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2001,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Flapjack",
    "show": "The Marvelous Misadventures of Flapjack",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2008,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Captain K'nuckles",
    "show": "The Marvelous Misadventures of Flapjack",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2008,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Bubbie",
    "show": "The Marvelous Misadventures of Flapjack",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2008,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Leonardo",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Michelangelo",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Donatello",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Raphael",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Splinter",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "April O'Neil",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Casey Jones",
    "show": "Teenage Mutant Ninja Turtles",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2012,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Jenny (XJ-9)",
    "show": "My Life as a Teenage Robot",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Goddard",
    "show": "My Life as a Teenage Robot",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2003,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Danny Fenton (Danny Phantom)",
    "show": "Danny Phantom",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sam Manson",
    "show": "Danny Phantom",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Tucker Foley",
    "show": "Danny Phantom",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Jazz Fenton",
    "show": "Danny Phantom",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 2004,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Scooby-Doo",
    "show": "Scooby-Doo",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1969,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Shaggy Rogers",
    "show": "Scooby-Doo",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1969,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Fred Jones",
    "show": "Scooby-Doo",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1969,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Daphne Blake",
    "show": "Scooby-Doo",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1969,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Velma Dinkley",
    "show": "Scooby-Doo",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 1969,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Nick Birch",
    "show": "Big Mouth",
    "network": "Netflix",
    "is_main": True,
    "release_year": 2017,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Andrew Glouberman",
    "show": "Big Mouth",
    "network": "Netflix",
    "is_main": True,
    "release_year": 2017,
    "still_airing": True,
    "gender": "Male"
  },
  {
    "name": "Jessi Glaser",
    "show": "Big Mouth",
    "network": "Netflix",
    "is_main": False,
    "release_year": 2017,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Missy Foreman-Greenwald",
    "show": "Big Mouth",
    "network": "Netflix",
    "is_main": False,
    "release_year": 2017,
    "still_airing": True,
    "gender": "Female"
  },
  {
    "name": "Bugs Bunny",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Daffy Duck",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": True,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Tweety",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Sylvester",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Porky Pig",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Yosemite Sam",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Lola Bunny",
    "show": "The Looney Tunes Show",
    "network": "Cartoon Network",
    "is_main": False,
    "release_year": 2011,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Steve Williams",
    "show": "Brickleberry",
    "network": "Comedy Central",
    "is_main": True,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ethel",
    "show": "Brickleberry",
    "network": "Comedy Central",
    "is_main": True,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Malloy",
    "show": "Brickleberry",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Connie",
    "show": "Brickleberry",
    "network": "Comedy Central",
    "is_main": False,
    "release_year": 2012,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Rocko",
    "show": "Rocko's Modern Life",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 1993,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Heffer Wolfe",
    "show": "Rocko's Modern Life",
    "network": "Nickelodeon",
    "is_main": True,
    "release_year": 1993,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Filburt",
    "show": "Rocko's Modern Life",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1993,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ed Bighead",
    "show": "Rocko's Modern Life",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1993,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Mrs. Bighead",
    "show": "Rocko's Modern Life",
    "network": "Nickelodeon",
    "is_main": False,
    "release_year": 1993,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Phineas Flynn",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": True,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Ferb Fletcher",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": True,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Candace Flynn",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Perry the Platypus",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Isabella Garcia-Shapiro",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Baljeet",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Buford",
    "show": "Phineas and Ferb",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2007,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Milo",
    "show": "Fish Hooks",
    "network": "Disney Channel",
    "is_main": True,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Bea",
    "show": "Fish Hooks",
    "network": "Disney Channel",
    "is_main": True,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Female"
  },
  {
    "name": "Oscar",
    "show": "Fish Hooks",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  },
  {
    "name": "Guppy",
    "show": "Fish Hooks",
    "network": "Disney Channel",
    "is_main": False,
    "release_year": 2010,
    "still_airing": False,
    "gender": "Male"
  }
]
        

    print(f"Total entries in Cdata: {len(Cdata)}")
    unique_data = {entry["name"]: entry for entry in Cdata}.values()
    print(f"Unique entries after deduplication: {len(unique_data)}")
    
    # Clear existing data
    CartoonCharacter.objects.all().delete()
    
    # Populate with image URLs
    for data in unique_data:
        image_url = get_wikipedia_image(data["name"], data["show"])
        data["image_url"] = image_url  # Add fetched image URL
        CartoonCharacter.objects.get_or_create(**data)
        print(f"Added {data['name']} with image: {image_url}")
    
    print(f"Database populated with {len(unique_data)} unique characters.")
    print(f"Total characters in database: {CartoonCharacter.objects.count()}")

if __name__ == "__main__":
    populate_cartoon_data()