'''
Created on Feb 6, 2019

@author: colin
'''


import os 
import csv
import re

output=open('/Users/colin/Desktop/copy.sh','w')
    
input_file = csv.DictReader(open("/Users/colin/Desktop/boxcovers.csv"))    

for row in input_file:
    try:
        full_name = row['boxcover']
        base_name =os.path.basename(full_name)
        ext_name = base_name.split('.')[1]
        idno = row['idno'].upper()
        clean_id = idno.replace('_BOOKS','')
        new_name = clean_id + "_BOXCOVER." + ext_name.upper()
    except:
        pass
        
    output.write("cp '/Volumes/Finished/{0}' '/Users/colin/Desktop/Boxcovers_XML/{1}'\n".format(full_name,new_name))
output.close()