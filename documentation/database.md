# Database
- ideaHub uses google cloud datastore as the database provider
- Entities are repsented in data.py, calls to the database are done through datastore.py
- There are two entity types stored inside of the database:
	- users
	- ideas (aka projects)

## User
- represents a user on ideaHub
- fields:
	- username
	- email
	- list of owned ideas (by title)
	- list of followed ideas (by title)

## Idea
- represents an idea held by a user being pitched on ideahub as a project
- fields:
	- owner (user -> name/email)
	- title
	- pitch date
	- description
		- conjecture
		- quality
		- qualifications for applications
		- work
		- additional info
	- url to project image
	- tags
