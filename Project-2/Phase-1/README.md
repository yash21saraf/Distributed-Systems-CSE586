## Instructions for Phase 1 Execution- 

- Run the following commands in the terminal in Files directory. 

```bash
docker build -t phase1 .
docker run -d -p 5000:5000 phase1
```

This will create the docker image and run the same at port 5000. 