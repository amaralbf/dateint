from setuptools import setup


def README():
    with open('README.md', 'rt', encoding='utf-8') as f:
        readme = f.read()
    return readme


setup(
    name='dateint',
    version='0.1.0',
    author='Bruno Amaral',
    author_email='amaralbf@gmail.com',
    url='https://github.com/amaralbf/dateint',
    description=('Helper library for manipulation of formatted date/datetime values.'),
    long_description=README(),
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=['dateint'],
    python_requires='>=3.7,<4.0',
    install_requires=['pandas', 'python-dateutil'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
