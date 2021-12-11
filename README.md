# WorkerPool 

## About

WorkerPool is a project used to download information about the most visited websites from https://www.alexa.com/topsites/countries.

## Dependencies

- **python3**
- **redis**

## Building

If you want to run  the project directly on your machine, use `make install` but i do not recommand it.

A better alternative is to use `docker` and `docker-compose`. Build the images using `make build`.

# Running

To run the project on your machine you need to start your redis server, create 2 folders named `data` and `logs` and run `python src/worker_pool/entrypoints/master.py` and  
`python src/worker_pool/entrypoints/worker.py`.

A better alternative is to start it with `docker-compose` using `make start` to start the project and `make stop` to stop it, nothing more.

In `data` folder you can find the downloaded websites.  
In `logs` folder you can find the logs.
