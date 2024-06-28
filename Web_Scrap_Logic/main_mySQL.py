from nba_scrape import FetchNBA_Names_HREF
from PlayerProfileScraper import PlayerProfileScraper
from push_profile_to_mysql import PushProfileToMySQL

if __name__ == "__main__":
    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_password = 'Fishboy@27!'
    mysql_database = 'nba_data'

    try:
        # Create an instance of the FetchNBA_Names_HREF class
        print("Creating FetchNBA_Names_HREF instance...")
        nba_fetcher = FetchNBA_Names_HREF()

        # Fetch player data
        print("Fetching NBA player data...")
        page_source = nba_fetcher.get_all_players_page_source()
        player_data = nba_fetcher.get_player_data(page_source)
        print(f"Found {len(player_data)} players.")

        # Create an instance of the PlayerProfileScraper class
        print("Creating PlayerProfileScraper instance...")
        profile_scraper = PlayerProfileScraper()

        # Scrape player profiles using the obtained player_data
        print("Scraping player profiles...")
        profile_data = profile_scraper.scrape_player_profiles(player_data)
        print(f"Scraped profiles for {len(profile_data)} players.")

        # Create an instance of the PushProfileToMySQL class
        print("Creating PushProfileToMySQL instance...")
        profile_pusher = PushProfileToMySQL(mysql_host, mysql_user, mysql_password, mysql_database)
        # Ensure table exists and columns are correct
        profile_pusher.check_table_columns_existence()
        # Push profile data to MySQL
        print("Pushing profile data to MySQL...")
        profile_pusher.push_profile_data_to_mysql(profile_data)
        print("Profile data successfully pushed to MySQL.")

    except Exception as e:
        print(f"An error occurred: {e}")
