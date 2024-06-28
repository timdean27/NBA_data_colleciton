import mysql.connector
from mysql.connector import Error
from nba_scrape import FetchNBA_Names_HREF
import logging

class PushProfileToMySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_table(self):
        try:
            with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            ) as connection:
                cursor = connection.cursor()

                create_table_query = """
                    CREATE TABLE IF NOT EXISTS nba_players (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        full_name VARCHAR(255) NOT NULL,
                        first_name VARCHAR(255) NOT NULL,
                        last_name VARCHAR(255) NOT NULL,
                        href VARCHAR(255) UNIQUE NOT NULL COLLATE utf8_general_ci,
                        img_src VARCHAR(255) NOT NULL,
                        ppg FLOAT,
                        rpg FLOAT,
                        apg FLOAT,
                        pie FLOAT
                    )
                """
                cursor.execute(create_table_query)
                connection.commit()
                logging.info("Table 'nba_players' created successfully or already exists.")

        except mysql.connector.Error as error:
            logging.error(f"Error creating table: {error}")
    def check_table_columns_existence(self):
            try:
                with mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                ) as connection:
                    cursor = connection.cursor()

                    cursor.execute("DESCRIBE nba_players")
                    columns = cursor.fetchall()

                    required_columns = {'ppg', 'rpg', 'apg', 'pie'}
                    existing_columns = {column[0] for column in columns}

                    if not required_columns.issubset(existing_columns):
                        logging.warning("Required columns are missing in the table.")
                        self.add_columns_if_not_exist()

                    return True

            except mysql.connector.Error as error:
                logging.error(f"Error checking columns existence: {error}")
                return False
        
    def add_columns_if_not_exist(self):
        try:
            with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            ) as connection:
                cursor = connection.cursor()

                cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'nba_players'")
                existing_columns = [column[0] for column in cursor.fetchall()]

                columns_to_add = ['ppg', 'rpg', 'apg', 'pie']

                for column in columns_to_add:
                    if column not in existing_columns:
                        alter_query = f"ALTER TABLE nba_players ADD COLUMN {column} FLOAT"
                        cursor.execute(alter_query)
                        logging.info(f"Column '{column}' added successfully to 'nba_players' table.")

                connection.commit()

        except mysql.connector.Error as error:
            logging.error(f"Error adding columns: {error}")

   

    def push_profile_data_to_mysql(self, profile_data_list):
        try:
            with mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            ) as connection:
                cursor = connection.cursor()

                self.check_table_columns_existence()

                for profile_data in profile_data_list:
                    player_name = profile_data['name']
                    ppg = profile_data['ppg']
                    rpg = profile_data['rpg']
                    apg = profile_data['apg']
                    pie = profile_data['pie']

                    insert_query = """
                        INSERT INTO nba_players (full_name, first_name, last_name, href, img_src, ppg, rpg, apg, pie)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            ppg = VALUES(ppg),
                            rpg = VALUES(rpg),
                            apg = VALUES(apg),
                            pie = VALUES(pie)
                    """
                    values = (profile_data['name'], profile_data['first_name'], profile_data['last_name'],
                              profile_data['href'], profile_data['img_src'], ppg, rpg, apg, pie)

                    cursor.execute(insert_query, values)
                    connection.commit()

                    logging.info(f"Player: {player_name} - PPG: {ppg}, RPG: {rpg}, APG: {apg}, PIE: {pie} - Updated in MySQL")

        except mysql.connector.Error as error:
            logging.error(f"Error pushing profile data: {error}")

# Set up logging
logging.basicConfig(level=logging.INFO)

# Example usage:
if __name__ == "__main__":
    try:
        mysql_host = 'localhost'
        mysql_user = 'root'
        mysql_password = 'Fishboy@27!'
        mysql_database = 'nba_data'

        # Initialize PushProfileToMySQL instance
        profile_pusher = PushProfileToMySQL(mysql_host, mysql_user, mysql_password, mysql_database)

        # Create the table if it doesn't exist
        profile_pusher.create_table()

        # Initialize FetchNBA_Names_HREF instance to get player data
        nba_fetcher = FetchNBA_Names_HREF()
        page_source = nba_fetcher.get_all_players_page_source()
        player_data = nba_fetcher.get_player_data(page_source)

        if player_data:
            # Push profile data to MySQL
            result = profile_pusher.push_profile_data_to_mysql(player_data)
            logging.info(f"Pushed profiles for {len(player_data)} players to MySQL.")
        else:
            logging.warning("No player data fetched.")

    except mysql.connector.Error as error:
        logging.error(f"Error connecting to MySQL: {error}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
