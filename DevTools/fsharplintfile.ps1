#Script to Extract fSharph lint  from source file..\fsharplintfile.ps1 > output.txt

param(
        [Parameter(
                    Mandatory=$true,
                    Position=0,
                    HelpMessage='Set path file variable')]
        [string] $w
)

#configure path as per your environment
[string]$input_path = $w

 
$FileExists = Test-Path $input_path 

If ($FileExists -eq $True) 
     {
	    
	    dotnet fsharplint lint  $input_path
		
     }

  Else {Write-Host "No file at this location"}
  

  


