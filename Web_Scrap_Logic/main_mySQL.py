# main_script.py
from nba_scrape import FetchNBA_Names_HREF
from PlayerProfileScraper import PlayerProfileScraper
from push_profile_to_mysql import PushProfileToMySQL

if __name__ == "__main__":
    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_password = 'Fishboy@27!'
    mysql_database = 'nba_data'

    # Create an instance of the FetchNBA_Names_HREF class
    nba_fetcher = FetchNBA_Names_HREF()

    # Fetch player data
    page_source = nba_fetcher.get_all_players_page_source()
    player_data = nba_fetcher.get_player_data(page_source)

    # Create an instance of the PlayerProfileScraper class
    profile_scraper = PlayerProfileScraper()

    # Scrape player profiles using the obtained player_data
    profile_data = profile_scraper.scrape_player_profiles(player_data)

    # Create an instance of the PushProfileToMySQL class
    profile_pusher = PushProfileToMySQL(mysql_host, mysql_user, mysql_password, mysql_database)

    # Push profile data to MySQL
    profile_pusher.push_profile_data_to_mysql(profile_data)
