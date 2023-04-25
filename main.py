#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A Python Script to Filter All your combolist for Mailing Use

I Hope you Enjoy It !

Done BY :  OUZROUR
Date : 19.4.23
"""

__author__ = "Ilyas Ouzrour"
__version__ = "1.0.0"
__email__ = "ilyas.ouzrour@gmail.com"
__status__ = "Production"

# =======================
# STANDARD Libs
# =======================

# Read CSV file ( To Export Them )
import csv
# READ DIR / Files / Rename Sometimes
import os
# to filter ISPs
import re
# MOVE FILEs
import shutil
# delete duplicated lines in a csv file
import pandas
# CSV to Table To Stop The Big O(exp) -> I/O
import pyfiglet
# random name
import random
# for pause time
import time


# ===============================
# String Manipulation
# ===============================

def EraseEnd(word, end):
    """
    If The Word end with the substring , then this function return just the word without the substring
    :param word: the word that you want to modify
    :param end: the substring that may exist in the end of the suggested word
    :return: the word without the substring in the end
    """
    if end and word.endswith(end):
        return word[:-len(end)]
    return word


def endWith(list_words, ending):
    """
    A function that filter from a list of elements the ones that
    Ends With Some special substring and put them in a list ( in return )
    :param list_words: the list of words that you want to filter
    :param ending: the substring
    :return: a list of words that contain the substring in the end
    """
    return [word for word in list_words if word[len(word) - len(ending):] == ending]


# ===============================
# File Manipulation
# ===============================

def absolute_and_join(relative, other_folder):
    """
    transform from relative path to absolute , and join it in the end to another folder name
    :param relative: the relative folder
    :param other_folder: the folder we want to add it
    :return: the absolute path of the relative folder + the other folder
    """
    # transform the relative path to absolute
    absolute = os.path.abspath(relative)
    # return the absolute path joined with the name of the name of the other folder "..abs path../other_folder"
    return os.path.join(absolute, other_folder)


def the_dir_must_exist(absolute):
    """
    create the absolute path in case if it doesn't exist
    :param absolute: the absolute path of folder
    :return: Nothing. Just create the path if it doesn't exist
    """
    if not os.path.exists(absolute):
        os.mkdir(absolute)


def txt_to_csv(relative_dir_txt):
    """
    A Function to Convert text to csv : copy the content of the
    text file into the .csv file ( they have the same name , and
    belong to the same directory )
    :param relative_dir_txt: the relative of the file
    :return: Nothing .
    """
    with open(relative_dir_txt, 'r', encoding="utf8") as in_file:
        # To remove all the whitespaces if they exist from every line
        stripped = (line.strip() for line in in_file)
        # sprit the line in 2 parts : The part that contain Email and the part that contain password
        lines = (line.split(",") for line in stripped if line)
        # Create a new file with the same name but with another extension ".csv"
        with open(EraseEnd(relative_dir_txt, '.txt') + '.csv', 'w', newline='', encoding="utf8") as out_file:
            # we use csv to write the rows that are included in a variable "lines"
            # in our new files with the extension ".csv"
            csv.writer(out_file).writerows(lines)


def move_the_files(list_of_files, relative_source_folder, relative_destination_folder):
    """
    A function that move a list of files from a folder ( source ) to another folder ( destination ) ,
    if the file exist already in the destination folder , it changes the name of the file using a random
    number between 3 and 9999 and move it ( to avoid replacement )
    :param list_of_files: the names of the files that you want to move
    :param relative_source_folder: the relative path of the source folder , ex : '/xxx/'
    :param relative_destination_folder: the relative path of the another folder , ex : '/yyy/'
    :return: Nothing . Just move all the files from a directory to another
    """
    # For Loop in the list of names
    for file in list_of_files:
        # The Absolute path of the file ( source + file )
        source = absolute_and_join(relative_source_folder, file)
        # The Absolute path of the file after the move ( destination + file )
        destination = absolute_and_join(relative_destination_folder, file)

        # The List of files names to analysis it ( to check if the name of the file already
        # exist in the destination directory )
        list_of_files_names_in_destination_folder = os.listdir(os.path.abspath(relative_destination_folder))
        #  if the name of the file exist in the list of files ( in the destination folder )
        # then we must rename it ( else , it gonna replace the old one )
        if file in list_of_files_names_in_destination_folder:
            # Generate a random name for the file name ( ex : 666.name_of_file.extension )
            tempFileName = str(random.randint(3, 9999)) + "." + file
            # rename the file ( from name_of_file.extension => 9534.name_of_file.extension)
            os.rename(os.path.join(EraseEnd(os.path.abspath(file), file), relative_source_folder, file),
                      os.path.join(EraseEnd(os.path.abspath(file), file), relative_source_folder, tempFileName))
            # change the source directory ( because the name of the file has changed )
            source = absolute_and_join(relative_source_folder, tempFileName)
            # change the destination directory ( because the name of the file has changed )
            destination = absolute_and_join(relative_destination_folder, tempFileName)
        # move file
        shutil.move(source, destination)
        # Notification that the file have successfully moved
        print('Moved:', file)


def extract_mail_from_list_csv(relative_folder_of_csv, relative_destination_folder):
    """
    extract mails from a combo list of csv ( the list exist in the folder of the first parameter )
    :param relative_folder_of_csv: the folder where the CSVs exists
    :param relative_destination_folder: the Folder where the Extracted mails gonna go to
    :return: Nothing . Just extract mail from a list of csv
    """
    # List of Files in the relative_folder_of_csv
    folder = os.listdir(relative_folder_of_csv)
    # Filter only the name of files that end with ".csv"
    list_of_files_csv = endWith(folder, '.csv')
    # loop into the list of the names ( of the files ) that end with ".csv" in the folder relative_folder_of_csv
    for file in list_of_files_csv:
        # read every file
        with open(absolute_and_join(relative_folder_of_csv, file), 'r', encoding="utf8") as read_obj:
            # a csv function that convert a csv file to a list of lines
            csv_reader = csv.reader(read_obj)
            # Iterate over each row after the header in the csv ( don't forget that csv_reader is
            # a LIST of rows & that each row is a list of the content of each column , for example :
            # 'test1,test2,test3
            # test4,test5,test6'
            # gonna be transformed to :
            # [['test1','test2','test3'],['test4','test5','test6']]
            # in our situation , all rows have only 1 column so our list gonna be like
            # [ ['mail1@ISP1.com:password1'],['mail2@ISP2.com:password2'],['mail3@ISP3.com:password3']]
            # so Keep Attention when you want to manipulate the CSV files with the CSV library )
            for row in csv_reader:
                # 3 remarks :
                # 1. row variable is a list that represents a row in csv
                # 2. the row[0] in a combo list ( specially , after the transformation with the function
                # "txt_to_csv" ) always gonna be like this 'mail@ISP.com:password'
                # 3. arobase gonna find the position of the arobase to extract the ISP ( for example :
                #  ilyas.ouzrour@gmail.com ==> ISP : gmail )
                arobase = row[0].find('@')
                # search the position of ":" to extract the mail
                double_dots = row[0].find(':')
                # extract the mail : it begins from the start of the row to the character ":" ( without including it )
                Mail = row[0][0:double_dots]
                # extract the ISP : it begins from the arobase to the character ":" ( without including the 2 of them )
                Isp = row[0][arobase + 1:double_dots]
                # a list of all characters that are forbidden to be included in a folder name ( in Windows as I know )
                b = "*/\\|#%<>$+%!`&*'|{ }?=:"
                # remove these characters from ISP and Mail if they exist
                for char in b:
                    # replace any of these character if founded in ISP with a void string
                    Isp = Isp.replace(char, "")
                    # replace any of these character if founded in the mail with a void string
                    Mail = Mail.replace(char, "")
                # 2 cases :
                # Case 1 : if the file : relative_destination_folder+ISP+".csv" doesn't exist , it gonna be created
                if not os.path.exists(absolute_and_join(relative_destination_folder, Isp + '.csv')):
                    # we gonna create the new file with a specific name : ISP.csv ( for example : gmail.csv
                    # , yahoo.csv ... )
                    with open(relative_destination_folder + Isp + '.csv', 'w', newline='', encoding="utf8") as out_file:
                        # use the function writer of the csv library to easily change
                        # the content of the CSV file
                        writer = csv.writer(out_file)
                        # we must write a row ( a row = a list , that why we must
                        # transform the mail from string to list )
                        writer.writerow([Mail])
                        # Notification to be sure that all things are good
                        print("=> Creation : \n" + Mail)
                # Case 2 : if the file : relative_destination_folder+ISP+".csv" exist . in this case , we don't need to
                # the write MOD , we need just to append the ".csv" file
                else:
                    # open the file in APPEND MOD and not the Write MOD
                    with open(relative_destination_folder + Isp + '.csv', 'a', newline='', encoding="utf8") as out_file:
                        # use the function writer of the csv library to easily change
                        # the content of the CSV file
                        writer = csv.writer(out_file)
                        # we must write a row ( a row = a list , that why we must
                        # transform the mail from string to list )
                        writer.writerow([Mail])
                        print("=> Append : " + Mail)
        # Remove the file after Using it to avoid the duplication ( if you re-run the program )
        os.remove(absolute_and_join(relative_folder_of_csv, file))


# ===============================
# Decoration
# ===============================

def begin_of_step(text):
    """
    Print An acceptable text to show with the name of the step
    :param text: the name of the step
    :return:
    """
    # Clean the Screen
    os.system('cls')
    # Print The Header of the Program
    print(pyfiglet.figlet_format("OUZROUR"))
    print(pyfiglet.figlet_format("MAIL FILTER"))
    print("                  VERSION 1.0                   ")
    print(" =============================================== ")
    # Print The Step
    print("            START : " + text)
    print(" =============================================== ")


def end_of_step(text):
    """
    Print An acceptable text to show with the name of the step
    :param text: the name of the step
    :return:
    """
    print(" =============================================== ")
    # Print The Step
    print("            END : " + text)
    print(" =============================================== ")
    time.sleep(1)


# ===============================
# Cleaner
# ===============================

def clean_mail(output_directory: str = "output"):
    """
    clean all dumps ISPs
    :param output_directory: the directory that contain the csv files that
    contain combolist ( separated with ISPs ) , to be exact , it the folder
    where the Combo_Decrypt class save the result after decrypting the combolists
    :return: Just clean the dump ISPs
    """
    # the correct shape of an ISP ( gmail.com.csv = correct // gmail.csv = incorrect  )
    # the shape = String1.String2.csv
    RegexForFiltringDATA = re.compile(r'(^\w+)+\.+(\w+)+\.csv')
    # list the names of all files in the output directory
    list_output_directory = os.listdir(output_directory)
    # loop mod into this list
    for file in list_output_directory:
        # if a file doesn't have the shape of a normal ISP ( String.String.csv ) , then :
        if (not (RegexForFiltringDATA.search(file) == None or re.search('_', file) == None)):
            # delete It
            os.remove(absolute_and_join(output_directory, file))
            # print that it is deleted
            print('Removed with Regex : ' + file)


# ===============================
# Organize By Country
# ===============================

def organize_by_country(Database_directory, Country_directory):
    """
    Move the CSVs from the folder of the Database to the Country Directory
    By Respecting The Rule : put the ISP in the Right Country Folder Name !
    Example : String.it.csv ===> moved to : Italy/String.it.csv
    :param Database_directory: The Folder where the CSVs exist ( named after ISPs )
    :param Country_directory:  The Folder that gonna contain all countries name , each folder
    with a specific country name contain all CSVs that respect the rule in the description.
    :return:
    """

    # make the directory if it doesn't exist
    the_dir_must_exist(Country_directory)
    # The list of files name in the directory of Database
    DataBase = os.listdir(os.path.abspath(Database_directory))

    # Parse the file country-tlds.csv to extract the name and extension of countries
    with open("country-tlds.csv") as file_name:
        # read the csv
        csvreader = csv.reader(file_name)
        # initialise a new variable that gonna contain the content of the csv file
        country_tlds = []
        # fill the list country_tlds with the content of the csv
        # the list gonna be like that :
        # [ ... , [ "france" , "fr" ] , ... ]
        for row in csvreader:
            country_tlds.append(row)
    # now we gonna loop in the list of countries with the convention that :
    # element_i_of_country_tlds[0] = the name of the country
    # element_i_of_country_tlds[1] = the specific Country code ( top-level domains )
    for double_case_list_of_country_domain in country_tlds:
        # This Variable indicate if the actual country has an ISP that belongs to it
        # if this variable remains 0 , that mean No Isp Belongs to it
        # else , we gonna print a message ( in the end of every loop )
        i = 0
        # loop in the list of files names in the Database directory
        for file in DataBase:
            # 2 cases :
            # Case 1 : The file already exist
            if (os.path.exists(absolute_and_join(Database_directory, file))):
                # Detect if the structure of the file is like this : String.code.csv
                # ( for ex : if the country is france and the code is fr ==> yahoo.fr.csv is valid ,
                # but yahoo.de.csn isn't )
                DataByCountry = re.compile(r'\.' + double_case_list_of_country_domain[1].replace('.', '') + r'\.')
                # if the file name validate the rule DataByCountry
                if (DataByCountry.search(file) != None):
                    # we have one more element founded
                    i = i + 1
                    # indicate the absolute path of the Country Directory joined to the name of the country
                    folder_with_name_country = absolute_and_join(Country_directory,
                                                                 double_case_list_of_country_domain[0])
                    # be sure that this directory exist
                    the_dir_must_exist(folder_with_name_country)
                    # indicate the source file
                    source = absolute_and_join(Database_directory, file)
                    # indicate the destination file
                    destination = absolute_and_join(folder_with_name_country, file)
                    # 2 cases :
                    # case 1 : The destination file already exist ( yahoo.fr.csv already exist ,
                    # we must append the new lines to it and not replace it )
                    if (os.path.exists(destination)):
                        # open the file source
                        with open(source, 'r', encoding="utf8") as read_obj:
                            # read the csv
                            csv_reader = csv.reader(read_obj)
                            # Iterate over each row after the header in the csv
                            for row in csv_reader:
                                # copy the row and append it to the file that already exist
                                with open(destination, 'a', newline='', encoding="utf8") as out_file:
                                    writer = csv.writer(out_file)
                                    writer.writerow(row)
                        # remove the source file ( we don't need it anymore )
                        os.remove(source)
                    else:
                        # case 2 : the file don't exist , so moving it to the destination directory don't gonna
                        # overwrite the old file ( it doesn't exist )
                        shutil.move(source, destination)
        if (i != 0):
            # if the variable changed , that mean that a file that satisfy the regex condition exist ,
            # so we gonna print a little msg with the name of the country and
            # the number of files that satisfy the regex condition based on the name of this country
            print("[ADDITION WITH SUCCES] " + double_case_list_of_country_domain[0] + " : ~~ " + str(i) + " ~~ MAILs")


# ===============================
# Delete The Remained CSV in the database directory
# ===============================

def delete_remained_csv(Database_directory):
    """
    Delete All The Files in the DataBase Directory ( Be AWARE when you use this function ,
     it clear all the content of this directory !! )
    :param Database_directory: the directory where the CSV exists
    :return: Nothing . Only Erase all files in this directory
    """
    # The list of files name in the directory of Database
    DataBase = os.listdir(os.path.abspath(Database_directory))

    # loop in the list of files names
    for file in DataBase:
        # the absolute path of the file
        source = absolute_and_join(Database_directory, file)
        # delete it
        os.remove(source)
        # a little msg to be sure that all things go well
        print("Done ! Deleting the file  : " + file + " ....... DONE ! ")

    # indicate the end of the operations and showing the number of the files that was removed
    print('Done ! ' + str(len(DataBase)) + ' Removed dump list ! \n\n')
    # time to read the image
    time.sleep(3)


# ===============================
# Delete Duplicated lines in all CSVs in the Country_Directory Folder
# ===============================

def delete_duplication(Country_Directory: str):
    """
    Delete All Duplicated lines in all CSVs in the Country_Directory Folder
    :param Country_Directory: The Country_Folder that contain CSV files
    :return:
    """
    # walk through all directory ( return sufficient information about
    # all folders and sub-folders that exist in a specific directory )
    for dirpath, dirnames, filenames in os.walk("."):
        # when it found a sub-folder of the folder Country_Directory, do that :
        if (Country_Directory in dirpath):
            # find all csv in that folder and do a loop in to them
            for filename in [f for f in filenames if f.endswith(".csv")]:
                # source file
                source = os.path.join(dirpath, filename)
                # read csv file with pandas
                df = pandas.read_csv(source, sep=",")
                # remove duplicated rows with pandas
                df.drop_duplicates(subset=None, inplace=True)
                # replace the old one with this one
                df.to_csv(source, index=False)
            print(
                "Deleting All duplications in file : " + dirpath.replace(Country_Directory, "")[3:] + " ....... DONE ! ")


# ===============================
# Class To Extract The Csv(s) from text combolist file(s)
# ===============================
class ComboDecrypter:
    """
    Separate the combolists to many csv files , these csv files are named after their ISPs .
    The Original files are always conserved in a specific folder ( Originals )
    """

    def __init__(self, input_folder="input", folder_list_originals="Originals", output_folder="output"):
        """
        Separate the combolists to many csv files , these csv files are named after their ISPs .
        The Original files are always conserved in a separate folder ( Originals )
        :param input_folder:  the name of the folder where the combolists gonna exist
        :param folder_list_originals: the name of the folder where the original files gonna be moved to
        :param output_folder:  the name of the folder where the separated CSV gonna exist
        """

        # ===============================
        # Initialisation
        # ===============================

        # initialise the name of the folder that contain the combolists
        self.folder_list = input_folder
        # initialise the name of the folder where the text combolist gonna be moved on after converting them to CSV
        self.folder_list_originals = folder_list_originals
        self.output_folder = output_folder

        # ===============================
        # Create the folder that gonna contain the combolists if it doesn't exist
        # ===============================

        the_dir_must_exist(self.folder_list)

        # ===============================
        # List of the files to work with
        # ===============================

        # the list of files in the Folder that contain the combolists
        list_folder_list = os.listdir(self.folder_list)
        # the list of the files that end with
        list_of_files_in_list = endWith(list_folder_list, '.txt')

        # ===============================
        # Convert To CSV
        # ===============================

        begin_of_step("Convert to CSV")
        # Convert All text combolists in the folder csv
        self.transform_to_csv(list_of_files_in_list)
        end_of_step("Convert to CSV")

        # ===============================
        # Move the Originals Text Files after Finishing The Process of Converting
        # ===============================
        begin_of_step("Move the Original Files")

        # creation originals folder that gonna contain the original txt files
        # after converting them to .csv
        self.creation_original_file(folder_list_originals)

        # Move all text combolists ( after the conversion ) to a new directory ( already created below )
        move_the_files(list_of_files_in_list, self.folder_list, self.folder_list_originals)

        end_of_step("Move the Original Files")

        # ===============================
        # Extract The Mail Files
        # ===============================
        begin_of_step("Extract Mails")

        # creation directory
        the_dir_must_exist(self.output_folder + "/Databases/")
        extract_mail_from_list_csv(self.folder_list, self.output_folder + "/Databases/")

        end_of_step("Extract Mails")

    def creation_original_file(self, folder_list_originals):
        # Creation of the Folder Originals in List
        # This folder gonna contain all
        the_dir_must_exist(folder_list_originals)

    def transform_to_csv(self, list_of_files_in_list):
        for file in list_of_files_in_list:
            txt_to_csv(absolute_and_join(self.folder_list, file))


# ===============================
# Class To Organize Csv files by Country and clean it after that ( deleting the rest + deleting all duplicated rows )
# ===============================

class Organize_Clean:
    """
    Class To Organize Csv files by Country and clean it after that ( deleting the rest + deleting all duplicated rows )
    """

    def __init__(self, input_directory: str = "input", output_directory: str = "output/Databases",
                 Country_directory: str = "Output\\ByCountry"):
        """
        Class To Organize Csv files by Country and clean it after that ( deleting the rest + deleting all duplicated rows )
        :param input_directory: the input folder
        :param output_directory: the output folder
        :param ByCountry_Directory: the ouput folder where the final result gonna be
        """

        # ===============================
        # Clean All dumps mail
        # ===============================
        begin_of_step("Clean All dumps mail")

        # clean all dumps ISPs
        clean_mail(output_directory)

        end_of_step("Clean All dumps mail")

        # ===============================
        # Organize CSVs by Country
        # ===============================
        begin_of_step("Organize CSVs by Country")

        # organize data by country ( The result gonna be in the Country_Directory )
        organize_by_country(output_directory,Country_directory)

        end_of_step("Organize CSVs by Country")

        # ===============================
        # Deleting all the remained CSVs
        # ===============================
        begin_of_step("Deleting all the remained CSVs")

        # delete all the remained CSVs
        delete_remained_csv(output_directory)

        end_of_step("Deleting all the remained CSVs")

        # ===============================
        # Delete All Duplicated lines in all CSVs
        # ===============================
        begin_of_step("Delete All Duplicated lines in all CSVs ")

        # delete all the remained CSVs
        delete_duplication(Country_directory)

        end_of_step("Delete All Duplicated lines in all CSVs ")


if __name__ == "__main__":
    ComboDecrypter()
    Organize_Clean()
