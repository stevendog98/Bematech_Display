from setuptools import setup, find_packages

setup(
    name='bematech-display',
    version='0.1.0',
    description='Python driver for Bematech LCI USB customer displays',
    author='Steven Williams',
    author_email='stevendog98@mail.overstrike.org',
    packages=find_packages(),
    install_requires=[
        'pyserial>=3.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
