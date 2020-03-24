#Script to Extract fSharph lint  from source file..\fsharplintbatch.ps1 > output.txt

param(
        [Parameter(
                    Mandatory=$true,
                    Position=0,
                    HelpMessage='Set path variable')]
        [string] $w
)

#configure path as per your environment
$input_path = $w

 
$FileExists = Test-Path $input_path 
#Set-Location -Path 'C:\fsharp'
If ($FileExists -eq $True) 
     {
		Get-ChildItem -Path $input_path -Recurse -ErrorAction SilentlyContinue -Filter *.fs | Select FullName | convertto-csv | out-file "fsharplist.csv"

     }

  Else {Write-Host "No file at this location"}
  
$fsList = Import-Csv -Path 'fsharplist.csv'
ForEach ($fs in $fsList) {

    $fname="'$fs'"
	$fnn=$fname -replace "'@{"
	$fnnr=$fnn -replace "FullName="
	$fin=$fnnr -replace "}'"
	$FilePathWithQuotes = '"{0}"' -f $fin
	
	#Write-Host $FilePathWithQuotes
    #Set-Location -Path 'C:\Program Files\dotnet\sdk'
    dotnet fsharplint lint  $FilePathWithQuotes 
	
	
}
  


