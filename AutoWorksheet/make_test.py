import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import numpy as np
import openpyxl
from rpa import make_template

def rand_worktime():
    int_part = np.random.randint(0,6,31)
    deci = [0.25, 0.5, 0.75, 1.0]
    work_time = []
    for i in range(31):
        work_time.append(float(int_part[i] * np.random.choice(deci)))
    return work_time

if __name__ == '__main__':
    for m in range(12):
        year = '2017'
        month = str(m+1)
        make_template.make_template(int(year), int(month))
        workbook = openpyxl.load_workbook(f'worksheet_{year}_{month}.xlsx')
        sheet = workbook["Sheet"]
        ran = rand_worktime()
        for i in range(16):
            sheet[f'E{2*i+5}'] = ran[i]
        for i in range(15):
            sheet[f'S{2*i+5}'] = ran[i+16]
        workbook.save(f'worksheet_{year}_{month}.xlsx')