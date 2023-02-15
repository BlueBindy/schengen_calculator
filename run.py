# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials

#SCOPE code taken from Code Institute Python Essentials Project Walthrough module
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
#Code to link to SHEET taken from Code Institute Python Essentials Project Walthrough module
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS= CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('schengen_calculator')

#remove pprint before deployment
#input statements need \n (new line character) to deploy
#using this Github template

print('Welcome to 90 Days in 180. Enter the dates of your recent trips to find out how much of your 90 days of tourist allowance in the past 180days you have still available as of today. Only trips in the last 180 days are relevant and only historic trips (not future) are counted here.')
