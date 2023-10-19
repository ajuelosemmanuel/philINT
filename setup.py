from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name="philINT",
    version="0.1.a",
    packages=find_packages(),
    author="Emmanuel Ajuelos",
    author_email="ajuelosemmanuel@gmail.com",
    install_requires=["iso-639","pycountry","httpx","selenium", "gpxpy", "folium", "asyncio", "pandas"],
    long_description_content_type='text/markdown',
    long_description=long_description,
    description="philINT is a library that allows OSINT investigators to retrieve and organize data from an email address or an username.",
    include_package_data=True,
    url="https://github.com/ajuelosemmanuel/philINT",
    entry_points = {
        "console_scripts": [
            "philINT = philINT.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
