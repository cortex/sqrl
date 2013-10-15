try:
    from setuptools import setup
except:
    from disutils.core import setup

dependencies = ['docopt', 'ed25519']

setup(
    name='sqrl',
    version='0.0.1',
    description='Command line SQRL client',
    url='http://gitbub.com/bushxnyc/sqrl',
    author='Brian Pinkney',
    author_email='bushxnyc@gmail.com',
    install_requires=dependencies,
    packages=['sqrl'],
    entry_points={
        'console_scripts': [
            'sqrl=sqrl.sqrl:main'
        ],
    },
    classifiers=(
        'Development Satus :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language ::  English',
        'License ::  OSI Approved :: MIT License',
        'Programming Language : Python',
        'Programming Language : Pythoni :: 2.7',
    )
)
