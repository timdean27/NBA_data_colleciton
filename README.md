# NBA Player Profile Scraper and MySQL Data Pusher

This project is a Python-based application that scrapes NBA player profiles and stores the data in a MySQL database. It uses Selenium for web scraping and the MySQL connector for database operations.

## Features

- Scrapes player data from the NBA website.
- Stores player data, including stats such as Points Per Game (PPG), Rebounds Per Game (RPG), Assists Per Game (APG), and Player Impact Estimate (PIE), into a MySQL database.
- Handles missing or unavailable data by assigning default values.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- Google Chrome browser and ChromeDriver
- MySQL server
- Required Python packages listed in `requirements.txt`

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/nba-player-scraper.git
    cd nba-player-scraper
    ```

2. **Install the Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure MySQL Database**

    Create a MySQL database and update the database configuration in the `main.py` script:
    ```python
    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_password = 'your-password'
    mysql_database = 'nba_data'
    ```

## Usage

1. **Run the Scraper and Data Pusher**

    The `main.py` script will scrape the NBA player profiles and push the data to the MySQL database:
    ```bash
    python main.py
    ```

## Code Overview

### `nba_scrape.py`

Contains the `FetchNBA_Names_HREF` class responsible for fetching player names and profile links from the NBA website.

### `player_profile_scraper.py`

Contains the `PlayerProfileScraper` class responsible for scraping individual player profile data, including stats such as PPG, RPG, APG, and PIE.

### `push_profile_to_mysql.py`

Contains the `PushProfileToMySQL` class responsible for creating the MySQL table and inserting player profile data into the database.

### `main.py`

Main script to run the scraping and data insertion process.

## Example Output

