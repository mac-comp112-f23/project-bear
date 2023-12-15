from imdb import Cinemagoer
import csv
import time

ia = Cinemagoer()

def write_to_csv(data, filename):
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def get_movie_details(movie_id):
    try:
        time.sleep(1)  # Wait for 1 second between requests
        movie = ia.get_movie(movie_id)
        return {
            'rating': movie.get('rating', 'N/A'),
            'genres': ', '.join(movie.get('genres', [])),
            'directors': ', '.join(str(d) for d in movie.get('director', [])),
            'plot': movie.get('plot outline', 'N/A')
        }
    except Exception as e:
        print(f"Error fetching movie details: {e}")
        return {'rating': 'N/A', 'genres': 'N/A', 'directors': 'N/A', 'plot': 'N/A'}

def get_composer_data(name, csv_filename):
    try:
        # Search for the person
        people = ia.search_person(name)
        if not people:
            print(f"No data found for {name}")
            return None

        # Fetching person data
        person_id = people[0].personID
        person = ia.get_person(person_id, info=['filmography', 'awards'])

        if 'name' in person:
            print(f"\nName: {person['name']}")
        else:
            print(f"Name not found for {name}")

        print(f"Birth Date: {person.get('birth date', 'N/A')}")

        # Awards
        print("\nAwards:")
        for award in person.get('awards', []):
            print(f"- {award['year']}: {award['award']} for {award.get('movie', 'N/A')}")

        # Filmography (limited)
        print("\nFilmography (limited):")
        for role in person.get('filmography', []):
            print(f"\n{role}:")
            for i, movie in enumerate(person['filmography'][role]):
                if i >= 6:  # Limiting to first 6 entries
                    break
                title = movie.get('title', 'N/A')
                year = movie.get('year', 'N/A')
                print(f"- {title} ({year})")

        # Write filmography to CSV
        for role in person.get('filmography', []):
            for movie in person['filmography'][role]:
                title = movie.get('title', 'N/A')
                year = movie.get('year', 'N/A')
                movie_id = movie.movieID
                movie_details = get_movie_details(movie_id)
                
                data_row = [
                    name, title, year, role, 
                    movie_details['rating'], movie_details['genres'], 
                    movie_details['directors'], movie_details['plot']
                ]
                write_to_csv(data_row, csv_filename)

        return person

    except Exception as e:
        print(f"Error: {e}")
        return None

# Specify the filename for the CSV
csv_filename = "composer_data.csv"

# Fetch data for each composer and write to CSV
danny_elfman = get_composer_data("Danny Elfman", csv_filename)
daniel_pemberton = get_composer_data("Daniel Pemberton", csv_filename)
hans_zimmer = get_composer_data("Hans Zimmer", csv_filename)
