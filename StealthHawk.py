import os
import subprocess
import requests
import time
from tqdm import tqdm
from colorama import init, Fore

# Initialize colorama for colored terminal output
init(autoreset=True)

class ToolChecker:
    """
    Class to check the availability of required tools and install them if missing.
    """
    tools = ["dirsearch", "sublist3r", "amass", "curl", "nmap", "whatweb", "nikto", "sslscan", "tor", "proxychains"]

    @staticmethod
    def check_and_install_tools():
        """
        Checks for the presence of required tools, installs them if not found.
        """
        print(Fore.GREEN + "Testing for Tools...")
        for tool in tqdm(ToolChecker.tools, desc="Checking Tools", ncols=75):
            # Check if the tool is available on the system
            result = subprocess.run(f"which {tool}", shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(Fore.GREEN + f"Success: {tool} is installed.")
            else:
                print(Fore.RED + f"Failed to find {tool}. Installing it now...")
                ToolChecker.install_tool(tool)

    @staticmethod
    def install_tool(tool):
        """
        Installs a missing tool using the apt package manager.
        """
        print(Fore.YELLOW + f"Installing {tool}...")
        # Using subprocess.run to execute the installation command
        subprocess.run(f"sudo apt-get install -y {tool}", shell=True, check=True)
        print(Fore.GREEN + f"{tool} installation complete.")

class TorManager:
    """
    Class to handle TOR network configuration and connection checks.
    """
    @staticmethod
    def check_tor_connection():
        """
        Verifies the connection to the TOR network by making an HTTP request.
        """
        print(Fore.YELLOW + "Checking TOR connection...")
        # Configure proxy settings for TOR
        proxies = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'}
        try:
            # Attempt to retrieve the current IP address using the TOR network
            response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
            print(Fore.GREEN + "Connected to TOR. Your IP is: " + response.text)
            return True
        except requests.RequestException as e:
            # Handle connection failure
            print(Fore.RED + "Failed to connect to TOR. Ensure TOR is running.")
            return False

class ProxyManager:
    """
    Class to manage and validate proxy chains from a provided file.
    """
    @staticmethod
    def validate_proxychains(file_path):
        """
        Validates a list of proxies by testing connections to each proxy.
        """
        print(Fore.YELLOW + "Validating proxy chain list...")
        valid_proxies = []
        # Read the proxy list from the file
        with open(file_path, 'r') as file:
            proxies = file.readlines()
        for proxy in proxies:
            proxy = proxy.strip()
            if ProxyManager.test_proxy(proxy):
                valid_proxies.append(proxy)
                print(Fore.GREEN + f"Success: Proxy {proxy} is valid.")
            else:
                print(Fore.RED + f"Failed: Proxy {proxy} is not valid.")
        return valid_proxies

    @staticmethod
    def test_proxy(proxy):
        """
        Tests a single proxy by attempting a connection to a web service.
        """
        try:
            # Attempt to connect using the proxy
            response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
            return response.ok
        except requests.RequestException:
            return False

class ReconTool:
    """
    Base class for defining common functionalities for reconnaissance tools.
    """
    def __init__(self, domain, use_tor=False, proxies=None):
        self.domain = domain
        self.use_tor = use_tor
        self.proxies = proxies

    def run(self):
        """
        Runs the reconnaissance tool. To be overridden by subclasses.
        """
        pass

class Dirsearch(ReconTool):
    """
    Class implementing the Dirsearch tool for directory brute-forcing.
    """
    def run(self):
        """
        Executes Dirsearch with the provided domain.
        """
        base_command = f"dirsearch -u {self.domain} -e *"
        # Append proxychains if using TOR or proxies
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        # Execute the command and capture the output
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class Sublist3r(ReconTool):
    """
    Class implementing the Sublist3r tool for subdomain enumeration.
    """
    def run(self):
        """
        Executes Sublist3r with the provided domain.
        """
        base_command = f"sublist3r -d {self.domain} -o subdomains.txt"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class Amass(ReconTool):
    """
    Class implementing the Amass tool for subdomain and OSINT enumeration.
    """
    def run(self):
        """
        Executes Amass with the provided domain.
        """
        base_command = f"amass enum -d {self.domain} -o amass_subdomains.txt"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class Curl(ReconTool):
    """
    Class implementing the cURL tool for HTTP header analysis.
    """
    def run(self):
        """
        Executes cURL to retrieve HTTP headers for the provided domain.
        """
        base_command = f"curl -I {self.domain}"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class Nmap(ReconTool):
    """
    Class implementing the Nmap tool for network scanning and port discovery.
    """
    def run(self):
        """
        Executes Nmap to scan for open ports and services on the provided domain.
        """
        base_command = f"nmap -sV -p- {self.domain}"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class WhatWeb(ReconTool):
    """
    Class implementing the WhatWeb tool for technology identification.
    """
    def run(self):
        """
        Executes WhatWeb to identify technologies used by the web application on the provided domain.
        """
        base_command = f"whatweb {self.domain}"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class Nikto(ReconTool):
    """
    Class implementing the Nikto tool for web server vulnerability scanning.
    """
    def run(self):
        """
        Executes Nikto to scan for known vulnerabilities on the provided domain's web server.
        """
        base_command = f"nikto -h {self.domain}"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class SSLScan(ReconTool):
    """
    Class implementing the SSLScan tool for SSL/TLS configuration analysis.
    """
    def run(self):
        """
        Executes SSLScan to analyze the SSL/TLS configuration of the provided domain.
        """
        base_command = f"sslscan {self.domain}"
        if self.use_tor:
            command = f"proxychains {base_command}"
        elif self.proxies:
            command = f"proxychains -q {base_command}"
        else:
            command = base_command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)
        return process.stdout

class StealthHawk:
    """
    Main class for the StealthHawk reconnaissance tool.
    """
    def __init__(self):
        self.domains = []
        self.use_tor = False
        self.proxies = []

    def clear_screen(self):
        """
        Clears the terminal screen for a clean output view.
        """
        os.system('clear')

    def ensure_https(self, url):
        """
        Ensures the provided URL uses HTTPS protocol.
        """
        if not url.startswith("http"):
            return "https://" + url
        return url

    def main_menu(self):
        """
        Displays the main menu and collects user input for target domains.
        """
        self.clear_screen()
        print(Fore.GREEN + "Welcome to StealthHawk")
        print(Fore.BLUE + "A powerful tool for stealthy reconnaissance and vulnerability assessment.")
        time.sleep(1)
        self.domains = input(Fore.YELLOW + "Enter domain(s) separated by space: ").split()

    def configure_tor(self):
        """
        Configures the TOR connection based on user preference.
        """
        self.use_tor = input(Fore.YELLOW + "Do you want to use TOR nodes? (yes/no): ").strip().lower() == 'yes'
        if self.use_tor:
            if not TorManager.check_tor_connection():
                print(Fore.RED + "Exiting... Please start TOR service and try again.")
                exit()

    def configure_proxies(self):
        """
        Configures proxy chains based on user preference and validates them.
        """
        if input(Fore.YELLOW + "Do you want to use a proxy chain list? (yes/no): ").strip().lower() == 'yes':
            proxy_file = input(Fore.YELLOW + "Enter the path to your proxy chain file: ").strip()
            self.proxies = ProxyManager.validate_proxychains(proxy_file)

    def run_tools(self):
        """
        Runs reconnaissance tools on the provided domains using the configured options.
        """
        for domain in self.domains:
            domain = self.ensure_https(domain)
            # Initialize and run Dirsearch tool with specified options
            dirsearch = Dirsearch(domain, use_tor=self.use_tor, proxies=self.proxies)
            dirsearch_output = dirsearch.run()
            print(Fore.CYAN + "Dirsearch Results:")
            print(dirsearch_output)

            # Initialize and run Sublist3r tool
            sublist3r = Sublist3r(domain, use_tor=self.use_tor, proxies=self.proxies)
            sublist3r_output = sublist3r.run()
            print(Fore.CYAN + "Sublist3r Results:")
            print(sublist3r_output)

            # Initialize and run Amass tool
            amass = Amass(domain, use_tor=self.use_tor, proxies=self.proxies)
            amass_output = amass.run()
            print(Fore.CYAN + "Amass Results:")
            print(amass_output)

            # Initialize and run Curl tool
            curl = Curl(domain, use_tor=self.use_tor, proxies=self.proxies)
            curl_output = curl.run()
            print(Fore.CYAN + "Curl HTTP Headers:")
            print(curl_output)

            # Initialize and run Nmap tool
            nmap = Nmap(domain, use_tor=self.use_tor, proxies=self.proxies)
            nmap_output = nmap.run()
            print(Fore.CYAN + "Nmap Scan Results:")
            print(nmap_output)

            # Initialize and run WhatWeb tool
            whatweb = WhatWeb(domain, use_tor=self.use_tor, proxies=self.proxies)
            whatweb_output = whatweb.run()
            print(Fore.CYAN + "WhatWeb Results:")
            print(whatweb_output)

            # Initialize and run Nikto tool
            nikto = Nikto(domain, use_tor=self.use_tor, proxies=self.proxies)
            nikto_output = nikto.run()
            print(Fore.CYAN + "Nikto Scan Results:")
            print(nikto_output)

            # Initialize and run SSLScan tool
            sslscan = SSLScan(domain, use_tor=self.use_tor, proxies=self.proxies)
            sslscan_output = sslscan.run()
            print(Fore.CYAN + "SSLScan Results:")
            print(sslscan_output)

    def execute(self):
        """
        Executes the main logic of the StealthHawk tool.
        """
        self.main_menu()
        self.configure_tor()
        self.configure_proxies()
        self.run_tools()

if __name__ == "__main__":
    # Create an instance of StealthHawk and execute the main program
    stealth_hawk = StealthHawk()
    stealth_hawk.execute()
