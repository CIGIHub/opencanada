# Article Management Commands

## Twitterati

'inittwitterati` and `updatetwitterati` are management commands for
loading and updating information about Twitter users for the twitterati
series of articles.


### inittwitterati

```
./manage updatetwitterati <slug> <filename.csv>
```


`init` expects only one additional argument, the name of a csv file with
the following columns, full name, twitter handle, bio, and category.

This is used to initize the json file before sourcing the data from
twitter.

It create a json file with this format:

```
[
    {
        "category": "advocacy",
        "description": "advocacy & academia",
        "members": [
            {
                "twitter_handle": "APClarkson",
                "profile_image_url": "",
                "full_name": "Adrienne Clarkson",
                "follower_count": "",
                "biography": "Adrienne Clarkson is a former Governor General of Canada, ..."
            },
            ...
        ]
    }
]
```

The json file is saved into the article with the slug provided
overwritting an existing file if there is one.

It is also possible to upload the json file manually if you one with the
correct format.

### updatetwitterati

```
./manage.py updatetwitterati <slug> --consumerkey <twitter api consumer key> --consumersecret <twitter api consumer secret> --token <twitter api token> --token-secret <twitter api token secret>
```

Retreives the existing json file from the article with the
provided slugs and iterates through the data updating the
`profile_image_url` and `follow_count` fields. The profile image is
downloaded an saved using the same storage interface as the JsonField
objects, so S3 currently in produciton or your local disk in
development.

Other fields in the json file are not touched.
