from pypdb import make_query, do_search
import pandas as pd
import os
import urllib.request
import shutil
import pathlib

# Let me get both inspected genes and the output directory from "parameters_pdb.txt" file
parameter_path=os.path.join(pathlib.Path(__file__).parent.absolute(),'parameters_pdb.txt')
parameters=pd.read_csv(parameter_path,sep="\t",engine="python",skipinitialspace=True)
gene_name=parameters[parameters.columns[0]][0]
path=parameters[parameters.columns[0]][1]
number=int(parameters[parameters.columns[0]][2])
my_query=gene_name.split(",")


os.chdir(path)
check=os.path.join(path,"pdb_data")

# Let me create the output folder
while True:
    if os.path.isdir(check):
        askuser = int(input("The directory you have entered already exist, if you want to remove, type 0, if you want to create a new directory, type anything other than zero: "))
        if askuser == 0:
            shutil.rmtree(check)
            os.makedirs(check)
            break
        else:
            check=input("Please re-write the output directory again: ") # ex: /home/a/Desktop/pdb_data2
            os.makedirs(check)

    else:
        os.makedirs(check)

# Let me change the directory
os.chdir(check)

for each in my_query:
    search_dict = make_query(each)
    found_pdbs = do_search(search_dict)
    if len(found_pdbs)>number:
        found_pdbs = found_pdbs[0:number]
    for ids in found_pdbs:
        # I created all the paths for each pdb ID
        ext="{}.pdb".format(ids)
        search_path= 'https://files.rcsb.org/view'
        full_path=os.path.join(search_path,ext)

        # I created a new folder for each gene name in the given list

        my_new_folder= os.path.join(check,each)
        if not os.path.isdir(my_new_folder):
            os.makedirs(my_new_folder)

        new_full = os.path.join(my_new_folder,ext)

        urllib.request.urlretrieve(full_path,new_full)






