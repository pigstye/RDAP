<#
	.SYNOPSIS
		Lookup RDAP (Registration Data Access Protocol) information about a website or IP address
	.DESCRIPTION
		Uses rdap.org to look up the RDAP data - the replacement for Whois - about a website or IP address.
        It determines whether it is an IP or domain with a regular expression. It returns a PowerShell object with the data.
        It will accept pipeline data.
	.Parameter webIP
		Either the IP or domain name
    .INPUTS
        Either an IP address or domain name
    .OUTPUTS
        A PowerShell object containing the rdap data
	.EXAMPLE
		> "127.0.0.1" | .\rdap.ps1 
        An IP address sent through pipeline
    .EXAMPLE
        > .\rdap.ps1 'www.example.com'
    .EXAMPLE
        > ('www.example.com' | .\rdap.ps1).events
        To return the registration dates
	.NOTES
	Author: Tom Willett 
	Date: 4/21/2025
#>
Param([Parameter(Mandatory=$True,ValueFromPipeline=$True)][string]$webIP)

process {
    # Regex to detect a valid IP
    $regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

    # url to do the lookup
    $url='https://rdap.org/'
    
    if ($webIP -match $regex) {$url += 'ip/' + $webIP} else {$url += 'domain/' + $webIP}
    $t=(new-object Net.WebClient).DownloadString($url)
    $rdap = $t | ConvertFrom-Json
    return $rdap
}
