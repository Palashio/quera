@echo on

:: define args
set JDK="C:\\Program Files\\Java\\jdk1.8.0_221"
set methodName=sampleIf
set methodIntParamsCount=1
set ID=%1
set fileName=%2
set filePath=%ID%/%fileName% 
set loggerPath=%3

start java -jar fuzzing.jar %JDK% %ID% %loggerPath% %filePath% %methodName% %methodIntParamsCount%


python nnFuzzer.py %ID%


