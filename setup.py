from distutils.core import setup

setup(
    name='NaveggUtils',
    version='0.1.1',
    author='Felipe Arenhardt Tomaz',
    author_email='felipa.a.tomaz@gmail.com',
    packages=['navegg_utils'],
    url='http://www.navegg.com/',
    license='LICENSE.txt',
    description='Navegg Utils - Python Library.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pika >= 0.9.13",
        "MySQL-python >= 1.2.4",
    ],
)
