# beemo

A Python-based static site generator. Bring your own content and templates and it'll quickly
generate you a deployable HTML website/blog. Also includes support for building a simple analytics
site based on the known site structure by processing Apache logs.

![](https://raw.githubusercontent.com/bennuttall/beemo/refs/heads/main/beemo.png)

## Features

- Content as HTML, markdown or reStructuredText
- Pages
- Blog:
  - Posts
  - Tags
  - Archives (index, years and months)
  - Atom feed
- Three modes:
  - Posts only
  - Pages only
  - Pages + posts
- XML sitemap
- Custom Chameleon templates
- Custom CSS, JS and other static files
- Apache log analytics (optional, via ``beemo[logs]``)

## Install

Install the latest release with:

```
pip install beemo
```

For Apache log analytics, install the `logs` extra:

```
pip install beemo[logs]
```

## Documentation

Documentation is available at [beemo.readthedocs.io](https://beemo.readthedocs.io/)

## Examples

Sites built with Beemo:

- [bennuttall.com](https://bennuttall.com) ([repo](https://github.com/bennuttall/web-content))
- [blog.piwheels.org](https://blog.piwheels.org) ([repo](https://github.com/piwheels/blog))
- [pynw.org](https://pynw.org/) ([repo](https://github.com/pythonnorthwestengland/pynw.org))
- [pyjok.es](https://pyjok.es/) ([repo](https://github.com/pyjokes/website))

If you wish to use this project for your own website, these examples will be a useful reference.

## Links

- [PyPI](https://pypi.org/project/beemo/)
- [GitHub](https://github.com/bennuttall/beemo)
- [ReadTheDocs](https://beemo.readthedocs.io/)

## Licence

- [BSD-3-Clause](LICENSE.txt)
