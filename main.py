
from fitparse import FitFile

if __name__ == "__main__":
    fitfile = FitFile('/Users/mattrobinson/Downloads/Half_Price_Braps.fit')

    for record in fitfile.get_messages('record'):
        for record_data in record:
            if record_data.name == "heart_rate":
                print(" * {}: {} {}".format(
                    record_data.name, record_data.value, record_data.units,
                ))
