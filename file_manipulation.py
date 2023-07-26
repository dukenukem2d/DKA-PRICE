'''
Модуль для манипуляции с файлами
'''
# import os
# import glob
#
# def remove_files(file):
#     '''
#     Функция удаления старых excel файлов
#     '''
#     mylist = glob.glob('*.xlsx')
#     mylist.remove(file)
#     for _a in mylist:
#         os.remove(_a)
import os
import datetime

# Get the current date
# today = datetime.date.today()

# Get the current directory


def remove_old_files(today):
    dir_path = os.getcwd()

    # Loop through all files in the directory
    for filename in os.listdir(dir_path):
        # Check if the file is an Excel file
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            # Get the creation time of the file
            creation_time = datetime.date.fromtimestamp(
                os.path.getctime(filename))
            # Check if the file was created today
            if creation_time == today:
                # Print the file name
                print(filename)
            else:
                # Delete the file
                os.remove(filename)
