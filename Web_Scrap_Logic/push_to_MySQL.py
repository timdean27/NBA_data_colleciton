import mysql.connector
from nba_scrape import FetchNBA_Names_HREF

class Push_to_mySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_table(self):
        try:
            # Establish a connection to MySQL
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Define the SQL query to create a table
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS nba_players (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(255) NOT NULL,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    href VARCHAR(255) UNIQUE NOT NULL COLLATE utf8_general_ci,
                    img_src VARCHAR(255) NOT NULL
                )
            """

            # Execute the query
            cursor.execute(create_table_query)

            # Commit the changes
            connection.commit()

            print("Table 'nba_players' created or already exists.")

        except mysql.connector.Error as error:
            print(f"Error creating table: {error}")

        finally:
            # Close the cursor and connection
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed.")

    def push_data_to_mysql(self):
        try:
            # Create an instance of the FetchNBA_Names_HREF class
            nba_fetcher = FetchNBA_Names_HREF()

            # Fetch player data
            page_source = nba_fetcher.get_all_players_page_source()
            players = nba_fetcher.get_player_data(page_source)

            if not players:
                print("No player data fetched. Exiting data insertion.")
                return

            # Establish a connection to MySQL
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Insert player data into the MySQL table
            for player in players:
                full_name = player['name']
                first_name = player['first_name']
                last_name = player['last_name']
                href = player['href']
                img_src = player['img_src']

                # Define the SQL query to insert data into the table
                insert_query = "INSERT IGNORE INTO nba_players (full_name, first_name, last_name, href, img_src) VALUES (%s, %s, %s, %s, %s)"
                values = (full_name, first_name, last_name, href, img_src)

                try:
                    # Execute the query
                    cursor.execute(insert_query, values)

                    # Commit the changes
                    connection.commit()

                    print(f"Player '{full_name}' inserted into MySQL.")

                except mysql.connector.Error as error:
                    print(f"Error inserting player '{full_name}': {error}")

            print("Data successfully pushed to MySQL.")

        except mysql.connector.Error as error:
            print(f"Error pushing data: {error}")

        finally:
            # Close the cursor and connection
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection closed.")

if __name__ == "__main__":
    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_password = 'Fishboy@27!'
    mysql_database = 'nba_data'

    pusher = Push_to_mySQL(mysql_host, mysql_user, mysql_password, mysql_database)

    # Create the table if it doesn't exist
    pusher.create_table()

    # Push player data to MySQL
    pusher.push_data_to_mysql()
