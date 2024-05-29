"""
Setup file to package this tool
"""

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="cine_aalst_cli",
    version="0.1.0",
    author="vdmkenny",
    description="View movie schedules for Ciné Aalst",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vdmkenny/cine-aalst-cli",
    packages=find_packages(),
    install_requires=[
        "requests",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "cine-aalst=cine_aalst_cli.cine_aalst:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
