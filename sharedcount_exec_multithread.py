import requests
import csv
import concurrent.futures
import tkinter as tk
from tkinter import filedialog, messagebox
import os

DEFAULT_API_KEY = ""
DEFAULT_MAX_WORKERS = 30  # Default number of concurrent threads

def fetch_url_data(url, api_key):
    endpoint = "https://api.sharedcount.com/v1.1/"
    params = {"apikey": api_key, "url": url}
    try:
        response = requests.get(endpoint, params=params, timeout=10)
        if response.status_code == 429:
            return url, None, "Rate Limit Reached"
        elif response.status_code == 200:
            data = response.json()
            # Check for engagement data in Facebook or Pinterest
            facebook_data = data.get("Facebook", {})
            pinterest_data = data.get("Pinterest", 0)
            
            if facebook_data or pinterest_data:
                # Ensure valid engagement data exists (not just URL crawl)
                if not all(
                    platform == 0 for platform in [
                        facebook_data.get("total_count", 0),
                        facebook_data.get("comment_count", 0),
                        facebook_data.get("reaction_count", 0),
                        facebook_data.get("share_count", 0),
                        pinterest_data
                    ]
                ):
                    return url, data, None  # Data is collected (even if it's zero)
                else:
                    return url, None, "Post exists but has no interactions."
            else:
                return url, None, "Post not shared or no engagement found."

        else:
            return url, None, f"API Error: {response.text}"
    except requests.RequestException as e:
        return url, None, f"Request Error: {str(e)}"


def process_urls(csv_file, api_key, max_workers, output_file):
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header
            urls = [row[0] for row in csv_reader]
    except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found!")
        return

    results = []
    error_count = 0

    # Use ThreadPoolExecutor for concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch_url_data, url, api_key): url for url in urls}

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                result_url, data, message = future.result()
                if message:
                    error_count += 1
                    print(f"Error for {result_url}: {message}")
                else:
                    results.append({"url": result_url, "data": data})
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
    
    # Save results to CSV
    if results:
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["URL", "Message", "Pinterest", "Facebook Total", "Facebook Comments", "Facebook Reactions", "Facebook Shares"])
            for item in results:
                writer.writerow([
                    item["url"],
                    "Data Collected Successfully",
                    item["data"].get("Pinterest", 0),
                    item["data"]["Facebook"].get("total_count", 0),
                    item["data"]["Facebook"].get("comment_count", 0),
                    item["data"]["Facebook"].get("reaction_count", 0),
                    item["data"]["Facebook"].get("share_count", 0),
                ])
        messagebox.showinfo("Success", f"Results saved to {os.path.abspath(output_file)}")
    else:
        messagebox.showwarning("No Data", "No data was collected.")
    
    print(f"Processed {len(results)} successful requests. Encountered {error_count} errors.")

def open_file_dialog(csv_path_var):
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        csv_path_var.set(file_path)  # Set the file path to the Entry widget

def save_file_dialog(output_path_var):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        output_path_var.set(file_path)  # Set the file path to the Entry widget

def run_gui():
    window = tk.Tk()
    window.title("SharedCount Engagement Checker")

    # CSV file selection
    tk.Label(window, text="Select CSV file:").pack(pady=5)
    csv_path_var = tk.StringVar()
    entry_field = tk.Entry(window, textvariable=csv_path_var, width=50)
    entry_field.pack(pady=5)
    tk.Button(window, text="Browse", command=lambda: open_file_dialog(csv_path_var)).pack(pady=5)

    # API Key input
    tk.Label(window, text="API Key (optional):").pack(pady=5)
    api_key_var = tk.StringVar(value=DEFAULT_API_KEY)
    tk.Entry(window, textvariable=api_key_var, width=50).pack(pady=5)

    # Max Workers (concurrent threads) input
    tk.Label(window, text="Max Workers (threads):").pack(pady=5)
    max_workers_var = tk.IntVar(value=DEFAULT_MAX_WORKERS)
    tk.Entry(window, textvariable=max_workers_var, width=50).pack(pady=5)

    # Output file location and name input
    tk.Label(window, text="Select Output File:").pack(pady=5)
    output_path_var = tk.StringVar()
    output_entry_field = tk.Entry(window, textvariable=output_path_var, width=50)
    output_entry_field.pack(pady=5)
    tk.Button(window, text="Browse", command=lambda: save_file_dialog(output_path_var)).pack(pady=5)

    def run_process():
        csv_file = csv_path_var.get()
        api_key = api_key_var.get()
        max_workers = max_workers_var.get()
        output_file = output_path_var.get()

        if not csv_file:
            messagebox.showwarning("Input required", "Please select a CSV file.")
        elif not output_file:
            messagebox.showwarning("Input required", "Please select an output file.")
        else:
            process_urls(csv_file, api_key, max_workers, output_file)
    
    tk.Button(window, text="Run", command=run_process).pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    run_gui()
