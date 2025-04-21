# RDAP
Python and PowerShell scripts to query RDAP Registration Data Access Protocol) data - the replacement for Whois.
Here are two simple programs to query RDAP data. 
The more complicated is in Python3.11 developed on a Debian 12 Bookworm.
The simple one is PowerShell script designed to be used in a pipeline.
Both are somewhat self documenting but there is a more complete explanation of both below.
In my testing rdap was not as reliable as Whois and often ran into rate limits.
Not all registrars return the same information. The reliable things that were returned were:  'type', 'status', 'startAddress', 'rdapConformance', 'port43', 'objectClassName', 'notices', 'name', 'links', 'ipVersion', 'handle', 'entities' and 'endAddress'. Sometimes 'events' (registration dates), 'country' and  'cidr0_cidrs' are available. Seldom 'remarks' and 'redacted' are also available.
The data is returned as json with embedded json and lists designed to be easy to parse.
## rdap.py
By default both rdap.py and rdap.ps1 will determine if they are given an IP address or Domain name and proceed accordanly. rdap.py has some other options.
By default it will return a pretty printed version of the data but the --json flag will cause it to return the original json.
You can use the --type option to request one of the other queries like autnum or entity. These vary by registrar.
Finally the --property option accepts a comma delimited group of properties that are returned. You could, for instance ask for the dates and nameservers with "--property events,nameservers". Additionally you can do "--property keys" and it will return the list of properies available.
##rdap.ps1
This is a much simpler implementation. It can be fed an IP or Domain and it will return the RDAP data as a PowerShell object. It accepts both pipeline and normal parameters. It has no error handling. If I was going to use this script, as I often did Whois while working, I would create a PowerShell script that accepted the object and extracted the data of interest and wrote it to a csv file. That way I could feed it a list of IPs and Domains and collect the data. It would not be hard but I have better things to do.
