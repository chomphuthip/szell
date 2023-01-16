import openpyxl as xl

def process(input, workbook):

    print(input)

    book = xl.Workbook()
    sheet = book.active
    sheet['a1'] = 'names:'
    sheet.title = 'tool1'

    for i in range(len(input['names'])):
        sheet.cell(row=i+2, column=1).value = input['names'][i]
    return book