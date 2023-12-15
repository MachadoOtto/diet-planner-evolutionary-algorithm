# Diet Planner Evolutionary Algorithm

This project uses an evolutionary algorithm (NSGA-II) to solve a diet planning problem. The goal is to find the optimal diet plan that meets certain nutritional requirements while maximizing variety.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need Python 3.x and the following libraries installed on your machine:

- numpy
- matplotlib
- jmetalpy

You can install these packages using pip:

```bash
pip install numpy matplotlib jmetalpy
```

### Running the Program

To run the program, navigate to the project directory and run the `main.py` script with the instance number and project name as arguments:

```bash
python main.py 1 my_project
```

In this example, `1` is the instance number and `my_project` is the project name.

The program will create a new directory in the `output` folder with the name of your project. Inside this directory, it will generate a `.csv` file with the results of the algorithm and a `.txt` file with detailed information about each execution. It will also generate a scatter plot of the Pareto optimal solutions.

### Executed Instances for Research

The following instances were executed for the research:

- Instance 1: `python main.py 1 instance_1`

- Instance 2: `python main.py 2 instance_2`

## Project Structure

- `main.py`: This is the main script that you run to start the program.
- `src/models`: This directory contains the classes used in the program, including `Args`, `Config`, `CrossoverCustom`, `DietProblem`, and `Result`.
- `src/utils`: This directory contains utility functions.
- `config`: This directory contains configuration files for the algorithm and the diet problem model.
- `data`: This directory contains the food data in a `.csv` file.
- `output`: This directory is where the program saves the results.

## Authors

- Jorge Miguel Machado
- Santiago Pereira
