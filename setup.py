from setuptools import setup

setup(
    name='dateint',
    version='0.1.0',
    description=(
        'Library for arithmetic/manipulation of date/datetime values in other formats.'
    ),
    long_description=None,
    author='Bruno Amaral',
    author_email='amaralbf@gmail.com',
    package_dir={'': 'src'},
    packages=['dateint'],
    python_requires='>=3.7,<4.0',
    install_requires=['pandas', 'python-dateutil'],
)
