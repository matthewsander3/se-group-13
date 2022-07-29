# UTSA CS 3773 (Fall 2021) - Software Engineering Group 13

# Project: Hotel Reservation System

## Group members

- Matthew Sander: Project Manager (Back-end)
- Kyle Melbert: Lead developer (Back-end)
- Benjamin Ndruzi: UI Designer (Front-end/Back-end)

## About

This project was our final project and counted as our final exam for the semester. The professor asked each group to build an application from the ground up by using any technology we wanted. We were placed into different groups of three to five people. The goal of this project was to give us an idea of software engineering best practices. We learned about the interaction between the development team and the client, designing the project based on client needs by using personas, scenarios, and user stories. We also learned about popular software methodologies such as agile and scrum. After having distributed responsibilities among members, we organized ourselves by doing small scrums meetings to discuss features and functionalities and made sure we stayed updated with the client (The professor). This project was built in three weeks.

## Features

**General Eric's Hotels** is a hotel reservation web application focused on simplicity and ease of use. Following are features you can find in the app:

The customer must create an account before accessing all the features.

The user/customer can:
- Create an account and/or login/logout
- Search hotels by entering the following: check-in and check-out dates, weekend differential, min and max room prices, room type, and number of rooms
- View past and future reservations
- Book and/or cancel reservations
- Edit their account information

The following are Admin specific features:

The admin can:
- Edit hotels
- Delete reservations
- View customers
- Delete customers

## Tech-stack

- **Front-end**: HTML, CSS
- **Back-end**: Python, Flask (Flask RESTful, Jinja), Postman (API development and testing)
- **Database**: We used JSON files as a temporary substitute for a database since none of us had taken any database course at that time.

Note: 
- Given the short time we had to finish the project, we went for Flask as our back-end because it is lightweight, allows for fast development, and is easy to understand.
- We wish we used Flask SQLAlchemy to store information in a database for easy data manipulation
- We wish we used hashing for storing users' password as a more secure way of authentication

## How to run

- Download source code
- Make sure you have Python installed in your computer
- Open code editor and open project folder
- Install all dependencies: 
    * `pip freeze > requirements.txt`
    * `pip install -r requirements.txt`
- Run the code and visit localhosted site


## Database Schema

![Database Schema](/other/db_schema.png)

## Project flow

![Project Flow](/other/project_flow.png)
