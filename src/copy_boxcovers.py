#!/usr/bin/env python3
# encoding: utf-8
'''
copy_boxcovers -- Program to copy boxcovers from a csv file to a directory

copy_boxcovers is a description

It defines classes_and_methods

@author:     colin


@copyright:  2018 Edge Interactive Publishing, Inc. All rights reserved.

@license:    license

@contact:    colin@goedge.com
@deffield    updated: Updated
'''

import sys
import os
import csv
import re


from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2018-12-30'
__updated__ = '2018-12-30'

DEBUG = False
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

def getVolumes(*args):
    print('Volumes: {}'.format(args))
    volumes=[]
    for each in os.listdir('/edge/EdgeSource01'):
        if re.match('(^[A-Z][0-9][A-Z0-9]\d{3})', each):
        
            if not re.search('MOVED', each):
                print('\t',each)
    return volumes
    

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

  Created by Colin on %s.
  Copyright 2018 Edge Interactive Publishing, Inc.. All rights reserved.

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
        parser.add_argument("-i", "--input", dest="input", action="store", help="set input filename in csv format")
        parser.add_argument("-o", "--output", dest="output", action="store", help="set output directory")
        parser.add_argument("-d", "--debug", dest="debug", action="store", default="INFO", help="set the debug level [INFO|ERROR|WARN|DEBUG]")
        parser.add_argument("-n", "--noexec", dest="noexec", action="store_true", help="Do not make any changes to data or os layer, just show what you would do" )
        # Process arguments
        args = parser.parse_args()
        print(args)

        config = args.config
        logfile = args.log
        debug = args.debug
        inputfile = args.input
        outputfile = args.output
        noexec = args.noexec
    


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
         
        
        
        #===========================================================================
        # Main program starts here
        #===========================================================================
        logger.info('{0} starting with debug level of {1}'.format(os.path.basename(__file__),debug))        


        #=======================================================================
        # Get Volume List
        #=======================================================================

        VOLUME=['/edge/EdgeSource01','/edge/EdgeSource02','/edge/EdgeSource03']
        
        getVolumes(VOLUME)
        
        



#         #=======================================================================
#         # Verify CSV file, and output directory, if valid load the csv file
#         #=======================================================================
#         
#         if os.path.isfile(inputfile) and os.path.isdir(outputfile):
#             logger.info("{0} for input exists and {1} for output exists".format(os.path.basename(inputfile),outputfile))
#         
#         else:
#             if not os.path.isfile(inputfile):
#                 logger.error('Input filename does not exist')
#             if not os.path.isdir(outputfile):
#                 logger.error('Output directory does not exist')
#                 
#             return 2
#             
#         with open(inputfile, newline='') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 if row['idno'] != None and row['BoxCover'] != None:
#                     idno = row['idno'].strip()
#                     boxcover = row['BoxCover'].replace('\n','').strip()
#                     logger.info("===================================================================================================================================")
#                     logger.info("id: {0} : filename  [{1}]".format(idno,boxcover))
#                     logger.info("-----------------------------------------------------------------------------------------------------------------------------------")
#                     logger.info("unmodified: [{}]".format(row['BoxCover']))
#                     if re.search(r'\S', row['BoxCover']):
#                         logger.info('Contains leading space')
#                     if re.search(r'\S$', row['BoxCover']):
#                         logger.info('Contains trailing space')
#                     if re.search(r'\n',row['BoxCover']):
#                         logger.info('Contains carriage return')
#                     if re.search(r'[ ]{2}',row['BoxCover']):
#                         logger.info('Contains multiple spaces')
#                     logger.info("===================================================================================================================================")


        #=======================================================================
        # Main program ends here
        #=======================================================================

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
        sys.argv.append("-d INFO")
        
    if TESTRUN:
        import doctest
        doctest.testmod()
    if NOEXEC:
        print("No exec")
        sys.argv.append("--noexec")
        
    
    



   
        
    sys.exit(main())