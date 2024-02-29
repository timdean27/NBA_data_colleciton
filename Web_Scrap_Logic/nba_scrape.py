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
        dropdown.select_by_index(1)

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


        # Extract player names, href attributes, and image sources
        player_data = []
        limit_players_for_test = 10
        for row in player_list.find_all("td", class_="primary text RosterRow_primaryCol__1lto4"):
            player_name_container = row.find("div", class_="RosterRow_playerName__G28lg")
            player_first_name = player_name_container.find("p", class_="RosterRow_playerFirstName__NYm50").text
            player_last_name = player_name_container.find_all("p")[1].text  # Select the second <p> tag for last name
            player_page_link = row.find("a", class_="Anchor_anchor__cSc3P RosterRow_playerLink__qw1vG")
            player_image = row.find("img", class_="PlayerImage_image__wH_YX PlayerImage_round__bIjPr")

            # Check if all required elements are not None before extracting data
            if player_name_container and player_first_name and player_page_link and player_image:
                full_name = f"{player_first_name} {player_last_name}"
                first_name = f"{player_first_name}"
                last_name = f"{player_last_name}"
                player_href = player_page_link.get("href")
                player_img_src = player_image.get("src")  # Extract 'src' attribute directly
                player_data.append({"name": full_name, "first_name": player_first_name, "last_name": player_last_name, "href": player_href, "img_src": player_img_src})
            
            if len(player_data) >= limit_players_for_test:
                break  # Stop collecting more players once the limit is reached

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
