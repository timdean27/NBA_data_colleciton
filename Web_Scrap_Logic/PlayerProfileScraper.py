
from nba_scrape import FetchNBA_Names_HREF
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class PlayerProfileScraper:
    def __init__(self):
        self.base_url = "https://www.nba.com"

    def scrape_player_profiles(self, player_data):
        print("Running scrape_player_profiles method in PlayerProfileScraper class")
        profile_data_list = []

        # Set up Chrome WebDriver
        with webdriver.Chrome() as driver:
            for player in player_data:
                player_href = player['href']
                player_profile_url = f"{self.base_url}{player_href}/profile"

                try:
                    # Use Selenium to get the dynamic content of the player's profile
                    driver.get(player_profile_url)
                    time.sleep(2)  # Add a delay to ensure the page loads

                    # Use BeautifulSoup to parse the player's profile page
                    profile_page_source = driver.page_source
                    profile_soup = BeautifulSoup(profile_page_source, "html.parser")

                    # Example: Extract Points Per Game (PPG)
                    points_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="PPG")
                    points_per_game_value = points_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text if points_per_game else None

                    # Example: Extract Rebounds Per Game (RPG)
                    rebounds_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="RPG")
                    rebounds_per_game_value = rebounds_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text if rebounds_per_game else None

                    # Example: Extract Assists Per Game (APG)
                    assists_per_game = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="APG")
                    assists_per_game_value = assists_per_game.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text if assists_per_game else None

                    # Example: Extract Player Impact Estimate (PIE)
                    pie = profile_soup.find("p", class_="PlayerSummary_playerStatLabel__I3TO3", string="PIE")
                    pie_value = pie.find_next("p", class_="PlayerSummary_playerStatValue___EDg_").text if pie else None

                    # Store the scraped data in a dictionary
                    player_profile_data = {
                        'name': player['name'],
                        'ppg': points_per_game_value,
                        'rpg': rebounds_per_game_value,
                        'apg': assists_per_game_value,
                        'pie': pie_value
                    }

                    profile_data_list.append(player_profile_data)

                except Exception as e:
                    print(f"Error scraping player profile: {e}")

        return profile_data_list

# Example usage:
if __name__ == "__main__":
    # Initialize FetchNBA_Names_HREF and get player data
    nba_fetcher = FetchNBA_Names_HREF()
    page_source = nba_fetcher.get_all_players_page_source()
    player_data = nba_fetcher.get_player_data(page_source)

    # Initialize PlayerProfileScraper and scrape player profiles
    profile_scraper = PlayerProfileScraper()
    result = profile_scraper.scrape_player_profiles(player_data)

    # Print or process the scraped data as needed
    if result:
        print(f"Scraped profiles for {len(result)} players.")
        for player_profile in result:
            print(player_profile)
    else:
        print("No player profiles scraped.")
