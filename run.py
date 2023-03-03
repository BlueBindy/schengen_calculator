# Deployed terminal is 80 characters wide and 24 rows high
# Input statements need \n (new line character) to deploy
# while using this Github template
# Import Google Sheet class from Google module to access
# Google spreadsheet
import gspread
from google.oauth2.service_account import Credentials
# Import the class datetime, from within datetime module
# to manipulate dates
from datetime import datetime, timedelta


# SCOPE code taken from Code Institute Python Essentials Project
# Walkthrough module
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]
# Code to link to SHEET taken from Code Institute Python Essentials Project
# Walkthrough module
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('schengen_calculator')


def observed_period_start():
    """
    Get period of visa waiver days and relevant date range from sheet,
    as a list. Convert to an integer and subtract from today's date using
    datetime and timedelta classes in datetimemodule.
    Class datetime produces a datetime object, which allows operations.
    Standard datetime format (YYYY-MM-DDTHH:MM:SS. mmmmmm)
    converted to dd/mm/yyyy during print statement as
    .strftime() is a string (does not allow for operations.)
    Present user with programme instructions.

    Args:
        None

    Returns:
        Nothing
    """
    # Suggestion of timedelta module to calculate date from Steve B.
    # from StackOverflow.
    visa_period = SHEET.worksheet('visa_allowance').get_all_values()
    visa_range = visa_period[1]
    visa_converted = int(visa_range[0])

    total_period = SHEET.worksheet('restricted_period').get_all_values()
    total_range = total_period[1]
    total_converted = int(total_range[0])

    restricted_period_starts = (
        datetime.today() - timedelta(days=total_converted)
    )
    # print(' \n') included for readability
    print(
        f' Welcome to Schengen Calculator. \n'
        f' \n'
        f' Visa-exempt nationals are allowed {visa_converted} '
        f'days in a rolling period of {total_converted} days \n'
        f' on a visa waiver programme in the Schengen zone. \n'
        f' \n'
        f' Enter the dates of your recent trips below '
        f'and you will find out how much \n of your '
        f'{visa_converted} days allowance you have still have available '
        f'as of today. \n'
        f' Please note your anonymised allowance will be '
        f'added to a central database on \n completion. '
        f' \n'
        f' \n'
        f' Only trips in the last {total_converted} days are '
        f'relevant and only historic (not future) \n trips are counted here. '
        f'Your {total_converted} rolling period started on '
        f"{restricted_period_starts.strftime('%d/%m/%Y')}, \n so please enter "
        f"dates of trips between then and today's date. \n"
        f' Ensure multiple trip dates do no overlap, as this will '
        f'cause days used to be overstated and days available to be '
        f'understated.'
    )


def get_user_trip():
    """
    Get start of relevant date range from Google sheet as a list
    and convert to an integer. Subtract from today's date.
    Get start date of trip from user. Input returned as string converted
    to datetime object using .strptime. Validate for valid date, trip
    begins after restricted_period_starts and before today's date.
    Get end date of trip from user, convert to datetime object.
    Validate for valid date, trip begins after trip starts and before
    today's date. Return `start_date`, `end_date` as datetime objects.

    Args:
        none

    Returns:
        `start_date`, `end_date` (datetime objects) as a tuple
    """
    total_period = SHEET.worksheet('restricted_period').get_all_values()
    total_range = total_period[1]
    total_converted = int(total_range[0])

    restricted_period_starts = (
        datetime.today() - timedelta(days=total_converted)
    )

    today = datetime.today().strftime('%d/%m/%Y')

    print(
        f' \n'
        f' The first day of your trip must be after '
        f"{restricted_period_starts.strftime('%d/%m/%Y')} "
        f'and before {today}.'
    )
    # input data is string, need to convert to datetime object
    # using the datetime.strptime method.

    while True:
        start_date_str = input(
            ' Enter the date your trip started '
            'as dd/mm/yyyy:\n'
            )
        try:
            start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
        except ValueError as e:
            print(
                ' \n'
                ' Invalid date format, try again.'
                )
            continue

        if check_start_date_current(start_date):
            # print blank statement to add a blank line
            print(' ')
            break
    print(
        f' \n'
        f' The last day of your trip must be after '
        f"{start_date.strftime('%d/%m/%Y')} and before {today}."
    )

    while True:
        end_date_str = input(
            ' Please enter the end date of your trip '
            'as dd/mm/yyyy: \n'
            )
        try:
            end_date = datetime.strptime(end_date_str, '%d/%m/%Y')
        except ValueError as e:
            print('Invalid date format, try again.')
            continue

        if check_end_date_valid(start_date, end_date):
            # print(' ') to add a blank line for readability
            print(' ')
            break
    return (start_date, end_date)


def check_start_date_current(start_date):
    """
    Get start of relevant date range from Google sheet as a list
    and convert to an integer. Subtract from today's date.
    Check user entered start dates are after
    `restricted_period_starts` and before today's date.

    Args:
        `start_date` (datetime object); user-entered trip start date.

    Return:
        `True` if `start_date` valid (after `restricted_period_starts` and
        before `datetime.today()` (today's date))
        `False` if `start_date` invalid

    """
    # Use of operands on datetime objects suggested by Paolo Moretti,
    # StackOverflow
    total_period = SHEET.worksheet('restricted_period').get_all_values()
    total_range = total_period[1]
    total_converted = int(total_range[0])
    restricted_period_starts = (
        datetime.today() - timedelta(days=total_converted)
    )

    if start_date < restricted_period_starts:
        print(
            f' \n'
            f' The start date of your trip '
            f"({start_date.strftime('%d/%m/%Y')}) "
            f'is before your 180 '
            f'day period starts.  Please enter a date after '
            f"{restricted_period_starts.strftime('%d/%m/%Y')}."
        )
        return False

    if start_date > datetime.today():
        print(
            f' \n'
            f' The start date of your trip '
            f"({start_date.strftime('%d/%m/%Y')}) "
            f'is in the future.'
            f' The trip period \n must be historical.'
            )
        return False
    return True


def check_end_date_valid(start_date, end_date):
    """
    Check user entered ends dates are after
    trip start date and before today's date.

    Args:
        `start_date`, `end_date` (datetime objects)

    Returns:
        `True` if `end_date` after `start_date` and before `datetime.today()`
        `False` if not True
    """
    if start_date > end_date:
        print(
            f' \n'
            f" The end date of your trip ({end_date.strftime('%d/%m/%Y')}) is "
            f'before your trip '
            f'starts.\n Please enter a date after '
            f"({start_date.strftime('%d/%m/%Y')}). "
        )
        return False

    if end_date > datetime.today():
        print(
            f' \n'
            f"The end date of your trip ({end_date.strftime('%d/%m/%Y')}) "
            f'is in the future.'
            f' The trip period must be historical.'
            )
        return False
    return True


def calculate_days_left(trip_list):
    """
    Get visa waiver period from Google sheet as a list, convert to an
    integer. Subtracts total visa waiver days used from visa waiver allowance
    to calculate remaining allowance.

    Args:
        `trip_list` (list of tuples, of user-entered start date and end date)
    Returns:
        `days_remaining` (integer of `visa_converted` - `total_days`)
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
        f' \n'
        f' Your trip/s totaled {total_days} day/s long. \n'
        f' As of today, you have {days_remaining} day/s left of your '
        f'visa waiver allowance.'
        )
    return days_remaining


def main():
    """
    Call `observed_period_start()`, append trip start and end dates as tuples
    in `trip_list`. Asks users if they want to include additional trips and
    then calls function to calculate days used and days remaining and inform
    user. Days remaining appended to Google spreadsheet and user informed.

    Args:
        None

    Returns:
        Nothing
    """
    observed_period_start()

    trip_list = []

    while True:
        trip = get_user_trip()
        trip_list.append(trip)
        # use of .strip() at Brian Macharia's suggestion
        # use of .strftime on list comprehension based on Steve B.
        # suggestion, Stack Overflow
        while True:
            date_str = [
                (dt[0].strftime("%d/%m/%Y"), dt[1].strftime("%d/%m/%Y"))
                for dt in trip_list
                ]
            another_trip = input(
                f' Your current trip dates are: {date_str}. '
                f'Do you want to add another trip? Y/N :\n'
            ).lower().strip()
            if another_trip not in ('y', 'yes', 'n', 'no'):
                print('Input must be Y or N')
            else:
                break
        if another_trip in ('y', 'yes'):
            continue
        else:
            break

    days_remaining = calculate_days_left(trip_list)
    data = [days_remaining]
    worksheet_to_update = SHEET.worksheet('days_available')
    worksheet_to_update.append_row(data)
    print(
        f' \n'
        f' Your anonymised remaining allowance has been added '
        f'to the central database.\n'
    )


if __name__ == "__main__":
    main()
