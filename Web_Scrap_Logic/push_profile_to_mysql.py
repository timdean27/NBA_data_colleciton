# push_profile_to_mysql.py
import mysql.connector

class PushProfileToMySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def add_columns_if_not_exist(self, cursor):
        # Get existing columns from the information schema
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'nba_players'")
        existing_columns = [column[0] for column in cursor.fetchall()]

        # Define the columns to add
        columns_to_add = ['ppg', 'rpg', 'apg', 'pie']

        # Add missing columns
        for column in columns_to_add:
            if column not in existing_columns:
                alter_query = f"ALTER TABLE nba_players ADD COLUMN {column} INT"
                cursor.execute(alter_query)

    def check_table_columns_existence(self, cursor):
        try:
            # Execute a query to check if the table and columns exist
            cursor.execute("DESCRIBE nba_players")

            # Fetch all the results
            columns = cursor.fetchall()

            # Check if the required columns exist
            required_columns = {'ppg', 'rpg', 'apg', 'pie'}
            existing_columns = {column[0] for column in columns}

            if not required_columns.issubset(existing_columns):
                print("Required columns are missing in the table.")
                return False

            return True

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def push_profile_data_to_mysql(self, profile_data_list):
        # Establish a connection to MySQL
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Add columns if they do not exist
        self.add_columns_if_not_exist(cursor)

        # Check if the required columns exist
        if not self.check_table_columns_existence(cursor):
            # Close the cursor and connection
            cursor.close()
            connection.close()
            return

        # Insert player profile data into the MySQL table
        for profile_data in profile_data_list:
            player_name = profile_data['name']
            ppg = profile_data['ppg']
            rpg = profile_data['rpg']
            apg = profile_data['apg']
            pie = profile_data['pie']

            print(f"Player: {player_name}, PPG: {ppg}, RPG: {rpg}, APG: {apg}, PIE: {pie}")

            # Define the SQL query to insert data into the table
            insert_query = "UPDATE nba_players SET ppg = %s, rpg = %s, apg = %s, pie = %s WHERE full_name = %s"
            values = (ppg, rpg, apg, pie, player_name)

            try:
                # Execute the query
                cursor.execute(insert_query, values)

                # Commit the changes
                connection.commit()

                # Print information for each player
                print(f"{player_name} - PPG: {ppg}, RPG: {rpg}, APG: {apg} - Updated in MySQL with comment: Custom comment here")

            except mysql.connector.Error as err:
                print(f"Error updating data: {err}")

        # Close the cursor and connection
        cursor.close()
        connection.close()
