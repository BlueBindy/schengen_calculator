![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome BlueBindy,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!


# Introduction to Residency-Checker  

Schengen_Calculator is a python project. The goal for the website is to allow those third country nationals who have a visa waiver access to the Schengen zone to calculate their remaining days available for the zone. Users are prompted to enter the dates of their historical trips and are given a calculation of their days remaining. The programme calculates the historical 180 day period from which their allowance is evaluated, checks that dates entered are valid dates, occur after the 180 day period starts and are before the current date. Trip end dates are validated to ensure they occur after the trip start date. 

The 90 eligible days in the rolling 180 day period (the structure of the Schenge visa waiver scheme) are retrieved from a Google spreadsheet. This allows for easy update should the scheme change. A log of calculated available days is sent to the Google spreadsheet so a typical remaining allowance can be seen.

The Schengen_Calculator is designed to be provided by a company to its employees. Employees can check their remaining allowance in the programme, and Human Resources can review the typical remaining allowance of its employees from the Google spreadsheet. 

# Demo  

<a href="https://schengen-calculator.herokuapp.com/">Click here for a live demo</a>

Several screenshots of the website can be found below illustrating the progression of the site before and after user use.


## Page on load
This screenshot is what a user will see before they have entered any data...


![Screenshot of website on page load](/docs/docs-images/screenshot-preuse.png "Website screenshot on page  load")
## Page on submit
This screenshot is taken after a user has entered sample data...

![Screenshot of website page](/docs/docs-images/screenshot.png "Website screenshot")

## Page on 404 error  
A screenshot of the page that loads when a non-existent URL is sought (the 404 error page) is found below. This page notifies the user of the error and provides a link to navigate back to the existing page. 

![Screenshot of website page](/docs/docs-images/screenshot-404.png "Website screenshot 404 error page")



# Technologies Used
Python

# UX
## User Stories
As a third country national, I want to know how many days left in the Schengen based on the trips I have already taken.

As a Human Resources manager, I want to know what the typical allowance remaining is of staff members so I can plan work accordingly.

## Strategy
The strategic aim is to create a programme that is easy to use and gives an unambiguous answer. The programme is designed to be easy to use through the automatic prevention of common errors with the use of data validation. The answer is designed to be simple by limiting it to a single, numeric response and a binary conclusion as to whether availability remains or not.  Common errors include trip start dates that are before the relevant rolling 180 day period, end dates that are before the trip start date or after the current date. These errors are met with an error warning and prompt to re-enter the data. 

## Scope
This version is designed as a minimum viable product (MVP) to assess availability based on historical trips in the Schengen. Later versions could include provision to include future trips for Schengen availability on a future date. Further, employee log-in could be added so that remaining availability (saved in Google spreadsheet) could be matched to an employee. Finally, the framework could be replicated for additional visa schemes in the rest of the world.  

## Structure
??? 

## Skeleton (insert wirefames)

Insert lucid here <br>  

![Screenshot of website page](/docs/docs-images/wireframe.png "Wireframe")<br>  



## Surface
??? 

## Features
### Features included in this current version
Users can enter their trips, by start date and end date. They are able to enter as many additional historical trips as they wish, via a prompt to select 'Add another trip? Y/N'. When they select no they are given the calculation of their availability in text form. Human Resource Managers can review the Google spreadsheet to see typical availability and update the parameters of the visa waiver scheme should that change.

![Screenshot of website page](/docs/docs-images/dates.png "Website screenshot of dates")

The user is presented with error warnings if they enter invalid data. 
![Screenshot of website page](/docs/docs-images/errormessage.png "Website screenshot of error message")



![Screenshot of website page](/docs/docs-images/results.png "Website screenshot of results")


### Features planned for later versions
Later versions will incorporate future trips, for a dynamic evaluation of planned trips. In addition, a user log-in feature is planned so that the availability sent to the Google spreadsheet can be matched to an employee for greater specificity.

# Deployment
Google API was set up via: 
https://console.cloud.google.com/ A new project ('schengencalculator') was created. From here, navigate to 'API and Services' and then 'Library' from teh memu. Using the search bar to find the Google API, it was enabled and then credentials created. The following options were selected:
Which API are you using: Google Drive API
What data will you be accessing: Application Data
Are you planning to use this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions?: 'No, I'm not using them'

Service account name is fionaschengen and the service account is:
fionaschengen@schengencalculator-377909.iam.gserviceaccount.com

From within Credentials on the menu, the service account was selected and then Keys was selected from the available menu. From here 'Add Key' -> 'Create New Key' with 'JSON' selected as key type. The file that was created and downloaded was saved into the directory as 'creds.json'. The client email account from wtihin this file was shared with the Google sheet that is linked to this programme.

Finally, from within the Library tab on the menu, Google Sheets API was searched for and enabled. 

Sensitive data in the cred.json file was withheld from being pushed to GitHub by listing in .gitignore

Two dependencies, Google-auth (needed to authenticate access to the Google cloud account for the spreadsheet) and gspread (a library), were installed using 'pip3 install gspread google-auth' in the command line and then imported into directory file: 'run.py'


Development was within a Github repository, based on the Code Institute template: https://github.com/Code-Institute-Org/python-essentials-template . Repository is: https://github.com/BlueBindy/schengen_calculator and was built using the Gitpod button on the template repository menu. 

Deployment to Heroku
Dependencies necessary for deployment to Heroku were adding by using 'pip3 freeze > requirements.txt' to terminal 

From Heroku dashboard, 'Create New App' was selected from the menu. App is called 'schengen-calculator'. In the Settings tab, a config var was set up for creds.json (which is not pushed to GitHub but is required by Heroku for deployment.) In Config Vars, for Key, 'CREDS' was entered. In Value, the contents of creds.json file was copied and pasted. An additional Key, PORT, with value 8000, was also added. 

Python and node.js were added as Buildpacks (in that order).

In the Deploy tab, GitHub was chosen and connected. Automatic deployment was selected. Then Deploy using branch: main. 

The live app, hosted by Heroku, is available at: https://schengen-calculator.herokuapp.com/

# Testing
All tests peformed on 'bluebindy.github.io/residency-checker/' on Chrome, Safari and Firefox browsers on a 13-inch early 2015 Macbook Air using MacOS Monterey v12.6.2. The exception to this is the Lighthouse accesssibility test which was performed on Chrome only.
## 1. Functionality Testing
### Test label: Pushing data to Google spreadsheet
| Test step | Outcome |
| --- | --- |
| Test action | ... |
| Expected outcome | ... |
| Notes | ...  |
| Test outcome | PASS |  


### Test label: Retrieval of visa waiver framework 
| Test step | Outcome |
| --- | --- |
| Test action | Confirm programme is retrieving Google spreadsheet data |
| Expected outcome | Y...|
| Notes | None to add |
| Test outcome | PASS |  


### Test label: Calculation of eligibility
| Test step | Outcome |
| --- | --- |
| Test action | ... |
| Expected outcome | ...|
| Notes | None to add |
| Test outcome | PASS |  


### Test label: Error message for incomplete data 
| Test step | Outcome |
| --- | --- |
| Test action |... |
| Expected outcome | ...  |
| Notes | None to add |
| Test outcome | PASS |  


### Test label: Error message for invalid data 
| Test step | Outcome |
| --- | --- |
| Test action | Enter data ... |
| Expected outcome | ... |
| Notes | None to add |
| Test outcome | PASS |  

### Test label: Deployment 
| Test step | Outcome |
| --- | --- |
| Test action | Enter data ... |
| Expected outcome | ... |
| Notes | None to add |
| Test outcome | PASS |  

### Test label: Eligibility message
| Test step | Outcome |
| --- | --- |
| Test action | Enter valid data at the prompts and select 'N' when asked to add another trip. |
| Expected outcome | On submit... |
| Notes | None to add |
| Test outcome | PASS |




### Test label: File organisation
| Test step | Outcome |
| --- | --- |
| Test action | Manually review all files and directories |
| Expected outcome | XXX |
| Notes |  |
| Test outcome | PASS |  



### Test label: Code format standardisation
| Test step | Outcome |
| --- | --- |
| Test action | Manually review all code, and all file and directory names.|
| Expected outcome | XXXX |
| Notes |  |
| Test outcome | PASS  |  


## 4. Validator Testing
### Code Institute Python Linter
| Test step | Outcome |
| --- | --- |
| Test action | Perform a Linter validation test |
| Expected outcome | Validation passed with zero flagged results (with discretion applied to code line length as appropriate.) |
| Notes | XXXXXXX |
| Test outcome | PASS |  


# Acknowledgements and Copyright
SCOPE code and code to link the programme to the Google Sheet was taken from Code Institute Python Essentials Project Walthrough module

README structure derived from the Code Institute's example. The structure and The testing approach and structure is based on advice from Brian Macharia.  

Mentoring from Brian Macharia. All errors and ommissions the responsibility of Fiona Thompson.

Content is drafted by Fiona Thompson.

ENDS

-------------------------
