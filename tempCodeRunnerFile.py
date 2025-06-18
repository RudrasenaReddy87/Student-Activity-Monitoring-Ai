import os
import ctypes
import sys
import subprocess

# List of websites to unblock
websites_to_unblock = [
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

# Ensure admin privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except Exception:
        return False

def run_as_admin():
    if not is_admin():
        print("[!] Requesting administrator privileges...")
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        sys.exit()

# Function to unblock websites
def unblock_websites():
    try:
        print("[+] Unblocking websites...")

        # Ensure admin access
        if not os.access(hosts_path, os.W_OK):
            raise PermissionError("Permission denied: Cannot write to hosts file.")

        # Read and filter the hosts file
        with open(hosts_path, "r") as file:
            lines = file.readlines()

        with open(hosts_path, "w") as file:
            for line in lines:
                if not any(website in line for website in websites_to_unblock):
                    file.write(line)

        print("[✔] Websites have been successfully unblocked!")

    except PermissionError as pe:
        print(f"[-] Error: {pe}")
    except Exception as e:
        print(f"[-] Error: {e}")

# Flush DNS cache
def flush_dns():
    try:
        print("[+] Flushing DNS cache...")
        subprocess.run("ipconfig /flushdns", shell=True, check=True)
        print("[✔] DNS cache successfully flushed!")
    except Exception as e:
        print(f"[-] Failed to flush DNS cache: {e}")

# Main
if __name__ == "__main__":
    run_as_admin()
    unblock_websites()
    flush_dns()
