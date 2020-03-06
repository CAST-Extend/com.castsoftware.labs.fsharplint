import cast.analysers.ua
from cast.analysers import log as Print, CustomObject
from cast.application import ApplicationLevelExtension, create_link,  ReferenceFinder
import re
import os
import random
from pathlib import Path
import subprocess, sys





class fsharplintExtension(cast.analysers.ua.Extension):
    
    def _init_(self):
        self.filename = ""
        self.namespace = ""
        self.modulename = ""
        self.file = ""    
        self.initial_crc =  None
        self.file_ref=""
        self.extnls=[]
        self.counter = 0
        return

    def start_analysis(self):
        Print.info("fsharp : Running extension code start")
        #p = subprocess.call(["powershell","C:\\Fsharp\\fsharplintbatch.ps1"])
        #self.intermediate_file_fslint = self.get_intermediate_file("fsout.txt")
        #with self.intermediate_file_fslint.write as file:
            #subprocess.call(["powershell","C:\\Fsharp\\fsharplintbatch.ps1"], stdout=file)
        try:
            with open("fsout.txt", "w") as file:
                subprocess.call(["powershell","C:\\Fsharp\\fsharplintbatch.ps1"], stdout=file)
          
        except:
            Print.info ("error executing fsharp lint power shell process") 
    
    
    def start_file(self,file):
        Print.info("fsharp : Running extension code start file")
        self.file = file
        self.filename = file.get_path()
        if file.get_name().endswith('.fs'):
            Print.info('Scanning fs  file :'+str(Path(file.get_path()).name))
            if (os.path.isfile(file.get_path())):
                self.parsefsharpnamespace(file.get_path(), file);
                self.parsefsharpmodule(file.get_path(), file);
                self.parsefsharptype(file.get_path(), file);
                self.parsefsharplet(file.get_path(), file);
                self.parsefsharpopen(file.get_path(), file);
             
              
              
              
    def parsefsharpmodule(self, fsharpfile, file): 
        try :
            Print.info("file scan module :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('moduleexport', before='', element = 'module.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('module') is not -1:
                        if ref.value.find('=') is not -1: 
                                response = ref.value.replace("=", '"')
                                resp = response.replace("module", '"')
                                fsobj = cast.analysers.CustomObject()
                                fsobj.set_name(str(resp.strip()))
                                self.modulename =str(resp.strip())
                                fsobj.set_type('fsharp_module')
                                fsobj.set_parent(file)
                                parentFile = file.get_position().get_file() 
                                self.fielPath = parentFile.get_fullname()
                                fsobj.set_guid(self.fielPath+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                                fsobj.save()
                                setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                                Print.info("Save object module:"+resp.strip())
                             
                except ValueError:
                    Print.info ("error loading fsharp2 module")
        except:
            return          
    
    def parsefsharpnamespace(self, fsharpfile, file): 
        try :
            Print.info("file scan namespace :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('namespaceexport', before='', element = 'namespace.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('namespace') is not -1:
                        response = ref.value.replace("namespace", '"')
                        fsobj = cast.analysers.CustomObject()
                        fsobj.set_name(str(response.strip()))
                        self.namespace =str(response.strip())
                        fsobj.set_type('fsharp_namespace')
                        fsobj.set_parent(file)
                        parentFile = file.get_position().get_file() 
                        self.fielPath = parentFile.get_fullname()
                        fsobj.set_guid(self.fielPath+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                        fsobj.save()
                        Print.info("Save object namespace:"+response.strip())
                     
                except ValueError:
                    Print.info ("error loading fsharp2 namespace")
        except:
            return          
        
    def parsefsharptype(self, fsharpfile, file): 
        try :
            Print.info("file scan type :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('typeexport', before='', element = 'type.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('type') is not -1:
                        if ref.value.find('=') is not -1: 
                                response = ref.value.replace("=", '"')
                                resp = response.replace("type", '"')
                                fsobj = cast.analysers.CustomObject()
                                fsobj.set_name(str(resp.strip()))
                                fsobj.set_type('fsharp_type')
                                fsobj.set_parent(file)
                                parentFile = file.get_position().get_file() 
                                self.fielPath = parentFile.get_fullname()
                                fsobj.set_guid(self.fielPath+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                                fsobj.save()
                                setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                                Print.info("Save object type:"+resp.strip())
                             
                except ValueError:
                    Print.info ("error loading fsharp2 type")
        except:
            return          
        
    def parsefsharplet(self, fsharpfile, file): 
        try :
            Print.info("file scan let :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('letexport', before='', element = 'let.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(fsharpfile)]
            for ref in greferences:
                
                try:
                    if ref.value.find('let') is not -1:
                                response = ref.value.replace("=", '"')
                                resp = response.replace("let", '"')
                                fsobj = cast.analysers.CustomObject()
                                fsobj.set_name(str(resp.strip()))
                                fsobj.set_type('fsharp_let')
                                fsobj.set_parent(file)
                                parentFile = file.get_position().get_file() 
                                self.fielPath = parentFile.get_fullname()
                                fsobj.set_guid(resp+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                                fsobj.save()
                                setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                                setpropertyparent.add_propertymodule(fsobj,  self.modulename)
                                #Print.info("Save object let:"+resp.strip())
                             
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
                        response = ref.value.replace("open", '"')
                        fsobj = cast.analysers.CustomObject()
                        fsobj.set_name(str(response.strip()))
                        fsobj.set_type('fsharp_open')
                        fsobj.set_parent(file)
                        parentFile = file.get_position().get_file() 
                        self.fielPath = parentFile.get_fullname()
                        fsobj.set_guid(response+str(Path(file.get_path()).name)+str(random.randint(1, 200))+str(random.randint(1, 200)))
                        fsobj.save()
                        setpropertyparent.add_propertynamespace(fsobj,  self.namespace)
                        Print.info("Save object open:"+response.strip())
                 
                             
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