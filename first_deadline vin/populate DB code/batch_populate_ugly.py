import csv
import pyodbc
from tqdm import tqdm

def delete_table_contents(connection, table_name):
    try:
        # Create a cursor from the connection
        cursor = connection.cursor()

        # Execute the DELETE statement
        delete_query = f'DELETE FROM {table_name}'
        cursor.execute(delete_query)

        # Commit the transaction
        connection.commit()

        print(f'Contents of table {table_name} deleted successfully.')

    except pyodbc.Error as e:
        print(f'Error: {e}')

    finally:
        # Close the cursor (connection will be closed outside the function)
        cursor.close()
            
def populate_custody_from_csv_batch(file_path, batch_size=1000):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip the header
        next(csv_reader)
        
        rows = [(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        ) for row in csv_reader]

    # Insert rows in batches with tqdm
    with tqdm(total=len(rows), desc='Inserting into Custody table') as pbar:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            cursor.executemany('''
                INSERT INTO Custody (custody_id, participant_id, gun_id, geo_id, date_id, crime_gravity)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', batch)

            conn.commit()

            # Update the progress bar
            pbar.update(len(batch))

def populate_geography_from_csv_batch(file_path, batch_size=1000):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip the header
        next(csv_reader)
        
        rows = [(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        ) for row in csv_reader]

    # Insert rows in batches with tqdm
    with tqdm(total=len(rows), desc='Inserting into Geography table') as pbar:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            cursor.executemany('''
                INSERT INTO Geography (geo_id, latitude, longitude, city, state, continent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', batch)

            conn.commit()

            # Update the progress bar
            pbar.update(len(batch))

def populate_gun_from_csv_batch(file_path, batch_size=1000):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip the header
        next(csv_reader)
        
        rows = [(
            row[0],
            row[1],
            row[2]
        ) for row in csv_reader]

    # Insert rows in batches with tqdm
    with tqdm(total=len(rows), desc='Inserting into Gun table') as pbar:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            cursor.executemany('''
                INSERT INTO Gun (gun_id, is_stolen, gun_type)
                VALUES (?, ?, ?)
            ''', batch)

            conn.commit()

            # Update the progress bar
            pbar.update(len(batch))

def populate_date_from_csv_batch(file_path, batch_size=1000):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip the header
        next(csv_reader)
        
        rows = [(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            row[5]
        ) for row in csv_reader]

    # Insert rows in batches with tqdm
    with tqdm(total=len(rows), desc='Inserting into Date table') as pbar:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            cursor.executemany('''
                INSERT INTO Date (date_id, date, day, month, year, quarter, day_of_week)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', batch)

            conn.commit()

            # Update the progress bar
            pbar.update(len(batch))

def populate_incident_from_csv_batch(file_path, batch_size=1000):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip the header
        next(csv_reader)
        
        rows = [(
            row[0]  # Assuming the first column is the incident_id
            # Add other columns as needed
        ) for row in csv_reader]

    # Insert rows in batches with tqdm
    with tqdm(total=len(rows), desc='Inserting into Incident table') as pbar:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            cursor.executemany('''
                INSERT INTO Incident (incident_id)
                VALUES (?)
            ''', batch)

            conn.commit()

            # Update the progress bar
            pbar.update(len(batch))
            
def populate_participant_from_csv_batch(file_path, batch_size=1000):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        # Skip the header
        next(csv_reader)
        
        rows = [(
            row[0],  # Assuming the first column is the participant_id
            row[1],  # Assuming the second column is age_group
            row[2],  # Assuming the third column is gender
            row[3],  # Assuming the fourth column is status
            row[4]   # Assuming the fifth column is type
            # Add other columns as needed
        ) for row in csv_reader]

    # Insert rows in batches with tqdm
    with tqdm(total=len(rows), desc='Inserting into Participant table') as pbar:
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            cursor.executemany('''
                INSERT INTO Participant (participant_id, age_group, gender, status, type)
                VALUES (?, ?, ?, ?, ?)
            ''', batch)

            conn.commit()

            # Update the progress bar
            pbar.update(len(batch))

if __name__ == '__main__':
    
    # Connection data
    server = 'tcp:lds.di.unipi.it'
    username = 'Group_ID_183'
    password = 'TH023H6M'
    database = 'Group_ID_183_DB'

    # Connection string
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    delete_table_contents(conn, 'Geography') # Delete the contents of the table before populating it
    populate_geography_from_csv_batch('DATA/Geography.csv')

    delete_table_contents(conn, 'Gun')  # Delete the contents of the table before populating it
    populate_gun_from_csv_batch('DATA/Gun.csv')

    delete_table_contents(conn, 'Date')  # Delete the contents of the table before populating it
    populate_date_from_csv_batch('DATA/Date.csv')

    delete_table_contents(conn, 'Incident')  # Delete the contents of the table before populating it
    populate_incident_from_csv_batch('DATA/Incident.csv',)

    delete_table_contents(conn, 'Participant')  # Delete the contents of the table before populating it
    populate_participant_from_csv_batch('DATA/Partecipant.csv')

    delete_table_contents(conn, 'Custody')  # Delete the contents of the table before populating it
    populate_custody_from_csv_batch('DATA/Custody.csv')

    cursor.close()
    conn.close()