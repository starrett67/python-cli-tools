from setuptools import setup

setup(
    name="tbs",
    version="0.0.1",
    pymodules=['tbs'],
    install_requires=[
        'Click',
    ],
    dependency_links=["git@github.com:3Blades/python-sdk.git"],
    entry_points="""
        [console_scripts]
        tbs=tbs:main
    """
)
