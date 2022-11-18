"""haakon8855, forked from AxelFl/CSTimer-Total"""

import glob
import json
import math
import sys

total_solves = 0
total_time_ms = 0

# This is where the stats of individual sessions will go
session_stats = []

# Finds all .txt files and if only 1 is present save that file name, else exit the program
file_names = glob.glob("*.txt")
if len(file_names) != 1:
    print("Please have 1 .txt file in this directory")
    sys.exit()
else:
    file_name = file_names[0]

# Loads the found file
with open(file_name, "r", encoding="utf-8") as file:
    text = file.read()

# Make read string into a JSON file, if it is an invalid file,
# ask the user for a good file and exit the program
try:
    json_file = json.loads(text)
except json.JSONDecodeError:
    print("Please supply a valid CSTimer file")
    sys.exit()

# Go through all the sessions in the file,
# Range should be + 1 to reach the last one, because it is not inclusive
# But since we have an extra object with session no modification is required
for session_nr in range(1, len(json_file)):
    session = json_file[f"session{session_nr}"]

    # First index is time and second is number of solves
    # Third is the name of the session which will be filled in later
    session_stats.append([0, 0, None])

    for solve in session:
        total_solves += 1
        session_stats[session_nr - 1][1] += 1

        # Get the time in milliseconds
        time_ms = solve[0][1]

        total_time_ms += time_ms

        # Add the time to that sessions stats
        session_stats[session_nr - 1][0] += time_ms

# Load cstimer properties
properties = json_file["properties"]
# Load session metadata
# json.loads() is needed once again due to contents of properties["sessionData"]
# being a string of json-encoded data.
session_data = json.loads(properties["sessionData"])
# For all the session add the sessions name to session_stats
for session_nr in range(1, len(session_data) + 1):
    current_session = session_data[str(session_nr)]
    session_name = current_session["name"]
    session_stats[session_nr - 1][2] = session_name


def get_time(millis):
    """
    Calculate the time in hours, minutes and seconds
    Returns a tuple with the times (hrs, mins, secs)
    """
    # Everything gets floored because it gets covered by the lower unit
    # Seconds are so small and just gets rounded anyways
    # First and second is obvious
    seconds = millis / 1000
    hours = math.floor(seconds / 3600)
    # Gives me total minutes mod 60 because the rest are taken by hours
    minutes = math.floor((seconds / 60) % 60)
    # Takes the number of seconds mod 60 because of the minutes
    seconds = round(seconds % 60)
    return hours, minutes, seconds


# Find the most used session in time
highest_time = 0
for session in session_stats:
    if session[0] > highest_time:
        most_used_time = session
        highest_time = session[0]

# Find the most used session in number of solves
highest_solves = 0
for session in session_stats:
    if session[1] > highest_solves:
        most_used_solves = session
        highest_solves = session[1]

# Print out all the special statistics at the end
total_time = get_time(total_time_ms)
print(
    f"You have spent a total of {total_time[0]} hours, " +
    f"{total_time[1]} minutes and {total_time[2]} seconds of solving in CSTimer"
)
print(f"With a total of {total_solves} solves")

# Only print hours if it is greater than zero, same for minutes
avg_time = get_time((total_time_ms / total_solves))
if avg_time[0] > 0:
    print(
        f"Average time: {avg_time[0]} hours, {avg_time[1]} minutes and {avg_time[2]} seconds"
    )
elif avg_time[1] > 0:
    print(f"Average time: {avg_time[1]} minutes and {avg_time[2]} seconds")
else:
    print(f"Average time: {avg_time[2]} seconds")

print(
    f"\nThe session you have spent the most time solving with is {most_used_time[2]}"
)
longest_session = get_time(most_used_time[0])
print(f"In that session you spent a total of {longest_session[0]} hours, " +
      f"{longest_session[1]} minutes and {longest_session[2]} seconds")
print(f"With a total of {most_used_time[1]} solves")

# Only print hours if it is greater than zero, same for minutes
avg_time = get_time(most_used_time[0] / most_used_time[1])
if avg_time[0] > 0:
    print(
        f"Average time: {avg_time[0]} hours, {avg_time[1]} minutes and {avg_time[2]} seconds"
    )
elif avg_time[1] > 0:
    print(f"Average time: {avg_time[1]} minutes and {avg_time[2]} seconds")
else:
    print(f"Average time: {avg_time[2]} seconds")

print(f"\nThe session you have the most solves with is {most_used_solves[2]}")
most_solves = get_time(most_used_solves[0])
print(f"In that session you spent a total of {most_solves[0]} hours, " +
      f"{most_solves[1]} minutes and {most_solves[2]} seconds")
print(f"With a total of {most_used_solves[1]} solves")

# Only print hours if it is greater than zero, same for minutes
avg_time = get_time(most_used_solves[0] / most_used_solves[1])
if avg_time[0] > 0:
    print(
        f"Average time: {avg_time[0]} hours, {avg_time[1]} minutes and {avg_time[2]} seconds"
    )
elif avg_time[1] > 0:
    print(f"Average time: {avg_time[1]} minutes and {avg_time[2]} seconds")
else:
    print(f"Average time: {avg_time[2]} seconds")

# Prints out all of the stats at the end
for session in session_stats:
    print("\n" + str(session[2]))
    time = get_time(session[0])
    print(f"{time[0]} hours, {time[1]} minutes and {time[2]} seconds")
    print(f"{session[1]} solves")
    # If there are no solves, there is no average
    if not session[1]:
        continue
    avg_time = get_time(session[0] / session[1])
    if avg_time[0] > 0:
        print(
            f"Average time: {avg_time[0]} hours, {avg_time[1]} minutes and {avg_time[2]} seconds"
        )
    elif avg_time[1] > 0:
        print(f"Average time: {avg_time[1]} minutes and {avg_time[2]} seconds")
    else:
        print(f"Average time: {avg_time[2]} seconds")
