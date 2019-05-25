##Instructions for Phase 2 Execution- 

- Run the following commands in the terminal in Files directory. 

```bash
docker build -t phase2 .
docker run -d -p 5000:5000 phase2
```

This will create the docker image and run the same at port 5000. 