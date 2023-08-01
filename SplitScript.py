#%%
import csv
#%%
#reads in a configuration file
#creates a dictionary of columns that need to be split, associated with a list of all the new columns that need to be created
config_rows = []
parameters = {}

with open("config.csv", "r") as configfile:
    csvreader = csv.reader(configfile)
    for row in csvreader:
        config_rows += [row]

#pull user entries for the filenames
data_in_filename = config_rows[2][0]
data_out_filename = config_rows[6][0]

#if user tries to export data to the same file they are importing
#send error message and change the output file to avoid overwriting their data. Program still runs.
if data_in_filename == data_out_filename:
    print('Same filename for input data and output datafile.\nOutput filename will be changed to "split_data_out_default.csv" to avoid overwriting your data\n')
    data_out_filename = 'split_data_out_default.csv'

#pull user entry for specific row number they want to use as headers
header_index = int(config_rows[4][0]) - 1
print("Row {} is being used for headers.\n".format(header_index + 1))

#organize a dictionary with the following format: {header:[keyword1, keyword2]}
num_cols_to_split = len(config_rows[8])

for i in range(num_cols_to_split):
    new_entries = []
    for newcol in config_rows[10:]:
        if newcol[i] != '':
            new_entries += [newcol[i]]
    parameters[config_rows[8][i]] = new_entries

#echo the parameters that the user requested in their config file.
print("Parameters for splitting columns:")
for key in parameters.keys():
    print('    ' + key + ":", end='')
    for entry in parameters[key]:
        print(' "' + entry + '"', end='')
    print()
print()
#%%
#reads in the raw data into a list of lists (row by column)
print("Reading data from {}.\n".format(data_in_filename))

rawdata = []

with open(data_in_filename, "r") as datafile:
    csvreader = csv.reader(datafile)
    for row in csvreader:
        rawdata += [row]

#Deep copy the raw data into a new table that will be manipulated before being written back into a CSV
expanded_table = []
for row in rawdata:
    expanded_table += [row.copy()]

#%%
def insertcol(expanded_table, newcol_category, newcol_name, header_index):

    #set the index for the new column, by looking at the input string
    if newcol_category in expanded_table[header_index]:
        newcol_index = expanded_table[header_index].index(newcol_category) + 1
        
    #only executes this block if the column entered does not exist, will create a leftmost column and fill it with error messages
    #also reports the error to the user
    else:
        print('Error: "' + newcol_category + '" not found in headers. 1) make sure you are referencing the correct header row. 2) Check your spelling carefully in the config file.\n')
        
        newcol_index = 0
        newcol_name = 'Error! "' + newcol_category + '" not found in headers'
        expanded_table[header_index].insert(newcol_index, newcol_name)
        for rownum in range(header_index + 1,len(expanded_table)):
            expanded_table[rownum].insert(newcol_index,'error')
        for rownum in range(0, header_index):
            expanded_table[rownum].insert(newcol_index,'')
        
        return expanded_table
    
    #creates a new column after the column to split, first creates the header, then populates cells below with counts
    #create new header
    expanded_table[header_index].insert(newcol_index, newcol_category + ": " + newcol_name)
    counter = 0
    
    #add either a 1 or 0 in each row for if keyword is found or not
    for rownum in range(header_index + 1,len(expanded_table)):
        if newcol_name in expanded_table[rownum][newcol_index - 1]:
            expanded_table[rownum].insert(newcol_index, 1)
            counter += 1
        else:
            expanded_table[rownum].insert(newcol_index, 0)

    #add empty cells above header (if header is not top row) to keep alignment
    if header_index != 0:
        for rownum in range(0, header_index):
            expanded_table[rownum].insert(newcol_index,'')
    
    #if keyword was not found in any row, report it to the user
    if counter == 0:
        print('Error: "{}" was not counted in any row under the header "{}". Ensure it is not present in your data. The column was still created successfully.\n'.format(newcol_name,newcol_category))
    return expanded_table

#%%
#feed each keyword through the function to create new columns
for category in parameters.keys():
    #flip the list associated with the key, because cosmetically new columns are added to the left of previously added ones
    parameters[category] = list(reversed(parameters[category]))   
    #feeds list of keywords through and creates new columns for each one.
    for newcol in parameters[category]:
        insertcol(expanded_table,category,newcol,header_index)

#%%
#create new output file
with open(data_out_filename, "w", newline='') as csvoutput:
    csvwriter = csv.writer(csvoutput)
    csvwriter.writerows(expanded_table)
    
print('New columns were added to data table, and exported to "{}".\n\nIf "{}" already existed in this directory, it has been overwritten.\n'.format(data_out_filename, data_out_filename))

#%%
print('This program has finished. Once you are done reading the messages on the screen, press enter to exit')
user_input = input('')