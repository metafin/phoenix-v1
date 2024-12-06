## Setup for a clean computer (Windows)

### Install Python v3.10 (see below)
pyenv is the way to go

### set up a virtual environment (NEED INSTRUCTIONS)

### verify that you're running Python v3.10 in your virtual env:

```bash
  python --version
```

### install packages

```bash
    pip install wpilib==2025.0.0b2 robotpy==2025.0.0b2 phoenix6==25.0.0b3 robotpy[commands2] pynetworktables
```

## you need to make sure that the python interpreter in pycharm is set to python v 3.10


## How To Install Python v3.10

Install Chocolatey (if not already installed):

- Open Command Prompt or PowerShell as an Administrator.
- Run the following command to install Chocolatey:
  ```bash
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.WebClient]::new().DownloadString('https://chocolatey.org/install.ps1') | Invoke-Expression
  ```
- Install a specific version of Python:
  ```bash
   choco install python --version=3.10
  ```
- Verify the installation:
  ```bash
    python --version
  ```

## Install pyenv-win in PowerShell.

https://github.com/pyenv-win/pyenv-win

```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

Reopen PowerShell

Run to check if the installation was successful.

```bash
  pyenv --version
```

Run to check a list of Python versions supported by pyenv-win

```bash
  pyenv install -l
```

Run to install the supported version

```bash
  pyenv install 3.10
```

Run to set a Python version as the global version

```bash
  pyenv global 3.10
``` 

Check which Python version you are using and its path

```bash
  pyenv version
```

<version> (set by \path\to\.pyenv\pyenv-win\.python-version)
Check that Python is working

```bash
  python -c "import sys; print(sys.executable)"
```

\path\to\.pyenv\pyenv-win\versions\<version>\python.exe


# RoboRIO set up

## 2025 image required

We need to latest image RIO to be compatible with the latest Phoenix and robotpy
URL to download: https://github.com/wpilibsuite/2025Beta/releases/tag/NI_GAME_TOOLS_BETA_2

Need to install the latest versions onto the RIO

```bash
 python -m robotpy installer install phoenix6== 25.0.0b3 
 ```
Maybe we need to install all the packages listed above