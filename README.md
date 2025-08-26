# blog

A Python-based static generator to build my website [bennuttall.com](https://bennuttall.com)

## Content

Content and templates for my site are at [github.com/bennuttall/web-content]. If you wish to use
this project for your own website, this repo will be a useful reference.

## Features

- Content as markdown and/or HTML
- Pages
- Posts
- Tags
- Archives (index, years and months)
- XML sitemap
- Atom feed
- Custom Chameleon templates
- Custom CSS, JS and other static files

## Usage

Create content directories e.g. `posts`, `pages`, `static` and `templates`.

### Posts

Populate your `posts` directory with your blog posts. Each post must be in its own directory but can
be organised in any hierarchy e.g. by year, year/month or just flat. Post directories must contain a
`meta.yml` and an `index.md` and can contain images in an `images` directory, used within your post.

### Pages

Populate your `pages` directory with your pages. Each page must be in its own directory but can
be organised in any hierarchy e.g. by year, year/month or just flat. Post directories must contain a
`meta.yml` and an `index.md`.

### Static

Any files in your `static` directory will be copied into the site build root. Keep your CSS files
and such in this directory.

### Templates

Create Chameleon templates for your site in the `templates` directory. See the [Chameleon
docs](https://chameleon.readthedocs.io/en/latest/) for reference.

### Environment variables

Set environment variables for each of your content directories, and your output directory.

The output directory must exist. Note it will be deleted and re-created with your new site build.

```
export BLOG_POSTS_DIR=/home/ben/Projects/bennuttall/web-content/content/posts
export BLOG_PAGES_DIR=/home/ben/Projects/bennuttall/web-content/content/pages
export BLOG_STATIC_DIR=/home/ben/Projects/bennuttall/web-content/static
export BLOG_TEMPLATES_DIR=/home/ben/Projects/bennuttall/web-content/templates
export BLOG_OUTPUT_DIR=/home/ben/Projects/bennuttall/blog/www
```

### Install

Create a virtual environment and run `make develop` to install the library and its dependencies.

### Build

Build the site by running the command `blog` in the virtualenv. It will build your site into
`BLOG_OUTPUT_DIR`. This can be served locally with `make serve` and will be running at
`http://localhost:8000/`.

## Licence

[BSD-3-Clause](LICENSE.txt)