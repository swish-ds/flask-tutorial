from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)

# To include other files, such as the static and templates directories, include_package_data is set. Python needs another file named MANIFEST.in to tell what this other data is.

# Nothing changes from how you’ve been running your project so far. 
# FLASK_APP is still set to flaskr and flask run still runs the application, 
# but you can call it from anywhere, not just the flask-tutorial directory.