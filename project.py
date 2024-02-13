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
import datetime

load_dotenv()

options = ["Release year", "Vote"]
advanced_options = ["Language", "Vote threshold"]

DEFINITIONS = {
    "Release year": "searches for movies with an initial release in the given year - Default current year",
    "Language": "searches for movies with dialogue in the given language - Default English",
    "Vote threshold": "minimum amount of user votes for ratings - Default 2500",
    "Vote": "minimum voter rating score - Default 8.0"
}

DEFAULT_YEAR = str(datetime.datetime.now().year)
DEFAULT_LANGUAGE = "en"
VOTE_COUNT_THRESHOLD = "2500"
VOTE_SCORE = "8"

def main():
    intro()

    search = True
    while search:
        define_search()

        user_choice = input()
        if user_choice.isalpha() and user_choice.upper() == 'A':
            advanced_search()
            define_search()

        for option in options:
            get_option(option)

        get_movies()

        # get_year()
        user_choice = input("What you like to initiate another search? Y/N: ")
        if user_choice.upper() == "N":
            search = False
            print("\nThank you for using Top Movie Finder! Goodbye!")


def get_option(option):
    match option:
        case "Release year":
            return get_year()
        case "Language":
            return get_language()
        case "Vote threshold":
            return get_threshold()
        case "Vote":
            return get_vote()


def get_movies():
    global DEFAULT_YEAR
    global DEFAULT_LANGUAGE
    url = (f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1"
           f"&primary_release_year={DEFAULT_YEAR}&sort_by=vote_average.desc&vote_average.gte={VOTE_SCORE}"
           f"&vote_count.gte={VOTE_COUNT_THRESHOLD}&with_original_language={DEFAULT_LANGUAGE}")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('API_KEY')}"
    }

    response = requests.get(url, headers=headers)

    # print(response.text)
    movies = response.json()

    print(f"\nSearch query - Year: {DEFAULT_YEAR} Language: {DEFAULT_LANGUAGE} Vote Threshold: {VOTE_COUNT_THRESHOLD}"
          f" Rating: {VOTE_SCORE}\n")
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
    print("This application is intended to locate the best movies released in a given year\nand display "
          "them in order of popularity, so that you can work your way through\nall the top hits!\n")


def define_search():
    print("The following default search options are currently enabled:\n")
    num = 1
    for option in options:
        print(f"{num})  {option} - {DEFINITIONS[option]}")
        num += 1

    print("\nTo enable advanced search options input 'A' at the menu screen. Be advised that enabling custom\n"
          "search options could negatively impact the quality of search results. Options currently include\n"
          "Language selection and Vote threshold.\n")


def advanced_search():
    print("******************************************************************************")
    print("Advanced Search Options")
    num = 1
    for option in advanced_options:
        print(f"{num})  {option} - {DEFINITIONS[option]}")
        num += 1
    print("******************************************************************************\n")

    user_choice = True
    while user_choice:
        print("Input the number of the option you would like to enable or disable or hit enter to continue:")
        print(f"Currently enabled options {options}")
        user_choice = input()

        if user_choice:
            if advanced_options[int(user_choice) - 1] in options:
                options.remove(advanced_options[int(user_choice) - 1])
            else:
                options.append(advanced_options[int(user_choice) - 1])


def get_year():
    global DEFAULT_YEAR
    year = input("Please enter the year would you like to see the top movies from:")
    DEFAULT_YEAR = str(year)


def get_language():
    global DEFAULT_LANGUAGE
    print("Language options are in two letter language codes i.e. English-en, French-fr, Spanish-es")
    language = input("Please enter the language would you like to see the top movies from:")
    DEFAULT_LANGUAGE = language


def get_threshold():
    global VOTE_COUNT_THRESHOLD
    print("Input a positive integer for the user vote threshold for ratings or press enter to continue.")
    threshold = input("Please enter the vote threshold would you like to see the top movies starting from:")
    if threshold:
        VOTE_COUNT_THRESHOLD = threshold


def get_vote():
    global VOTE_SCORE
    print("Input a positive integer for the user score threshold for ratings or press enter to continue.")
    vote = input("Please enter the user score would you like to see the top movies starting from:")
    if vote:
        VOTE_SCORE = vote


if __name__ == "__main__":
    main()
