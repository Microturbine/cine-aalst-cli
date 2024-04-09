# CineAalstCLI

CineAalstCLI is a command-line interface tool that allows users to view movie schedules and details for Cine Aalst cinema in Aalst.
It provides a simple way to check the movie schedules for today, tomorrow, or a specific date, search for movies by title, and get detailed information about a specific movie.
You can get a direct link to book tickets or get more information.

## Disclaimer

This tool is not affiliated with Cine Aalst cinema in any way. The tool scrapes data from the cinema's website in a respectful manner and does not introduce any harm to the website.

The tool is intended for personal use only, and the author does not take any responsibility for any misuse of the tool.


## Features

- View movie schedules for today, tomorrow, or a specific date.
- Search for movies by title.
- Get detailed information about a specific movie.
- Filter movies by warnings (e.g., age ratings, content advisories).
- Option to view a simple bulleted list of all movie titles.

## Installation

1. Install dependencies:

```bash
# Python 3 and pip are required
pip install -r requirements.txt
```

## Usage

Options:

- `-d, --date [DATE]`: Specify the date for which to get movie schedules (format: YYYY-MM-DD, 'today', or 'tomorrow').
- `-m, --movie [TITLE]`: Search for a movie by title.

These options can be combined.

## Examples

```bash
# Show movie schedules for today
python cine-aalst.py -d today

# Show movie schedules for tomorrow
python cine-aalst.py -d tomorrow

# Show movie schedules for a specific date (Schedules are available for the next 7 days or so)
python cine-aalst.py -d 2024-04-12

# Search for a movie by title (Partial matches are also supported)
python cine-aalst.py -m "Kung Fu Panda"

# Search for a specific movie on a specific date
python cine-aalst.py -d 2024-04-12 -m "Kung Fu Panda"

```
