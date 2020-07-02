import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsp",
    version="1.0.0",
    author="Felix Bartusch",
    author_email="fbartusch@web.de",
    description="Implementation of travelling salesperson (tsp) problem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fbartusch/travellingSalesperson",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['numpy', 'pandas', 'scipy', 'networkx'],
    entry_points={"console_scripts": ["tsp=tsp.__main__:main"]}
)