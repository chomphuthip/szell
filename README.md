# szell
An extensible OSINT knowledge consolidation framework written in Python.

Szell is a knowledge consolidation framework that uses plugins written in Python to consolidate the results of OSINT tools into a single XLSX file. Plugins are written in Python and expose a ```process()``` function that takes input defined in the ```config``` file and the master XLSX workbook. Plugins processing is extremely flexible, allowing for groups of plugins to be run in sequence or in parallel.

### config.json

Szell loads the ```config.json``` file that contains a ```plugins``` array and an ```input``` object. The ```plugins``` array contains plugins that will be ran sequencially. However, putting multiple plugins in a single array element will result in those plugins being run in parallel.

```
"plugins: ["plugin1", "plugin2", "plugin3"]
``` 
will result in sequential execution, starting with ```plugin1```.

```
"plugins: [["plugin1", "plugin2"], "plugin3"]
``` 
will result in ```plugin1``` and ```plugin2``` running in parrellel and ```plugin3``` running after.

The ```input``` object contains the input that will be passed to each plugin. Each plugin is a Python file that defines a ```process``` function. The ```process``` function takes two parameters, ```input``` and ```workbook``` and returns a ```book```. If the ```input``` object is declared as:
```
...
    "input" : {
        "foo": {
            "bar": ["baz", "bed"]
        }
    }
...
```
The ```foo``` plugin will be passed ```"bar": ["baz", "bed"]```.

### Plugins
Szell loads plugins based on the plugin names in ```config.json```. [importlib](https://docs.python.org/3/library/importlib.html) is used to import plugins at runtime. Plugins _MUST_ have the same filename as it is in the ```plugins``` array in ```config.json```. A ```foo``` plugin will be defined in the ```foo.py``` file.

Plugins take ```input``` and ```workbook``` as parameters to the ```process``` funtion. The ```input``` parameter is a dictionary object derived from the corresponding object defined in ```config.json```.  Plugins have the ability to read from the master workbook through the ```workbook``` parameter. **DO NOT DIRECTLY MANIPULATE THE MASTER WORKBOOK IN A PLUGIN**. Szell uses [openpyxl](https://openpyxl.readthedocs.io/en/stable/) to read, write, and manipulate XLSX files. Plugins must return a Workbook object that will be appended to the master workbook. Since the workbook is passed to the plugin, post reconissiance plugins that use prior collected data can easily be implemented. Plugins that are thin wrappers around powerful tools such as [theHarvester](https://github.com/laramies/theHarvester) and [Recon-ng](https://github.com/lanmaster53/recon-ng) are not only  trivial to write, but using Szell, can be ran in parallel and then have their data consolidated.

### Why XLSX?
XLSX files are a happy medium between human readability, arbitrary data accessability, and serialization. 
