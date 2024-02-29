from selenium import webdriver
from bs4 import BeautifulSoup
import time
from nba_scrape import FetchNBA_Names_HREF  # Make sure to adjust the import based on your project structure

class PlayerProfileScraper:
    def __init__(self):
        self.base_url = "https://www.nba.com"

    def scrape_player_profiles(self, player_data):
        # Set up Chrome WebDriver
        driver = webdriver.Chrome()

        profile_data_list = []  # List to store scraped player profiles

        for player in player_data:
            player_href = player['href']

            # Build the URL for each player's profile
            player_profile_url = f"https://www.nba.com{player_href}/profile"

            # Use Selenium to get the dynamic content of the player's profile
            driver.get(player_profile_url)
            time.sleep(2)  # Add a delay to ensure the page loads

            # Use BeautifulSoup to parse the player's profile page
            profile_page_source = driver.page_source
            profile_soup = BeautifulSoup(profile_page_source, "html.parser")

            # Extract Points Per Game (PPG)
            points_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Points Per Game")
            if points_per_game:
                points_per_game_value = points_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Extract Rebounds Per Game (RPG)
            rebounds_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Rebounds Per Game")
            if rebounds_per_game:
                rebounds_per_game_value = rebounds_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Extract Assists Per Game (APG)
            assists_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Assists Per Game")
            if assists_per_game:
                assists_per_game_value = assists_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Extract Player Impact Estimate (PIE)
            pie = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Player Impact Estimate")
            if pie:
                pie_value = pie.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Store the scraped data in a dictionary
            player_profile_data = {
                'name': player['name'],
                'ppg': points_per_game_value if points_per_game else None,
                'rpg': rebounds_per_game_value if rebounds_per_game else None,
                'apg': assists_per_game_value if assists_per_game else None,
                'pie': pie_value if pie else None
            }

            profile_data_list.append(player_profile_data)

        driver.quit()
        return profile_data_list

