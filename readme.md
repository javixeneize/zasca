# Yasca

Yasca (Yet Another SCA tool) is an opensource SCA tool based on Github advisories.

This is presented as a CLI tool, covering only Maven based projects by now.

## How does it work

It is quite simple to understand how the tool works. Given a pom.xml, it generates the dependency tree, retrieves all
the libraries, and for each of them, it queries Github advisory endpoint to check if there is any vulnerability.

Finally, it generates a report with all the vulnerabilities in all the libraries used in the project.

Because it needs to connect to github, the tool needs to have a valid github PAT configured as an enviromental
variable (GITHUB_TOKEN)

## How to use it

First of all, as pre-requirements, it requres Maven installed, as it needs to build the dependency tree, and a github
PAT configured as an enviromental variable, as detailed above.

This is still not included in pypi, so you can either run the pyhton script, or download the code and install it as a
local package. It will generate a binary called Yasca-cli

The tool needs to receive a parameter with the path to the pom.xml to be scanned. It also has two optional parameters

--html (default True): To generate an html report 

--sbom (default False): To generate a cyclonedx sbom file 

