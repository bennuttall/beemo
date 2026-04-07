# beemo

A Python-based static site generator. Bring your own content and templates and it'll quickly
generate you a deployable HTML website/blog.

![](https://raw.githubusercontent.com/bennuttall/beemo/refs/heads/main/beemo.png)

## PyPI

- [beemo](https://pypi.org/project/beemo/)

## Features

- Content as HTML, markdown or reStructuredText
- Pages
- Posts
- Tags
- Archives (index, years and months)
- XML sitemap
- Atom feed
- Custom Chameleon templates
- Custom CSS, JS and other static files
- Apache log analytics (optional, via `beemo[logs]`)

## Usage

Create content directories e.g. `posts`, `pages`, `static` and `templates`.

### Posts

Populate your `posts` directory with your blog posts. Each post must be in its own directory but can
be organised in any hierarchy e.g. by year, year/month or just flat. Post directories must contain a
`meta.yml` and a content file (`index.html`, `index.md` or `index.rst`), and can contain images in
an `images` directory, used within your post.

### Pages

Populate your `pages` directory with your pages. Each page must be in its own directory. Post
directories must contain a `meta.yml` and a content file (`index.html`, `index.md` or `index.rst`).

### Static

Any files in your `static` directory will be copied into the site build root. Keep your CSS files
and such in this directory.

### Templates

Create Chameleon templates for your site in the `templates` directory. See the [Chameleon
docs](https://chameleon.readthedocs.io/en/latest/) for reference.

## Configuration

The Beemo config file is a YAML file with three optional top-level sections: `build`, `logs`,
and `report`. All paths are relative to the config file.

### Site build

The `build` section configures the `beemo` site builder. Here `pages_dir` and `posts_dir` are
both specified — the site will be built with both pages and blog posts:

```yml
build:
  posts_dir: content/posts
  pages_dir: content/pages
  static_dir: static
  templates_dir: templates
  blog_root: blog
  output_dir: www
```

Omit `pages_dir` for blog-only mode, or omit `posts_dir` for pages-only mode. Either one must
be present. If `posts_dir` is specified, archives, tag indexes and such are generated
automatically.

### Log analytics

Optional `logs` and `report` sections configure the `beemo-logs` and `beemo-report` commands.
`templates_dir` and `manifest` are taken from the `build` section automatically.

```yml
logs:
  logs_dir: ../apache2               # directory of gzipped Apache log files
  csv_dir: ../csv                    # output directory for processed CSVs
  pattern: "bennuttall.com-access*"  # glob filter for log filenames

report:
  csv_dir: ../csv                    # input CSV directory
  output: ../html/summary.html       # report output path
  base_url: https://bennuttall.com
  title: ""                          # optional; derived from base_url and date range if omitted
```

### Environment variables

The only environment variable required is `BEEMO_CONFIG` which must point to your site's config
file:

```
export BEEMO_CONFIG=config.yml
```

## Install

Install the latest release with:

```
pip install beemo
```

For Apache log analytics, install the `logs` extra:

```
pip install beemo[logs]
```

### Development

Create a virtual environment and run `make develop` to install the library and its dependencies.

This can be served locally with e.g. `python -m http.server -d www` and viewed at e.g.
`http://localhost:8000`.

### Build

Build your site by running the command `beemo` with the environment variable `BEEMO_CONFIG` set
pointing at a valid config file. It will build your site into your configured `output_dir`.

### Log analytics

With `beemo[logs]` installed and `logs`/`report` sections in your config, run the full pipeline:

```bash
beemo-logs       # process Apache gz logs → CSV files
beemo            # build site and generate manifest.json
beemo-report     # generate HTML analytics report
```

All three commands read their defaults from `BEEMO_CONFIG`. Any setting can be overridden on the
command line — run with `--help` for details.

## Examples

Sites built with Beemo:

- [bennuttall.com](https://bennuttall.com) ([repo](https://github.com/bennuttall/web-content))
- [blog.piwheels.org](https://blog.piwheels.org) ([repo](https://github.com/piwheels/blog))
- [pynw.org](https://pynw.org/) ([repo](https://github.com/pythonnorthwestengland/pynw.org))
- [pyjok.es](https://pyjok.es/) ([repo](https://github.com/pyjokes/website))

If you wish to use this project for your own website, these examples will be a useful reference.

## Licence

- [BSD-3-Clause](LICENSE.txt)