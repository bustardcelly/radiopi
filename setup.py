
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Using a Raspberry Pi to receive various inputs from an old radio.',
    'author': 'Todd Anderson',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'bustardcelly@gmail.com',
    'version': '0.1.0',
    'install_requires': ['nose', 'lettuce'],
    'packages': ['radiopi'],
    'scripts': [],
    'name': 'radiopi'
}

setup(**config)
