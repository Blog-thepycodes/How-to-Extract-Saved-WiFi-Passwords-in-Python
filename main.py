import subprocess
import re
import platform
 
 
def get_wifi_passwords():
   system = platform.system()
   passwords = {}
   try:
       if system == 'Windows':
           result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, check=True)
           profiles = re.findall(r'All User Profile\s*:\s*(.*)', result.stdout)
           for profile in profiles:
               profile_result = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True, check=True)
               if "Key Content" in profile_result.stdout:
                   password_line = [line.strip() for line in profile_result.stdout.splitlines() if "Key Content" in line][0]
                   password = password_line.split(":")[1].strip()
                   passwords[profile] = password
       elif system == 'Linux':
           result = subprocess.run(['nmcli', 'connection', 'show', '--active'], capture_output=True, text=True, check=True)
           connections = re.findall(r'(\S+)\s+\S+\s+\S+\s+wifi\s+\S+\s+(\S+)', result.stdout)
           for connection in connections:
               ssid = connection[0]
               password_result = subprocess.run(['nmcli', 'connection', 'show', 'id', ssid, 'wifi.secrets'], capture_output=True, text=True, check=True)
               if "password:" in password_result.stdout:
                   password = re.search(r'password: (.+)', password_result.stdout).group(1)
                   passwords[ssid] = password
       elif system == 'Darwin':  # macOS
           result = subprocess.run(['/usr/sbin/security', 'find-generic-password', '-ga', 'WIFI'], capture_output=True, text=True, check=True)
           password = re.search(r'password: "(.*)"', result.stdout).group(1)
           passwords["Wi-Fi"] = password
       else:
           print("Unsupported operating system.")
   except Exception as e:
       print("Error:", e)
   return passwords
 
 
passwords = get_wifi_passwords()
if passwords:
   print("Saved Wi-Fi passwords:")
   for ssid, password in passwords.items():
       print(f"SSID: {ssid}, Password: {password}")
else:
   print("No saved Wi-Fi passwords found.")
