'''
Created on 20200130
Update on 20200130
@author: Eduardo Pagotto
'''

from subprocess import check_call

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install

PACKAGE = "PyGravity"
VERSION = __import__(PACKAGE).__version__

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        #check_call("apt-get install this-package".split())
        check_call("echo 'DevelopInstall'".split())
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        #check_call("apt-get install this-package".split())
        check_call("echo 'POSTINSTALL'".split())
        install.run(self)

setuptools.setup(
    include_package_data=True, # para adicionar o manifest
    name="PyGravity",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="Game Engine in openGL",
    long_description="Game Engine in openGL",
    long_description_content_type="text/markdown",
    url="https://github.com/EduardoPagotto/PyGravity.git",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    scripts=['bin/gravity.py'],
    data_files=[('etc',['etc/gravity.yaml']),],
    install_requires=['PyOpengl',
                      'PyGLM',],
    cmdclass={ # ref: https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools
    'develop': PostDevelopCommand,
    'install': PostInstallCommand,}
)
