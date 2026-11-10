'''
Program: IP Port Scanner and Operating System Detection
Author: Lauren Ashbee laurenashbee4@gmail.com
Course: BCIT XCSA-1100, Final Project

This program uses the Python-Nmap library, and a user-supplied
target_ip address to scan the top 1000 TCP ports and identify open ports
and detect the operating system.

The user is prompted for an ip_address in the terminal. The scan results,
including port states, services running, and possible OS matches are then
displayed in the terminal.
'''

import nmap
import sys

# Get the target_ip address from the user
# .strip() removes leading and trailing spaces
print('\n')
target_ip = input("Enter the ip address you wish to scan: ").strip()

print('\n')
print("Scanning Ports and Detecting Operating System: \n")

# Create a scanner object from the PortScanner class in nmap module
scanner = nmap.PortScanner()

# Start an nmap scan with disabled host discovery (-Pn),
# service/version detection (-sV), and OS detection (-O).
# Scan results are stored internally in the scanner object!
scanner.scan(target_ip, arguments = "-Pn -sV -O")

# Check if Nmap returned the target IP address.
# If it did, retrieve the inner dictionary of the scan's results.
# Otherwise print a message and exit.
if target_ip in scanner.all_hosts():
    scan_results = scanner[target_ip]    
else:
    print(f'\nNo scan results returned for {target_ip}. Device is possibly offline.')
    sys.exit()

# Retrieve tcp ports info and the os matches from the scan results
# If either key is not present, use an empty list or dictionary.
ports = scan_results.get('tcp', {})
os_matches = scan_results.get('osmatch', [])

# If TCP port info was returned, iterate through each key-value pair.
# The key is the port number and the value is the dictionary of info
# about the port, including its state and service name.
# If no port info was returned print a message.
if ports:
    for port, port_info in ports.items():
        print(f'Port {port} is {port_info.get('state', 'in an unknown state')}. The service is {port_info.get('name', 'unknown')}.')
else:
    print('No ports are open.')

print('\n')

# If OS matches were returned, iterate through them using enumerate
# Each match is a dictionary containing a possible OS match and its
# accuracy percentage.
# If a key is not present, use 'not detected' or 0.
# If no matches are returned, print a message
if os_matches:
    for index, match in enumerate(os_matches):
        print(f'Match {index + 1} of {len(os_matches)} possible matches:')
        print(f'Operating System: {match.get('name', 'not detected')}')
        print(f'Match Accuracy: {match.get('accuracy', 0)}%')
        print('\n')
else:
    print('The operating system could not be detected.')

print('\nScan complete.\n')