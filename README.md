# Pokemon to GCP ETL

Basic python ETL script to request some pokemon data, select a subset of columns, light transformation to capitlise the text columns, and finally load the transformed data into GCP.

## Description

This app was created as a way to learn how to make use of API requests, using python for basic ETL and finally how to structure a project to write out the transformed data into GCP as a csv file. This project also served as a way to learn how to use docker and how to containerise a project to be run anywhere through docker.

## Getting Started

### Dependencies

- Docker to run the docker image

### Installing

Amendments to make before running:

- Add GCP credentials JSON in the config folder
- Required details filled in the config_file.json in config folder

### Executing program

- How to run the program: build the docker image using command

`docker build -t python-app .`

- Run the app through command:

`docker run python-app`

## Acknowledgments

Inspiration, code snippets, etc.

- [Coursea - IBM: Python Project for Data Engineering](hhttps://www.coursera.org/learn/python-project-for-data-engineering)
