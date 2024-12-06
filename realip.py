import socket
import os
from ipaddress import ip_address, ip_network
from datetime import datetime
import time
import sys

# List of Cloudflare IP ranges
CLOUDFLARE_IP_RANGES = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
]

def is_cloudflare_ip(ip):
    """Check if an IP is within Cloudflare's range."""
    try:
        ip_obj = ip_address(ip)
        for cf_range in CLOUDFLARE_IP_RANGES:
            if ip_obj in ip_network(cf_range):
                return True
    except ValueError:
        pass
    return False

def resolve_domain(domain):
    """Resolve a domain to its IP addresses and check if they are Cloudflare IPs."""
    try:
        ips = socket.gethostbyname_ex(domain)[2]  # Get all resolved IPs
        if not ips:
            return ["No IP Found"]

        result = []
        for ip in ips:
            ip_type = "Cloudflare IP" if is_cloudflare_ip(ip) else "Real IP"
            result.append(f"{ip} ({ip_type})")
        return result
    except socket.gaierror:
        return ["No IP Found"]

def scan_domains(domains, output_file):
    """Scan domains and write results to a file."""
    with open(output_file, "w") as outfile:
        for domain in domains:
            domain = domain.strip()
            if domain:
                ips = resolve_domain(domain)
                result = f"{domain} - {', '.join(ips)}\n"
                print(result.strip())
                outfile.write(result)
    print(f"\033[1;32mScan completed. Results saved in {output_file}.\033[0m")

def generate_filename(input_source):
    """Generate a file name based on the input source (domain list or file) with a timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if isinstance(input_source, str):
        # If it's a single domain name, use it to generate the filename
        return f"{input_source}_{timestamp}_result.txt"
    else:
        # If it's a file input (list of domains), use the file name
        return f"{os.path.basename(input_source).split('.')[0]}_{timestamp}_result.txt"

def typing_effect(text, delay=0.01):  # Reduced delay for faster typing
    """Simulate typing effect for text output."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # To move to the next line after the typing effect.

def display_name():
    # Name Art with style
    name_art = """
    \033[32m
    █████╗ ███████╗ █████╗ ██████╗ ██╗███╗   ██╗███████╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║████╗  ██║██╔════╝
    ███████║███████╗███████║██████╔╝██║██╔██╗ ██║███████╗
    ██╔══██║╚════██║██╔══██║██╔══██╗██║██║╚██╗██║╚════██║
    ██║  ██║███████║██║  ██║██║  ██║██║██║ ╚████║███████║
    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═╝  ╚═══╝╚══════╝
    """
    
    # Tool Name with added colors and bold formatting
    tool_name = "\033[1;36mTool Name: Web Domain Scanner\033[0m"

    # Adding a separator with color
    separator = "\033[1;34m" + "="*60 + "\033[0m"

    # Display the result with typing effect
    print(separator)
    typing_effect(name_art)
    print(separator)
    typing_effect(tool_name)
    print(separator)

def main():
    try:
        display_name()  # Display the banner with typing effect
        typing_effect("\033[1;33mWelcome to the Domain Scanner Tool!\033[0m")
        typing_effect("Choose an option:")
        typing_effect("1. Enter a single domain")
        typing_effect("2. Provide a file with a list of domains")

        choice = input("Enter your choice (1 or 2): ").strip()
        domains = []

        if choice == "1":
            domain = input("Enter the domain name: ").strip()
            if domain:
                domains.append(domain)
                output_file = generate_filename(domain)
            else:
                typing_effect("Invalid input. Exiting.")
                return
        elif choice == "2":
            file_path = input("Enter the path to the file with domains: ").strip()
            if os.path.exists(file_path):
                with open(file_path, "r") as infile:
                    domains = infile.readlines()
                output_file = generate_filename(file_path)
            else:
                typing_effect("File not found. Exiting.")
                return
        else:
            typing_effect("Invalid choice. Exiting.")
            return

        scan_domains(domains, output_file)

    except KeyboardInterrupt:
        # Catch the Ctrl+C and show a custom exit message
        print("\n\033[1;31mExiting... Goodbye!\033[0m")  # Red color for exit message
        sys.exit(0)

if __name__ == "__main__":
    main()
