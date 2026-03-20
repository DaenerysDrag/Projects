from setuptools import setup, find_packages

setup(
    name='flipkart_scraper',
    version='1.0.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'pandas',
        'openpyxl',
        'fake_useragent',
    ],
    entry_points={
        'console_scripts': [
            'flipkart-scraper=flipkart_scraper.main:main',
        ],
    },
)
