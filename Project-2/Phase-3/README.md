
### Instructions for Phase 3 Execution- 

- Run the following commands in the terminal in Files directory. 

```bash
$ docker-compose build
$ docker-compose up
```

- This will create the docker image and run the same at port 5000. 

There are two containers running. 
-One is the central database i.e. the db container which has 
 mongoDB.
-Second one is web container which has the entire pubsub system. 
This can be scaled to multiple containers as per the requirement
as all the containers will have the link to the same database. 
