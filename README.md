# Trade Journal Desktop Application

## Description
The Trade Journal is a desktop application for keeping track of trade entries. Users can add, view, update, delete, and manage their trade journal entries. The application features a tabbed interface with sections for adding new entries, viewing existing entries, and managing trashed entries.

## Features
- Add trade entries with optional titles and descriptions.
- View all trade entries in a list format.
- Update existing trade entries.
- Move entries to trash and restore or permanently delete them from trash.
- Fully maximizable and resizable application window.
- Dark-themed user interface.

## Prerequisites
- Python 3.x
- `tkinter` library (included with Python standard library)
- `ttkbootstrap` library for theming (`pip install ttkbootstrap`)
- `sqlite3` library (included with Python standard library)
- `PyInstaller` for building the application (`pip install pyinstaller`)

## Setup and Installation

1. **Clone the repository or download the script.**
   ```bash
   git clone https://github.com/Rishikesh0523/Trade-Journal-Desktop-Application.git
   cd Trade-Journal-Desktop-Application
   ```

2. **Ensure all required libraries are installed.**
   ```bash
   pip install ttkbootstrap
   ```

3. **Save the script as `trade_journal.py`.**

## Building the Application

1. **Open a command prompt in the directory containing the script.**
   ```bash
   cd path_to_directory_containing_script
   ```

2. **Run PyInstaller to build the application.**
   ```bash
   pyinstaller --onefile --windowed trade_journal.py
   ```

3. **Locate the executable in the `dist` folder.**
   The executable file will be generated in the `dist` folder within your current directory.

## Running the Application

- **Windows:**
  Double-click the executable file in the `dist` folder to run the application.

- **Linux/Mac:**
  Open a terminal and navigate to the `dist` folder, then run:
  ```bash
  ./trade_journal
  ```

## Usage

### Adding a Trade Entry
1. Open the application.
2. Go to the "Add Entry" tab.
3. Enter a title (optional) and description for your trade.
4. Click "Add Entry" to save the entry.

### Viewing Trade Entries
1. Open the application.
2. Go to the "View Entries" tab.
3. Select an entry from the list on the left to view its details.

### Updating a Trade Entry
1. In the "View Entries" tab, select an entry.
2. Click "Update Entry" and modify the details in the popup window.
3. Save the changes.

### Deleting a Trade Entry
1. In the "View Entries" tab, select an entry.
2. Click "Delete Entry" to move the entry to the trash.

### Managing Trash
1. Go to the "Trash" tab to view trashed entries.
2. Use the provided buttons to restore or permanently delete entries.