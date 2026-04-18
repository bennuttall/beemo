=========
Beemo CLI
=========

.. program:: beemo

The ``beemo`` command-line interface (CLI) provides a convenient way to build your website and
perform other tasks. Run ``beemo --help`` for a list of available commands and options.

.. code-block:: console

    $ beemo

    ╭─ Options ─────────────────────────────────────────────────────────────────────────────────╮
    │ --install-completion          Install completion for the current shell.                   │
    │ --show-completion             Show completion for the current shell, to copy it or        │
    │                               customize the installation.                                 │
    │ --help                        Show this message and exit.                                 │
    ╰───────────────────────────────────────────────────────────────────────────────────────────╯
    ╭─ Commands ────────────────────────────────────────────────────────────────────────────────╮
    │ build      Build the site.                                                                │
    │ logs       Process Apache log gz files into CSV.                                          │
    │ analytics  Generate HTML analytics site from log CSVs.                                    │
    ╰───────────────────────────────────────────────────────────────────────────────────────────╯

.. toctree::
   :maxdepth: 1

   build
   logs
   analytics