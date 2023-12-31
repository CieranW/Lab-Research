# Part 1: Establish a Dashboard for Data Collection and Display

1.	Define Data Structure: Determine the structure of the data you want to collect. Ensure it's uniform across different models. Identify the global attributes you want to track.
2.	Integrate Models: Implement mechanisms to collect data from different models. This may involve using APIs, database connections, or direct integration based on the model type.
3.	Dashboard Interface: Design a user-friendly dashboard that visualizes the collected data. Use charts, tables, or graphs to represent the data. Consider using web technologies like HTML, CSS, and JavaScript for creating an interactive dashboard.
4.	Inconsistency Handling: Implement functionality to detect inconsistencies in the global attributes across models. Provide options for users to either push data to synchronize models or accept the inconsistencies.
5.	User Actions: Integrate user actions into the dashboard interface. Allow users to push data to other models or handle inconsistencies based on predefined workflows.

## Technologies Part 1: 

-	Python for data analysis (NumPy or Pandas)
-	Web technology? Could use HTML/CSS and JavaScript
-	Database: SQL for storing/managing
-	How are we connecting to the database? 
-	Deployment? Could go cloud like AWS or Docker for container.
-	Dashboard design (link to web tech) 

## Weekly updates and todos:

### October 14 - 22, 2023

-   Implement the baseline for the dashboard. 
-   Create 3 datasets with similar variables throughout. EX. Dataset 1 has time, length, and speed; Dataset 2 has speed, height, and width; and Dataset 3 has width, height, and length. 
-   Import the data from the datasets and match like variables. 
-   Create an output file(might do the terminal for now) that contains each variable found and lists which dataset it came from and the value of the variable

### October 20 - November 12, 2023

-   Create a web page for the visual dashboard, complete with interactive features that allow for variable change, analyzing a certain dataset, and displaying the current output. 
-   Implement a notification system within the dashboard that will notify the user of the most recent changes within the dashboard, be that external or internal changes to a dataset.
-   Find a way to keep track of the previous datasets for comparison with the new dataset within the notification system.  