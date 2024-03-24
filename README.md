# Project: Jobs_and_Internships-nest

[![Github license](https://img.shields.io/github/license/Patrick-052/Jobs_and_Internships-nest)]()
[![Github stars](https://img.shields.io/github/stars/Patrick-052/Jobs_and_Internships-nest)]()
[![Github forks](https://img.shields.io/github/forks/Patrick-052/Jobs_and_Internships-nest)]()
[![Github issues](https://img.shields.io/github/issues/Patrick-052/Jobs_and_Internships-nest)]()
[![Github pull requests](https://img.shields.io/github/issues-pr/Patrick-052/Jobs_and_Internships-nest)]()
[![Github contributors](https://img.shields.io/github/contributors/Patrick-052/Jobs_and_Internships-nest)]()
[![Github repo size](https://img.shields.io/github/repo-size/Patrick-052/Jobs_and_Internships-nest)]()
[![Github code size](https://img.shields.io/github/languages/code-size/Patrick-052/Jobs_and_Internships-nest)]()
[![Github language count](https://img.shields.io/github/languages/count/Patrick-052/Jobs_and_Internships-nest)]()
[![Github top language](https://img.shields.io/github/languages/top/Patrick-052/Jobs_and_Internships-nest)]()
[![Github release](https://img.shields.io/github/v/release/Patrick-052/Jobs_and_Internships-nest)]()
[![Github tag](https://img.shields.io/github/v/tag/Patrick-052/Jobs_and_Internships-nest)]()
[![Github commit activity](https://img.shields.io/github/commit-activity/m/Patrick-052/Jobs_and_Internships-nest)]()
[![Github last commit](https://img.shields.io/github/last-commit/Patrick-052/Jobs_and_Internships-nest)]()
[![Github commit activity](https://img.shields.io/github/commit-activity/y/Patrick-052/Jobs_and_Internships-nest)]()
[![Github commit activity](https://img.shields.io/github/commit-activity/w/Patrick-052/Jobs_and_Internships-nest)]()
[![Github contributors](https://img.shields.io/github/contributors/Patrick-052/Jobs_and_Internships-nest)]()
[![Github closed issues](https://img.shields.io/github/issues)]()



# Jobs_and_Internships-nest

## Table of Contents
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
- JI-Nest: This directory contains the main application code including temporary data storage,
           API controllers and data manipulation
- config: This File contains the configuration settings for the application
- Tests: This directory contains the test cases for the application
- LICENSE: This file contains the license information for the application
- README.md: This file contains the information about the application
- requirements.txt: This file contains the dependencies for the application
- setup.py: This file contains the setup information for the application

## Installation
To set up this project, follow these steps:
1. Clone the repository
```bash
git clone https://github.com/Patrick-052/Jobs_and_Internships-nest.git
```

2. Create a virtual environment (Recommended).

### pip: `venv` or `virtualenv`

If you use pip as your Python package manager, you can create a virtual
environment using either the built-in `venv` or the (better) `virtualenv`
packages. With `venv`, run

    python -m venv <venv_path>

to initialize the new virtual environment, where `<venv_path>` is the
path to the directory to be created, and one of the following commands
to activate the environment, depending on your operating system (OS) and
shell:

* POSIX: bash/zsh

      source <venv_path>/bin/activate

* POSIX/Windows: PowerShell

      <venv_path>\Scripts\Activate.ps1

* Windows: cmd.exe

      <venv_path>\Scripts\activate.bat

With `virtualenv`, you can create a virtual environment using

    virtualenv <venv_name>

where `<venv_name>` is the name of the new environment, and activate it
using

* Linux or macOS:

      source <venv_name>/bin/activate

* Windows:

      .\<venv_name>\Scripts\activate

3. Install the project dependencies by running:

Option 1:

```bash
python -m pip install -e .
```

Option 2:

```bash
pip install -r requirements.txt
```

4. Setup the database by running:

```bash
./setup.sh
```

This is to be done after creating the environment and starting it.

5. Run the application using the following commands:

```bash
cd JI-Nest/Interface
```
Then run:

```bash
python3 Gui.py
```

## Usage
To use this application press the App Usage button on the GUI Interface and follow the instructions.

## Contributing

We welcome contributions to this project. Please follow the steps below:

1. Fork this repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For inquiries, comments or suggestions, please send an email to:
- [Patrick](mailto:Patrick-052@example.com)
