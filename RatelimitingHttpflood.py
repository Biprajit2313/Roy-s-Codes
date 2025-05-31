import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import time
from collections import defaultdict
import matplotlib.pyplot as plt
import webbrowser
def display_csv_table(filename):
    """Displays the contents of a CSV file in a tabular format."""
    try:
        df = pd.read_csv(filename)
        print(df.to_string(index=False))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")


csv_filename = input("Please enter the CSV filename (e.g., 'http_requests.csv'): ")
try:
    data = pd.read_csv(csv_filename)
except FileNotFoundError:
    print(f"Error: File '{csv_filename}' not found. Exiting.")
    exit()
display_csv_table(csv_filename)
required_columns = ['ip_address', 'request_type', 'response_time', 'is_flood']
if not all(col in data.columns for col in required_columns):
    print(f"Error: The CSV file must contain the following columns: {required_columns}. Exiting.")
    exit()

original_request_types = data['request_type'].unique()
data['request_type'] = data['request_type'].astype('category').cat.codes
features = data[['request_type', 'response_time']]
labels = data['is_flood']
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

RATE_LIMIT = 5
TIME_WINDOW = 10

request_count = defaultdict(list)
def detect_flood(request):
    current_time = time.time()
    ip_address = request['ip_address']

    request_count[ip_address] = [timestamp for timestamp in request_count[ip_address] if
                                 current_time - timestamp < TIME_WINDOW]

    if len(request_count[ip_address]) >= RATE_LIMIT:
        print(f"Rate limit exceeded for IP: {ip_address}. Taking mitigation actions.")
        mitigate_flood(ip_address)
        return

    request_count[ip_address].append(current_time)

    request_type_num = pd.Categorical([request['type']], categories=original_request_types).codes[0]

    request_data = {
        'request_type': request_type_num,
        'response_time': request['response_time']
    }

    request_df = pd.DataFrame([request_data])
    request_scaled = scaler.transform(request_df)
    prediction = model.predict(request_scaled)
    if prediction[0] == 1:
        print(f"Flood detected from IP: {ip_address}. Taking mitigation actions.")
        mitigate_flood(ip_address)
def open_ip_in_chrome(ip_address, status):
    """Opens the IP address in Chrome with a status message."""
    url = f"http://{ip_address}"
    html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{ip_address}</title>
        </head>
        <body>
            <h1>{status}</h1>
        </body>
        </html>
    """
    with open('../status.html', 'w') as f:
        f.write(html_content)
    webbrowser.open_new_tab('status.html')
def mitigate_flood(ip_address):
    open_ip_in_chrome(ip_address, "HTTP flood mitigated")
def simulate_requests(num_requests=20):
    ip_addresses = data['ip_address'].unique()  # Use IPs from the dataset
    request_types = data['request_type'].unique()  # Use request types from the dataset

    timestamps = []
    request_rates = []

    for _ in range(num_requests): # Changed 'in num_requests)' to 'in range(num_requests)' to iterate correctly
        request = {
            'ip_address': np.random.choice(ip_addresses),
            'type': np.random.choice(request_types),
            'response_time': np.random.exponential(scale=0.5)
        }
        detect_flood(request)
        time.sleep(0.5)

        timestamps.append(time.time())
        request_rates.append(len(request_count[request['ip_address']]))

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, request_rates, marker='o', linestyle='-')
    plt.title('HTTP Request Rate Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Request Rate')
    plt.grid(True)
    plt.show()

    ip_request_counts = pd.DataFrame(list(request_count.items()), columns=['IP Address', 'Request Count'])
    ip_request_counts['Request Count'] = ip_request_counts['Request Count'].apply(len)

    print("\nIP Address Request Counts:")
    print(ip_request_counts.to_string(index=False))
simulate_requests(20)