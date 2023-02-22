# Write your code to expect a terminal of 80 characters wide and 24 rows high
# Import Google Sheet class from Google module
import gspread
from google.oauth2.service_account import Credentials
# Import the class datetime, from within datetime module
from datetime import datetime, timedelta


# SCOPE code taken from Code Institute Python Essentials Project
# Walkthrough module
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
# Code to link to SHEET taken from Code Institute Python Essentials Project
# Walkthrough module
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('schengen_calculator')

# remove pprint before deployment
# input statements need \n (new line character) to deploy
# using this Github template

# print('Welcome to 90 Days in 180. Enter the dates of your recent trips to
# find out how much of your 90 days of tourist allowance in the past 180days
# you have still available as of today. Only trips in the last 180 days are
# relevant and only historic trips (not future) are counted here.')


def observed_period_start():
    """
    Get period of restricted travel from sheet as a list, convert to an
    integer and subtract from today's date using datetime and timedelta
    classes in datetimemodule. Class datetime returns a datetime object,
    which allows operations like subtraction to be calculated. Standard
    datetime format (YYYY-MM-DDTHH:MM:SS. mmmmmm) converted to dd/mm/yyyy
    during print statement as .strftime() returns a string which does
    not allow for operations. Suggestion of timedelta module to calculate
    date from Steve B. from StackOverflow.
    """
    visa_period = SHEET.worksheet('visa_allowance').get_all_values()
    visa_range = visa_period[1]
    visa_converted = int(visa_range[0])

    total_period = SHEET.worksheet('restricted_period').get_all_values()
    total_range = total_period[1]
    total_converted = int(total_range[0])

    restricted_period_starts = (
        datetime.today() - timedelta(days=total_converted)
    )

    print(
        f"Welcome to Schengen Calculator. \n" 
        f"Visa-exempt nationals are allowed {visa_converted} "
        f"days in a rolling period of {total_converted} days \n"
        f"on a visa waiver programme. \n" 
        f"Enter the dates of your recent trips below "
        f"and you will find out how much \n of your "
        f"{visa_converted} days allowance you have still have available "
        f"as of today. \n" 
        f"Only trips in the last {total_converted} days are  "
        f"relevant and only historic (not future) \ntrips are counted here. \n"
        f"Your {total_converted} rolling period started on "
        f"{restricted_period_starts.strftime('%d/%m/%Y')}, so only enter "
        f"dates of trips \nfrom that period onwards, up until today's date. \n"
    )


def calculate_trips():
    """
    Get start date of trip from user. Validate for valid date, trip
    begins after restricted_period_starts and before today's date.
    Get end date of trip from user. Validate for valid date, trip
    begins after trip starts and before today's date. Append trip to
    variable and ask user for another trip or to calculate.
    """
    total_period = SHEET.worksheet('restricted_period').get_all_values()
    total_range = total_period[1]
    total_converted = int(total_range[0])

    restricted_period_starts = (
        datetime.today() - timedelta(days=total_converted)
    )

    today = datetime.today().strftime('%d/%m/%Y')

    print(
        f"The first day of your trip must be after "
        f"{restricted_period_starts.strftime('%d/%m/%Y')} "
        f"and before {today}."
    )
    # note data is string, need to convert to datetime object
    # using the datetime.strptime method.
    trip_list = []
    start_date = input("Enter the date your trip started as dd/mm/yyyy:\n")
    if validate_dates(start_date):
        if check_start_date_current(start_date):
            # print blank statement to add a blank line
            print(" ")
        else:
            return
    else:
        return

    print(
        f"The last day of your trip must be after {start_date} "
        f"and before {today}."
    )
    end_date = input("Please enter the end date of your trip as dd/mm/yyyy: \n")
    if validate_dates(end_date):
        if check_end_date_valid(start_date, end_date):
            # print blank statement to add a blank line
            print(" ")
        else:
            return
    else:
        return

    trip_list.append((start_date, end_date))

    def ask_another_trip(trip_list):
        while True:
            another_trip = input("Do you want to add another trip? Y/N :\n")
            if another_trip == ("n"):
                calculate_days_left(trip_list)
                break
            else:
                calculate_trips(trip_list)
    ask_another_trip(trip_list)

    # print(trip_list)
    return trip_list


def validate_dates(dates):
    """
    validate dates
    """
    try:
        date = datetime.strptime(dates, "%d/%m/%Y")
    # ValueError code based on Code Institute Walkthrough Project
    # Find out how to change error message to user friendly language
    except ValueError as e:
        print(f"Invalid dates: {e}, please try again.\n")
        return False
    return True


def check_start_date_current(start_date):
    """
    check user entered start dates are after
    restricted_period_starts and before today's date.
    """
    # Use of operands on dates suggested by Paolo Moretti, StackOverflow
    total_period = SHEET.worksheet('restricted_period').get_all_values()
    total_range = total_period[1]
    total_converted = int(total_range[0])
    restricted_period_starts = (
        datetime.today() - timedelta(days=total_converted)
    )
    trips_date = datetime.strptime(start_date, '%d/%m/%Y')

    if trips_date < restricted_period_starts:
        print(
            f"The start date of your trip ({start_date}) is before your 180 "
            f"day period starts. Please enter a date after "
            f"{restricted_period_starts.strftime('%d/%m/%Y')}."
        )
        return False

    if trips_date > datetime.today():
        print(
            f"The start date of your trip ({start_date}) is in the future."
            f" The trip period must be historical."
            )
        return False

    return True


def check_end_date_valid(start_date, end_date):
    """
    check user entered ends dates are after
    trip start date and before today's date.
    """
    end_date_converted = datetime.strptime(end_date, '%d/%m/%Y')
    if start_date < end_date:
        print(
            f"The end date of your trip ({end_date}) is before your trip "
            f"starts. Please enter a date after ({start_date}). "
        )
        return False

    if end_date_converted > datetime.today():
        print(
            f"The start date of your trip ({start_date}) is in the future."
            f" The trip period must be historical."
            )
        return False

    return True


def calculate_days_left(trip_list):
    """
    Function to calculate the days between user entered trips.
    Returns string of days.
    """
    visa_period = SHEET.worksheet('visa_allowance').get_all_values()
    visa_range = visa_period[1]
    visa_converted = int(visa_range[0])
    for start_date_str, end_date_str in trip_list:
        start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        delta = end_date - start_date
        days_between = delta.days
    days_remaining = visa_converted - days_between
    print(
        f"Your trip was {days_between} days long. \n"
        f"As of today, you have {days_remaining} days left on your "
        f"visa waiver allowance.")


def main():
    observed_period_start()
    calculate_trips()


main()

# next step: ask user for another trip or calculate
# next step2: calculate and give user a response
# next step3: push remaining allowance to gsheet.


# get today's date and convert to dd/mm/yyyy
# Returns the current local date as a string from datetime module import
# using strftime to format as dd/mm/yyyyy.
# today = datetime.today().strftime('%d/%m/%Y')
# restricted_period_starts.strftime('%d/%m/%Y'))
