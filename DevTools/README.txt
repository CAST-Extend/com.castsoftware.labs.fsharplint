***********************
*       README        *
***********************

  MetricsCompiler.bat (deployed by JENKINS)
  -----------------------------------------
  CLI for the portable and lightweight Metrics Compiler. 
  This MetricsCompiler provides basic commands for people working on AssessmentModel fragments: CoE, UA, Extensions, Components
  usage: MetricsCompiler -help
  Required Files:
	- MetricsCompilerCLI.jar
	- (optionally postgresql-9.2.1004.jdbc3.jar)


  MetricsCompilerCLI.jar (deployed by JENKINS)
  --------------------------------------------
  MetricsCompiler classes for the CLI and the API. 


***********************
* DEPRECATED Material *
***********************

  MetricsCompiler.jar 
  -------------------
  Required for the Doc2Conf tool.
  It should be discarded
  Generated with Script ANT: svn:\AssessmentModelMasterFiles\scripts\

  CASTMS/CAST-MetricsCompiler.jar (deployed by JENKINS)
  -----------------------------------------------------
  Required for the Doc2Conf tool.
  It should be replaced with MetricsCompilerCLI.jar
  
  Changes required in QualityRules2Conf.groovy
  ---------------------------------------------
  import com.castsoftware.metricscompiler.*
  import com.castsoftware.metricscompiler.masterfiles.*
  import MetricsCompiler
  def metrics = new Metrics(ModelType.FULL, ParserSeverity.LAX);
  MetricsCompiler.setSettingsFromTemplates(inputDir);
  MasterModelsParser.parse(inputDir, metrics);
  
  import com.castsoftware.metricscompiler.*;
  import com.castsoftware.metricscompiler.masterfiles.*;
  // removed include
  def inputDir = "";
  def metrics = new Metrics(ModelType.FULL, ParserSeverity.LAX);
  MetricsCompilerCLI.setSettingsFromTemplates(inputDir); // see MetricsCompilerCLI
  MasterModelsParser.parse(inputDir, metrics);

  Changes required in ConvertDoc.groovy
  -------------------------------------
  Ref to 'MetricsCompiler.jar' and '\\EngBuild\\NightlyBuilds\\AssessmentModel\\CASTMS\\CAST-MetricsCompiler.jar'
  must be replaced with '\\EngBuild\\NightlyBuilds\\AssessmentModel\\MetricsCompilerCLI.jar'
