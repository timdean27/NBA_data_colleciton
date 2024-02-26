import mysql.connector
from Push_to_MySQL import FetchNBA_Names_HREF

class Push_to_mySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_table(self):
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
        create_table_query = """
        CREATE TABLE IF NOT EXISTS nba_players (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            href VARCHAR(255) NOT NULL
        )
        """

        # Execute the query
        cursor.execute(create_table_query)

        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

    def push_data_to_mysql(self):
        # Create an instance of the FetchNBA_Names_HREF class
        nba_fetcher = FetchNBA_Names_HREF()

        # Fetch player data
        page_source = nba_fetcher.get_all_players_page_source()
        players = nba_fetcher.get_player_data(page_source)

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
            full_name = player['name'].split(' ')
            first_name = full_name[0]
            last_name = full_name[1] if len(full_name) > 1 else ''
            href = player['href']

            # Define the SQL query to insert data into the table
            insert_query = "INSERT INTO nba_players (first_name, last_name, href) VALUES (%s, %s, %s)"
            values = (first_name, last_name, href)

            # Execute the query
            cursor.execute(insert_query, values)

        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

if __name__ == "__main__":
    # Replace 'your_mysql_host', 'your_mysql_user', 'your_mysql_password', and 'your_mysql_database' with your MySQL credentials
    mysql_host = 'your_mysql_host'
    mysql_user = 'your_mysql_user'
    mysql_password = 'your_mysql_password'
    mysql_database = 'your_mysql_database'

    pusher = Push_to_mySQL(mysql_host, mysql_user, mysql_password, mysql_database)

    # Create the table if it doesn't exist
    pusher.create_table()

    # Push player data to MySQL
    pusher.push_data_to_mysql()
