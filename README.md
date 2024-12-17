# Flask Record Management App 
## CS50 2024 Final Project
### Video Demo: https://youtu.be/oiENXPdaf6k
### Description: Digitization of Office letters and Record Management System

In the erra of Artificial intelligence and its boom submitting this project to CS50 might seems like 
> Howling to the moon.

But I am happy to have completed this project and being able to have expressed my thoughts in terms of code.

Having first hand experience of dealing with constant combing through hard copies of documents searching for some document every day and not finding it when it is needed even though you are looking in the right folder (hard copy) it made me frustated and when I learned CS50 in 2024 and also Python in 2017 from Youtube, I got the opportuinity to submit a final project in CS50. I thought why not do this project which can serve both purposes. 

Hence here comes the final product. which is the first version of the project and can be enhanced to eventually be linked up with AI to get the fruits as the record of any office can be kept for years and can become important such as SOPs, Invoices, letters, communicae etc. 

This is a simple Flask web application that allows users to manage documents with ease. It allows users to view pending / completed references. This application is the first step in any type of business as a major part of  communications is still in practice in certian countries.

# Goals
The biggest problem with hard copies filing system is that if the record keeping mechanism in an orginzation is not in place and even if it is inplace but it can get out of hands very easily. My goal is to digitize the records for easy access as and when needed.

## Project Structure and File Description
This app is set up in the recommended way of Flask Application which is dividing each aspect of the application into a package for easy maintenance and easy understanding. 

- Project: it is the main project directory.
    * app.py: This is the entry point of the application.
    * some of the config files and requirement files.
    * pension: this is the package which contains all the files related to the application.

        * init.py: This file contains the logic required for the creation of app and Database.
        * models.py: This file contains the blueprints for the models used in the application for database schema.

        * Dashboard: This folder contains the python logic for the creation of Dashboard which manily is a few lines of pandas code in the routes.py file.
        * main: This folder contains the python logic for the creation of routes pertaining to the entry point such as index.
            * routes.py This file contains the logic for displaying the index page to the user.
            * useful_func: This is just a file which i used for research having stumbling upon a good function or some of the good writing codes that i liked.
            * utils.py This file contains helper functions which are used multiple times in the application.
        * static: This Folder Contains the static files like Java script, Css and logos.
        * templates: This is the folder where all the HTML pages are located. which are used for rendering to the user in different routes. all the other pages extends the functionality of layout.html except login and register.
        * diary: This folder contains the python logic for the creation of routes pertaining to the records of Receipts and CRUD Operations.
            * forms.py: This file contains the blueprint for forms which are a subclass of FlaskForm from flask_wtf
            * routes.py This file contains the logic for route creation forms processing and rendering pages to the user.
        * despatch: This folder contains the python logic for the creation of routes pertaining to the records of Issue and CRUD Operations.
            * forms.py: This file contains the blueprint for forms which are a subclass of FlaskForm from flask_wtf
            * routes.py This file contains the logic for route creation forms processing and rendering pages to the user.
        * UPLOADS: This folder contains the files which are uploaded by the users in the application.

## Design choice
When i first started working on this project I noticed that the flask routes opens a new page or it redraws the new page on the old page and the user has to click the back button, which was not very friendly given that if a user has to enter record of more than 10 Records in the system he would have to click almost twice the back button to enter records which can be tedious and also will slow down the performance and eventually the user might not even try to enter records into the system. 

So I searched online and viewed some of the builds like this which used a single page for crud operations. The process was simple enough for users although it was not an easy one Some of the search results suggested to use ajax for the crud operations but I failed to grasp the concept even though at some point I managed to succeed in ajax operations but still choose to leave it as I am not good at Javascript and this would certianly compromise my ability as a software developer to maintain if a bug or an endpoint fails.

Although the structuring of the project was a bit overwhelming. Thanks to @CoreyMSchafer I have watched his videos on refactoring a flask application and it enabled me to early on package the flask app in the way it is easy to maintain. 

## What I learned.
This project took almost 3 months due to my regular job and personal engagements. It proved to be a very difficult and some times even impossible when i stuck but writing this README file I am confident that I can make some thing in python.

### Follwoing technologies I learned.
* Python 
* Flask
* SQLALCHEMY
* relationships in databases i.e one to many and many to many etc.
* Working in a virtual environment.
* File Uploading.
* working with file path using pathlib and os modules.
* Flask_wtf using form and form validation.
* Jinja2 for dynamic webpage creation.
* For user login flask_login.
* for security werkzeug
* bootstrap for front end which was a pain to deal with especially in tables.
* working with config files to avoid leaking of secrets.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rafi-2024/record_management_app.git
2. Install requirements:
    pip install -r requirements.txt
3. Run Application
    python app.py

## Usage
* Visit http://localhost:5000 in your web browser.
* You can access the following endpoints:
* /: View the welcome page of the application.
* /diaries/new: View all Receipt letters and perform crud operations .
* /issues/new: View Issue letters records and perform crud operations.
* /dashboard: View a preview of pending completed and total records entered.
* /logout: Logout of the current session.
* /login: Create a new session.
* /register: Create a new user. 


## REQUIREMENTS
* Python 3.x
* SQLALCHEMY
* Flask
* Pandas
* Werkzeug for Security

(Other dependencies listed in requirements.txt)


## License
This project is licensed under the MIT License. see the LICENSE file for details

## Special Thanks.
### For making it easier for me to learn.
* David J. Malan https://cs.harvard.edu/malan/
* Harvard CS50 Team
* edx team https://www.edx.org/cs50 
* Corey M Schaffer https://github.com/CoreyMSchafer
* Julian Nash https://www.youtube.com/channel/UC5_oFcBFlawLcFCBmU7oNZA/videos
* and of course https://chatgpt.com/