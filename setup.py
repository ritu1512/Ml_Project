from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    reguirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requiremnets = [req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requiremnets


setup(
name = 'ML_Project',
version = '0.0.1',
author = 'Ritu', 
author_email = 'ritugaba123@gmail.com', 
packages = find_packages(), 
install_requires = get_requirements('requirements.txt')

)
