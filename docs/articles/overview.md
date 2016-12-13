# Articles

The main models for the OpenCanada website are located in the `articles`
app.


## Relationships Between Articles

There are a couple of ways articles can be related to eachother. Here is
an overview of the options and which situations they are used for.

### Read More Articles

These generally appear at the bottom of an article and are generated
dynamically. See `ArticlePage.related_articles()` for the exact
implementation. It grabs articles in the primary topics first, then
secondary topics, and then more by the author and then finally just
recently published aritcles.

### Series Articles

An explicit relationship between a special container page and a list of
articles. Series live under the indepth branch of the site hierarchy.
What make series unique is the conatain page which is represented by the
`SeriesPage` model.

### Related Items

A stream field which allows a list of related articles to be embedded
into the body of an article, be it an `ArticlePage` or likely a
`SeriesPage`.

The implemation is in `articles/fields.py`, see the `RelatedItemsBlock`
class.

The way the related items look can be customized through
the themeing mechanism.

### Response Articles

Similar to Series Articles, but without the special container page and
the need for that container to live under indepths.

There is a wagtail style faux many to many relationship between
`ArticlePage` and itself where an given article will have a collection
of response articles. The model for this relationship is
`ResponseArticleLink`.

The thorugh table gives an article the following attributes.
`response_to_links` which is a related query set of
`ResponseArticleLinks` where the `response_to` attribute is the article
this article is a response to. This should either be empty or only
contain 1 article. See the `response_to` property below.
`response_links` is a related query set of `ResponseArticleLinks` where
the `response` attribute one of the articles which is a response to this
article.

In addition to these default attributes provided by the relationship
between the models, the `ArticlePage` model definte two properties and
a method to make working with related articles easier.

`is_response` return True if this article is a response to something and
False if not. This inturn calls `response_to`, which is one reason
`response_to` caches the result.

`response_to` get the one article this article is a response to if it
exists, or is None. Note: if for some reason an article become a
response to multiple articles, a warning is emitted which should appear
on Sentry, and only the first article is returned. What first means is
poorly defined, but probably related to published date. `response_to` is
cached per request.

`responses()` a method which return the list of all articles which are a
response to this article. This doesn't return a queryset, it returns the
list of responses already loaded into memory.

An article can access it responses through the `responses` manager, and
an article can use the `is_response` property to detect if it is a
response, `response_to` to get the article it is a response to if it
exists.

Here is some example template code:

```
{% if self.is_response %}
<h3>Response to <a href="{{ self.response_to.url }}">{{
self.response_to.title }}</a><h3>
<p>Read other responses:</p>
<ul>
  {% for response in self.response_to.responses %}
    <li><a href="{{ response.url }}"></a>{{ response.title }}</li>
  {% endfor %}
</ul>
{% endif %}
```
