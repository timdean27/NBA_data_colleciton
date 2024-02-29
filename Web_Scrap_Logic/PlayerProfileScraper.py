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

        for player in player_data:
            player_href = player['href']

            # Build the URL for each player's profile
            player_profile_url = f"https://www.nba.com{player_href}/profile"

            # Use Selenium to get the dynamic content of the player's profile
            driver = webdriver.Chrome()
            driver.get(player_profile_url)
            time.sleep(2)  # Add a delay to ensure the page loads

            # Use BeautifulSoup to parse the player's profile page
            profile_page_source = driver.page_source
            profile_soup = BeautifulSoup(profile_page_source, "html.parser")

            # Extract Points Per Game (PPG)
            points_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Points Per Game")
            if points_per_game:
                points_per_game_value = points_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text
                print(f"{player['name']} - Points Per Game: {points_per_game_value}")

            # Extract Rebounds Per Game (RPG)
            rebounds_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Rebounds Per Game")
            if rebounds_per_game:
                rebounds_per_game_value = rebounds_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text
                print(f"{player['name']} - Rebounds Per Game: {rebounds_per_game_value}")

            # Extract Assists Per Game (APG)
            assists_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Assists Per Game")
            if assists_per_game:
                assists_per_game_value = assists_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text
                print(f"{player['name']} - Assists Per Game: {assists_per_game_value}")

            # Extract Player Impact Estimate (PIE)
            pie = profile_soup.find("p", class_="PlayerSummary_playerStatValue___EDg_", string="Player Impact Estimate")
            if pie:
                pie_value = pie.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text
                print(f"{player['name']} - Player Impact Estimate: {pie_value}")

            driver.quit()

if __name__ == "__main__":
    # Create an instance of the FetchNBA_Names_HREF class
    nba_fetcher = FetchNBA_Names_HREF()

    # Fetch player data
    page_source = nba_fetcher.get_all_players_page_source()
    player_data = nba_fetcher.get_player_data(page_source)

    # Create an instance of the PlayerProfileScraper class
    profile_scraper = PlayerProfileScraper()

    # Scrape player profiles using the obtained player_data
    profile_scraper.scrape_player_profiles(player_data)
