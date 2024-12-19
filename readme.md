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
Note: needs to be pip install robotpy\\[commands2\\] on Mc

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

Funky - the software required a RIO version one earlier. So I found that here:
https://github.com/wpilibsuite/2025Beta/releases

## Install base software on the RIO
 python -m robotpy installer download-python        

Need to install the latest versions onto the RIO

```bash
 python -m robotpy installer install phoenix6== 25.0.0b3 
 ```
Maybe we need to install all the packages listed above


# BN Notes
- python v3.13.0
- delete all site-packages from .venv/Lib
- reinstall pip
- run pip script above
- robotpy sim runs

## now on rio
- run robotpy sync
- (this will run a long script to install stuff on rio)
- robotpy deploy fails becuase of some issues with tests
- but when i run "robotpy deploy --skip-tests" is seems to deploy


llm prompts

