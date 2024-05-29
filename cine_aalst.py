"""
Cine Aalst CLI tool to fetch and display movie schedules.
"""

import argparse
import json
import re
from datetime import datetime, timedelta

import requests

# Dictionary to map warning options to emojis
warning_emojis = {
    "kw-discrimination": "🚫",
    "kw-fear": "😱",
    "kw-rating-12": "-12",
    "kw-rating-14": "-14",
    "kw-rating-16": "-16",
    "kw-rating-6": "-6️⃣",
    "kw-rating-all": "🅰️",
    "kw-violence": "🔫",
    "kw-coarse-language": "🤬",
    "kw-drugs": "💊",
    "kw-sex": "🍆",
    "kw-nudity": "🍑",
}


def get_movies_and_schedules():
    """
    Fetches the movie and schedule data from the Cine Aalst website.
    """
    url = "https://cine-aalst.be/nl/movies/today"
    response = requests.get(url)
    content = response.text
    pattern = r'<script id="storeData">window.storeData =(.+?);<\/script>'
    match = re.search(pattern, content)

    if match:
        json_data = match.group(1)
        data = json.loads(json_data)
        movies = data.get("movies", [])
        schedules = data.get("schedules", [])
        cinemas = data.get("cinemas", [])
        screens = data.get("screens", [])
        return movies, schedules, cinemas, screens

    print("JSON data not found.")
    return [], [], [], []


def filter_schedules_by_date(schedules, target_date):
    """
    Filters the schedules by the target date.
    """
    filtered_schedules = []
    for schedule in schedules:
        start_time = datetime.fromisoformat(schedule["start"].split("+")[0])
        if start_time.date() == target_date:
            filtered_schedules.append(schedule)
    return filtered_schedules


def aggregate_schedules_by_movie(schedules):
    """
    Aggregates schedules by movie ID.
    """
    aggregated_schedules = {}
    for schedule in schedules:
        movie_id = schedule["movie_id"]
        if movie_id not in aggregated_schedules:
            aggregated_schedules[movie_id] = []
        aggregated_schedules[movie_id].append(schedule)
    return aggregated_schedules


def get_cinema_details(cinemas, cinema_id):
    """
    Retrieves details of a cinema by its ID.
    """
    for cinema in cinemas:
        if cinema["id"] == cinema_id:
            return cinema
    return None


def get_screen_details(screens, screen_id):
    """
    Retrieves details of a screen by its ID.
    """
    for screen in screens:
        if screen["id"] == screen_id:
            return screen
    return None


def print_movie(movie, schedules, cinemas, screens):
    """
    Prints the details of a movie along with its schedules.
    """
    movie_name = movie["title"]
    options = movie.get("options", [])
    warning_symbols = [warning_emojis.get(option, "") for option in options]
    print(f"\033[94m{movie_name}\033[0m:")
    print(f"  - \033[1mWarnings:\033[0m {', '.join(warning_symbols)}")

    description = movie.get("description", "")
    if description:
        description = re.sub("<[^<]+?>", "", description)
        print(f"  - \033[1mDescription:\033[0m {description}")

    # Print movie details
    print_movie_details(movie)

    # Print schedules
    print_schedules(schedules, cinemas, screens)


def print_movie_details(movie):
    """
    Prints movie details.
    """
    print(f"  - \033[1mDirector:\033[0m {movie['director']}")
    if movie["actors"] is not None:
        print(f"  - \033[1mActors:\033[0m {movie['actors']}")
    print(
        f"  - \033[1mPoster:\033[0m \x1B]8;;https://cine-aalst.be{movie['poster']}\x1B\\Link\x1B]8;;\x1B\\"
    )
    print(f"  - \033[1mTrailer:\033[0m \x1B]8;;https:{movie['trailer']}\x1B\\Link\x1B]8;;\x1B\\")
    print(f"  - \033[1mRuntime:\033[0m {movie['runtime']} minutes")
    if movie["nation"] is not None:
        print(f"  - \033[1mNation:\033[0m {movie['nation']}")
    release_date = datetime.fromisoformat(movie["release"].split("+")[0])
    print(f"  - \033[1mRelease Date:\033[0m {release_date.strftime('%Y-%m-%d')}")


def print_schedules(schedules, cinemas, screens):
    """
    Prints movie schedules.
    """
    print("  - \033[1mSchedules:\033[0m")
    for schedule in schedules:
        start_time = datetime.fromisoformat(schedule["start"].split("+")[0])
        cinema_details = get_cinema_details(cinemas, schedule["cinema_id"])
        screen_details = get_screen_details(screens, schedule["screen_id"])
        accessibility = "♿️" if screen_details and screen_details["accessible_disabled"] else ""
        mask_emoji = (
            "😷" if screen_details and screen_details["config"]["social_distancing_enabled"] else ""
        )
        ticket_link = f"https://cine-aalst.be/nl/buy/tickets/{schedule['id']}"
        cinema_name = cinema_details["name"]
        cinema_address = (
            f"{cinema_details['address']['address1']}, {cinema_details['address']['city']}"
        )
        zaal_name = screen_details["name"]
        print(
            f"    - {start_time.strftime('%A, %d %B %H:%M')}{accessibility}{mask_emoji} - "
            f"{zaal_name} ({cinema_name}, {cinema_address}) - \x1B]8;;{ticket_link}\x1B\\Tickets\x1B]8;;\x1B\\"
        )
    print("---")


def print_movies_by_date(movies, schedules, cinemas, screens, target_date):
    """
    Prints movies and schedules for a specific date or all dates.
    """
    if target_date is None:
        print("\033[1mMovies and Schedules for all dates:\033[0m")
    else:
        print(f"\033[1mMovies and Schedules for {target_date.strftime('%Y-%m-%d')}:\033[0m")
    aggregated_schedules = aggregate_schedules_by_movie(schedules)
    for movie_id, movie_schedules in aggregated_schedules.items():
        for movie in movies:
            if movie["id"] == movie_id:
                print_movie(movie, movie_schedules, cinemas, screens)
                break


def print_movies_by_title(search_query, movies, schedules, cinemas, screens):
    """
    Prints movies and schedules that match a given search query.
    """
    matching_movies = [movie for movie in movies if search_query.lower() in movie["title"].lower()]
    if matching_movies:
        print(f"\033[1mMovies matching '{search_query}':\033[0m")
        for movie in matching_movies:
            movie_schedules = [
                schedule for schedule in schedules if schedule["movie_id"] == movie["id"]
            ]
            print_movie(movie, movie_schedules, cinemas, screens)
    else:
        print(f"No movies found matching '{search_query}'.")


def parse_date(date_str):
    """
    Parses a date string into a date object.
    """
    if date_str == "today":
        return datetime.today().date()
    if date_str == "tomorrow":
        return datetime.today().date() + timedelta(days=1)
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Invalid date format. Please use YYYY-MM-DD, 'today' or 'tomorrow'."
        ) from exc


def main():
    """
    Main function to parse arguments and print movie schedules.
    """
    parser = argparse.ArgumentParser(description="Get movie schedules for Cine Aalst.")
    parser.add_argument(
        "-d",
        "--date",
        type=parse_date,
        help="Date for which to get movie schedules. Can be 'today', 'tomorrow', or YYYY-MM-DD format. Can be combined with -m.",
    )
    parser.add_argument(
        "-m",
        "--movie",
        type=str,
        help="Search for a movie by title. Can be combined with -d.",
    )
    args = parser.parse_args()

    movies, schedules, cinemas, screens = get_movies_and_schedules()
    if args.movie:
        if args.date:
            filtered_schedules = filter_schedules_by_date(schedules, args.date)
        else:
            filtered_schedules = schedules  # All schedules
        print_movies_by_title(args.movie, movies, filtered_schedules, cinemas, screens)
    else:
        if args.date:
            filtered_schedules = filter_schedules_by_date(schedules, args.date)
        else:
            filtered_schedules = schedules  # All schedules
        print_movies_by_date(movies, filtered_schedules, cinemas, screens, args.date)


if __name__ == "__main__":
    main()
