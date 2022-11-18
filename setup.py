from distutils.core import setup

with open("README.md", "r") as f:
  long_description = f.read()

setup(name='Pynopticon',
      version='0.0.5',
      description='Pynopticon',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Rick Wierenga',
      author_email='rick_wierenga@icloud.com',
      url='https://www.github.com/rickwierenga/pynopticon/',
      packages=['pynopticon'],
      entry_points={
            'console_scripts': [
                  'pynopticon-server = pynopticon.server:main'
            ]   
      } 
   )

