This script will look through a designated column in a CSV file for designated keywords. Each keyword will be given its own new column, and if the keyword is found in the column where the script is looking, the new column receives the value 1. If the keyword is not found, the new column receives the value 0.

This script does not count occurrences of keywords. It only looks within the string for whether the keyword is present or not. The output is boolean.

Place your .csv data file, the script SplitScript.py, and your configuration file config.csv in the same directory.

The config file contains instructions, fill out the necessary cells with the appropriate information and save it. Its name must remail config.csv.

Your data file may have any name, so long as it is in .csv format. The config file has a field for designating the input datafile.

The config file also asks for the filename for the output file.

Once config.csv is ready and saved with the datafile and SplitScript.py, run the script. The script will write the output file.