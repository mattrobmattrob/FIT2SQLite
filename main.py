
from dis import dis
from fitparse import FitFile
import argparse
import glob
import gzip
import shutil
import sqlite3
import os

# - Assumes FIT file is gzip'd.
# - Create empty database using 'sqlite3 file.db "VACUUM;"'.

def decompress_fit_gz(input_fit_file):
    output_fit_file = input_fit_file + ".fit"
    print("Converting '{}' => '{}'".format(input_fit_file, output_fit_file))
    with gzip.open(input_fit_file, 'rb') as f_in:
        with open(output_fit_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return output_fit_file

def create_table():
    db_connection = sqlite3.connect(input_database)
    db_cursor = db_connection.cursor()
    db_connection.execute('''CREATE TABLE IF NOT EXISTS activities (file_id, timestamp text, lat text, long text, heart_rate real, distance real)''')
    return (db_connection, db_cursor)

def parse_fit_file(fit_file_path, db_connection, db_cursor):
    input_file_id = os.path.basename(fit_file_path).split('/')[-1].split('.fit')[0]
    fit_file =  FitFile(fit_file_path)
    for record in fit_file.get_messages('record'):
        def get_message_named(name):
            message = ([record_data for record_data in record if record_data.name == name] or [None])[0]
            return message.value if message else None

        # Print types of messages for searching below.
        # for record_data in record:
        #     print(record_data.name)

        timestamp = get_message_named("timestamp")
        position_lat = get_message_named("position_lat")
        position_long = get_message_named("position_long")
        heart_rate = get_message_named("heart_rate")
        distance = get_message_named("distance")

        print(" * {}: timestamp: {}, latlng: ({}, {}), hr: {}, distance (m): {}".format(
            input_file_id, timestamp, position_lat, position_long, heart_rate, distance
        ))

        # Run the SQL insertion
        data_insert = """INSERT INTO activities
                            (file_id, timestamp, lat, long, heart_rate, distance)
                            VALUES (?, ?, ?, ?, ?, ?);"""
        data_tuple = (input_file_id, timestamp, position_lat, position_long, heart_rate, distance)
        db_cursor.execute(data_insert, data_tuple)

    # Commit the INSERTs
    db_connection.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit_file_dir', type=str, required=True)
    parser.add_argument('--database', type=str, required=True)

    args = parser.parse_args()
    input_fit_file_dir = args.fit_file_dir
    input_database = args.database
    if not os.path.exists(input_fit_file_dir) or not os.path.exists(input_database):
        raise Exception("'input_fit_file' and 'database' must exist")

    for fit_file in glob.glob(input_fit_file_dir + '/*.fit.gz'):
        print("Processing '{}'".format(fit_file))
        output_fit_file = decompress_fit_gz(fit_file)
        db_connection, db_cursor = create_table()
        parse_fit_file(output_fit_file, db_connection, db_cursor)
