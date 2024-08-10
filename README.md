# StealthHawk

**StealthHawk** is a powerful reconnaissance tool designed for ethical hackers and security professionals. It combines various reconnaissance techniques with advanced anonymity options, using TOR and proxy chains to protect user identity during operations.

## Features

- **Directory Brute-Forcing:** Utilize `dirsearch` to find hidden directories and files on web servers.
- **Subdomain Enumeration:** Use `Sublist3r` and `amass` for comprehensive subdomain discovery.
- **HTTP Header Analysis:** Retrieve and analyze HTTP headers with `cURL`.
- **Network Scanning:** Identify open ports and services with `Nmap`.
- **Technology Identification:** Detect technologies used by web applications with `WhatWeb`.
- **Vulnerability Scanning:** Scan for known vulnerabilities with `Nikto`.
- **SSL/TLS Analysis:** Analyze SSL/TLS configurations with `SSLScan`.
- **Anonymity Options:** Optionally route all traffic through TOR or custom proxy chains.

## Installation

### Prerequisites

- **Kali Linux:** StealthHawk is designed to run on Kali Linux or other Debian-based distributions.
- **Python 3.x:** Ensure Python 3.x is installed on your system.
- **Required Tools:** The script will automatically check for required tools and install them if missing.

### Installing Python Dependencies

Clone the repository and navigate to the directory:

```
$ git clone https://github.com/yourusername/stealthhawk.git
$ cd stealthhawk
```
_Create a virtual environment (optional but recommended):_
```
$ python3 -m venv stealthhawk_env
$ source stealthhawk_env/bin/activate
```
_Install the Python packages from requirements.txt:_
```
$ pip install -r requirements.txt
```
### Usage 
1. Run the Script:
```
$ python3 StealthHawk.py
```
2. Follow the On-Screen Instructions:
  * Enter one or more domains to target.
  * Choose whether to use TOR Nodes for Anonymit.
  * Choose whether to use a custom proxy chain list.

## Configuration

### TOR
_To use TOR, ensure the TOR service is installed and running:
```
$ sudo apt-get install -y tor
$ sudo service tor start
```
### Proxy Chains
If using a custom proxy list, create a text file with one proxy per line in the format:  
`http://ip:port`  
OR  
`https://ip:port`  

### Contributin
_Contributions are welcome! Please follow these steps:
1. Fork the repository.  
2. Create a new branch (`git checkout -b feature/YourFeature`).  
3. Make your changes and commit them (`git commit -am 'Add your feature notes'`).  
4. Push to the branch (`git push origin feature/YourFeature`).  
5. Open a Pull Request.  

## Contact
_If you would like to contact the developer, please utilize the following methods:_  
alove@darkmcs.com | roguepayload@darkmcs.com  
https://darkmcs.com  

