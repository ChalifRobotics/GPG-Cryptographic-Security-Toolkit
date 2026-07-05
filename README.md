GPG Cryptographic Security Toolkit
Project Summary
The GPG Cryptographic Security Toolkit is a Python/Tkinter cybersecurity application created by Jesse Chalif, owner of CHALIF ROBOTICS L.L.C., as part of his cybersecurity portfolio.

This project demonstrates practical cryptography workflows through a graphical user interface. It is designed for cybersecurity education, portfolio demonstration, and hands-on practice with hashing, digital signatures, key verification, public key certification, encryption, decryption, and GPG key management.

This application is available for anyone to use, study, and modify however they want. You may download the project, change the code, customize the interface, replace the images, or build your own version from it.

What This Application Can Do
This toolkit includes the following cybersecurity actions:

1. Compute SHA-256 Hash
Creates a SHA-256 hash file for a selected file. This is useful for proving file integrity because any change to the original file will create a different hash value.

2. Stored Hash Files
Displays hash files created by the application. From this section, users can view, export, or delete stored hash files.

3. Asymmetric Key Generation
Creates a new public/private GPG key pair. The application allows the user to enter a real name, email address, optional comment, password/passphrase, and expiration date.

This section also supports:

Viewing available secret keys
Revoking a public key
Deleting a key pair
4. Create Digital Signatures
Allows a user to digitally sign a stored SHA-256 hash file with a selected private key. This creates a detached signature file that can later be used to prove authenticity and non-repudiation.

5. Digitally Signed Files
Displays digital signature files created by the application. Users can view, export, or delete stored signature files.

6. Verify & Certify Public Key
Allows a user to load a public key file, verify its fingerprint, certify the public key with their own private key, and export the certified public key.

This section demonstrates the trust process behind public key cryptography.

7. Verify Digital Signature
Allows a user to load a signature file, hash file, and public key file to verify a digital signature. This helps prove that the signed file was created by the expected private key and that the file hash has not been changed.

8. Encrypting / Decrypting Files
Supports both asymmetric and symmetric encryption workflows.

The application can perform:

Asymmetric encryption with a public key
Asymmetric decryption with a private key
Symmetric encryption with a password/passphrase
Symmetric decryption with a password/passphrase
9. Encrypted / Decrypted Files
Displays encrypted and decrypted files created by the application. Users can view, export, or delete stored encrypted/decrypted files.

Folder Structure
After extracting the ZIP file, the project should look like this:

GPG-Cryptographic-Security-Toolkit-Portable/
├── GPG-Toolkit-Portable.py
├── assets/
│   ├── cipher_text_and_key_with_pen.png
│   └── digital_keys_and_pens.png
├── app_data/
├── exports/
├── requirements.txt
├── README.md
└── .gitignore
Do not remove the assets folder. The Python application uses that folder to load the images used inside the GUI.

Requirements
This project uses both system-level software and Python libraries.

Required System Software
Python 3 — runs the application.
GnuPG / GPG — performs cryptographic operations such as key generation, signing, verification, encryption, and decryption.
Tkinter — provides the graphical user interface. On Windows, this normally comes with Python. On Linux, it may need to be installed separately.
Python Packages in requirements.txt
The requirements.txt file includes:

Pillow
tkcalendar
What each Python package is used for:

Pillow — loads, resizes, and displays the application images/backgrounds.
tkcalendar — displays the calendar used when selecting an expiration date for a GPG key.
The application also uses Python built-in modules such as os, glob, hashlib, shutil, subprocess, tempfile, datetime, and tkinter. These are included with Python and do not need to be installed with pip.

Windows Instructions After Extracting the ZIP File
These instructions are for Windows PowerShell.

Step 1 — Open PowerShell
Open the folder where you extracted the project. Then right-click inside the folder and choose Open in Terminal or open PowerShell manually.

Step 2 — Go into the extracted project folder
Example command:

cd "$HOME\Downloads\GPG-Cryptographic-Security-Toolkit-Portable"
Explanation:

cd means change directory.
$HOME\Downloads\... points PowerShell to the project folder inside your Downloads folder.
If your project is in a different folder, replace the path with your actual extracted folder path.
Step 3 — Check that Python is installed
python --version
Explanation:

This checks whether Python is installed and available from PowerShell.
If Python is installed correctly, it should show a version such as Python 3.x.x.
If Python is not installed, you can install it with Windows Package Manager:

winget install --id Python.Python.3.12 -e
Explanation:

winget install installs software from Windows Package Manager.
--id Python.Python.3.12 selects the Python package.
-e means use the exact package ID.
After installing Python, close PowerShell and open it again, then run:

python --version
Step 4 — Install GnuPG/Gpg4win
The application needs the gpg command to perform cryptographic operations.

Install Gpg4win with this command:

winget install --id GnuPG.Gpg4win -e
Explanation:

winget install installs software.
--id GnuPG.Gpg4win selects Gpg4win, which provides GnuPG/GPG for Windows.
-e uses the exact package ID.
After installing Gpg4win, close PowerShell and open it again, then check that GPG works:

gpg --version
Explanation:

This confirms that the gpg command is available.
If PowerShell says gpg is not recognized, restart your computer or make sure Gpg4win was added to your system PATH.
Step 5 — Create a Python virtual environment
python -m venv .venv
Explanation:

python -m venv creates a private Python environment for this project.
.venv is the name of the virtual environment folder.
This keeps the project libraries separate from your main Python installation.
Step 6 — Activate the virtual environment
.\.venv\Scripts\Activate.ps1
Explanation:

This turns on the virtual environment.
After activation, installed Python packages will go into .venv instead of your global Python installation.
If PowerShell blocks activation scripts, run this command:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Then try activating again:

.\.venv\Scripts\Activate.ps1
Explanation:

Set-ExecutionPolicy changes script permissions for your Windows user account.
-Scope CurrentUser means the change applies only to your user account.
RemoteSigned allows local scripts, such as the virtual environment activation script, to run.
Step 7 — Upgrade pip
python -m pip install --upgrade pip
Explanation:

pip is Python's package installer.
This updates pip before installing the project libraries.
Step 8 — Install the Python libraries
pip install -r requirements.txt
Explanation:

pip install installs Python libraries.
-r requirements.txt tells pip to install every package listed inside requirements.txt.
This installs Pillow and tkcalendar.
Step 9 — Run the application
python GPG-Toolkit-Portable.py
Explanation:

This starts the Python GUI application.
Keep the assets folder in the same directory as the Python file so the images load correctly.
Linux Instructions After Extracting the ZIP File
These instructions are for Debian-based Linux systems such as Kali Linux, Ubuntu, Debian, and many WSL Linux environments.

Step 1 — Open a terminal
Open a terminal in Linux.

Step 2 — Go into the extracted project folder
Example command:

cd ~/Downloads/GPG-Cryptographic-Security-Toolkit-Portable
Explanation:

cd means change directory.
~/Downloads/... points to the project folder inside your Downloads folder.
If you extracted the ZIP somewhere else, replace the path with your actual project folder path.
Step 3 — Update the Linux package list
sudo apt update
Explanation:

sudo runs the command with administrator privileges.
apt update refreshes the list of available packages from your Linux software repositories.
This should be run before installing system packages.
Step 4 — Install the required Linux system packages
sudo apt install -y python3 python3-pip python3-venv python3-tk gnupg
Explanation:

python3 installs Python 3.
python3-pip installs pip for Python 3.
python3-venv allows you to create a Python virtual environment.
python3-tk installs Tkinter support for the graphical interface.
gnupg installs the GPG command-line tool used by the application.
-y automatically answers yes to the installation prompt.
Step 5 — Confirm Python is installed
python3 --version
Explanation:

This checks that Python 3 is installed correctly.
Step 6 — Confirm GPG is installed
gpg --version
Explanation:

This checks that the gpg command is installed and available.
The application depends on this command for hashing support workflows, key generation, signing, verification, encryption, and decryption.
Step 7 — Create a Python virtual environment
python3 -m venv .venv
Explanation:

python3 -m venv creates a private Python environment for this project.
.venv is the folder that stores the virtual environment.
This keeps the required Python libraries separate from your system Python installation.
Step 8 — Activate the virtual environment
source .venv/bin/activate
Explanation:

source runs the activation script in your current terminal session.
After activation, your terminal should show (.venv) near the prompt.
Step 9 — Upgrade pip
python -m pip install --upgrade pip
Explanation:

This updates pip inside the virtual environment.
Using python -m pip makes sure pip runs from the active virtual environment.
Step 10 — Install the Python libraries
pip install -r requirements.txt
Explanation:

This installs the Python packages listed in requirements.txt.
This installs Pillow and tkcalendar.
Step 11 — Run the application
python GPG-Toolkit-Portable.py
Explanation:

This starts the Python GUI application.
Because the virtual environment is active, Python can find the required packages.
If your Linux system requires python3 instead of python, use:

python3 GPG-Toolkit-Portable.py
Notes for Kali Linux / WSL Users
The file picker may start at /mnt/ when that folder exists. This is useful in WSL/Kali because Windows drives are usually available through paths like:

/mnt/c/Users/YourName/Downloads
Important Security Warning
Do not upload real private keys, passphrases, secret files, or your real GPG keyring to GitHub. Use demo/test keys and demo/test files only.

This application is meant for cybersecurity education, project demonstration, and portfolio use.
