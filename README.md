# Mission-to-Mars
## Overview
The purpose of this web-scraping project was to extract the latest news articles and images from several different websites and create a web application to display the most up-to-date information regarding the Mission to Mars. Using Beautiful Soup and Splinter to automate a browser and scrape for the latest news, storing the extracted data in MongoDB and then using Flask to create the web application to display the information. In the end we ended up using Bootstrap to add a little polish and style to the html used to build the web application. 

## Resources
Beautiful Soup, Splinter, MongoDB, Flask, Bootstrap, Jupyter Notebook, VS Code, python, html

## Challenges
There were several challenges that I faced in this module and assignment but the biggest was getting MongoDB to work properly.  Installation was no problem but making the connection to the database was different. After spending 4 days researching, troubleshooting error messages and working with the teaching assistants to resolve this issue, I was finally able to figure it out.  The issue was with the db path and using the right commands to initiate and connect with mongo. I had to create the path for my Mongo database and I had to figure out the correct commands to start an instance and connect to mongo with my MacBook M1 processor. In the end I had to start an instance by actually typing my db path every single time into terminal.  To connect to mongo I had to type the command 'mongo --host localhost:27017'.  Not only was I able to figure this out and get mongodb working, I was able to help a classmate having the same issue to get hers running too! Success!
