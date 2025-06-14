from setuptools import setup,find_packages

with open('requirements.txt') as f:
  requirements = f.read().splitlines()
  
setup(
  name="House_Reservation_prediction",
  version="0.1",
  author="Akbar_Sheikh",
   packages=find_packages(),
   install_requires = requirements,
)
