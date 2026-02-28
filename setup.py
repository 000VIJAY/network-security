'''
The setup.py file is used to specify the dependencies and 
metadata for a Python project. It is typically used in conjunction 
with a requirements.txt file that lists the specific packages needed for the project. 
In this case, the setup.py file would include information about the project such as its name, 
version, author, and description, as well as a reference to the requirements.txt file to ensure that all necessary packages are installed when setting up the project.
'''

from setuptools import setup, find_packages

from typing import List

def get_requirements() -> List[str]:
    '''
    Reads the requirements from a given file path and returns them as a list of strings.
    '''
    requirement_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                requirements = line.strip()
                if requirements and requirements != 'e .':
                    requirement_list.append(requirements)
    except FileNotFoundError:
        print("The requirements.txt file was not found.")
    return requirement_list

setup(
    name ="network-security",
    version = "0.0.1",
    author="Vijay kumar",
    packages=find_packages(),
    install_requires=get_requirements()
)