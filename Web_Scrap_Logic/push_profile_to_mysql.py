import mysql.connector

class PushProfileToMySQL:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def add_columns_if_not_exist(self, cursor):
        try:
            # Get existing columns from the information schema
            cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'nba_players'")
            existing_columns = [column[0] for column in cursor.fetchall()]

            # Define the columns to add
            columns_to_add = ['ppg', 'rpg', 'apg', 'pie']

            # Add missing columns
            for column in columns_to_add:
                if column not in existing_columns:
                    alter_query = f"ALTER TABLE nba_players ADD COLUMN {column} FLOAT"
                    cursor.execute(alter_query)
                    print(f"Added column '{column}' to the table 'nba_players'.")

        except mysql.connector.Error as err:
            print(f"Error adding columns: {err}")

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
            print(f"Error checking table columns: {err}")
            return False

    def push_profile_data_to_mysql(self, profile_data_list):
        # Establish a connection to MySQL
        try:
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
                ppg = profile_data.get('ppg', None)
                rpg = profile_data.get('rpg', None)
                apg = profile_data.get('apg', None)
                pie = profile_data.get('pie', None)

                # Print information about each player data being updated
                print(f"Updating data for Player: {player_name}")

                # Define the SQL query to update data in the table
                update_query = "UPDATE nba_players SET ppg = %s, rpg = %s, apg = %s, pie = %s WHERE full_name = %s"
                values = (ppg, rpg, apg, pie, player_name)

                try:
                    # Execute the query
                    cursor.execute(update_query, values)

                    # Commit the changes
                    connection.commit()

                    # Print success message
                    print(f"{player_name} - Data updated successfully in MySQL")

                except mysql.connector.Error as err:
                    print(f"Error updating data for {player_name}: {err}")

            # Close the cursor and connection
            cursor.close()
            connection.close()

        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
