# OpenCanada Website
[![Build Status](https://travis-ci.org/OpenCanada/website.svg?branch=master)](https://travis-ci.org/OpenCanada/website)
[![Coverage Status](https://coveralls.io/repos/OpenCanada/website/badge.svg?branch=master)](https://coveralls.io/r/OpenCanada/website?branch=master)

The opencanada.org website source


# Required Environment Variables
OPEN_CANADA_SECRET_KEY - The django SECRET_KEY setting.

OPEN_CANADA_BASE_URL - Base URL to use when referring to full URLs within the 
Wagtail admin backend. e.g. in notification emails. Don't include '/admin' or 
a trailing slash.
