#!/usr/bin/env python3
'''
Created on Sep 18, 2018

@author: colin

Create XLS exports for store importing.


'''
from docutils.nodes import row
from itertools import product


def make_products(*args):
    pass


def make_categories(*args):
    pass

def make_options(*args):
    pass

def make_filters(*args):
    pass

def make_attributes(**kwargs):
    for key, value in kwargs.items():
        print("{0} = {1}".format(key, value))

def write_sheet(**kwargs):
    try:
        sheet_name = kwargs['sheet'] 
        table_name = kwargs['table']
        limit = kwargs['limit'] if 'limit' in kwargs else ''
        sort  = kwargs['sort'] if 'sort' in kwargs else ''
        
        
        
        
    except KeyError:
        pass
    
    print('Creating worksheet named {0} from sql table named {1}'.format(sheet_name,table_name))
    
    cursor = cnx.cursor()
    query = ("select * from {0} {2} {1}".format(table_name,sort,limit))
    #print('Query = {}'.format(query))
    cursor.execute(query)
    header_row = cursor.column_names

    # Create Sheet
    worksheet = workbook.add_worksheet(sheet_name)
    
    # Header Row
    for cell in range(len(header_row)):
        worksheet.write(0,cell, header_row[cell])
        if 'date' in header_row[cell]:
            #print ('Cell {0} contains a date field'.format(cell))
            pass
    # Data Elements
    counter = 1
    for row in cursor:
        myArray = row
        for cell in range(len(row)):
            worksheet.write(counter,cell,row[cell])
        counter = counter + 1
        
    
    else:
        return False


import mysql.connector
import xlsxwriter
# Database login parameters

config = {
  'user': 'colin',
  'password': 'Izzy2002!',
  'host': '127.0.0.1',
  'database': 'edge',
  'raise_on_warnings': True,
  'charset': 'utf8',
  'raise_on_warnings': False
}

cnx = mysql.connector.connect(**config)

myArray = []
counter = 0
product_block = 3000

# Run Prep Category SQL Scripts

cursor = cnx.cursor()
query = ("call purge_duplicates_from_raw_series();")
cursor.execute(query)
print("Run procedure to purge duplicate records in raw series")
for each in cursor:
    print("Results of purge duplicate records in raw series {}".format(each))

cursor = cnx.cursor()
query = ("call make_active_categories()")
cursor.execute(query)
print("Run procedure make_active_categories()")
for each in cursor:
    print("Results of make active categories scripts {}".format(each))


cursor = cnx.cursor()
query = ("call create_commercial_license()")
cursor.execute(query)
print("Run procedure make  create_commercial_license()")
for each in cursor:
    print("Results of create commercial license {}".format(each))

cursor = cnx.cursor()
query = ("call create_product_options_values();")
cursor.execute(query)
print("Run procedure to create product options and values")
for each in cursor:
    print("Results of create  product options and values {}".format(each))    

cursor = cnx.cursor()
query = ("call create_related_id();")
cursor.execute(query)
print("Run procedure to create product related ids")
for each in cursor:
    print("Results of create product related ids {}".format(each)) 
    
workbook = xlsxwriter.Workbook('/Users/colin/Desktop/categories_upload.xlsx')
 
write_sheet(sheet='Categories',table='export_categories',sort='order by category_id')
write_sheet(sheet='CategoryFilters',table='export_category_filters',sort='order by category_id')
write_sheet(sheet='CategorySEOKeywords',table='export_category_seo_keywords',sort='order by category_id')
workbook.close()
 
workbook = xlsxwriter.Workbook('/Users/colin/Desktop/options_upload.xlsx')
write_sheet(sheet='Options',table='export_options')
write_sheet(sheet='OptionValues',table='export_option_values')
workbook.close()
  
workbook = xlsxwriter.Workbook('/Users/colin/Desktop/attributes_upload.xlsx')
write_sheet(sheet='AttributeGroups',table='export_attribute_group')
write_sheet(sheet='Attributes',table='export_attributes')
workbook.close()
  
workbook = xlsxwriter.Workbook('/Users/colin/Desktop/filters_upload.xlsx')
write_sheet(sheet='FilterGroups',table='export_filter_groups')
write_sheet(sheet='Filters',table='export_filters')
workbook.close()

#Get the number of products
cursor = cnx.cursor()
query = ("select count(*) from export_products")
cursor.execute(query)


for row in cursor:
    num_products = int(row[0])

print ('Products {0} Block Size {1}'.format(num_products, product_block))

for block in range(0,num_products,product_block):
    print('Writing Products from {0} to {1}'.format(block,product_block + block-1))
    #Get the first and number of product_id for this block
    cursor = cnx.cursor()
    
    if block+product_block > num_products:
        query = ("(select product_id from export_products order by product_id limit 1 offset {0} )union (select product_id from export_products order by product_id limit 1 offset {1})".format(block,num_products-1))
    else:
        query = ("(select product_id from export_products order by product_id limit 1 offset {0} )union (select product_id from export_products order by product_id limit 1 offset {1})".format(block,product_block+block-1))
            
    end_number = block+product_block -1
    
#     print ("Query = {}".format(query))
    cursor.execute(query)

    row = cursor.fetchone()
    start_product_id = row[0]
    row = cursor.fetchone()
    end_product_id = row[0]
    
    
    
    print('Start Product {0} End Product {1} Total Products {2}'.format(start_product_id,end_product_id,num_products))
    
    workbook = xlsxwriter.Workbook('/Users/colin/Desktop/products_upload_' + str(block) +'_to_' + str(end_number) + '.xlsx')
    write_sheet(sheet='Products',table='export_products',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='Specials', table='export_product_specials',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='Discounts', table='export_product_discounts',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='Rewards', table='export_product_rewards',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='ProductOptions', table='export_product_options',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='ProductOptionValues', table='export_product_option_values',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='ProductAttributes', table='export_product_attributes',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='ProductFilters', table='export_product_filters', limit='where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    write_sheet(sheet='ProductSEOKeywords', table='export_products_seo_keywords',limit= 'where product_id between ' + str(start_product_id) + ' and ' + str(end_product_id),sort = 'order by product_id asc')
    workbook.close()

    




print('End of Job')    
