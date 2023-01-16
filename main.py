import json
import openpyxl as xl
import pluginhandler as ph

def main():
    configHandle = open('config.json')
    config = json.load(configHandle)

    workbook = xl.Workbook()

    for i in range(len(config['plugins'])):
        if type(config['plugins'][i]) == list:
            ph.run_parallel(config['plugins'][i], config['input'], workbook)
        else:
            ph.run_plugin(config['plugins'][i], config['input'], workbook)

    workbook.save('intel.xlsx')

if __name__ == "__main__":
    main()
