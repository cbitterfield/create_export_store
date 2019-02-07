#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
import_xml -- Import XML file into MySQL

import_xml is a This program imports an XML program from LiveCode into a MySQL database table. input=xml file output=mysql_table

It defines classes_and_methods

@author:     colin


@copyright:  2019 Edge Interactive Publishing, Inc. All rights reserved.

@license:    GNU 3

@contact:    colin@goedge.com
@deffield    updated: Updated
'''

import sys
import os
import mysql.connector
import xml
import xml.etree.ElementTree as ET
import re

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2019-01-19'
__updated__ = '2019-01-19'

DEBUG = True
TESTRUN = False
NOEXEC = False

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2019 Edge Interactive Publishing, Inc. All rights reserved.

  Licensed under the GNU Public License 3.0
  https://www.gnu.org/licenses/gpl-3.0.en.html

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-c","--configfile", dest="config", default="config.yaml", help="use config file, default is config.yaml in working dir")
        parser.add_argument("-l","--log", action="store",default="console", help="logfile for output, if none is selected then use console" )
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument("-i", "--input", dest="input", action="store", help="set input filename")
        parser.add_argument("-o", "--output", dest="output", action="store", help="set output filename")
        parser.add_argument("-d", "--debug", dest="debug", action="store", default="INFO", help="set the debug level [INFO|ERROR|WARN|DEBUG]")
        parser.add_argument("-n", "--noexec", dest="noexec", action="store_true", help="Do not make any changes to data or os layer, just show what you would do" )
        parser.add_argument("-u", "--user", dest="user", action="store", help="MySQL Username" )
        parser.add_argument("-p", "--password", dest="password", action="store", help="MySQL Password" )
        parser.add_argument("-s", "--schema", dest="schema", action="store", help="MySQL database" )

        # Process arguments
        args = parser.parse_args()
        print(args)

        config = args.config
        logfile = args.log
        debug = args.debug
        source = args.input
        output   = args.output
        noexec = args.noexec
        user = args.user
        password = args.password
        schema = args.schema
    


        if debug:
            print("Debug Value: {}".format(debug))
            
        if noexec:
            print("NOEXEC=True; No data or files will be changed")

        #===============================================================================
        # Setup  Logging
        #===============================================================================
        import logging
        import logging.config 
        logger = logging.getLogger(__name__)
        
        
        if not args.log == 'console':   
            logging.basicConfig(filename=args.log, format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=args.debug)
        else:
            logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=args.debug)
         
        
        # Test that input is a file
        
        if not os.path.isfile(source):
            return 2
        
        #===========================================================================
        # Main program starts here
        #===========================================================================
        logger.info('{0} starting with debug level of {1}'.format(os.path.basename(__file__),debug)) 
        
        logger.info('Removing all ODD Characters')
        logger.info(source)
        inputfile = open(source,'r',encoding="utf-8")
        newfilename = str(source) + str('_fixed')
        logger.info('Open new file without bad characters {}'.format(newfilename))
        
        outputfile = open(newfilename,'w',encoding="utf-8")
        logger.info(newfilename)
        
        sqlfile = open('/Users/colin/Desktop/record.sql','w',encoding="utf-8")  
        # 
        lines = inputfile.readlines()
        for line in lines:
            fixed = re.sub(r'\x00','',line)
            fixed = re.sub(r'\x19','',fixed)
            outputfile.write(fixed)
               
   
        outputfile.close()
        #
         
        input_xml = open(newfilename,'r',encoding="utf-8")
                
        logger.info('Loading XML data from {}'.format(input_xml))
        tree = ET.parse(input_xml)
        root = tree.getroot()
        
        logger.info('XML: Root Tag {}'.format(root.tag))
        
        # MySQL Connector
        
        config = {
              'user': user,
              'password': password,
              'host': '127.0.0.1',
              'database': schema,
              'raise_on_warnings': False,
              'charset': 'utf8'
                }
        logger.info('Connecting to MySQL server on 127.0.0.1 as {0} with schema {1} and loading data to table {2}'.format(user,schema,output))
        try:
            cnx = mysql.connector.connect(**config)
            if cnx.is_connected():
                logger.info('Connection is working')
        except:
            logger.error('Connection failed')
            return 2
        
        cursor = cnx.cursor()
        
        # Truncate source table
        # Work better safety logic later
        logger.info('DROP TABLE IF EXISTS {}'.format(output))
        cursor.execute('DROP TABLE IF EXISTS ' + output)
        
        field_names = []
        
        for child in root:
            for record in child:       
                field_names.append(record.tag)
            break
        make_table = 'CREATE TABLE `' + output +  '` (\n'
        
        for column in field_names:
            make_table = make_table + '`'+ column + '` TEXT, \n'
            
        make_table = make_table + " `num_cast` TEXT"
        make_table = make_table + ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;'
        logger.info(make_table)
        cursor.execute(make_table)
        cnx.autocommit = True
        
        records=0
        for child in root:
            records = records + 1
            line = ""
            col_array = []
            data_array = []
              
            for record in child:       
                col_array.append(str(record.tag))
                element_text = record.text
                if element_text == None:
                    data_array.append('')
                      
                else:
                    data_array.append(str(record.text).strip())
            columns = '`'  +'`,`'.join(col_array) + '`'
            data =   '''  +''','''.join(data_array) + ''' 
            logger.info('Number of columns = {}'.format(len(col_array))) 
            variables = '%s,'* len(col_array)
            
            query = "insert into " + schema + "." + output + "("  + columns + ")" + "VALUES" + "(" + variables[:-1] + ")"
            
            logger.info(query)
            cursor = cnx.cursor()
            sql_data = tuple(data_array)
            logger.info(type(sql_data))
            logger.info(sql_data)
            logger.info(query)
#             sqlfile.write('Query: {0}'.format(query))
#             sqlfile.write('Data: {0}'.format(sql_data))
            result=cursor.execute(query,sql_data)
        logger.info('Records uploaded {}'.format(records))    
            
            
        cursor = cnx.cursor()
        query = ("call create_num_cast();")
        cursor.execute(query)
         
        cursor = cnx.cursor()
        query = ("CALL load_marked_data()")
        cursor.execute(query,multi=True)
            
        
        #=======================================================================
        # Main program ends here
        #=======================================================================
        logger.info('END of Program')
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2
    
    
    
    
    

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-dINFO")
        
    if TESTRUN:
        import doctest
        doctest.testmod()
    if NOEXEC:
        print("No exec")
        sys.argv.append("--noexec")
        
    
    



   
        
    sys.exit(main())