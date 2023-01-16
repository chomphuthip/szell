import importlib
import concurrent.futures

def append_book(src_book, dest_book):
    for src_sheet in src_book:
        dest_sheet = dest_book.create_sheet(src_sheet.title)
        for row in range(1, src_sheet.max_row + 1):
            for column in range(1, src_sheet.max_column + 1):
                cell = src_sheet.cell(row=row, column=column)
                dest_sheet.cell(row=row, column=column).value = cell.value


def run_parallel(names, input, workbook):
    plugins = []
    for name in names:
        plugins.append(importlib.import_module(name))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(plugins[i].process, input[names[i]], workbook) for i in range(len(plugins))]
        for future in concurrent.futures.as_completed(futures):
            result_book = future.result()
            append_book(result_book, workbook)
            result_book.close()
            



def run_plugin(name, input, workbook):
    plugin = importlib.import_module(name)
    book = plugin.process(input[name], workbook)
    append_book(book, workbook)