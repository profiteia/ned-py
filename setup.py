from setuptools import setup, find_packages

setup(
    name="ned-py",
    version="0.2",
    packages=find_packages(),
    description="Python wrapper for Nationaal Energie Dashboard API.",
    long_description="Receive and parse data from the Nationaal Energie Dashboard (ned.nl).",
    author="Profiteia",
    author_email="victor@profiteia.io",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="ned.nl nationaal energie dashboard",
    install_requires=[
        "beautifulsoup4",
        "bidict",
        "datetime",
        "pandas",
        "requests",
        "typing",
    ],
    python_requires=">=3.6, <4",
    url="https://github.com/profiteia/ned-py",
    project_urls={
        "Source": "https://github.com/profiteia/ned-py",
        "Documentation": "https://github.com/profiteia/ned-py",
        "Issue Tracker": "https://github.com/profiteia/ned-py/issues",
    },
)
