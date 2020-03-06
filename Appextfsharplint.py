import cast_upgrade_1_5_11 # @UnusedImport
from cast.application import ApplicationLevelExtension,create_link,  ReferenceFinder
import logging
import cast.application
import xml.etree.ElementTree as ET
import os


class fsharpExtensionApplication(cast.application.ApplicationLevelExtension):

    def __init__(self):   
        pass     
    
       
        
        
    def end_application(self, application):
        logging.info("fsharp : Running extension code at the end of an application")
        for line in self.get_intermediate_file('fsout.txt'):
            logging.info("get_intermediate_file.." + str(line))
        
     