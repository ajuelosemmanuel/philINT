from setuptools import setup, find_packages

setup(
    name="philINT",
    version="1.00",
    packages=find_packages(),
    author="Emmanuel Ajuelos",
    author_email="ajuelosemmanuel@gmail.com",
    install_requires=["iso-639","pycountry","httpx","selenium", "gpxpy", "folium", "asyncio", "pandas"],
    description="philINT is a library that allows OSINT investigators to retrieve and organize data from an email address or an username.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
