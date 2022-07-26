
from fitparse import FitFile
import gzip
import shutil

if __name__ == "__main__":
    input = '/Users/mattrobinson/Downloads/6684555922.fit.gz'
    output = '/Users/mattrobinson/Downloads/6684555922.fit'

    # Unzip 'foo.fit.gz'
    with gzip.open(input, 'rb') as f_in:
        with open(output, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Parse FIT file
    for record in FitFile(output).get_messages('record'):
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
