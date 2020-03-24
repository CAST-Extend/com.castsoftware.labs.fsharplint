import cast_upgrade_1_6_5 # @UnusedImport
from cast.application import ApplicationLevelExtension,create_link,  ReferenceFinder, open_source_file
import logging
from subprocess import check_output, PIPE
import cast.application
import xml.etree.ElementTree as ET
import os
from pathlib import Path
import re
import  subprocess, sys
import shutil




class fsharpExtensionApplication(cast.application.ApplicationLevelExtension):

    def __init__(self): 
        self.ruledict={} 
        self.xmlfile="" 
        self.xmlroot=None
        self.Lintingfile=""
        self.Lintingerror=""
        self.errordesc=""
        self.errorlinestr=""
        self.currentsrcfile=""
        self.appobj=None
        self.fsharpmoduleObjReferences=None
        pass     
      
    def end_application(self, application):
        logging.info("fsharp : Running extension code at the end of an application")
        Rulekey = []
        RuleValue=[]
        self.appobj=application
        #declare ownershipship for 1 diags (this call also performs the required init cleaning)
        self.QAdeclarerules(application);
        #application.declare_property_ownership('fsharplint_CustomMetrics.RulesHintRefactor',["fsharp_module"])
        s= self.get_plugin()
        #logging.info(str(s.get_plugin_directory()))
        self.xmlfile =str(s.get_plugin_directory())+ "\\rulemap.xml" 
        logging.info(self.xmlfile)
        self.parsexmltree(self.xmlfile, "") 
         
        for o in application.search_objects(category='sourceFile'):
            fn = o.get_fullname()
            ff = o.get_name()
# 
#             
            if fn.endswith('.fs'):
                    self.currentsrcfile=fn
                    #logging.info('sourceFile objects successfully retrieved 1'+fn)
                #if fn.find("ModelConverter.fs") is not -1:   
                    self.reset()
                    
                    #proc=subprocess.call(["powershell", pspath, fn],stdout=subprocess.PIPE)
                     
                    cform= "dotnet fsharplint lint "+'"'+fn+'"'
                    #logging.info(cform)
                    result = self.run_command(cform)
                    cmdoutput = str(result[1])
                    #logging.info(str(result[1]))
                    if len(cmdoutput) > 0:
                        self.processmapping(application, cmdoutput, fn, o ) 
                    
    def searchmodule(self, application,key, file): 
       # try :
            #Print.info("file scan module :"+Path(file.get_path()).name)
            rf = ReferenceFinder()
            greferences = []
            rf.add_pattern('moduleexport', before='', element = 'module.*', after='')
            greferences += [reference for reference in rf.find_references_in_file(file)]
            for ref in greferences:
                
                try:
                    if ref.value.find('module') is not -1:
                        if ref.value.find('=') is not -1: 
                                response = ref.value.replace("=", '')
                                resp = response.replace("module", '') 
                                cleanvalue= re.sub('[^0-9a-zA-Z.]+', ' ', resp)
                                fsharpmoduleObjReferences = application.search_objects(category='fsharp_module',name=cleanvalue,  load_properties=False) 
                                if fsharpmoduleObjReferences is not None:
                                    for o in fsharpmoduleObjReferences: 
                                        self.scan_fs(application, key, o, file)
                
                except AttributeError:
                    logging.info("error search module sub")
        #except :
            #logging.info("error search module main")                  
                    
    def processmapping(self, application, result, sfile, program): 
        if result.find("Summary: 0 warnings")   is not  -1   and   result.find("Finished: 0 warnings") is not -1:
            logging.info("file as no error to map :" + sfile)
        else:
            #self.scan_fs(application,result, sfile)
            logging.info("processing  :" + sfile)
            split_sub="\\r\\n"
            split_mainsub="---------------------------------------------------"
            res = [i for i in range(len(result)) if result.startswith(split_sub, i)]
            #res = [i.start() for i in re.finditer("\r\n",  result)] 
            # printing result  
            #logging.info("The start indices of the substrings are : " + str(res)) 
            list_values = result.split(split_sub)
            for i in list_values:
              linevalue = str(i).replace("\\r", "")
              if linevalue.find('========== Finished:') is not -1:
                  break
              if linevalue.find("Linting")is not -1:
               self.Lintingfile=linevalue 
              if linevalue.startswith("Error"):
               self.Lintingerror=linevalue 
              if linevalue.endswith("."):
               self.errordesc=linevalue 
              if linevalue.find("^")is  -1 and  linevalue.find("==========")is -1 and  linevalue.find("Error") is -1 and linevalue.endswith(".") is False and linevalue.find('----------------------------') is - 1:   
                self.errorlinestr =linevalue
                #logging.info("error:"+str(self.errorlinestr))
              if linevalue.find('---------------------------------------------------') is not -1:
                key = self.parsexmltree(self.xmlfile, self.errordesc)
                if self.errordesc.find("`") is not -1:
                   #logging.info("inside key2" +str( self.errordesc)) 
                   key2 = self.partialparsexmltree(self.xmlfile, self.errordesc)
                   if key2 is not None and len(self.errorlinestr) >2 :
                      self.searchmodule( application,key2, program)
                      #logging.info("key:"  "key2:"+ str(key2))
                if key is not None and len(self.errorlinestr) >2:
                   #logging.info("inside key") 
                   self.searchmodule( application,key, program)
              
                
 
    def run_command(self, command):
        #print("Running command: {}".format(command))
        #os.system(command)
        p = subprocess.Popen(command, shell=True, stdout=PIPE)
        out, err = p.communicate()
        return (p.returncode, out, err)
    
    def parsexmltree(self, xmlfile, searchstr): 
         returnkey =""
         rulekey=[]
         rulevalue=[] 
         if  self.xmlroot != "" and searchstr =="":
            tree = ET.parse(xmlfile)  
            self.xmlroot = tree.getroot()
         else:
            tree = ET.parse(xmlfile)  
            self.xmlroot = tree.getroot()
            for elem in self.xmlroot.getiterator():
                try:
                    if (elem.tag == 'data'):
                        rulekey.append(str(elem.get('name')))
                        returnkey =str(elem.get('name'))
                        #logging.info(elem.get('name'))
                    if (elem.tag == 'value'):
                      if (elem.text) == searchstr:
                        rulevalue.append(str(elem.text))
                        #logging.info("desc:"+elem.text + " Key :"+ returnkey) 
                        break
                      else:
                        returnkey=None
                except AttributeError:
                    logging.info("error reading rule map")
            return returnkey
       
    def partialparsexmltree(self, xmlfile, searchstr): 
         returnkey =""
         finder=""
         rulekey=[]
         rulevalue=[] 
         logging.info("search:"+searchstr)
         if  self.xmlroot != "" and searchstr =="":
            tree = ET.parse(xmlfile)  
            self.xmlroot = tree.getroot()
         else:
            tree = ET.parse(xmlfile)  
            self.xmlroot = tree.getroot()
            for elem in self.xmlroot.getiterator():
                try:
                    if (elem.tag == 'data'):
                        rulekey.append(str(elem.get('name')))
                        returnkey =str(elem.get('name'))
                        #logging.info(elem.get('name'))
                    if (elem.tag == 'value'):
                        finder=""
                        if elem.text.find("`{0}`") is not - 1:
                          matchstrone = elem.text.split("`{0}`")[1]
                          finder=matchstrone
                          #logging.info("finder:"+ finder)
                          if elem.text.find("`{1}`") is not - 1:
                              matchstrtwo = finder.replace("`{1}`","")
                              matchstrtwo = matchstrtwo.replace(".","")
                              finder=matchstrtwo
                              #logging.info("findertwo:"+ finderparttwo)
                              
                        if ((searchstr.find(finder) is not -1)  and len(finder)>0):
                                rulevalue.append(str(elem.text))
                                #logging.info("desc:"+elem.text + " Key :"+ returnkey) 
                                break
                        else:
                          returnkey=None
                except AttributeError:
                    logging.info("error reading partial rule map")
                    returnkey=None
            return returnkey
        
        
    def reset(self):  
                    self.Lintingfile=""
                    self.Lintingerror=""
                    self.errordesc=""
                    self.errorlinestr=""
                    self.count=0       
          
    def scan_fs(self, application, errorkey,program, file):
        # one RF for multiples patterns
        if len(self.errorlinestr) >0:
           
            searchpattern= re.escape(self.errorlinestr)
           
            rfCall = ReferenceFinder()
            rfCall.add_pattern(('srcline'),before = '', element = searchpattern, after = '')     # requires application_1_4_7 or above
            
            # search all patterns in current program
            try:
               references = [reference for reference in rfCall.find_references_in_file(self.currentsrcfile)]
            except FileNotFoundError:
                logging.warning("Wrong file or file path:" + str(self.currentsrcfile))
            else:
               #try:   # for debugging and traversing the results
                for reference in references:
                    if  reference.pattern_name=='srcline':
                        reference.bookmark.file= file
                        #logging.info(reference.bookmark)
                    #logging.debug("DONE: reference found: >"+errorkey +str(reference))
                        program.save_violation('fsharplint_CustomMetrics_'+errorkey+"."+errorkey, reference.bookmark)
                        logging.info("violation saved: >" +'fsharplint_CustomMetrics.'+errorkey+"  line:::"+self.errorlinestr)
               #except:
                   #logging.warning("violation not saved" +self.errorlinestr+"file " +str(self.currentsrcfile))
            
    def QAdeclarerules(self, application):
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFailwithfWithArgumentsMatchingFormatString.RulesFailwithfWithArgumentsMatchingFormatString',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFailwithWithSingleArgument.RulesFailwithWithSingleArgument',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFavourIgnoreOverLetWildError.RulesFavourIgnoreOverLetWildError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesReimplementsFunction.RulesReimplementsFunction',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesHintRefactor.RulesHintRefactor',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesHintSuggestion.RulesHintSuggestion',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNamingConventionsCamelCaseError.RulesNamingConventionsCamelCaseError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNamingConventionsPascalCaseError.RulesNamingConventionsPascalCaseError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNamingConventionsUnderscoreError.RulesNamingConventionsUnderscoreError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNamingConventionsPrefixError.RulesNamingConventionsPrefixError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNamingConventionsPrefixError.RulesNamingConventionsPrefixError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNestedStatementsError.RulesNestedStatementsError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNumberOfItemsBooleanConditionsError.RulesNumberOfItemsBooleanConditionsError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNumberOfItemsClassMembersError.RulesNumberOfItemsClassMembersError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNumberOfItemsFunctionError.RulesNumberOfItemsFunctionError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNumberOfItemsTupleError.RulesNumberOfItemsTupleError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesRaiseWithSingleArgument.RulesRaiseWithSingleArgument',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesSourceLengthError.RulesSourceLengthError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyFileLengthError.RulesTypographyFileLengthError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyTabCharacterError.RulesTypographyTabCharacterError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyTrailingLineError.RulesTypographyTrailingLineError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyTrailingWhitespaceError.RulesTypographyTrailingWhitespaceError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesUselessBindingError.RulesUselessBindingError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesWildcardNamedWithAsPattern.RulesWildcardNamedWithAsPattern',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesInvalidArgWithTwoArguments.RulesInvalidArgWithTwoArguments',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesInvalidOpWithSingleArgument.RulesInvalidOpWithSingleArgument',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesNullArgWithSingleArgument.RulesNullArgWithSingleArgument',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTupleOfWildcardsError.RulesTupleOfWildcardsError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesCanBeReplacedWithComposition.RulesCanBeReplacedWithComposition',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesRedundantNewKeyword.RulesRedundantNewKeyword',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingPatternMatchClausesOnNewLineError.RulesFormattingPatternMatchClausesOnNewLineError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingPatternMatchOrClausesOnNewLineError.RulesFormattingPatternMatchOrClausesOnNewLineError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingTupleCommaSpacingError.RulesFormattingTupleCommaSpacingError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingTupleIndentationError.RulesFormattingTupleIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingTupleParenthesesError.RulesFormattingTupleParenthesesError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingTypedItemSpacingError.RulesFormattingTypedItemSpacingError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingFArrayPostfixError.RulesFormattingFArrayPostfixError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingFPostfixGenericError.RulesFormattingFPostfixGenericError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingGenericPrefixError.RulesFormattingGenericPrefixError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingPatternMatchClauseIndentationError.RulesFormattingPatternMatchClauseIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingLambdaPatternMatchClauseIndentationError.RulesFormattingLambdaPatternMatchClauseIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingPatternMatchClauseSameIndentationError.RulesFormattingPatternMatchClauseSameIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingMatchExpressionIndentationError.RulesFormattingMatchExpressionIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingModuleDeclSpacingError.RulesFormattingModuleDeclSpacingError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingClassMemberSpacingError.RulesFormattingClassMemberSpacingError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingUnionDefinitionIndentationError.RulesFormattingUnionDefinitionIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesFormattingUnionDefinitionSameIndentationError.RulesFormattingUnionDefinitionSameIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesConventionsTopLevelNamespaceError.RulesConventionsTopLevelNamespaceError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyIndentationError.RulesTypographyIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyRecordFieldIndentationError.RulesTypographyRecordFieldIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesTypographyOverridenIndentationError.RulesTypographyOverridenIndentationError',["fsharp_module"])
        application.declare_property_ownership('fsharplint_CustomMetrics_RulesConventionsRecursiveAsyncFunctionError.RulesConventionsRecursiveAsyncFunctionError',["fsharp_module"])