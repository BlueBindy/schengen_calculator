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


Deployment
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

Acknowledgements
SCOPE code and code to link the programme to the Google Sheet was taken from Code Institute Python Essentials Project Walthrough module