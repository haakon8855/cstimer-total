"""haakon8855, forked from AxelFl/CSTimer-Total"""

import glob
import json
import math
import sys


class CSTimerStats:
    """
    Calculate stats for time usage in csTimer.
    """
    def __init__(self, file_name: str):
        self.total_solves = 0
        self.total_time_ms = 0
        # List to store stats of individual sessions
        self.session_stats = []
        self.file_name = file_name
        self.json_data: dict = None

    @staticmethod
    def get_filename() -> str:
        """
        Finds all .txt files and if only 1 is present save that file name,
        else exit the program
        """
        file_names = glob.glob("*.txt")
        if len(file_names) != 1:
            print("Please have 1 .txt file in this directory")
            sys.exit()
        return file_names[0]

    @staticmethod
    def read_file(file_name: str) -> str:
        """
        Loads the found file
        """
        with open(file_name, "r", encoding="utf-8") as file:
            text = file.read()
        return text

    @staticmethod
    def get_time(millis: int) -> tuple[int, int, int]:
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

    @staticmethod
    def get_average_stats(avg_time: tuple[int, int, int]) -> str:
        """
        Returns a string presenting the given time as average time.
        (Used in multiple places)
        """
        outstring = ""
        if avg_time[0] > 0:
            outstring += f"\nAverage time: {avg_time[0]} hours, "
            outstring += f"{avg_time[1]} minutes and {avg_time[2]} seconds"
        elif avg_time[1] > 0:
            outstring += f"\nAverage time: {avg_time[1]} minutes and {avg_time[2]} seconds"
        else:
            outstring += f"\nAverage time: {avg_time[2]} seconds"
        return outstring

    def load_json(self) -> None:
        """
        Make read string into a JSON file, if it is an invalid file,
        ask the user for a good file and exit the program
        """
        text = CSTimerStats.read_file(self.file_name)
        try:
            self.json_data = json.loads(text)
        except json.JSONDecodeError:
            print("Please supply a valid CSTimer file")
            sys.exit()

    def load_session_stats(self) -> None:
        """
        Loads session metadata from all sessions present in the loaded json data.
        """
        for session_nr in range(1, len(self.json_data)):
            session = self.json_data[f"session{session_nr}"]

            # session stats format: [total_time, number_of_solves, session_name]
            self.session_stats.append([0, 0, None])

            for solve in session:
                self.total_solves += 1
                self.session_stats[session_nr - 1][1] += 1
                # Get the time in milliseconds
                time_ms = solve[0][1]
                self.total_time_ms += time_ms
                # Add the time to that sessions stats
                self.session_stats[session_nr - 1][0] += time_ms
        self.load_session_names()

    def load_session_names(self) -> None:
        """
        Loads session names and adds to previously added session metadata.
        """
        # Load cstimer properties
        properties = self.json_data["properties"]
        # Load session metadata
        # json.loads() is needed once again due to contents of properties["sessionData"]
        # being a string of json-encoded data.
        session_data = json.loads(properties["sessionData"])
        # For all the session add the sessions name to session_stats
        for session_nr in range(1, len(session_data) + 1):
            current_session = session_data[str(session_nr)]
            session_name = current_session["name"]
            self.session_stats[session_nr - 1][2] = session_name

    def get_stats(self) -> str:
        """
        Returns a string presenting time usage stats for the loaded csTimer json data.
        """
        if len(self.session_stats) == 0:
            self.load_json()
            self.load_session_stats()
        outstring = self.get_total_stats()
        outstring += self.get_most_time_session_stats()
        outstring += self.get_most_solves_session_stats()
        outstring += self.get_individual_sessions_stats()
        return outstring

    def get_total_stats(self) -> str:
        """
        Returns a string presenting the stats from the loaded cstimer json data.
        """
        outstring = "\n============================================================"
        total_time = CSTimerStats.get_time(self.total_time_ms)
        outstring += f"\nYou have spent a total of {total_time[0]} hours, "
        outstring += f"{total_time[1]} minutes and {total_time[2]} seconds of solving in CSTimer"
        outstring += f"\nWith a total of {self.total_solves} solves"

        # Only print hours if it is greater than zero, same for minutes
        avg_time = CSTimerStats.get_time(
            (self.total_time_ms / self.total_solves))
        outstring += CSTimerStats.get_average_stats(avg_time)
        return outstring

    def get_most_time_session_stats(self) -> str:
        """
        Return a string of stats for the session with longest total time.
        """
        highest_time = 0
        for session in self.session_stats:
            if session[0] > highest_time:
                most_used_time = session
                highest_time = session[0]

        outstring = ""
        outstring += "\n\nThe session you have spent the most time "
        outstring += f"solving with is {most_used_time[2]}"

        longest_session = CSTimerStats.get_time(most_used_time[0])
        outstring += f"\nIn that session you spent a total of {longest_session[0]} hours, "
        outstring += f"{longest_session[1]} minutes and {longest_session[2]} seconds"
        outstring += f"\nWith a total of {most_used_time[1]} solves"

        # Only print hours if it is greater than zero, same for minutes
        avg_time = CSTimerStats.get_time(most_used_time[0] / most_used_time[1])
        outstring += CSTimerStats.get_average_stats(avg_time)
        return outstring

    def get_most_solves_session_stats(self) -> str:
        """
        Return a string of stats for the session with most amount of solves.
        """
        highest_solves = 0
        for session in self.session_stats:
            if session[1] > highest_solves:
                most_used_solves = session
                highest_solves = session[1]

        outstring = ""
        outstring += f"\n\nThe session you have the most solves with is {most_used_solves[2]}"
        most_solves = CSTimerStats.get_time(most_used_solves[0])
        outstring += f"\nIn that session you spent a total of {most_solves[0]} hours, "
        outstring += f"{most_solves[1]} minutes and {most_solves[2]} seconds"
        outstring += f"\nWith a total of {most_used_solves[1]} solves"

        # Only print hours if it is greater than zero, same for minutes
        avg_time = CSTimerStats.get_time(most_used_solves[0] /
                                         most_used_solves[1])
        outstring += CSTimerStats.get_average_stats(avg_time)
        return outstring

    def get_individual_sessions_stats(self) -> str:
        """
        Returns a string of stats presenting stats for all sessions.
        """
        outstring = "\n"
        for session in self.session_stats:
            outstring += "\n\n" + str(session[2])
            time = CSTimerStats.get_time(session[0])
            outstring += f"\n{time[0]} hours, {time[1]} minutes and {time[2]} seconds"
            outstring += f"\n{session[1]} solves"
            # If there are no solves, there is no average
            if not session[1]:
                continue
            avg_time = CSTimerStats.get_time(session[0] / session[1])
            outstring += CSTimerStats.get_average_stats(avg_time)
        return outstring

    def __str__(self) -> str:
        return self.get_stats()


def main() -> None:
    """
    Calculate time usage stats for csTimer.
    """
    timer_stats = CSTimerStats(CSTimerStats.get_filename())
    print(timer_stats)


if __name__ == "__main__":
    main()
