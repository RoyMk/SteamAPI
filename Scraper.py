from os import PathLike
from pathlib import Path
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import csv


def scrape_games(
    pages: int,
    export_data: bool = False,
    export_location: str | bytes | PathLike = None
) -> list[dict[str, str]] | None:
    """
    Scrapes Steamcharts (https://steamcharts.com/) to retrieve player statistics for the top games.

    This function fetches data from the specified number of pages on the Steamcharts "Top Games" list.
    Each page contains up to 25 games. It returns a list of dictionaries with each dictionary representing
    a game and its player statistics.

    Args:
        pages (int): Number of pages to scrape. Each page contains up to 25 games.
        export_data (bool, optional): If True, exports the collected data to a CSV file.
            Defaults to False.
        export_location (str | bytes | PathLike, optional): File path to export the CSV data.
            Must be provided if `export_data` is True. The file extension is not required.
            Example: "C:/Users/User/Desktop/document"

    Returns:
        list[dict[str, str]] | None: A list of dictionaries with keys:
            - 'name': Game title (str)
            - 'current_players': Current number of players (str)
            - 'peak_players': Peak number of players (str)
        Returns None if `export_data` is True and export_location is not provided.

    Raises:
        ValueError: If `export_data` is True but `export_location` is None.

    Example:
        >>> games = scrape_games(pages=2, export_data=True, export_location="C:/data/steam_stats")
        >>> pprint(games)
    """
    if export_data and not export_location:
        raise ValueError("export_location must be specified if export_data is True.")

    games = []

    for i in range(1, pages + 1):
        if i == 1:
            url = "https://steamcharts.com/top"
        else:
            url = f"https://steamcharts.com/top/p.{i}"

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"class": "common-table"})
        rows = table.find_all("tr")[1:]  # Skip header row

        for row in rows:
            columns = row.find_all("td")
            name = columns[1].text.strip()
            current_players = columns[2].text.strip()
            peak_players = columns[4].text.strip()
            games.append({
                "name": name,
                "current_players": current_players,
                "peak_players": peak_players
            })

    if export_data:
        # Ensure export_location is a Path object and add .csv extension if missing
        export_path = Path(export_location)
        if export_path.suffix != ".csv":
            export_path = export_path.with_suffix(".csv")

        with open(export_path, 'w', newline='', encoding="utf-8") as csvfile:
            fieldnames = ['name', 'current_players', 'peak_players']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(games)

        return None  # Explicitly return None when exporting

    return games


if __name__ == "__main__":
    pprint(scrape_games(pages=5))
