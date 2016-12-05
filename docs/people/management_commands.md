# People Management Commands

## Contributor Export

The `contributor_export` management command takes a year and outputs
json text describing all of the contributor who contributed in a given
year sorted by last name. The information includes the contributors full
name and the url to their page. The output is encoded in UTF-8.

Example:

```
$ ./manage.py contributor_export 2013
[
    {
        "contributor_url": "/contributors/edward-akuffo/",
        "full_name": "Edward Akuffo"
    },
    {
        "contributor_url": "/contributors/asim/",
        "full_name": "Asim Ali"
    },
...
]
```
