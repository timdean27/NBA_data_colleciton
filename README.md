# NBA_data_colleciton

- must frist run Push_to_mySQL which will Use get_all_players_page_source method in FetchNBA_Names_HREF class
    - this will get players names , and hrefs to be used for scraping in scrape_player_profiles method in PlayerProfileScraper class

- second run main_mySQL which will intialize and run PushProfileToMySQL which will push data optained in
    - scraping in scrape_player_profiles method in PlayerProfileScraper class to mySQL