# Deployed terminal is 80 characters wide and 24 rows high
# Input statements need \n (new line character) to deploy
# while using this Github template
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
    # print(" \n") included for readability
    print(
        f" Welcome to Schengen Calculator. \n"
        f" \n"
        f" Visa-exempt nationals are allowed {visa_converted} "
        f"days in a rolling period of {total_converted} days \n"
        f" on a visa waiver programme in the Schengen zone. \n"
        f" \n"
        f" Enter the dates of your recent trips below "
        f"and you will find out how much \n of your "
        f"{visa_converted} days allowance you have still have available "
        f"as of today. \n"
        f" Please note your anonymised allowance will be "
        f"added to a central database on \n completion. "
        f" \n"
        f" \n"
        f" Only trips in the last {total_converted} days are "
        f"relevant and only historic (not future) \n trips are counted here. "
        f"Your {total_converted} rolling period started on "
        f"{restricted_period_starts.strftime('%d/%m/%Y')}, \n so please enter "
        f"dates of trips between then and today's date. \n"
    )


def calculate_trip():
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
        f" \n"
        f" The first day of your trip must be after "
        f"{restricted_period_starts.strftime('%d/%m/%Y')} "
        f"and before {today}."
    )
    # input data is string, need to convert to datetime object
    # using the datetime.strptime method.

    while True:
        start_date_str = input(
            " Enter the date your trip started "
            "as dd/mm/yyyy:\n"
            )
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        except ValueError as e:
            print(
                " \n"
                " Invalid date format, try again."
                )
            continue

        if check_start_date_current(start_date):
            # print blank statement to add a blank line
            print(" ")
            break
    print(
        f" \n"
        f" The last day of your trip must be after "
        f"{start_date.strftime('%d/%m/%Y')} and before {today}."
    )

    while True:
        end_date_str = input(
            " Please enter the end date of your trip "
            "as dd/mm/yyyy: \n"
            )
        try:
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
        except ValueError as e:
            print("Invalid date format, try again.")
            continue

        if check_end_date_valid(start_date, end_date):
            # print(" ") to add a blank line for readability
            print(" ")
            break
    return (start_date, end_date)


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

    if start_date < restricted_period_starts:
        print(
            f" \n"
            f" The start date of your trip "
            f"({start_date.strftime('%d/%m/%Y')}) "
            f"is before your 180 "
            f"day period starts.  Please enter a date after "
            f"{restricted_period_starts.strftime('%d/%m/%Y')}."
        )
        return False

    if start_date > datetime.today():
        print(
            f" \n"
            f" The start date of your trip "
            f"({start_date.strftime('%d/%m/%Y')}) "
            f"is in the future."
            f" The trip period \n must be historical."
            )
        return False
    return True


def check_end_date_valid(start_date, end_date):
    """
    check user entered ends dates are after
    trip start date and before today's date.
    """
    if start_date > end_date:
        print(
            f" \n"
            f" The end date of your trip ({end_date.strftime('%d/%m/%Y')}) is "
            f"before your trip "
            f"starts.\n Please enter a date after "
            f"({start_date.strftime('%d/%m/%Y')}). "
        )
        return False

    if end_date > datetime.today():
        print(
            f" \n"
            f"The start date of your trip ({start_date.strftime('%d/%m/%Y')}) "
            f"is in the future."
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
    total_days = 0
    for start_date, end_date in trip_list:
        delta = end_date - start_date
        days_between = delta.days
        total_days += days_between
    days_remaining = visa_converted - total_days

    print(
        f" \n"
        f" Your trip was {total_days} day/s long. \n"
        f" As of today, you have {days_remaining} day/s left of your "
        f"visa waiver allowance.")

    return days_remaining


def main():
    observed_period_start()

    trip_list = []

    while True:
        trip = calculate_trip()
        trip_list.append(trip)

        another_trip = input(" Do you want to add another trip? Y/N :\n")
        if another_trip.lower() in ("y", "yes"):
            continue
        elif another_trip.lower() in ("n", "no"):
            break
        else:
            print("Invalid entry, please try Y or N ")

    days_remaining = calculate_days_left(trip_list)
    data = [days_remaining]
    worksheet_to_update = SHEET.worksheet('days_available')
    worksheet_to_update.append_row(data)
    print(
        f" \n"
        f" Your anonymised remaining allowance has been added "
        f"to the central database.\n"
    )


main()
