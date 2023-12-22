import requests
import time

ip_address = ''

def call_api():
    # Replace 'your_api_url' with the actual URL of the API you want to call
    api_url = 'https://api64.ipify.org?format=json'
    
    try:
        # Make the API call
        response = requests.get(api_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()['ip']
        else:
            print(f"Error: API call failed with status code {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def update_google(ip):
    f = open("/config/dns_list.txt", "r")
    for line in f:
        d = line.strip().split(',')
        print(d)
        url = f"https://{d[1]}:{d[2]}@domains.google.com/nic/update?hostname={d[0]}&myip={ip}"
        print(url)
        response = requests.post(url)
        if response.status_code == 200:
            print("IP address updated")
        else:
            print(f"Error: API call failed with status code {response.status_code}")
    f.close()

# Interval between API calls in seconds (3600 seconds = 1 hour)
interval = 3600

while True:
    # Call the API
    new_ip = call_api()
    if (new_ip is not None) and ip_address != new_ip:
        ip_address = new_ip
        update_google(new_ip)

    # Wait for the specified interval before making the next API call
    print(f"Waiting for {interval} seconds before the next API call...")
    time.sleep(interval)
