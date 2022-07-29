# UTSA CS 3773 (Fall 2021) - Software Engineering Group 13

# Project: Hotel Reservation System

## Group members:

- Matthew Sander: Project Manager (Back-end)
- Kyle Melbert: Lead developer (Backend)
- Benjamin Ndruzi: UI Designer (Frontend/Backend)

## About:

This project was our final project and counted as our final exam for the semester. The professor asked about building a software from the ground up by using any technology we wanted. We were placed into different groups of three to five people. The goal of this project was to give us an idea of software engineering best practices. We learned about interaction between the development team and the client, designing the project based on client needs by using personas, scenarios and user stories. We also learned about popular software methodologies such as agile and scrum. After having distributed responsabilities among members, we organized ourselves by doing small scrum meeting to discuss features and functionalities, and made sure we stayed updated with the client (The professor).

## Features:

**General Eric's Hotels** is a hotel reservation web application focused on simplicity and ease of use. Following are features you can find in the app:

The customer must create an account before accessing all the features.

The user/customer can:
- create an account and/or login
- search hotels by entering the following: Checkin and checkout dates, weekend differential, min and max room prices, room type, and number of rooms
- book and/or cancel reservations 
- edit their account information

The following are Admin specific features:

The admin can:
- Edit hotels
- View customers
- Delete customers 
- Delete reservations

## Tech-stack:

- Front-end: HTML, CSS
- Back-end: Python, Flask (Flask RESTful, Jinja)
- API was developed and tested using Postman

Note: Given the short amount of time we had to finish the project, we went for Flask as our backend because it is lightweight, allow for fast development, and is easy to understand.

## How to run:

- Download source code
- Make sure you have Python installed in your computer
- Open code editor and open project folder
- Install all dependencies: 
    * `pip freeze > requirements.txt`
    * `pip install -r requirements.txt`
- Run the code and visit localhosted site
