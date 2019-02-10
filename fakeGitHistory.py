#!/usr/local/bin/python3

import sys, getopt, os
import subprocess
import re

import pandas as pd

'''
    Add given file to git
'''
def make_git_add(file):

    terminal_cmd = "git add " + file

    # execute in terminal
    print("CONSOLE COMMAND: ", terminal_cmd)
    os.system(terminal_cmd)


'''
    Make commit with timestamp of the files date and generated commit message
'''
def make_git_commit(timestamp1, timestamp2, commit_message):

    date_blank =  timestamp1.strftime('%c') + " +0100" #"Tue Dec 18 09:10 2018 +0100"
    date_blank2 =  timestamp2.strftime('%c') + " +0100" #"Tue Dec 18 09:10 2018 +0100"
    date_blank = date_blank
    date_blank2 = date_blank2

    date_minus =  timestamp2.strftime('%Y-%m-%d %H:%M:%S') #"#2018-12-18 09:10:22"

    terminal_cmd = 'GIT_AUTHOR_DATE="' + date_blank + '" GIT_COMMITTER_DATE="' + date_blank2 + '" git commit --date="' + date_minus + '" -m "' + commit_message + '"'

    # execute in terminal
    print("CONSOLE COMMAND: ", terminal_cmd)
    os.system(terminal_cmd)

'''
    For the given path, get the List of all files in the directory tree 
'''
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            # add folder to path only if it is a visible folder (name not starts with .foldername)
            if( fullPath.split("/")[-1].startswith(".") == False ):
                allFiles = allFiles + getListOfFiles(fullPath)
        else:
            # check if it is a invisible file
            if( fullPath.split("/")[-1].startswith(".") == False):
                allFiles.append(fullPath)

    return allFiles



'''
    Sort the files in a folder by its change timestamps and make commits to git per day
'''
def sort_files_in_folder_by_changetime(folder):

    # read all files in folder
    listOfFiles = getListOfFiles(folder)
    print("In the folder are ", len(listOfFiles), " files.")

    df = pd.DataFrame(columns=['path','date','timestamp_1','timestamp_2'])

    for i in range(len(listOfFiles)):
        file = listOfFiles[i]
        # get all change times per file (store both in DataFrame: file path, timestamp, date)
        result = subprocess.run(['stat', file], stdout=subprocess.PIPE)
        
        print("FILE #", i, ": ", file)
        #print("RESULT: ", result)
        #result.stdout
        timestamp = str(result.stdout).split('"')

        # adding a row
        df.loc[-1] = [str(file), 0, timestamp[3], timestamp[1]]
        # shifting index
        df.index = df.index + 1

    # sorting by index
    df = df.sort_index()

    # convert data types

    df['timestamp_1'] = pd.to_datetime(df['timestamp_1'])
    df['timestamp_2'] = pd.to_datetime(df['timestamp_2'])
    df['date'] = df['timestamp_1'].astype(str).str[:10]

    # group by date
    #groups = df.groupby('date')

    dates = df['date'].unique()

    for day in dates:
        # select only files last-edited at this day
        sub_df = df[df['date'] == day]

        # for every file edited at this day
        for z in sub_df.index:
            file = sub_df['path'][z]
            make_git_add(file)

        # make one commit for one day
        file_names = [file_name.split("/")[-1] for file_name in sub_df['path']]
        commit_message = "Add following files: " + str(file_names)[1:-1]
        timestamp_1 = sub_df['timestamp_1'][z]
        timestamp_2 = sub_df['timestamp_2'][z]

        print("COMMIT_MESSAGE: ", commit_message)
        make_git_commit(timestamp_1, timestamp_2, commit_message)



def handleArguments(argv):

    inputfolder = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifolder="])
    except getopt.GetoptError:
        print('fakeGitHistory.py -i <inputfolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('fakeGitHistory.py -i <inputfolder>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            inputfolder = arg

    return(inputfolder)


def main(argv):

    inputfolder = handleArguments(argv)

    if(inputfolder == ""):
        inputfolder = "."

    print('Input path is: "', inputfolder, '"')    

    pwd_path = os.getcwd()
    full_path = pwd_path + "/" + inputfolder

    print('Absolute path is: "', full_path, '"')

    sort_files_in_folder_by_changetime(full_path)

if __name__ == "__main__":
   main(sys.argv[1:])




