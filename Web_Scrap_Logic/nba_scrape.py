from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

class FetchNBA_Names_HREF:
    def __init__(self):
        self.url = "https://www.nba.com/players"

    def get_all_players_page_source(self):
        print("Running get_all_players_page_source method in FetchNBA_Names_HREF class")
        # Set up Chrome WebDriver
        driver = webdriver.Chrome()
        driver.get(self.url)

        try:
            # Wait for the dropdown to be present (adjust the time as needed)
            time.sleep(2)

            # Find all dropdowns with class "DropDown_select__4pIg9"
            dropdown_elements = driver.find_elements(By.CLASS_NAME, "DropDown_select__4pIg9")

            # Initialize a variable to store the correct dropdown element
            correct_dropdown = None

            # Iterate through each dropdown element
            for dropdown_element in dropdown_elements:
                # Check if the dropdown element has the title "Page Number Selection Drown Down List"
                if "Page Number Selection Drown Down List" in dropdown_element.get_attribute("title"):
                    correct_dropdown = dropdown_element
                    break  # Exit the loop once the correct dropdown is found

            # Check if a valid dropdown element was found
            if correct_dropdown:
                print("Found dropdown with title:", correct_dropdown.get_attribute("title"))

                # Use the Select class to interact with the dropdown
                dropdown = Select(correct_dropdown)

                # Click the dropdown to open options
                correct_dropdown.click()

                # Wait for the options to be visible (adjust time if necessary)
                time.sleep(2)

                # Select the "All" option by visible text
                dropdown.select_by_visible_text("All")

                # Optionally, click the dropdown again to close it (not necessary for functionality)
                correct_dropdown.click()

                # Wait for the page to load after selecting "All" (adjust the time as needed)
                time.sleep(2)

                # Get the page source after the dropdown selection
                page_source = driver.page_source

                # Print success message
                print("Successfully fetched page source after selecting 'All'.")

                # Return the page source
                return page_source

            else:
                print("No dropdown found with the title 'Page Number Selection Drown Down List'.")
                return None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            # Close the WebDriver
            driver.quit()

    def get_player_data(self, page_source):
        print("Running get_player_data method in FetchNBA_Names_HREF class")
        try:
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, "html.parser")

            # Use class names to select the table body
            player_list = soup.find("table", class_="players-list")

            # Extract player names, href attributes, and image sources
            player_data = []
            limit_players_for_test = 1
            for idx, row in enumerate(player_list.find_all("td", class_="primary text RosterRow_primaryCol__1lto4"), 1):
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
                    player_data.append({"name": full_name, "first_name": first_name, "last_name": last_name, "href": player_href, "img_src": player_img_src})

                    # Print information about each player data collected
                    print(f"Collected data for Player {idx}: {full_name}, Link: {player_href}")

                if len(player_data) >= limit_players_for_test:
                    break  # Stop collecting more players once the limit is reached

            return player_data

        except Exception as e:
            print(f"Error in get_player_data: {e}")
            return None

# Example usage:
if __name__ == "__main__":
    try:
        nba_fetcher = FetchNBA_Names_HREF()

        # Fetch player data
        page_source = nba_fetcher.get_all_players_page_source()

        if page_source:
            player_data = nba_fetcher.get_player_data(page_source)
            if player_data:
                print(f"Scraped profiles for {len(player_data)} players.")
                for player in player_data:
                    print(player)
            else:
                print("No player data fetched.")
        else:
            print("Failed to fetch page source.")

    except Exception as e:
        print(f"An error occurred: {e}")
