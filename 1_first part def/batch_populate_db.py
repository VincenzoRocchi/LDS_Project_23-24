import csv
import pyodbc
from tqdm import tqdm

def execute_many(cursor, query, data):
    cursor.executemany(query, data)

def populate_table_from_csv_batch(cursor, table_name, file_path, batch_size):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header
        rows = [tuple(row) for row in csv_reader]

    with tqdm(total=len(rows), desc=f'Inserting into {table_name} table') as pbar:
        try:
            for i in range(0, len(rows), batch_size):
                batch = rows[i:i + batch_size]
                num_columns = len(batch[0])
                placeholders = ', '.join(['?'] * num_columns)
                execute_many(cursor, f'INSERT INTO {table_name} VALUES ({placeholders})', batch)
                pbar.update(len(batch))
        except pyodbc.Error as e:
            print(f"Error: {e}")
        finally:
            conn.commit()


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

    try:
        # Delete all data from the tables
        cursor.execute('DELETE FROM Custody')
        cursor.execute('DELETE FROM Geography')
        # cursor.execute('DELETE FROM Gun')
        # cursor.execute('DELETE FROM Date')
        # cursor.execute('DELETE FROM Incident')
        # cursor.execute('DELETE FROM Participant')

        # Populate all tables using batch inserts
        populate_table_from_csv_batch(cursor, 'Geography', r'..\DATA\Geography.csv', batch_size=10000)
        # populate_table_from_csv_batch(cursor, 'Gun', '..\DATA/Gun.csv', batch_size=10000)
        # populate_table_from_csv_batch(cursor, 'Date', '..\DATA/Date.csv', batch_size=10000)
        # populate_table_from_csv_batch(cursor, 'Incident', '..\DATA/Incident.csv', batch_size=10000)
        # populate_table_from_csv_batch(cursor, 'Participant', '..\/Participant.csv', batch_size=10000)
        populate_table_from_csv_batch(cursor, 'Custody', r'..\DATA\Custody.csv', batch_size=10000)

        # Commit once after all batches are processed
        conn.commit()

    except pyodbc.Error as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()
