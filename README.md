# szell
An extensible OSINT knowledge consolidation framework written in Python.

Szell is a knowledge consolidation framework that uses plugins written in Python to consolidate the results of OSINT tools into a single XLSX file. Plugins are written in Python and expose a ```process()``` function that takes input defined in the ```config``` file and the master XLSX workbook. Plugins processing is extremely flexible, allowing for groups of plugins to be run in sequence or in parallel.
