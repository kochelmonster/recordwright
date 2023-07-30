"""
vica base package
"""
from setuptools import setup, find_namespace_packages



options = {
    "install_requires": [
        "playwright",
    ],
    "include_package_data": True,
    "package_data": {
        "recordwright": ["*.js"],
    }
}

setup(
    name="recordwright",
    version="1.0.0",
    package_dir={'': 'src'},
    packages=find_namespace_packages(where="src"),
    author="Michael Reithinger",
    author_email="mreithinger@web.de",
    description="recordwright",
    license="GNU",
    keywords="Library Test",
    url="http://github.com/RecordWright/",
    **options
)
