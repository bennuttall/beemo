==========
beemo logs
==========

.. program:: beemo-logs

Process Apache log files into CSV. Gzipped logs matched by ``--pattern`` are parsed once and
cached (a file is skipped if its CSV already exists). Non-gzipped logs matched by
``--live-pattern`` — the live access log, and any log rotated but not yet gzipped — are always
reprocessed, since they can still be growing.

.. code-block:: text

    Usage: beemo logs [OPTIONS] [INPUT]

Arguments
=========

.. option:: INPUT

    gz file or directory of log files.

Options
=======

.. option:: --csv-dir PATH

    Output directory for CSV files.

.. option:: --pattern TEXT

    Filename glob pattern for gzipped logs when input is a directory.

.. option:: --live-pattern TEXT

    Glob pattern for non-gzipped live/rotated logs, always reprocessed. Only applies when input is
    a directory; unset by default (disabled).

.. option:: --help

    Show this message and exit.
