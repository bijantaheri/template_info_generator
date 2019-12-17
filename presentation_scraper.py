import os, csv, itertools, pandas as pd
from xml.dom import minidom


### Global parameters; lists, dirs and dicts

maindir    = 'Z:/presentations/custom/'
dirs       = os.listdir(maindir)
pres       = []
deleted    = []
nonoList   = [' ', '+', ',', '.', '-']
ext        = ('.lnk', '.xml')
dictionary = {}


def scraper():

    ### Create a list of all presentations within the maindir and all its subfolders
    for dir in dirs:
        if not dir.endswith(ext):
            presentations = os.listdir(maindir + dir)
            for presentation in presentations:
                pres.append(maindir + dir + '/' + presentation)
            
    ### Read all label:value pairs for each presentation file, and add them to the main dictionary
    for i in pres:
        if '.xml' in i:

            xml = minidom.parse(i)

            labels = xml.getElementsByTagName('label')
            values = xml.getElementsByTagName('value')

            labelList = [label.firstChild.data.strip("'").strip().strip(':').strip() for label in labels[1:-2]]
            valueList = [value.firstChild.data.strip() for value in values[1:-2]]

            dictionary.update(dict(zip(valueList,labelList)))
            
    ### Clean the keys (labels) of the dictionary, by removing unwanted/dirty keys 
    print("\n\nCleanup:")    
    print("Dictionary length before: ", len(dictionary))

    for key in dictionary.keys():
        if any(char in key for char in nonoList):
            deleted.append(key)
        
    dictionary = {key:val for key, val in dictionary.items() if val not in deleted} 

    print("Dictionary length after: ", len(dictionary))    
    
    df = pd.DataFrame.from_dict(dictionary, orient="index")
    df.to_csv('dictionary.csv')
    
    return dictionary
    

if __name__ == "__main__":
    scraper()
    print("\nDictionary has been written to CSV file")
    input("\n\nPress Enter to exit...")