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

    print(restricted_period_starts.strftime('%d/%m/%Y'))
    print(
        f"Welcome to Schengen Calculator. Visa-exempt nationals are allowed "
        f"{visa_converted} days in a rolling period of {total_converted} days "
        f"on a visa waiver programme. Below, you can enter the dates of your "
        f"recent trips. You will find out how much of your {visa_converted} "
        f"days allowance you have still have available as of today. Only "
        f"trips in the last {total_converted} days are relevant and only "
        f"historic (not future) are counted here. \n"
        f"Your {total_converted} rolling period started on "
        f"{restricted_period_starts.strftime('%d/%m/%Y')}, so only enter "
        f"dates of trips from that period onwards, up until today's date."
    )


observed_period_start()

# get today's date and convert to dd/mm/yyyy
# Returns the current local date as a string from datetime module import
# using strftime to format as dd/mm/yyyyy.
# today = datetime.today().strftime('%d/%m/%Y')

