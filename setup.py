from setuptools import setup

setup(
    name='ecosia',
    description='Task',
    version='1.0',
    url='',
    author='Maria Teresa Chietera',
    author_email='maria.chietera@gmail.com',
    scripts=['ecosia'],
    py_module=['main.py'],
    entry_points={
        'console_scripts': ['main.py']
    },
    install_requires=['boto3']
)
