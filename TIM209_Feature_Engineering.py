#!/usr/bin/env python

import TIM209_Bank_Failure_Baseline as base
import os


def process_sheets_no_index(sheets, column, start_row, end_row, filename):
    print len(sheets)
    i = 1
    for sheet in sheets:
        # print sheet
        outfile = open(filename, 'a+')
        print "File Opened."
        if os.stat(filename).st_size == 0:
            for rows in sheet[str(str(column) + str(start_row)):str(str(column) + str(end_row))]:
                for cell in rows:
                    if cell.value == "#N/A N/A":
                        outfile.write("0 ")
                        outfile.write("\n")
                    else:
                        outfile.write(str(cell.value) + " ")
                        outfile.write("\n")
        else:
            cells = []
            for rows in sheet[str(str(column) + str(start_row)):str(str(column) + str(end_row))]:
                for cell in rows:
                    if cell.value == "#N/A N/A":
                        cells.append(0)
                    else:
                        cells.append(cell.value)

            outfile.seek(0)
            lines = outfile.readlines()
            outfile.close()
            j = 0
            outfile = open(filename, 'w')
            for line in lines:
                if j <= (end_row - start_row):
                    outfile.write('%s%s%s\n' % (line.rstrip('\n'), str(cells[j]), " "))
                    # outfile.write("\n")
                    j += 1
                else:
                    break
        outfile.close()
        print "File Closed"
        i += 1


def process_sheets_failed_banks_no_index(sheets, columns, start_row, end_row, filename):
    print len(sheets)
    i = 1
    k = 0
    for sheet in sheets:
        # print sheet
        outfile = open(filename, 'a+')
        print "File Opened."
        count = start_row
        if os.stat(filename).st_size == 0:
            for column in columns:
                cell_val = sheet[str(column) + str(count)].value
                if cell_val == "#N/A N/A":
                    outfile.write("0 ")
                else:
                    outfile.write(str(cell_val) + " ")
                outfile.write("\n")
                count += 1
            # outfile.close()
        else:
            cells = []
            for column in columns:
                cell_val = sheet[str(column) + str(count)].value
                if cell_val == "#N/A N/A":
                    cells.append(0)
                else:
                    cells.append(cell_val)
                count += 1
                # print cell_val

            outfile.seek(0)
            lines = outfile.readlines()
            outfile.close()
            j = 0
            outfile = open(filename, 'w')
            for line in lines:
                if j <= (end_row - start_row):
                    outfile.write('%s%s%s\n' % (line.rstrip('\n'), str(cells[j]), " "))
                    # outfile.write("\n")
                    j += 1
                else:
                    break
        outfile.close()
        print "File Closed"
        i += 1


def store_txt_file_as_list(filename):

    return [line.split() for line in open(filename)]


def feature_engineering(list_of_list):
    features = []
    for col in list_of_list:
        temp_list = []
        # print("col[11] =", col[11])
        # print("col[4] =", col[4])
        temp_list.append((float(col[11]) + 1) / (float(col[4]) + 1))
        temp_list.append((float(col[3]) + 1) / (float(col[4]) + 1))
        temp_list.append((float(col[31]) + 1) / (float(col[3]) + 1))
        temp_list.append((float(col[32]) + 1) / (float(col[3]) + 1))
        temp_list.append(((float(col[33]) + 1) + float(col[34])) / (float(col[3]) + 1))
        temp_list.append((float(col[22]) + 1) / (float(col[3]) + 1))
        temp_list.append((float(col[36]) + 1) / (float(col[3]) + 1))
        temp_list.append((float(col[7]) + 1) / (float(col[25]) + 1))
        temp_list.append((float(col[7]) + 1) / (float(col[4]) + 1))
        temp_list.append(((float(col[19]) + 1) + float(col[20])) / (float(col[4]) + 1))
        temp_list.append((float(col[25]) + 1) / (float(col[4]) + 1))
        temp_list.append(float(col[18]) / (float(col[19]) + 1))
        temp_list.append((float(col[25]) + 1) / ((float(col[19]) + 1) + float(col[20])))
        temp_list.append((float(col[7]) + 1) / (float(col[4]) + 1))
        temp_list.append((float(col[7]) + 1) / (float(col[11]) + 1))
        temp_list.append((float(col[19]) + 1) / (float(col[2]) + 1))
        temp_list.append((float(col[17]) + 1) / (float(col[25]) + 1))
        temp_list.append((float(col[28]) + 1) / (float(col[4]) + 1))
        temp_list.append(((float(col[28]) + 1) + float(col[37])) / (float(col[4]) + 1))
        temp_list.append((float(col[3]) + 1) / (float(col[2]) + 1))
        # print temp_list
        features.append(temp_list)

    print(features)
    return features


def write_list_to_libsvm_file(list_of_list, filename, label):
    outfile = open(filename, 'a+')
    print "File Opened."

    for list in list_of_list:
        i = 1
        outfile.write(str(label) + " ")
        for item in list:
            outfile.write(str(i) + ":" + str(item))
            if (i < len(list)):
                outfile.write(" ")
            i += 1
        outfile.write("\n")

    outfile.close()


def write_list_to_file(list_of_list, filename):
    outfile = open(filename, 'a+')
    print (filename + "File Opened.")

    for list in list_of_list:
        i = 1
        for item in list:
            outfile.write(str(item))
            if (i < len(list)):
                outfile.write(" ")
            i += 1
        outfile.write("\n")

    outfile.close()
    print (filename + "File Closed.")


if __name__ == '__main__':

    data_file = "BankList_Values_20161124.xlsx"
    data_file2 = "BankList_Values_20161115.xlsx"

    sheets = base.read_file(data_file)
    sheets2 = base.read_file(data_file2)
    sheets_total = sheets + sheets2
    print len(sheets_total)

    columns = ['AK', 'AI', 'BK', 'AM', 'AO', 'BG', 'AJ', 'BC', 'AJ', 'AR', 'AF', 'AY', 'AK', 'AJ', 'AB', 'BE', 'AN',
              'AJ', 'AJ', 'AC', 'AI', 'AN', 'AV', 'AJ', 'AS', 'AL', 'AM', 'AP', 'AD', 'AP', 'AR', 'AQ', 'AI', 'AM']

    label_failed = 0
    label_active = 1
    failed_file = "failed_banks_space_delimited.txt"
    process_sheets_failed_banks_no_index(sheets_total, columns, 3, 36, failed_file)

    active_file = "active_banks_space_delimited.txt"
    column_used_active_banks = 'AI'
    process_sheets_no_index(sheets_total, column_used_active_banks, 38, 167, active_file)
    failed_list = store_txt_file_as_list(failed_file)
    active_list = store_txt_file_as_list(active_file)
    failed_feature_list_of_list = []
    active_feature_list_of_list = []
    # print(failed_list[0])
    # print(failed_list[33])
    # print(failed_list[33][0])
    # print(failed_list[0][38])
    failed_feature_list_of_list = feature_engineering(failed_list)
    active_feature_list_of_list = feature_engineering(active_list)
    print(failed_feature_list_of_list)
    fe_file = "banks_feature_eng_AI_1colBeforeFailed_libsvm.txt"
    write_list_to_libsvm_file(failed_feature_list_of_list, fe_file, label_failed)
    write_list_to_libsvm_file(active_feature_list_of_list, fe_file, label_active)

    fe_file_sp_delimit = "banks_feature_eng_AI_1colBeforeFailed.txt"
    write_list_to_file(failed_feature_list_of_list, fe_file_sp_delimit)
    write_list_to_file(active_feature_list_of_list, fe_file_sp_delimit)

    training_file = "training_feature_eng.txt"
    test_file = "test_feature_eng.txt"
    base.split_into_training_test(fe_file, training_file, test_file)
    print(base.file_length(failed_file))
    print(base.file_length(active_file))
    print(base.file_length(fe_file))
    print (base.file_length(fe_file_sp_delimit))
    print (base.file_length(training_file))
    print(base.file_length(test_file))