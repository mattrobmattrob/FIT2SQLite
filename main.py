
from fitparse import FitFile
import argparse
import gzip
import shutil
from os.path import exists

# - Assumes FIT file is gzip'd.
# - Create empty database using 'sqlite3 file.db "VACUUM;"'.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit_file', type=str, required=True)
    parser.add_argument('--database', type=str, required=True)

    args = parser.parse_args()
    input_fit_file = args.fit_file
    input_database = args.database

    if not exists(input_fit_file) or not exists(input_database):
        raise Exception("'input_fit_file' and 'database' must exist")

    # Unzip 'foo.fit.gz'
    output_fit_file = input_fit_file + ".fit"
    print("Converting '{}' => '{}'".format(input_fit_file, output_fit_file))
    with gzip.open(input_fit_file, 'rb') as f_in:
        with open(output_fit_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Parse FIT file
    for record in FitFile(output_fit_file).get_messages('record'):
        def get_message_named(name):
            return ([record_data for record_data in record if record_data.name == name] or [None])[0]

        # Print types of messages for searching below.
        # for record_data in record:
        #     print(record_data.name)

        position_lat = get_message_named("position_lat").value
        position_long = get_message_named("position_long").value
        timestamp = get_message_named("timestamp").value
        heart_rate = get_message_named("heart_rate").value
        distance = get_message_named("distance").value

        print(" * {}: latlng: ({}, {}), hr: {}, distance (m): {}".format(
            timestamp, position_lat, position_long, heart_rate, distance
        ))
