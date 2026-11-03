# Smart Campus Resource Booking System

A desktop application using Python to automate and centralize a non-GUI resource booking system for Richfield Graduate Institution that was previously used and was very cumbersome and disorganized.

## Features
- Role Based Access Control: Different interfaces and permissions for Lecturers, Campus Administrators and System Operators.
- OOP Architecture: Encapsulation & Inheritance (models.py).
Campus-Specific Rules: These refer to booking rules in each campus (Johannesburg, Cape Town, Durban) which detail durations and hours.
Double-Booking Prevention: The system will automatically check for double booking of time slots before accepting a booking.
SQLite Database: Persistent Users, Campuses, Resources, and Bookings.
Reporting: System operators are able to create cross-campus reports (most used resources, average booking durations)

## Technologies Used
- **Python 3.13**
Tkinter (Graphical User Interface)
- **SQLite3** (Database Management)

## Project Structure
- `main.py`: This is where the application starts.
- `database.py`: Contains support for connecting to and creating tables in a SQLite database.
- The classes in OOP (User class, Lecturer class, Admin class and Operator class) are contained in the file models.py.
Separates campus-specific rules from core rules for future expansion in `- booking_rules.py`.
- `gui/`: Contains all the Tkinter windows (login, lecturer_view, admin_view, operator_view).

## How to Run
This repository needs to be cloned on your local machine.
2. Open your IDE's folder.
3. Run the `main.py` file.
It is important to note that on the first run, the SQLite database (campus.db) will be automatically created.

## Author
- **Andani** Student number: 402418534
