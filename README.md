# Save Living App
This project is being developed for CS-4503 Senior Software Project at the University of Tulsa.

## Setup and Installation (Angular Frontend)
1. Install [Node.js](https://nodejs.org/en/).
2. Clone the repository to a local directory.
3. Run `npm install` at the local repo directory to install dependencies.

> **_NOTE:_** There have been some issues related to installing in certain directories. If an issue arises with installation or running the code, try installing in a different directory.

## Build/Test Software (Angular Frontend)
To build the software, run `ng serve`. Add `--open` at the end to open in the default browser.

> **_NOTE:_** If you are using Windows and run into a "Running scripts is disabled on this system" issue, use `powershell -ExecutionPolicy ByPass ng serve --open`.

## Setup and Installation (Django Backend)
1. Ensure that Python 3.10 is installed.
2. Clone the repository to a local directory.
3. In a shell or command line, navigate to the "backend" directory and create a virtual python environment inside of it. Example for Powershell: `py -m venv venv`
4. Activate the environment by running the activate script inside of venv/Scripts. Example for Powershell within backend directory: `powershell -ExecutionPolicy ByPass .\venv\Scripts\activate.bat`
5. Set your preferred Python interpreter to be the one inside of venv/Scripts.
6. Within the virtual environment, install dependencies: `python -m pip install django`

## Build/Test Software (Django Backend)
To build the software, run `python manage.py runserver` in the backend/backend_server directory and navigate to `localhost:8080`.

## Contributing
To contribute, make a branch with any changes!
