#!/usr/bin/env python

import TIM209_Bank_Failure_Baseline as base
import os


def process_sheets_no_index_discard_0(sheets, start_col, end_col, start_row, end_row, filename):
    print len(sheets)

    list_of_sheets = []
    sum_quarters = 0

    for sheet in sheets:
        list_of_banks = []
        for row in sheet[str(str(start_col) + str(start_row)):str(str(end_col) + str(end_row))]:
            cells = []
            for cell in row:
                if cell.value == "#N/A N/A":
                    cells.append(0)
                else:
                    cells.append(cell.value)
            list_of_banks.append(cells)
            sum_quarters = len(cells)
        list_of_sheets.append(list_of_banks)

    outfile = open(filename, 'w')
    print filename, "File Opened."
    print "Number of Quarters = ", sum_quarters
    print "Number of Sheets = ", len(list_of_sheets)
    i = 0
    v = 0
    for k in range(sum_quarters):
        for j in range(end_row - start_row + 1):
            for i in range(len(list_of_sheets)):
                v = list_of_sheets[i][j][k]
                if (i == 0 and v == 0):
                    break
                else:
                    outfile.write(str(v) + " ")
            if (i == 0 and v == 0):
                pass
            else:
                outfile.write("\n")
                i = 0
    print "(Cash, AMFC, C) =", list_of_sheets[28][0][1]
    print "(ST_AND_LT, CKFC, D) =", list_of_sheets[30][1][3]

    outfile.close()
    print filename, "File Closed"


def process_sheets_failed_banks_no_index_discard_0(sheets, columns, start_row, end_row, filename):
    print len(sheets)
    no_value = []

    for sheet in sheets:
        outfile = open(filename, 'a+')
        print (filename, "File Opened.")
        count = start_row
        if os.stat(filename).st_size == 0:
            for column in columns:
                cell_val = sheet[str(column) + str(count)].value
                if cell_val == "#N/A N/A":
                    no_value.append(count)
                    count += 1
                    continue
                else:
                    outfile.write(str(cell_val) + " ")
                    count += 1
                outfile.write("\n")
        else:
            cells = []
            for column in columns:
                if count in no_value:
                    count += 1
                    continue
                cell_val = sheet[str(column) + str(count)].value
                if cell_val == "#N/A N/A":
                    cells.append(0)
                else:
                    cells.append(cell_val)
                count += 1

            outfile.seek(0)
            lines = outfile.readlines()
            outfile.close()
            print("Length of lines =", len(lines))
            print("Length of cells =", len(cells))
            j = 0
            outfile = open(filename, 'w')
            for line in lines:
                if j <= (end_row - start_row):
                    outfile.write('%s%s%s\n' % (line.rstrip('\n'), str(cells[j]), " "))
                    j += 1
                else:
                    break
        outfile.close()
        print (filename, "File Closed")


if __name__ == '__main__':

    data_file = "BankList_Values_20161124.xlsx"
    data_file2 = "BankList_Values_20161115.xlsx"

    sheets = base.read_file(data_file)
    sheets2 = base.read_file(data_file2)
    sheets_total = sheets + sheets2
    print len(sheets_total)

    ##### Better to write these columns into a file.
    columns1 = ['AK', 'AI', 'BK', 'AM', 'AO', 'BG', 'AJ', 'BC', 'AJ', 'AR', 'AF', 'AY', 'AK', 'AJ', 'AB', 'BE', 'AN',
              'AJ', 'AJ', 'AC', 'AI', 'AN', 'AV', 'AJ', 'AS', 'AL', 'AM', 'AP', 'AD', 'AP', 'AR', 'AQ', 'AI', 'AM']

    columns2 = ['AJ', 'AH', 'BJ', 'AL', 'AN', 'BF', 'AI', 'BB', 'AI', 'AQ', 'AE', 'AX', 'AJ', 'AI', 'AA', 'BD', 'AM',
              'AI', 'AI', 'AB', 'AH', 'AM', 'AU', 'AI', 'AR', 'AK', 'AL', 'AO', 'AC', 'AO', 'AQ', 'AP', 'AH', 'AL']

    columns3 = ['AI', 'AG', 'BI', 'AK', 'AM', 'BE', 'AH', 'BA', 'AH', 'AP', 'AD', 'AW', 'AI', 'AH', 'Z', 'BC', 'AL',
                'AH', 'AH', 'AA', 'AG', 'AL', 'AT', 'AH', 'AQ', 'AJ', 'AK', 'AN', 'AB', 'AN', 'AP', 'AO', 'AG', 'AK']

    columns4 = ['AH', 'AF', 'BH', 'AJ', 'AL', 'BD', 'AG', 'AZ', 'AG', 'AO', 'AC', 'AV', 'AH', 'AG', 'Y', 'BB', 'AK',
                'AG', 'AG', 'Z', 'AF', 'AK', 'AS', 'AG', 'AP', 'AI', 'AJ', 'AM', 'AA', 'AM', 'AO', 'AN', 'AF', 'AJ']

    label_failed = 0
    label_active = 1
    # cols = 4
    # failed_files = []
    # for i in range(cols):
    #     failed_files.append("failed_banks_col" + str(i+1) + "_space_delimited.txt")
    #
    # for f in failed_files:
    #     process_sheets_failed_banks_no_index_discard_0(sheets_total, columns1, 3, 36, f)

    ##### Have to save as 4 files because of outfile.seek(0) and outfile.readlines()
    ##### in process_sheets_failed_banks_no_index_discard_0().
    failed_file1 = "failed_banks_col1_space_delimited.txt"
    failed_file2 = "failed_banks_col2_space_delimited.txt"
    failed_file3 = "failed_banks_col3_space_delimited.txt"
    failed_file4 = "failed_banks_col4_space_delimited.txt"

    process_sheets_failed_banks_no_index_discard_0(sheets_total, columns1, 3, 36, failed_file1)
    process_sheets_failed_banks_no_index_discard_0(sheets_total, columns2, 3, 36, failed_file2)
    process_sheets_failed_banks_no_index_discard_0(sheets_total, columns3, 3, 36, failed_file3)
    process_sheets_failed_banks_no_index_discard_0(sheets_total, columns4, 3, 36, failed_file4)

    active_file = "active_banks_allBut1516_space_delimited.txt"
    last_column_used_active_banks = 'BI'
    process_sheets_no_index_discard_0(sheets_total, "B", last_column_used_active_banks, 38, 167, active_file)

    print(base.file_length(failed_file1))
    print(base.file_length(failed_file2))
    print(base.file_length(failed_file3))
    print(base.file_length(failed_file4))
    print(base.file_length(active_file))
