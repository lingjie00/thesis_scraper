"""Setup."""
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_desc = f.read()

setuptools.setup(
    name="finage",
    version="0.0.1",
    author="Ling",
    author_email="lingjie@u.nus.edu",
    description="scraper for thesis data source",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/lingjie00/thesis_scraper",
    project_urls={
        "Bug Tracker": "https://github.com/lingjie00/thesis_scraper/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "finage"},
    packages=setuptools.find_packages(where="finage"),
    python_requires=">=3.8"
)
