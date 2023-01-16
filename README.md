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
            "domains": ["baz.com", "bed.com"]
        }
    }
...
```
The ```foo``` plugin will be passed ```"domains": ["baz.com", "bed.com"]```.

### Plugins
Szell loads plugins based on the plugin names in ```config.json```. [importlib](https://docs.python.org/3/library/importlib.html) is used to import plugins at runtime. Plugins _MUST_ have the same filename as it is in the ```plugins``` array in ```config.json```. A ```foo``` plugin will be defined in the ```foo.py``` file.

Plugins take ```input``` and ```workbook``` as parameters to the ```process``` funtion. The ```input``` parameter is a dictionary object derived from the corresponding object defined in ```config.json```.  Plugins have the ability to read from the master workbook through the ```workbook``` parameter. **THE MASTER WORKBOOK SHOULD NOT BE DIRECTLY MODIFIED BY PLUGINS**. Szell uses [openpyxl](https://openpyxl.readthedocs.io/en/stable/) to read, write, and manipulate XLSX files. Plugins must return a Workbook object that will be appended to the master workbook. Since the workbook is passed to the plugin, post reconissiance plugins that can do addition research and processing based on prior collected data can be easily implemented. Plugins that are thin wrappers around powerful tools such as [theHarvester](https://github.com/laramies/theHarvester) and [Recon-ng](https://github.com/lanmaster53/recon-ng) are not only  trivial to write, but using Szell, can be ran in parallel and then have their data consolidated.

### Why XLSX?
XLSX files are a happy medium between human comprehension, arbitrary data accessability, and serialization. A master text file might provide a very accurate and fully formed desciption of an entity, but it would be difficult to access a list of hostnames or try and loop over those hostnames. A wiki-style database might make specific data more accessable, but would make it harder for someone to understand the big-picture of an entity and would also have awkward raw data storage. A JSON file might format data into a more easily transfered and manipulated but it would be difficult to understand the totality of that data. The XLSX file format trades a slight loss in human readability for huge gains in accessability and serialization. XLSX also allows for realtime collaboration between teammates in the form of the famous Google Sheets and other Saas products, leading to greater productivity and less time wasted manually sharing intelligence.

### Limitations of the XLSX format
The XLSX format does not scale very well and software often used to open XLSX files are not optimized to open and manipulate large (>2GB) files. XLSX is more suited towards storing intelligence on smaller to medium sized organizations due to these limitations. 
