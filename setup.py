from setuptools import setup

setup(
    name="wahlprogramme",
    version="1.0.0",
    packages=["wahlprogramme"],
    install_requires=["Flask>=2.0.0", "seaborn>=0.11.1", "PyYAML==5.4.1"],
    extras_require={"test": ["pytest==6.2.4"]},
    include_package_data=True,
    flake8={"max-line-length": 88},
)
