from pydub import AudioSegment
import os

def timestamp_to_miliseconds(timestamp):

    """
    INPUT: A timestamp string like '4:34' or 7:21.464' 
    OUTPUT: The input timestamp as miliseconds from the start
    """

    hours, minutes, seconds = (["0", "0"] + timestamp.split(":"))[-3:]
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)
    miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)

    return miliseconds

INPUT = {
    "a.mp3": {
        "test": ("00:10", "00:20")
    },

    # "Owl City - Live from Atlanta.mp3": {

    #     "1 - Intro": ("00:00", "00:27"),
    #     "2 - Umbrella Beach": ("00:27", "05:40"),
    #     "3 - Dental Care": ("05:40", "08:59"),
    #     "4 - Dear Vienna": ("08:59", "13:33"),
    #     "5 - Fuzzy Blue Lights": ("13:33", "18:10"),
    #     "6 - Cave In": ("18:10", "22:56"),
    #     "7 - The Bird and The Worm": ("22:56", "26:38"),
    #     "8 - The Tip of the Iceberg": ("26:38", "30:00"),
    #     "9 - This is the Future": ("30:00", "33:12"),
    #     "10 - Air Traffic": ("33:12", "37:39"),
    #     "11 - An Enchanted Evening": ("37:39", "39:32"),
    #     "12 - Meteor Shower": ("39:32", "42:08"),
    #     "13 - The Saltwater Room": ("42:08", "43:21"),
    #     "14 - The Technicolor Phase": ("43:21", "48:23"),
    #     "15 - Hot Air Balloon": ("48:23", "52:09"),
    #     "16 - Hello Seattle": ("52:09", "55:46"),
    #     "17 - Fireflies": ("55:46", "1:01:55"),
    #     "18 - On The Wing": ("1:01:55", "1:06:54"),

    # }, 

    # "Owl City - Live from London.mp3" :{

    #     "Umbrealla Beach": ("00:00", "06:01"),
    #     "The Bird and the Worm": ("06:01", "09:36"),
    #     "Air Traffic": ("09:36", "13:51"),
    #     "On The Wing": ("13:51", "18:58"),
    #     "Hot Air Balloon": ("18:58", "22:42"),
    #     "Dear Vienna": ("22:42", "27:07"),
    #     "Fuzzy Blue Lights": ("27:07", "31:45"),
    #     "Cave In": ("31:45", "36:20"),
    #     "An Enchanted Evening": ("36:20", "38:12"),
    #     "This is the Future": ("38:12", "41:30"),
    #     "Dental Care": ("41:30", "44:53"),
    #     "The Saltwater Room": ("44:53", "46:06"),
    #     "The Technicolor Phase": ("46:06", "51:01"),
    #     "Fireflies": ("51:01", "54:48"),
    #     "Meteor Shower": ("54:48", "58:55"),
    #     "Vanilla Twilight": ("58:55", "1:03:29"),
    #     "The Tip of the Iceberg": ("1:03:29", "1:08:15"),
    #     "Hello Seattle": ("1:08:15", "1:11:49"),
    # },

    "Owl City - Live from California (BVTV).mp3" : {
        
        "In The Dolphin Tank": ("00:00", "02:11"),
        "Hello Seattle (Remix)": ("02:11", "05:40"),
        "On The Wing": ("05:40", "10:10"),
        "Fuzzy Blue Lights": ("10:10", "15:08"),
        "Strawberry Avalanche": ("15:08", "18:22"),
        "Dear Vienna": ("18:22", "22:10"),
        "Hello Seattle": ("22:10", "27:00"),

    }
}

# print(timestamp_to_miliseconds("1:20:31"))

for input_filename, segments in INPUT.items():
    # input file is the parent file that is being sliced
    print("Processing: ", input_filename, end="")
    input_file = AudioSegment.from_mp3(input_filename)
    print(" ...done!")
    # all the segments will be saved in a folder of the input file, in the same directory
    output_path = "./" + input_filename.split(".")[0]
    os.makedirs(output_path, exist_ok=True)
    # iterating through the segments we want to cut out
    for segment_name, portion_ms in segments.items():
        # the start and end markings are in milliseconds
        segment_start, segment_end = timestamp_to_miliseconds(portion_ms[0]), timestamp_to_miliseconds(portion_ms[1])
        segmented = input_file[segment_start: segment_end]

        # writing the segment to a file with the alloted name
        segmented.export(os.path.join(output_path, segment_name + ".mp3"), format="mp3")

        print("Exported: ", segment_name)