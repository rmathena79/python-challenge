# Module 3 Challenge -- PyPoll
# Roy Mathena

# Imports
import os
import csv
import logging
import sys

# Use this logger for debug prints, so they can easily be disabled without impacting the real output
logging.basicConfig(stream=sys.stdout, level=logging.INFO) # set to logging.DEBUG to show debug prints, or logging.INFO to supress them
logger = logging.getLogger()

def main():
    # Open up the data file
    csv_path = os.path.join(".", "Resources", "election_data.csv")
    report_path = os.path.join(".", "analysis", "pypoll_report.txt")

    with open(csv_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        # Get the header
        header = next(reader)
        logger.debug(f"Header: {header}")

        # Get the data column by column name, not assuming locations, in case columns are added later
        candidate_idx = header.index("Candidate")
        logger.debug(f"Candidate index: {candidate_idx}")

        # Process each row, updating these values as you go:
        counts_dict = {}
        total_votes = 0
        for row in reader:
            name = row[candidate_idx]
            
            if not name in counts_dict.keys():
                logger.debug(f"New candidate: {row}")
                counts_dict[name] = 1
            else:
                # Increase vote count for existing candidate
                counts_dict[name] += 1

            total_votes += 1

        # Dump the accumlated data to debug output
        logger.debug(f"Results: {counts_dict}")

        # Start building up report as a multi-line string
        report = "Election Results\n"
        report += "-------------------------\n"
        report += f"Total Votes: {total_votes}\n"
        report += "-------------------------\n"

        # Figure out and report each candidate's results, and find the overall winner
        winner_name = ""
        winner_count = 0
        for name in counts_dict.keys():
            count = counts_dict[name]
            percent = count / total_votes
            report += f"{name}: {percent:.3%} ({count})\n"

            if count > winner_count:
                winner_name = name
                winner_count = count

        # Final report item: overall winner
        report += "-------------------------\n"
        report += f"Winner: {winner_name}\n"
        report += "-------------------------\n"

        # Write that report to stdout and a text file
        print(report)
        with open(report_path, "w") as report_file:
            report_file.write(report)

if __name__ == "__main__":
    main()