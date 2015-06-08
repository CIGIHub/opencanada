# OpenCanada Website
[![Build Status](https://travis-ci.org/OpenCanada/website.svg?branch=master)](https://travis-ci.org/OpenCanada/website)
[![Coverage Status](https://coveralls.io/repos/OpenCanada/website/badge.svg?branch=master)](https://coveralls.io/r/OpenCanada/website?branch=master)

The opencanada.org website source


## Setup
  -  Set up a virtualenv for the project
  -  Install the appropriate requirements
    -  for development: `pip install -r requirements/dev.txt`

    
## Required Environment Variables
OPEN_CANADA_SECRET_KEY - The django SECRET_KEY setting.
Set environment variable in bash

OPEN_CANADA_BASE_URL - Base URL to use when referring to full URLs within the 
Wagtail admin backend. e.g. in notification emails. Don't include '/admin' or 
a trailing slash.

## Migrations
Run any migrations required

The following are online required if you are importing data from Wordpress:

WP_IMPORTER_IMAGE_DOWNLOAD_DOMAINS - A tuple of domains for which any images 
should be downloaded locally. example: ("www.example.com", "example.com", )

WP_IMPORTER_USER_PHOTO_URL_PATTERN - The url pattern for the user photos.

## Git Hooks
Git hooks are provided in the hooks folder.

To install the hooks:

  -  navigate to the .git/hooks/ directory
  -  run `ln -s ../../hooks/<hookfile> <hookname>`  
    -  for example `ln -s ../../hooks/pre-commit.py pre-commit`
 

###Pre-Commit Hook
Performs flake8 and isort checks before allowing commit.


## Running Tests
To run the unit tests:

  -  run `./manage.py test --settings=opencanada.settings.test`
  
