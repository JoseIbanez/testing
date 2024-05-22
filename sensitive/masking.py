#!/usr/bin/env python3

"""
Anonymize a customers file in csv format.
@Jose Ibanez Vela
"""

SENSITIVE_FIELDS_TEXT = [ "Name", "Email"] 
SENSITIVE_FIELDS_NUMBER = [ "Billing" ] 
SPECIAL_CHARS = "@. "
REPORT_COLUMNS = ["Name","Billing"]
STRIP_OUTPUT = True

class ReportItem:
    """
    Class to generate statistics report. You need an object per column to report
    """

    def __init__(self,name):
        self.name:str = name
        self.min:float|None = None
        self.max:float|None = None
        self.count:int = 0
        self.sum:float = 0

    def update(self,value:int|float):
        """
        Update reportItem with new value
        """

        if self.max is None or value > self.max:
            self.max = value

        if self.min is None or value < self.min:
            self.min = value

        self.sum += value
        self.count += 1


    def __str__(self):
        """
        Pretty print
        """
        return f"{self.name}: Max. {self.max}, Min. {self.min}, Avg. {self.sum/self.count}"


def masking_file(in_filename:str,out_filename:str):
    """
    Main funcion. Iterates on file lines, generate output file, and statistics report
    """

    col_names:list[str] = []
    numerical_cols:list[int] = []
    report:dict[str,ReportItem] = {}

    with open(in_filename, 'r', encoding='UTF-8') as file:
        filelines = file.readlines()

    output_file = open(out_filename, 'w', encoding='UTF-8')


    for line in filelines:

        # 1st line is the header, has the column names
        if not col_names:
            header = line.strip()
            output_file.write(header+'\n')

            # List with the names of the colls, ex: [ "ID","Name","Email",.... ]
            col_names = header.split(',')

            # List of the positions of the numerical (sensitive) colls, ex: [4]
            numerical_cols = [ idx 
                               for idx,name in enumerate(col_names) 
                               if name in SENSITIVE_FIELDS_NUMBER 
                             ] 
            continue

        # values line, one iteration per line
        value_in_list = line.strip().split(',')
        value_out_list = [ '' for i in range(len(col_names)) ]
        average = calculate_line_average(value_in_list,numerical_cols)

        for idx, col_name in enumerate(col_names):
            
            # input value, collumn value
            value = value_in_list[idx] 

            # output value
            if col_name in SENSITIVE_FIELDS_TEXT:
                value_out_list[idx] = mask_text_collumn(value)

            elif col_name in SENSITIVE_FIELDS_NUMBER:
                value_out_list[idx] = str(average)

            else: 
                value_out_list[idx] = value

            # update report
            if col_name in REPORT_COLUMNS:
                report = update_report(report,col_name,value)


        # output
        output_line = ",".join(value_out_list)
        output_file.write(output_line+'\n')

    output_file.close()

    # Print report
    for _,report_item in report.items():
        print(report_item)


def mask_text_collumn(value:str) -> str:
    """
    To mask a single cell.

    :value: input value
    :return: output value
    """

    # Remove initial and final spaces, just in case
    if STRIP_OUTPUT:
        value = value.strip()

    # Split, replace and join. No libraries :)
    masked = [ 'X' if x not in SPECIAL_CHARS else x for x in value ]
    result = ''.join(masked)

    return result


def calculate_line_average(value_in_list:list[str|int|float],numerical_cols:list[int]) -> float:
    """
    Calculate the average of the numeric (sensitive) collumns

    :value_in_list: list of all values of a row
    :numerical_cols: position of the numeric collumns
    
    :return: avg. value of the collumns
    """

    if not numerical_cols or len(numerical_cols) == 0:
        return 0

    sum_ = 0
    for idx in numerical_cols:

        try:
            value = float(value_in_list[idx]) 
        except ValueError:
            value = 0

        sum_ += value

    average = sum_/len(numerical_cols)
    return average


def update_report(report:dict[str,ReportItem],col_name:str,value):
    """
    Update report list with a new value, col_name and col value
    """

    # Init report item
    if not report.get(col_name):
        report[col_name]=ReportItem(col_name)

    # Get value for report, float for number, len for strings
    if col_name in SENSITIVE_FIELDS_NUMBER:
        try:
            value_report = float(value)
        except ValueError:
            value_report = 0

    else: 
        value_report = len(value)

    # update parameters with new value
    report[col_name].update(value_report)

    return report 




def main():
    """
    Get input parameter, input file
    Execute main function, masking file
    """

    # I whould like to use argparse lib to get input param, and show shome help, but not
    # libraries for this exercise
    input_filename = input("Input filename to anonymize: ")
    output_filename = "./masked_clients.csv"
    
    try:
        masking_file(input_filename,output_filename)

    except OSError as err:
        print("OS error:%s",err)


if __name__ == '__main__':
    main()




