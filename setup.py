from setuptools import setup, find_packages
setup(
    name='weather2stats',
    packages=find_packages(),
    version='0.2',
    description='Convert stats websites to influx data',
    author='Felix Richter',
    license='WTFPL',
    author_email='github@syntax-fehler.de',
    url='https://github.com/makefu/weather2stats',
    install_requires = [
        'requests',
        'pytz',
        'beautifulsoup4',
        'docopt',
        'influxdb'
    ],
    entry_points = {
        'console_scripts': [
            'to-influx=weather2stats.to_influx:main'
        ],
    },

    keywords=['api'],
)
