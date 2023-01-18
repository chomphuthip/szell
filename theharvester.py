import openpyxl as xl
import re
import subprocess

class Cursor:
    def __init__(self):
        self._row = 1
        self._column = 1

    def column(self):
        return self._column

    def row(self):
        return self._row

    def move_down(self):
        self._row += 1

    def move_up(self):
        self._row -= 1

    def move_right(self):
        self._column += 1

    def move_left(self):
        self._column -= 1

    def write(self, value, sheet):
        sheet.cell(row=self.row(), column=self.column()).value = value

def extract(section, split_list):
    section_re = re.compile('.*' + section + '.*')
    section_info = list(filter(section_re.match, split_list))[0]
    print(section_info)
    if section_info != '[*] No ' + section + ' found.':
        number_of_entries = int(section_info.split()[len(section_info.split())-1])
        start_of_entries = split_list.index(section_info) + 2
        return split_list[start_of_entries:number_of_entries]
    else:
        return list()

def write_section(section_name, section, cursor, sheet):
    if section == []:
        cursor.write('No ' + section_name + ' found.', sheet)
        cursor.move_down()
    else:
        cursor.write(str(len(section)) + ' '+ section_name + ' found:', sheet)
        cursor.move_down()
        for entry in section:
            cursor.write(entry, sheet)
            cursor.move_down()
    cursor.move_down()


def process(input, workbook):

    #PROLOG
    book = xl.Workbook()
    sheet = book.active
    sheet.title = 'theHarvester ' + input['domain']

    result = subprocess.run(['theHarvester', '-d'+input['domain'], '-b'+str(input['sources']).strip('[]\'').replace(' ','')], capture_output=True)
    split_list = str(result.stdout, 'UTF-8').split('\n')

    
    #EXTRACTION
    ips = extract('IPs', split_list)
    emails = extract('emails', split_list)
    hosts = extract('Hosts', split_list)

    #WRITING 
    cursor = Cursor()
    write_section('IPs', ips, cursor, sheet)
    write_section('Emails', emails, cursor, sheet)
    write_section('Hosts', hosts, cursor, sheet)

    return book