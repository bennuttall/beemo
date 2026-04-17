from datetime import datetime


beemo_version = "0.5.0"

# -- General configuration ------------------------------------------------

project = "beemo"
version = beemo_version
release = version
author = "Ben Nuttall"
extensions = ["sphinx_rtd_theme", "sphinxcontrib.autodoc_pydantic"]
html_theme = "sphinx_rtd_theme"
copyright = "2025-%s %s" % (datetime.now().year, author)
html_title = "%s %s Documentation" % (project, version)
pygments_style = "sphinx"
autodoc_member_order = "bysource"

autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_validators = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_field_list_validators = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3.10", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}
