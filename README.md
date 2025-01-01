
## Inspecto-Engage

**Inspecto-Engage** is a Python tool that checks the social media engagement of URLs using the SharedCount API. It fetches interaction data from platforms like Facebook and Pinterest, displaying results via a simple and intuitive GUI. The tool supports batch URL processing, concurrent requests, and provides detailed feedback on post existence and engagement.

---

![img](assets/inspectogage.jpeg)

---

## For Linux Users:
- Python 3.x (Recommended: 3.8 or higher)
- Required Python Packages: `requests`, `tkinter`, `pyinstaller`
- You can install the necessary Python packages by running the following:

```bash
pip install requests tkinter
```

---

## Installation

### **Windows Installation (via .exe)**

1. Download the latest `.exe` installer from the GitHub releases section.
2. Run the installer `.exe` file. This will automatically extract the program and create a folder for Inspecto-Engage on your machine.
3. You can then run Inspecto-Engage from the extracted folder. If you want, you can also create shortcuts for easy access.


### **Linux Installation**

### Option 1: Using the Installer (Recommended for Simplicity)

1. Download the latest `.sh` installer from the GitHub releases section.
2. Make the installer executable by running the following command:
   ```bash
   chmod +x inspecto-engage-installer.sh
3. Run the installer script:
	```bash
	./inspecto-engage-installer.sh
4. The installer will automatically extract and set up the program.  You can run Inspecto-Engage from the installed directory.

### Option 2: Manual Installation (for developers)

1. Clone or download the project repository:

	```bash
	git clone https://github.com/yourusername/inspecto-engage.git
	cd inspecto-engage
	```

2. Install the necessary Python dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Run the program using the following command:

	```bash
	python3 sharedcount_exec_multithread.py
	```

This section provides both the easy installer option (using the `.sh` file) and the manual method for users who prefer to work with the code directly. Let me know if you need further adjustments!


---

## Usage

1. Open **Inspecto-Engage**.
2. **Select a CSV file** containing URLs you want to check. The file should have one URL per row.
3. Enter your **[SharedCount API Key](https://www.sharedcount.com/)**.
4. Choose the desired number of **Concurrent Requests** (the default is 30). You can adjust this based on your network and system capacity.
5. Specify the **output file name** and location where the results should be saved.
6. Click on **Run** to start the process. The program will process the URLs and display the results in the specified output file.

### Example CSV format:

```csv
https://example.com/article1
https://example.com/article2
https://example.com/article3
```

### Output:

The output CSV file will contain:

- **URL**: The URL that was checked.
- **Message**: A status message indicating whether the URL has engagement data, was not shared, or failed.
- **Pinterest**: Engagement count from Pinterest.
- **Facebook Total**: Total Facebook engagement.
- **Facebook Comments**: Number of Facebook comments.
- **Facebook Reactions**: Number of Facebook reactions.
- **Facebook Shares**: Number of Facebook shares.

---

## Error Handling

- **Rate Limit Reached**: If the SharedCount API rate limit is exceeded, the program will display a warning and stop further processing.
- **Request Errors**: If there are issues connecting to the API (e.g., network issues), the program will notify you with the error message.
- **No Data Found**: If a URL is found but has no engagement data, a message will be displayed indicating that the post exists but has no interactions.

---

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- The program utilizes the [SharedCount API](https://sharedcount.com/) to fetch social media engagement data.
- Thanks to the [Tkinter library](https://docs.python.org/3/library/tkinter.html) for creating the GUI.

---

## Contributing

We welcome contributions to Inspecto-Engage! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write tests to verify your changes.
4. Ensure all tests pass and that the code is properly formatted.
5. Submit a pull request describing your changes.

By submitting a pull request, you agree that your contributions will be licensed under the Apache License, Version 2.0.

For any bugs or feature requests, please open an issue on the GitHub repository.

Thank you for contributing!


---

Happy engagement inspection!
