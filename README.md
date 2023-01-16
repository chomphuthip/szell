# szell
An extensible OSINT knowledge consolidation framework written in Python.

Szell is a knowledge consolidation framework that uses plugins written in Python to consolidate the results of OSINT tools into a single XLSX file. Plugins are written in Python and expose a ```process()``` function that takes input defined in the ```config``` file and the master XLSX workbook. Plugins processing is extremely flexible, allowing for groups of plugins to be run in sequence or in parallel.

Szell loads the ```config.json``` file that contains a ```plugins``` array and an ```input``` object. The ```plugins``` array contains plugins that will be ran sequencially. However, putting multiple plugins in a single array element will result in those plugins being run in parallel.

```"plugins: ["plugin1", "plugin2", "plugin3"]``` will result in sequential execution, starting with ```plugin1```.

```"plugins: [["plugin1", "plugin2"], "plugin3"]``` will result in ```plugin1``` and ```plugin2``` running in parrellel and ```plugin3``` running after.
