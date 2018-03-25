import os
import sys
import json

def check_file_existance(path,file_name):
    if file_name in os.listdir(path):
        return True
    else:
        return False

def create_file(file_name):
    with open(file_name,"a"):
        pass
    with open(file_name,"w"):
        pass

def read_file(file_name):
    with open(file_name,encoding = "ISO-8859-1") as f:
        return f.read()

def check_folder_existance(folder_name):
    if folder_name in os.listdir():
        return True
    else:
        return False

def create_folder(folder_name):
    os.mkdir(folder_name)
