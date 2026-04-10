from datetime import datetime


beemo_version = "0.5.0"

# -- General configuration ------------------------------------------------

project = "beemo"
version = beemo_version
release = version
author = "Ben Nuttall"
extensions = ["sphinx_rtd_theme"]
html_theme = "sphinx_rtd_theme"
copyright = "2025-%s %s" % (datetime.now().year, author)
html_title = "%s %s Documentation" % (project, version)
pygments_style = "sphinx"
