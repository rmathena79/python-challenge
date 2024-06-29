# Module 3 Challenge -- PyBank
# Roy Mathena

# Imports
import os
import csv
import logging
import sys

# Use this logger for debug prints, so they can easily be disabled without impacting the real output
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # set to logging.DEBUG to show debug prints, or logging.INFO to supress them
logger = logging.getLogger()

# Open up the data file
csv_path = os.path.join('.', 'Resources', 'budget_data.csv')
with open(csv_path, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

    # Get the header
    header = next(reader)
    logger.debug(f"Header: {header}")

    # Get the data column numbers by column name, not assuming locations, in case columns are added later
    date_idx = header.index("Date")
    delta_idx = header.index("Profit/Losses")
    logger.debug(f"Date index       : {date_idx}")
    logger.debug(f"Profit/Loss Index: {delta_idx}")

    # Process each row, updating these values as you go:
    months = [] # Using a list rather than a simple count to check for duplicates
    net_total = 0 # All the profits / losses summed together
    change_total = 0 # Each months increase/decrease relative to previous month, to calculate an average at the end
    max_delta_month = ""
    max_delta_amount = 0
    min_delta_month = ""
    max_delta_amount = 0
    previous_delta = 0
    first = True
    for row in reader:
        month = row[date_idx]
        if month in months:
            print(f"ERROR: Month \"{month}\" duplicated")
            exit()

        months.append(month)
        delta = int(row[delta_idx])

        if first:
            first = False

            logger.debug("Setting initial values")
            max_delta_month = month
            max_delta_amount = delta
            min_delta_month = month
            min_delta_amount = delta
        else:
            change_total += delta - previous_delta

            #!!! My answers don't match the provided final output
            if delta > max_delta_amount:
                logger.debug("New max: %r", row)
                max_delta_month = month
                max_delta_amount = delta
            elif delta < min_delta_amount:
                logger.debug("New min: %r", row)
                min_delta_month = month
                min_delta_amount = delta

        net_total += delta
        previous_delta = delta

    # Calculate and display final stats
    print("Financial Analysis")
    print("----------------------------")
    print(f"Total Months: {len(months)}")
    print(f"Total: ${net_total}")
    average_change = change_total / (len(months)-1)
    print(f"Average Change: ${average_change:.2f}")
    print(f"Greatest Increase in Profits: {max_delta_month} (${max_delta_amount})")
    print(f"Greatest Decrease in Profits: {min_delta_month} (${min_delta_amount})")