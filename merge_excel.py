import xlrd
import openpyxl
import pandas as pd


def get_input_excel(excel_list, title):

    concat_excel = None
    for excel in excel_list:
        read_excel = pd.read_excel(excel)
        if concat_excel is None:
            concat_excel = read_excel
        else:
            concat_excel = pd.concat([concat_excel, read_excel], ignore_index=True)

    concat_excel.to_excel(title, index=None, header=True)


def main():

    input_excel = input("Excel list(seperated by comma) : ")
    output_excel = input("Output File name : ")
    excel_list = input_excel.split(',')
    get_input_excel(excel_list, output_excel)


if __name__ == "__main__":

    main()