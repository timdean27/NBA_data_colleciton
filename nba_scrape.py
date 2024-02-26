from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

class FetchNBA_Names_HREF:
    def __init__(self):
        self.url = "https://www.nba.com/players"

    def get_all_players_page_source(self):
        # Set up Chrome WebDriver
        driver = webdriver.Chrome()
        driver.get(self.url)

        # Wait for the dropdown to be present (adjust the time as needed)
        time.sleep(2)

        # Select "All" option in the dropdown
        dropdown_element = driver.find_element(by="xpath", value="/html/body/div[1]/div[2]/div[2]/main/div[2]/section/div/div[2]/div[1]/div[7]/div/div[3]/div/label/div/select")
        print(dropdown_element)
        dropdown_element.click()

        # Use the Select class to interact with the dropdown
        dropdown = Select(dropdown_element)

        # Select the first option in the dropdown
        dropdown.select_by_index(0)

        # Wait for the page to load after selecting "All" (adjust the time as needed)
        time.sleep(2)

        # Get the page source after the dropdown selection
        page_source = driver.page_source

        # Close the WebDriver
        driver.quit()

        # Return the page source
        return page_source

    def get_player_data(self, page_source):
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Use class names to select the table body
        player_list = soup.find("table", class_="players-list") 

        # Extract player names and href attributes
        player_data = []
        for row in player_list.find_all("td", class_="primary text RosterRow_primaryCol__1lto4"): 
            player_name = row.find("div", class_="RosterRow_playerName__G28lg")
            first_name = row.find("p", class_="RosterRow_playerFirstName__NYm50")
            player_page_link = row.find("a", class_="Anchor_anchor__cSc3P RosterRow_playerLink__qw1vG")

            # Check if both player_name and first_name are not None before extracting text
            if player_name and first_name and player_page_link:
                full_name = f"{first_name.text} {player_name.text}"
                player_href = player_page_link.get("href")
                player_data.append({"name": full_name, "href": player_href})
            
        return player_data

#     def fetch_and_display_players(self):
#         page_source = self.get_all_players_page_source()
#         players = self.get_player_data(page_source)

#         # Display the result
#         for i, player in enumerate(players, start=1):
#             print(f"{i}. Name: {player['name']}, Href: {player['href']}")

# # Create an instance of the class
# nba_fetcher = FetchNBA_Names_HREF()

# # Call the method to fetch and display players
# nba_fetcher.fetch_and_display_players()
