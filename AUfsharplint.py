import cast.analysers.ua
from cast.analysers import log as Print, CustomObject
from cast.application import ApplicationLevelExtension, CASTAIP, create_link,  Bookmark, ReferenceFinder, Package, open_source_file
import re
import os
from pathlib import PureWindowsPath
import random
from cast import Event
from pathlib import Path
import  subprocess, sys
import os
from Cython.Utils import open_source_from_loader

class fsharplintExtension(cast.analysers.ua.Extension):
    
    def _init_(self):
        self.filename = ""
        self.batchprocess = False
        self.deployfolder =""
        self.namespace = ""
        self.modulename = ""
        self.file = ""    
        self.initial_crc =  None
        self.file_ref=""
        self.extnls=[]
        self.parentOBJ=None
        self.parentOBJtwo=None
        self.counter = ""
        return

    def start_analysis(self):
        Print.info("fsharp : Running extension code start")
        self.intermediate_file_fslint = self.get_intermediate_file("fileresult.txt") 
        self.batchprocess = False
        self.counter = 0
#         try:
#              self.processexternalfshaplint()
#               
#         except:
#             Print.info ("error executing fsharp lint power shell process") 
        
#   
    def start_file(self,file):
        
        Print.info("fsharp : Running extension code start file")
        
        self.file = file
        if file.get_name().endswith('.fs'):
#             try:
#               self.processexternalfshaplint(file)
#             except:
#               Print.info ("error executing fsharp lint power shell process") 
              
            Print.debug('Scanning fs  file :'+str(Path(file.get_path()).name))
            if (os.path.isfile(file.get_path())):
                self.parsefsharpnamespace(file.get_path(), file);
                self.parsefsharpmodule(file.get_path(), file);
                self.parsefsharptype(file.get_path(), file);
                self.parsefsharplet(file.get_path(), file);
                self.parsefsharpopen(file.get_path(), file);
             
    def processexternalfshaplint(self, file):
        
        try:
            if self.batchprocess is not True:
                s= self.get_plugin()
                Print.info(str(s.get_plugin_directory()))
                 
                pspath =str(s.get_plugin_directory())+ "\\fsharplintbatchpath.ps1" 
                Print.info(pspath)
                p = str(Path(file.get_fullname()).parents[1])
                
                Print.info(str(p))
                
                with open("fsout.txt", "w") as file:
                   #subprocess.call(["powershell",pspath, "C:\\Fsharp\\Oxygenworkspacefsharplint\\com.castsoftware.labs.fsharplint\\tests\\fs"], stdout=file)
                   subprocess.call(["powershell",pspath, p], stdout=file)
                   file.close()
                 
                with open("fsout.txt", "r") as f:
                   self.intermediate_file_fslint.write(f.read())
                   self.intermediate_file_fslint.write("copied the file")
                   f.close()
                if os.path.isfile("fsout.txt"):
                    Print.info("file exist")
                    self.batchprocess = True
                   # os.remove("fsout.txt") 
                
            
        except:
            Print.info ("error executing fsharp lint power shell process")          
              
              
    def parsefsharpmodule(self, fsharpfile, file): 
        try :
            #Print.info("file scan module :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('moduleexport', before='', element = 'module.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('module') is not -1:
                        if ref.value.find('=') is not -1: 
                                response = ref.value.replace("=", '')
                                resp = response.replace("module", '')
                                self.counter = self.counter+1
                                fsobj = cast.analysers.CustomObject()
                                cleanvalue= re.sub('[^0-9a-zA-Z.]+', ' ', resp)
                                fsobj.set_name(str(cleanvalue))
                                self.modulename =str(resp.strip())
                                fsobj.set_type('fsharp_module')
                                fsobj.set_parent(file)
                                parentFile = file.get_position().get_file() 
                                self.fielPath = parentFile.get_fullname()
                                fsobj.set_guid(str(Path(file.get_path()).name)+str(self.counter))
                                fsobj.save()
                                bookmark = cast.analysers.Bookmark(file, 1,1,-1,-1)
                                fsobj.save_position(bookmark)
                                setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                                #Print.info("Save object module: "+cleanvalue)
                                self.parentOBJtwo =fsobj
                                cast.analysers.create_link('callLink',  self.parentOBJ, fsobj, bookmark)
                                #Print.info("link created: "+cleanvalue)
                except ValueError:
                    Print.info ("error loading fsharp2 module")
        except:
            return          
    
    def parsefsharpnamespace(self, fsharpfile, file): 
        try :
            #Print.info("file scan namespace :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('namespaceexport', before='', element = 'namespace.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('namespace') is not -1:
                        response = ref.value.replace("namespace", '')
                        fsobj = cast.analysers.CustomObject()
                        self.counter = self.counter+1
                        cleanvalue= re.sub('[^0-9a-zA-Z.]+', ' ', response)
                        fsobj.set_name(str( cleanvalue))
                        self.namespace =str(response.strip())
                        fsobj.set_type('fsharp_namespace')
                        fsobj.set_parent(file)
                        parentFile = file.get_position().get_file() 
                        self.fielPath = parentFile.get_fullname()
                        fsobj.set_guid(str(Path(file.get_path()).name)+str(self.counter))
                        fsobj.save()
                        self.parentOBJ =fsobj
                        bookmark = cast.analysers.Bookmark(file, 1,1,-1,-1)
                        fsobj.save_position(bookmark)
                        self.parentOBJ =fsobj
                        #Print.info("Save object namespace: "+cleanvalue )
                      
                     
                except ValueError:
                    Print.info ("error loading fsharp2 namespace")
        except:
            return          
        
    def parsefsharptype(self, fsharpfile, file): 
        try :
            #Print.info("file scan type :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('typeexport', before='', element = 'type.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('type') is not -1:
                        if ref.value.find('=') is not -1: 
                                response = ref.value.replace("=", '')
                                resp = response.replace("type", '')
                                fsobj = cast.analysers.CustomObject()
                                self.counter = self.counter+1
                                fsobj.set_name(str(resp.strip()))
                                fsobj.set_type('fsharp_type')
                                fsobj.set_parent(file)
                                parentFile = file.get_position().get_file() 
                                self.fielPath = parentFile.get_fullname()
                                fsobj.set_guid(str(Path(file.get_path()).name)+str(self.counter))
                                fsobj.save()
                                setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                                #Print.info("Save object type:"+resp.strip())
                                bookmark = cast.analysers.Bookmark(file, 1,1,-1,-1)
                                fsobj.save_position(bookmark)
                                cast.analysers.create_link('callLink', self.parentOBJ,fsobj, bookmark)
                                #Print.info("link created: "+resp.strip())
                             
                except ValueError:
                    Print.info ("error loading fsharp2 type")
        except:
            return          
        
    def parsefsharplet(self, fsharpfile, file): 
        try :
            #Print.info("file scan let :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('letexport', before='', element = 'let.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('let') is not -1:
                                response = ref.value.replace("=", '')
                                resp = response.replace("let", '')
                                fsobj = cast.analysers.CustomObject()
                                cleanvalue= re.sub('[^0-9a-zA-Z.]+', ' ', response)
                                fsobj.set_name(str(cleanvalue))
                                fsobj.set_type('fsharp_let')
                                fsobj.set_parent(file)
                                parentFile = file.get_position().get_file() 
                                self.fielPath = parentFile.get_fullname()
                                fsobj.set_guid(resp+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                                fsobj.save()
                                setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                                setpropertyparent.add_propertymodule(fsobj,  self.modulename)
                                #Print.info("Save object let: "+cleanvalue)
                                bookmark = cast.analysers.Bookmark(file, 1,1,-1,-1)
                                fsobj.save_position(bookmark)
                                cast.analysers.create_link('callLink', self.parentOBJtwo,fsobj, bookmark)
                                #Print.info("link created: "+cleanvalue)
                             
                except ValueError:
                    Print.info ("error loading fsharp2 let")
        except:
            return
        
    
        
    def parsefsharpopen(self, fsharpfile, file): 
        try :
            Print.info("file scan open "+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('openexport', before='', element = 'open.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('open') is not -1:
                        response = ref.value.replace("open", '')
                        fsobj = cast.analysers.CustomObject()
                        cleanvalue= re.sub('[^0-9a-zA-Z.]+', '', response)
                        fsobj.set_name(str(response.strip()))
                        fsobj.set_type('fsharp_open')
                        fsobj.set_parent(file)
                        parentFile = file.get_position().get_file() 
                        self.fielPath = parentFile.get_fullname()
                        fsobj.set_guid(response+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                        fsobj.save()
                        bookmark = cast.analysers.Bookmark(file, 1,1,-1,-1)
                        fsobj.save_position(bookmark)
                        setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                        #Print.info("Save object open: "+cleanvalue)
                        cast.analysers.create_link('callLink', self.parentOBJ,fsobj, bookmark)
                        #Print.info("link created: "+cleanvalue)
                 
                             
                except ValueError:
                    Print.info ("error loading fsharp2 open")
        except:
            return
        
            
     
    def end_analysis(self):
        Print.info("fsharp : Running extension code end") 
       
        pass



class setpropertyparent():  
    
    @staticmethod
    def add_propertynamespace(obj, ctx ):
        if ctx is not None:
            obj.save_property('parentnamespaceProperties.fsharpparent', str(ctx))
            #Print.info("namesp:"+ str(ctx))
        else:
            obj.save_property('parentnamespaceProperties.fsharpparent', 'None')
         
    @staticmethod
    def add_propertymodule(obj, ctx ):
        if ctx is not None:
            obj.save_property('parentmoduleProperties.fsharpparentmodule', str(ctx))
            #Print.info("modulep:"+ str(ctx))
        else:
            obj.save_property('parentmoduleProperties.fsharpparentmodule', 'None')
            
            
