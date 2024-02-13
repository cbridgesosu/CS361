# # LIST options: WATCH, LIKE, DISLIKE
# add_request = { 'user_ID': 12345, 'LIST': 'WATCH', 'movie_ID': 98765}
#
# # get request just sends user ID
# get_request = 12345
#
# return_request = {
#     'user_ID': 12345,
#     'WATCH': [98765],
#     'LIKE': [],
#     'DISLIKE': []
# }

import os
from dotenv import load_dotenv
import requests

load_dotenv()

options = ["Release year", "Language"]

definitions = {
    "Release year": "searches for movies with an initial release in the given year",
    "Language": "searches for movies with dialogue in the given language"
}

def main():
    intro()

    search = True
    while search:
        define_search()

        get_year()
        user_choice = input("What you like to initiate another search? Y/N: ")
        if user_choice.upper() == "N":
            search = False
            print("Thank you for using Top Movie Finder! Goodbye!")

def get_movies(year=""):
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1primary_release_year={year}&sort_by=popularity.desc"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.get(url, headers=headers)

    # print(response.text)
    movies = response.json()

    for movie in movies["results"]:
        print(movie["title"])


def intro():
    title = ("******************************************************************************\n"
             "* _    _      _                            _          _   _                  *\n"
             "*| |  | |    | |                          | |        | | | |                 *\n"
             "*| |  | | ___| | ___ ___  _ __ ___   ___  | |_ ___   | |_| |__   ___         *\n"
             "*| |/\\| |/ _ \\ |/ __/ _ \\| '_ ` _ \\ / _ \\ | __/ _ \\  | __| '_ \\ / _ \\        *\n"
             "*\\  /\\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |_| | | |  __/        *\n"
             "* \\/  \\/ \\___|_|\\___\\___/|_| |_| |_|\\___|  \\__\\___/   \\__|_| |_|\\___|        *\n"
             "*                                                                            *\n"
             "*                                                                            *\n"
             "* _____            ___  ___           _       ______ _           _           *\n"
             "*|_   _|           |  \\/  |          (_)      |  ___(_)         | |          *\n"
             "*  | | ___  _ __   | .  . | _____   ___  ___  | |_   _ _ __   __| | ___ _ __ *\n"
             "*  | |/ _ \\| '_ \\  | |\\/| |/ _ \\ \\ / / |/ _ \\ |  _| | | '_ \\ / _` |/ _ \\ '__|*\n"
             "*  | | (_) | |_) | | |  | | (_) \\ V /| |  __/ | |   | | | | | (_| |  __/ |   *\n"
             "*  \\_/\\___/| .__/  \\_|  |_/\\___/ \\_/ |_|\\___| \\_|   |_|_| |_|\\__,_|\\___|_|   *\n"
             "*          | |                                                               *\n"
             "*          |_|                                                               *\n"
             "******************************************************************************\n")

    print(title)
    print("This application is intended to locate the best movies released in a given year\nand display"
          "them in order of popularity, so that you can work your way through\nall the top hits!\n\n")


def define_search():
    print("The following search options are currently enabled:\n")
    num = 1
    for option in options:
        print(f"{num})  {option} - {definitions[option]}")
        num += 1

    print()

def get_year():
    year = input("Please enter the year would you like to see the top movies from:")

    get_movies(year)


if __name__ == "__main__":
    main()
