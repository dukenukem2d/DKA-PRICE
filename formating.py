"""
Модуль форматирования прайс листа
"""
from typing import Union
import pandas as pd # type: ignore

def formating(file_: bytes, customer_id: Union[str, None], now) -> None:
    """
    Функция форматирования
    # """
    df_ = pd.read_excel(file_, skiprows=10, usecols="A:C,E,F,I,J,M:S,U", engine='xlrd')
    df_ = df_.assign(Order='', Order_Sum='')
    df_['Quantity'] = df_['Quantity'].fillna(0)

    writer = pd.ExcelWriter(f'Price_list-{customer_id}-{now}.xlsx', engine='xlsxwriter') # pylint: disable=abstract-class-instantiated
    df_.to_excel(writer, sheet_name='Price_list', index=False, startrow=5)

    workbook = writer.book # pylint: disable=no-member
    worksheet = writer.sheets['Price_list']

    header_format = workbook.add_format({
        'bold': True,
        # 'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'fg_color': '#89FFBE',
        'border': 1})

    total_format = workbook.add_format({
        'bold': True,
        'border': 1})

    small_header_format = workbook.add_format({
        'bold': True,
        'border': 1,
        'align': 'center',
        'fg_color': '#89FFBE'})  # 41E3A1

    money_format = workbook.add_format({'num_format': '\"$ "# ##0.00_ ;-"$ "# ##0.00',
                                        'border': 1
                                        })

    money_format_ = workbook.add_format({'num_format': '\"$ "# ##0.00_ ;-"$ "# ##0.00'
                                         })

    volume_format = workbook.add_format({'num_format': '# ##0.000000'})

    cell_format = workbook.add_format({'border': 1,
                                       'num_format': '# ##0.00'})

    cbm_format = workbook.add_format({'border': 1,
                                      'num_format': '# ##0.0000'})

    cell_format_ = workbook.add_format({'border': 1})

    cell_format_order = workbook.add_format(
        {'bg_color': '#FFFFBE', 'border': 1})

    for col_num, value in enumerate(df_.columns.values):
        worksheet.write(5, col_num, value, header_format)

    columns = (10, 13, 13, 13, 16, 16, 30, 13, 13, 14, 12, 13, 12, 14, 14, 12, 19)
    for i, c_width in enumerate(columns):
        worksheet.set_column(i, i, c_width)

    # price column
    worksheet.set_column(13, 13, 14, money_format_)
    # volume column
    worksheet.set_column(9, 9, 14, volume_format)

    worksheet.write_string('A4', 'Customer:')
    worksheet.write_string('B4', f'{customer_id}')
    worksheet.write_string('A5', 'Currency:')
    worksheet.write_string('B5', 'USD')

    # Tables with reserve totals
    worksheet.write_string('N2', 'Total weight', total_format)
    worksheet.write_string('N3', 'Total CBM', total_format)
    worksheet.write_string('N4', 'Total Cartoons', total_format)
    worksheet.write_string('N5', 'Total Sum', total_format)

    # Small table's header
    worksheet.write_string('N1', '', small_header_format)
    worksheet.write_string('O1', 'Reserved', small_header_format)
    worksheet.write_string('P1', 'Order', small_header_format)
    worksheet.write_string('Q1', 'Total Res + Ord', small_header_format)

    # add formulas for reserved goods
    row_numbers = df_.shape[0] + 6
    worksheet.write_dynamic_array_formula(
        'O2', f'=SUM($I$7:$I${row_numbers}*$O$7:$O${row_numbers})', cell_format)  # Total weight
    worksheet.write_dynamic_array_formula(
        'O3', f'=SUM($J$7:$J${row_numbers}*$O$7:$O${row_numbers})', cbm_format)  # Total CBM
    worksheet.write_dynamic_array_formula(
        'O4', f'=SUM($K$7:$K${row_numbers}*$O$7:$O${row_numbers})', cell_format_)  # Total Cartoons
    worksheet.write_dynamic_array_formula(
        'O5', f'=SUM($N$7:$N${row_numbers}*$O$7:$O${row_numbers})', money_format)  # Total SUM

    # add formulas for ordered goods
    worksheet.write_dynamic_array_formula(
        'P2', f'=SUM($I$7:$I${row_numbers}*$P$7:$P${row_numbers})', cell_format)  # Total weight
    worksheet.write_dynamic_array_formula(
        'P3', f'=SUM($J$7:$J${row_numbers}*$P$7:$P${row_numbers})', cbm_format)  # Total CBM
    worksheet.write_dynamic_array_formula(
        'P4', f'=SUM($K$7:$K${row_numbers}*$P$7:$P${row_numbers})', cell_format_)  # Total Cartoons
    worksheet.write_dynamic_array_formula(
        'P5', f'=SUM($N$7:$N${row_numbers}*$P$7:$P${row_numbers})', money_format)  # Total SUM

    # Formula Amount of ordered goods
    worksheet.write_dynamic_array_formula(
        f'Q7:Q{row_numbers}',    f'=(N7:N{row_numbers}*P7:P{row_numbers})', money_format_)

    # add formulas for ordered + reserved goods
    worksheet.write_formula('Q2', 'O2+P2', cell_format)  # Total weight
    worksheet.write_formula('Q3', 'O3+P3', cbm_format)  # Total CBM
    worksheet.write_formula('Q4', 'O4+P4', cell_format_)  # Total Cartoons
    worksheet.write_formula('Q5', 'O5+P5', money_format)  # Total SUM

    worksheet.freeze_panes(6, 0)

    worksheet.autofilter('A6:Q6')

    merge_format = workbook.add_format({
        # 'bold':     True,
        'align':    'center',
        'valign':   'vcenter',
        'font_name': 'Calibri',
        'font_size': 25
    })

    worksheet.merge_range('A1:L3', f'PRICE LIST {now}', merge_format)

    worksheet.conditional_format(f'A7:Q{row_numbers}', {
                                 'type': 'no_errors', 'format': cell_format_})
    worksheet.conditional_format(f'P7:P{row_numbers}', {
                                 'type': 'no_errors', 'format': cell_format_order})

    worksheet.set_zoom(67)

    writer.save()
