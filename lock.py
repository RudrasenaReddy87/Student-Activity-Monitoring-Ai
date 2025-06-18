import os
import ctypes
import sys
import subprocess

# List of websites to block
websites_to_block = [
    "www.youtube.com",
    "www.facebook.com",
    "www.instagram.com",
    "www.twitter.com",
    "www.reddit.com",
    "www.tiktok.com",
    "www.netflix.com",
    "www.amazon.com",
    "www.linkedin.com",
    "www.whatsapp.com",
    "leetcode.com",
    "hackerrank.com",
    "codechef.com",
    "geeksforgeeks.org",
    "codeforces.com",
    "topcoder.com",
    "atcoder.jp",
    "edabit.com",
    "codewars.com",
    "cs50.harvard.edu"
]

# Windows hosts file path
hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect_ip = "127.0.0.1"

# Function to check for admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except Exception:
        return False

# Function to request admin privileges if not already elevated
def run_as_admin():
    if not is_admin():
        print("[!] Requesting administrator privileges...")
        # Relaunch the script with elevated privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

# Function to block websites by modifying the hosts file
def block_websites():
    try:
        print("[+] Blocking websites...")

        # Ensure the script is running with admin privileges
        if not os.access(hosts_path, os.W_OK):
            raise PermissionError("Permission denied: Cannot write to hosts file.")

        # Read the current hosts file
        with open(hosts_path, "r+") as file:
            content = file.read()
            lines_to_add = []

            for website in websites_to_block:
                if website not in content:
                    lines_to_add.append(f"{redirect_ip} {website}\n")

            if lines_to_add:
                file.write("\n" + "".join(lines_to_add))
                print("[✔] Websites have been successfully blocked!")
            else:
                print("[!] All websites are already blocked.")

    except PermissionError as pe:
        print(f"[-] Error: {pe}")
    except Exception as e:
        print(f"[-] Error: {e}")

# Function to flush the DNS cache
def flush_dns():
    try:
        print("[+] Flushing DNS cache...")
        subprocess.run("ipconfig /flushdns", shell=True, check=True)
        print("[✔] DNS cache successfully flushed!")
    except Exception as e:
        print(f"[-] Failed to flush DNS cache: {e}")

# Main function
if __name__ == "__main__":
    # Ensure admin privileges
    run_as_admin()

    # Block the websites
    block_websites()

    # Flush the DNS cache to apply changes
    flush_dns()

