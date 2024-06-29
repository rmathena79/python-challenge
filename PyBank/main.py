# Module 3 Challenge -- PyBank
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
    csv_path = os.path.join(".", "Resources", "budget_data.csv")
    report_path = os.path.join(".", "analysis", "pybank_report.txt")

    with open(csv_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        # Get the header
        header = next(reader)
        logger.debug(f"Header: {header}")

        # Get the data column numbers by column name, not assuming locations, in case columns are added later
        date_idx = header.index("Date")
        profit_idx = header.index("Profit/Losses")
        logger.debug(f"Date index       : {date_idx}")
        logger.debug(f"Profit/Loss Index: {profit_idx}")

        # Process each row, updating these values as you go:
        months = [] # Using a list rather than a simple count to check for duplicates
        net_total = 0 # All the profits / losses summed together
        delta_total = 0 # Each months increase/decrease relative to previous month, to calculate an average at the end
        max_delta_month = ""
        max_delta_amount = 0
        min_delta_month = ""
        max_delta_amount = 0
        previous_profit = 0
        
        first = True
        for row in reader:
            month = row[date_idx]
            if month in months:
                print(f"ERROR: Month \"{month}\" duplicated")
                exit()

            months.append(month)
            profit = int(row[profit_idx])

            if first:
                first = False

                logger.debug("Setting initial values")
                max_delta_month = month
                max_delta_amount = profit
                min_delta_month = month
                min_delta_amount = profit
            else:
                delta = profit - previous_profit
                delta_total += delta

                # Update biggest increase/decrease running stats
                if delta > max_delta_amount:
                    logger.debug("New max: %r", row)
                    max_delta_month = month
                    max_delta_amount = delta
                elif delta < min_delta_amount:
                    logger.debug("New min: %r", row)
                    min_delta_month = month
                    min_delta_amount = delta

            net_total += profit
            previous_profit = profit

        # Calculate final stats
        average_change = delta_total / (len(months)-1)

        # Build up report as a multi-line string
        report = "Financial Analysis\n"
        report += "----------------------------\n"
        report += f"Total Months: {len(months)}\n"
        report += f"Total: ${net_total}\n"
        report += f"Average Change: ${average_change:.2f}\n"
        report += f"Greatest Increase in Profits: {max_delta_month} (${max_delta_amount})\n"
        report += f"Greatest Decrease in Profits: {min_delta_month} (${min_delta_amount})\n"

        # Write that report to stdout and a text file
        print(report)
        with open(report_path, "w") as report_file:
            report_file.write(report)

if __name__ == "__main__":
    main()