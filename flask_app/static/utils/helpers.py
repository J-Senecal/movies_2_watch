import requests
from apikey import apikey


def api_call(title):
    try:
        movie = f"http://www.omdbapi.com/?t={title}&apikey={apikey}"

        response = requests.get(movie)
        data = response.json()
        # print(data)
        give_back = {
            'title': data['Title'],
            'year': data['Year'],
            'genre': data['Genre'],
            'plot': data['Plot'],
            'actors': data['Actors'],
            'ratings': data['Ratings'][0]['Value'],
            'poster': data['Poster']
        }

        return give_back
    
    except requests.exceptions.RequestException as e:
        # Catching any exception related to the request
        print("Error occurred during API call:", e)
        error = {
            'title': 'Title NOT found in IMDB',
            'year': 'year NOT found in IMDB',
            'genre': 'genre NOT found in IMDB',
            'plot': 'plot NOT found in IMDB',
            'actors': 'actors NOT found in IMDB',
            'ratings': 'ratings NOT found in IMDB',
            'poster': 'poster NOT found in IMDB'
        }
        return error
    
    except KeyError as e:
        # Catching KeyError which might occur if expected data is missing in the response
        print("KeyError occurred while processing response:", e)
        error = {
            'title': 'Title NOT found in IMDB',
            'year': 'year NOT found in IMDB',
            'genre': 'genre NOT found in IMDB',
            'plot': 'plot NOT found in IMDB',
            'actors': 'actors NOT found in IMDB',
            'ratings': 'ratings NOT found in IMDB',
            'poster': 'poster NOT found in IMDB'
        }
        return error
        return error
