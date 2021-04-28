# Medipal

Built for Innovate\@UCLA's Young Tech Professionals Bootcamp Spring 2021.

## Authors

Jason Lim (@jlimcode), Julia Offerman (@juliaofferman), Olivia Apuzzio (@oliviaapuzzio), and Isabel Roig (@isabelroig). 

## Description

Prescription reminder service to improve medical adherence.

## Usage

After cloning the git repository, run the following commands:

(For first time `pipenv` use)
```bash
pip install pipenv
```

Followed by:

```bash
cd medipal
pipenv install
```

You'll need to have a couple environment variables set up before running.

```bash
export FLASK_APP=server.py #this is a bash command
```

Once your environment is set up, you can start the venv and run the server.

```bash
pipenv shell
flask run
```
