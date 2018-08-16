# Minimalist Static Website Tool
This Python 2.x tool was built to produce my portfolio at : http://www.onirom.fr

You can find a complete usage example here : https://github.com/grz0zrg/portfolio

It provide a simple way to produce static HTML pages content from a combination of JSON data definitions and HTML templates, tags related to JSON definition in the form of `{tag}` can be used inside the template files along with simple conditional tags.

It also generate the sitemap file.

While it lack many features, this tool work great if your website has a simple structure with a navigation menu and pages listing items, ideal as a portfolio generator.

### Example

Directory structure (folders) :

* json
  * nav.json
  * items.json
* template
  * nav.html
  * items.html
* dist
  * get
    * *this is a folder where you place all downloadables stuff, all the content of this folder will be included in the sitemap*
  * index.html


#### sitemap

The sitemap will be automatically generated from the pages definition AND from all files in the `get` folder (recursively), all pages are given priority 1.0 with monthly update (can be changed in the source).

#### nav.json

This list all the pages to be generated, in this case a `software.html` and `library.html` will be produced, page name with space character are converted automatically with space replaced by an underscore so that "software library" produce a "software_library.html" file.

```json
{
    "pages": [
        {
            "name": "software"
        },
        {
            "name": "library"
        }
    ]
}
```

#### nav.html

The template file linked to `nav.json` which will generate a list of items, allowed tags :

* `name`
  * The page name
* `_name`
  * The page name as it was defined in the `nav.json` file (without space character conversion)
* `active`
  * This will be replaced by the string `active` if this item correspond to the generated page (so it can be highlighted as current page with a CSS class or something)

```html
<li class="item {active}">
    <a href="{name}.html" class="nav-link">
        {_name}
    </a>
</li>
```

#### items.json

This list all available definitions for each pages, all properties listed here can be used inside the `items.html` template file, you can use an array as a value so that each items are enclosed within a div (great for styling a list of items like tags)

```json
{
    "software": [
        {
            "thumb_url": "assets/thumb/my_software.png",
            "thumb_alt": "Software example",
            "link": "https://mysoftware.com",
            "title": "Software example",
            "tags": ["C", "Embedded systems", "REST", "JSON"]
        }
    ],
    "library": [
        {
            "thumb_url": "assets/thumb/mylibrary.png",
            "thumb_alt": "Library example",
            "link": "https://mylibrary.com",
            "title": "Library example",
            "tags": ["C/C++", "Linux"]
        }
    ]
}
```

**Note** : You can self-reference an item tag within itself, for example you can do : `"title": "{link}"`

#### items.html

The items template file linked to `items.json`

```html
<li class="item">
    %%link<a href="{link}" title="{link}" target="_blank" rel="noopener">link%%
        <img class="item-thumb" src="{thumb_url}" alt="{thumb_alt}"/>
        <div class="item-label">
            <span class="item-title">
                {title}
            </span>
            <div class="item-tags">
                <div class="item-tag">
                    {tags}
                </div>
            </div>
        </div>
    %%link</a>link%%
</li>
```

##### %%tag

Simple conditional which indicate that the content enclosed between **%%tag** and **tag%%** should be removed if **tag** is empty; this remove the link element if the link is empty in the example above.

**Note** : An item `{tag}` is removed if it exist in the template file but not in the definition file.

#### index.html

Your HTML skeleton, all pages will be generated from this page, you can use a tag of the same name as the JSON files to specify where the generated items goes such as `{nav}` and `{items}` in this example.

You can also use the tag `{date}` to place the generation date.

```html
<!DOCTYPE html>
<html lang="en">
    <head>
    </head>
    <body>
        <main class="content">
            <div class="content-nav">
                <ul class="items">
                    {nav}
                </ul>
            </div>
            <div class="content-items">
                <ul class="items">
                    {items}
                </ul>
            </div>
        </main>
        
        <footer>
            <div class="update">
                generated on {date}
            </div>
        </footer>
    </body>
</html>
    </body>
```

Then you call the tool : `python static_build.py json/nav.json json/items.json dist/index.html https://www.myportfolio.com`

All generated pages can be found in the `dist` folder along with the `sitemap.xml` file.