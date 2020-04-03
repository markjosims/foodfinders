# cs331e-idb
sample stuff in the readme

## Using virtualenv

If we want to have a virtual environment that's consistent across each of our machines, we need to follow these steps.

- create a venv on your machine (I just used `python3 -m venv venv`)
- activate the venv, command varies by OS
- type the following command:
`pip install -r requirements.txt`
- this will make sure all dependencies written in requirements.txt are installed on your venv
- *if you install any packages onto your venv while coding*
	- run the command `pip freeze > requirements.txt` while venv is active
	- this will add the dependencies you installed to the list of requirements, and all other users can just run `pip install -r requirements.txt` again and be up to date w/ your venv
- I put "venv" in the .gitignore file, that way my venv folder wouldn't be uploaded. if you name your virtual environment antything other than "venv", add that name to the .gitignore file