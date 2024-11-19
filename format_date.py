from datetime import datetime

# List of dates in various formats
# dates = ["July 23, 2024", "Nov 04, 2024", "2024-11-17", "6 November 2024", "Oct 10, 2024", "11/21/2024"]

def get_formatted_dates(dates):
    # Define the desired output format
    output_format = "%Y-%m-%d"  # Example: '2024-07-23'

    # Convert dates to the desired format
    standardized_dates = []
    for date_str in dates:
        for format in ("%B %d, %Y", "%b %d, %Y", "%Y-%m-%d", "%d %B %Y", "%m/%d/%Y"):
            try:
                parsed_date = datetime.strptime(date_str, format)
                standardized_dates.append(parsed_date.strftime(output_format))
                break
            except ValueError:
                continue
        else:
            print(f"Date format not recognized: {date_str}")

    # Print standardized dates
    print(standardized_dates)
    return standardized_dates

# get_formatted_dates(dates)