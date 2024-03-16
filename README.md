# NBA_data_colleciton

- must frist run "python Web_Scrap_Logic/push_to_MySQL.py" which will Use get_all_players_page_source method in FetchNBA_Names_HREF class
    - this will get players names , and hrefs to be used for scraping in scrape_player_profiles method in PlayerProfileScraper class

- second run "python Web_Scrap_Logic/main_mySQL.py" which will intialize and run PushProfileToMySQL which will push data optained in
    - scraping in scrape_player_profiles method in PlayerProfileScraper class to mySQL