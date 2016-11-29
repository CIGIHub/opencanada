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

There is a `ManyToMany` relationship between `ArticlePage` and itself
where an given article will have a collection of response articles.

An article can access it responses through the `responses` manager, and
an article can use the `is_response` property to detect if it is a
response, `response_to` to get the article it is a response to if it
exists.

Here is some example template code:

```
{% if self.is_response %}
<h3>Response to <a href="{{ self.reponse_to.url }}">{{
self.reponse_to.title }}</a><h3>
<p>Read other responses:</p>
<ul>
  {% for response in self.reponse_to.response.all() %}
    <li><a href="{{ reponse.url }}"></a>{{ response.title }}</li>
  {% endfor %}
</ul>
{% endif %}
```
