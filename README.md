# 📦 This is my midterm project!

# This app is a calculator App that provides results for the following operations:
   - power
   - root
   - integer division
   - percentage calculation
   - absolute difference
   - modulus

   ## Other features
   - log of calculation inputs/dates/messages is stored in calculator.log
   - log of calculation history is stored in calculator_history.cvs
   - undo/redo calculations
   - save calculation history to csv file
   - load calculation history from csv file
   - display calculation history
   - clear calculation history
   - color coded output using colorama!
      - green: success messages or calculation results
      - yellow: informational messages
      - red: error/exception messages
      - magenta: show available commands


# Installation Instructions:
   1: git clone git@github.com:Jeffches15/midtermproject.git
   2: navigate to directory where the project was cloned (cd commands)
   3: python3 -m venv venv: creates virtual environment named venv.
      - we use virtual environments to keep program isolated with its own packages/dependencies
   4: source venv/bin/activate: activates venv
   5: navigate to the directory where requirements.txt is located and run: pip install -r requirements.txt
   6: run code . to open project in Visual Studio Code

# Setting up .env file:
   1: in main project directory, create a file called .env (touch .env)
   2: add .env to gitignore file (so it isnt pushed to GitHub)
   3: refer to calculator_config.py for .env variable names. For security reasons, I will not list the contents of this file here
   4: if some variables are not included in .env, calculator_config.py will set default values

# 🔥 Useful Commands Cheat Sheet

| Action                         | Command                                          |
| ------------------------------- | ------------------------------------------------ |
| Install Homebrew (Mac)          | `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` |
| Install Git                     | `brew install git` or Git for Windows installer |
| Configure Git Global Username  | `git config --global user.name "Your Name"`      |
| Configure Git Global Email     | `git config --global user.email "you@example.com"` |
| Clone Repository                | `git clone <repo-url>`                          |
| Create Virtual Environment     | `python3 -m venv venv`                           |
| Activate Virtual Environment   | `source venv/bin/activate` / `venv\Scripts\activate.bat` |
| Install Python Packages        | `pip install -r requirements.txt`               |
| Build Docker Image              | `docker build -t <image-name> .`                |
| Run Docker Container            | `docker run -it --rm <image-name>`               |
| Push Code to GitHub             | `git add . && git commit -m "message" && git push` |

# Other useful Command Line Interface commands:

- **ls**: List files in a directory (`dir` in CMD)  
- **cd**: Change directory  
- **pwd**: Show current directory  
- **mkdir foldername**: Create a new directory  
- **touch filename**: Create a new file (`New-Item` in PowerShell)  
- **rm filename**: Delete a file (`del` in CMD)  
- **rm -r foldername**: Delete a folder and its contents  
- **cp source dest**: Copy files or directories  
- **mv old new**: Move or rename files/folders  

# Other useful git commands:

- **git init**: Initialize a Git repo  
- **git clone URL**: Clone a repo  
- **git status**: See current repo status  
- **git add .**: Stage all changes  
- **git commit -m "message"**: Commit changes  
- **git push**: Push to remote repo  
- **git pull**: Pull latest changes  
- **git checkout branchname**: Switch branches

# Testing instructions:
- create a directory called tests
- in this tests directory, create files starting with "test_" then the name of the file you want to write tests for
   - ex: test_calculation.py to test functionality in calculation.py
- the methods in these files have to start with "test_" as well
   - ex: if you are testing for an invalid root -> test_invalid_root method name
- after writing some tests, run pytest command in terminal
- if you want to run pytest for only one file (test_config.py):
   - pytest tests/test_config.py 
- if you want to run pytest for one method in a file (test_invalid_precision):
   - pytest tests/test_config.py::test_invalid_precision
- make sure the Cover says 100% and there is nothing listed under Missing
   - Missing lists the line numbers that are not "tested"

# GitHub Actions:
- GitHub actions is GitHub's CI/CD approach used for automating work flows
- Purpose:
   - Automate testing
   - Build and deploy apps
   - Enforce code quality
   - Manage workflows
- python-app.yml is the file incorporating GitHub actions
- Some of the configuration in python-app.yml include:
   - setting Python version to 3.11
   - runs tests on pull/push to main branch
   - Install dependencies from requirements.txt
   - Run tests with pytest and enforce 90% coverage


# 🧩 1. Install Homebrew (Mac Only)

> Skip this step if you're on Windows.

Homebrew is a package manager for macOS.  
You’ll use it to easily install Git, Python, Docker, etc.

**Install Homebrew:**

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**Verify Homebrew:**

```bash
brew --version
```

If you see a version number, you're good to go.

---

# 🧩 2. Install and Configure Git

## Install Git

- **MacOS (using Homebrew)**

```bash
brew install git
```

- **Windows**

Download and install [Git for Windows](https://git-scm.com/download/win).  
Accept the default options during installation.

**Verify Git:**

```bash
git --version
```

---

## Configure Git Globals

Set your name and email so Git tracks your commits properly:

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

Confirm the settings:

```bash
git config --list
```

---

## Generate SSH Keys and Connect to GitHub

> Only do this once per machine.

1. Generate a new SSH key:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

(Press Enter at all prompts.)

2. Start the SSH agent:

```bash
eval "$(ssh-agent -s)"
```

3. Add the SSH private key to the agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

4. Copy your SSH public key:

- **Mac/Linux:**

```bash
cat ~/.ssh/id_ed25519.pub | pbcopy
```

- **Windows (Git Bash):**

```bash
cat ~/.ssh/id_ed25519.pub | clip
```

5. Add the key to your GitHub account:
   - Go to [GitHub SSH Settings](https://github.com/settings/keys)
   - Click **New SSH Key**, paste the key, save.

6. Test the connection:

```bash
ssh -T git@github.com
```

You should see a success message.

---

# 🧩 3. Clone the Repository

Now you can safely clone the course project:

```bash
git clone <repository-url>
cd <repository-directory>
```

---

# 🛠️ 4. Install Python 3.10+

## Install Python

- **MacOS (Homebrew)**

```bash
brew install python
```

- **Windows**

Download and install [Python for Windows](https://www.python.org/downloads/).  
✅ Make sure you **check the box** `Add Python to PATH` during setup.

**Verify Python:**

```bash
python3 --version
```
or
```bash
python --version
```

---

## Create and Activate a Virtual Environment

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate.bat  # Windows
```

### Install Required Packages

```bash
pip install -r requirements.txt
```

---

# 🐳 5. (Optional) Docker Setup

> Skip if Docker isn't used in this module.

## Install Docker

- [Install Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- [Install Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## Build Docker Image

```bash
docker build -t <image-name> .
```

## Run Docker Container

```bash
docker run -it --rm <image-name>
```

---

# 🚀 6. Running the Project

- **Without Docker**:

```bash
python main.py
```

(or update this if the main script is different.)

- **With Docker**:

```bash
docker run -it --rm <image-name>
```

---

# 📝 7. Submission Instructions

After finishing your work:

```bash
git add .
git commit -m "Complete Module X"
git push origin main
```

Then submit the GitHub repository link as instructed.

---

# 📋 Notes

- Install **Homebrew** first on Mac.
- Install and configure **Git** and **SSH** before cloning.
- Use **Python 3.10+** and **virtual environments** for Python projects.
- **Docker** is optional depending on the project.

---

# 📎 Quick Links

- [Homebrew](https://brew.sh/)
- [Git Downloads](https://git-scm.com/downloads)
- [Python Downloads](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [GitHub SSH Setup Guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
