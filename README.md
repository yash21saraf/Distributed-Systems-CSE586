## Distributed Systems Projects -

All the projects have been performed as the part of course work for CSE586 Distributed Systems. 

Course Website - [Professor Bina Ramamurthy](https://cse.buffalo.edu/~bina/)

### Project-1 - TravelSafe Website

#### Implementation Details - 

- The task is to implement a server side system which combines both the responses of Google maps and openweathermap APIs and plots a map in the frontend which gives a representation of the weather data from source to destination. 
- The project has been implemented in 2 phases where in the first phase the APIs are being hit for all the requests and in the second phase using MongoDB the support for caching the data has been added.
- The backend has been implemented using python flask.
- The frontend is simple HTML, Javascript. 

***Architecture Diagram-***

![image](https://github.com/yash21saraf/Distributed-Systems-CSE586/blob/master/images/1.png)

***Website Screenshot-***

![image](https://github.com/yash21saraf/Distributed-Systems-CSE586/blob/master/images/2.png)

### Project-2 Publisher Subscriber System 

- Created a Pub-Sub system and used two docker containers to deploy the application. 
- Used flask as the server and mongodb as the database both present in different containers. 
