Prompt 1: Project Setup and Database Initialization
Goal:
Set up a new Python project that uses Streamlit and SQLite.
Expectations:

Create a main application file (e.g., app.py).

Establish a connection to an SQLite database.

Define a framework to create necessary tables for student profiles and activity logs without hardcoding all field details.

Ensure the schema is flexible enough to be enhanced later.

Prompt 2: Basic Streamlit Layout and Navigation
Goal:
Build the core user interface using Streamlit.
Expectations:

Configure a clean layout with a title and sidebar.

Provide a navigation menu with options for major functionalities (e.g., adding a student, logging activity, and viewing a dashboard).

Include an option (like a sidebar button) to trigger sample data loading.

Let the LLM determine specific components and layout details.

Prompt 3: Implementing the "Add Student" Feature
Goal:
Develop functionality for adding student profiles.
Expectations:

Create a function to insert new student records into the database.

Design a Streamlit interface that allows users to input student details.

Ensure that the data model is generic and adaptable to additional fields in the future.

Prompt 4: Implementing the "Log Activity" Feature
Goal:
Enable users to log daily activity data for students.
Expectations:

Create a function that records activity metrics into the database.

Build a user interface that lets users select a student and enter activity details.

Allow flexibility for future additions of more activity metrics.

Prompt 5: Creating a Sample Data Loader Function
Goal:
Provide a mechanism to populate the database with representative sample data.
Expectations:

Develop a function that inserts a few sample student profiles.

Generate sample activity logs spanning several days for each student.

Ensure the data is randomized enough to mimic real-world variations.

Keep the implementation open for adjustments to the data generation process.

Prompt 6: Implementing Data Retrieval Helper Functions
Goal:
Build helper functions to fetch data from the database for display purposes.
Expectations:

Create functions for retrieving student lists, individual student details, and activity logs.

Design the functions to be reusable across different parts of the app (e.g., dashboard and logging features).

Ensure that the functions can handle varying amounts of data efficiently.

Prompt 7: Building the Dashboard – Profile and Metrics Display
Goal:
Develop a dashboard view that aggregates and displays student data.
Expectations:

Allow users to select a student and view their profile and performance metrics.

Display key statistics (e.g., total steps, average active minutes) dynamically.

Ensure the dashboard layout is intuitive and ready for additional enhancements.

Prompt 8: Adding Visualizations with a Charting Library
Goal:
Integrate visual components to represent activity trends and health metrics.
Expectations:

Incorporate line charts, gauges, or other visualizations to show trends over time.

Develop helper functions for computing derived metrics (like BMI) and categorizing them.

Let the LLM choose appropriate libraries and visualization styles while keeping future customizations in mind.

Prompt 9: Integrating User Feedback and Error Handling
Goal:
Improve the user experience by adding clear feedback and error handling.
Expectations:

Provide success messages, alerts, or warnings in the interface.

Ensure that operations like adding data or loading sample data communicate status to the user.

Design error handling that gracefully informs the user without exposing technical details.

Prompt 10: Code Modularization, Commenting, and Future Enhancement Framework
Goal:
Refactor the code to create a clean, maintainable, and extensible codebase.
Expectations:

Organize the code into logical sections or modules.

Add inline comments and documentation to explain key functions and decisions.

Establish a framework that facilitates future enhancements, such as advanced analytics, user authentication, or gamification elements.

Allow the LLM to decide on the best structure for maintainability and scalability.