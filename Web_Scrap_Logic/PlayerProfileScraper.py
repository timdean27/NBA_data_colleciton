
from nba_scrape import FetchNBA_Names_HREF
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class PlayerProfileScraper:
    def __init__(self):
        self.base_url = "https://www.nba.com"

    def scrape_player_profiles(self, player_data):
        print(f"running scrape_player_profiles method in PlayerProfileScraper class")
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
            points_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="PPG")
            if points_per_game:
                points_per_game_value = points_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Extract Rebounds Per Game (RPG)
            rebounds_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="RPG")
            if rebounds_per_game:
                rebounds_per_game_value = rebounds_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Extract Assists Per Game (APG)
            assists_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="APG")
            if assists_per_game:
                assists_per_game_value = assists_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text

            # Extract Player Impact Estimate (PIE)
            pie = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="PIE")
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

if __name__ == "__main__":
    # Create an instance of FetchNBA_Names_HREF class to get player data
    nba_fetcher = FetchNBA_Names_HREF()
    page_source = nba_fetcher.get_all_players_page_source()
    player_data = nba_fetcher.get_player_data(page_source)

    # Create an instance of PlayerProfileScraper class
    profile_scraper = PlayerProfileScraper()

    # Call the scrape_player_profiles method and print the result
    result = profile_scraper.scrape_player_profiles(player_data)
    print(result)