# ==================================================================================================
# GPG Cryptographic Security Toolkit
# ==================================================================================================
# Original creator: Jesse Chalif, owner of CHALIF ROBOTICS L.L.C.
#
# Portfolio purpose:
# This is a cybersecurity portfolio project that demonstrates hashing, digital signatures,
# public key certification, signature verification, GPG key generation, asymmetric encryption,
# asymmetric decryption, symmetric encryption, and symmetric decryption through a Python/Tkinter GUI.
#
# Usage/modification note:
# This project is available for anyone to use, study, and modify however they want.
#
# --------------------------------------------------------------------------------------------------
# REQUIRED PROJECT FOLDER LAYOUT
# --------------------------------------------------------------------------------------------------
# Keep this Python file beside the assets folder:
#
#     GPG-Cryptographic-Security-Toolkit-Portable/
#     ├── GPG-Toolkit-Portable.py
#     ├── assets/
#     │   ├── cipher_text_and_key_with_pen.png
#     │   └── digital_keys_and_pens.png
#     ├── app_data/
#     ├── exports/
#     ├── requirements.txt
#     └── README.md
#
# Do not remove the assets folder. The application loads its GUI images from that folder.
#
# --------------------------------------------------------------------------------------------------
# HOW TO RUN ON WINDOWS POWERSHELL AFTER EXTRACTING THE ZIP FILE
# --------------------------------------------------------------------------------------------------
# 1. Open PowerShell in the extracted project folder, or use cd to enter the folder:
#
#        cd "$HOME\Downloads\GPG-Cryptographic-Security-Toolkit-Portable"
#
#    cd means change directory. Replace the path if your extracted folder is somewhere else.
#
# 2. Check whether Python is installed:
#
#        python --version
#
#    If Python is not installed, install it with:
#
#        winget install --id Python.Python.3.12 -e
#
#    Close and reopen PowerShell after installing Python.
#
# 3. Install GnuPG/Gpg4win, which provides the gpg command used by this app:
#
#        winget install --id GnuPG.Gpg4win -e
#
#    Close and reopen PowerShell, then confirm GPG works:
#
#        gpg --version
#
# 4. Create a virtual environment for this project:
#
#        python -m venv .venv
#
# 5. Activate the virtual environment:
#
#        .\.venv\Scripts\Activate.ps1
#
#    If PowerShell blocks the activation script, run:
#
#        Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
#
#    Then activate again:
#
#        .\.venv\Scripts\Activate.ps1
#
# 6. Upgrade pip:
#
#        python -m pip install --upgrade pip
#
# 7. Install the Python libraries from requirements.txt:
#
#        pip install -r requirements.txt
#
#    This installs Pillow and tkcalendar.
#
# 8. Run the application:
#
#        python GPG-Toolkit-Portable.py
#
# --------------------------------------------------------------------------------------------------
# HOW TO RUN ON LINUX AFTER EXTRACTING THE ZIP FILE
# --------------------------------------------------------------------------------------------------
# These commands are for Debian-based Linux systems such as Kali Linux, Ubuntu, Debian, and many WSL
# Linux environments.
#
# 1. Open a terminal and go into the extracted project folder:
#
#        cd ~/Downloads/GPG-Cryptographic-Security-Toolkit-Portable
#
#    Replace the path if your extracted folder is somewhere else.
#
# 2. Update the package list:
#
#        sudo apt update
#
# 3. Install the required Linux system packages:
#
#        sudo apt install -y python3 python3-pip python3-venv python3-tk gnupg
#
#    python3      = runs the application
#    python3-pip  = installs Python libraries
#    python3-venv = creates a virtual environment
#    python3-tk   = provides Tkinter GUI support
#    gnupg        = provides the gpg command used for cryptographic operations
#
# 4. Confirm Python and GPG are installed:
#
#        python3 --version
#        gpg --version
#
# 5. Create a virtual environment:
#
#        python3 -m venv .venv
#
# 6. Activate the virtual environment:
#
#        source .venv/bin/activate
#
# 7. Upgrade pip:
#
#        python -m pip install --upgrade pip
#
# 8. Install the Python libraries from requirements.txt:
#
#        pip install -r requirements.txt
#
# 9. Run the application:
#
#        python GPG-Toolkit-Portable.py
#
#    If your system requires it, use:
#
#        python3 GPG-Toolkit-Portable.py
#
# --------------------------------------------------------------------------------------------------
# SECURITY WARNING
# --------------------------------------------------------------------------------------------------
# Do not upload real private keys, passphrases, secret files, or your real GPG keyring to GitHub.
# Use demo/test keys and demo/test files only.
# ==================================================================================================

import glob
import hashlib
import os
import shutil
import subprocess
import tempfile
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font as tkfont

from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkcalendar import Calendar

# ============================================================
# Portable project paths
# ============================================================
# Everything the app needs is now relative to this Python file.
# That means someone can download the full project folder and run:
#     python GPG-Toolkit-Portable.py
#
# Required folder layout:
#     GPG-Cryptographic-Security-Toolkit/
#     ├── GPG-Toolkit-Portable.py
#     ├── assets/
#     │   ├── cipher_text_and_key_with_pen.png
#     │   └── digital_keys_and_pens.png
#     └── app_data/              # created automatically
#
APP_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(APP_DIR, "assets")
STORAGE_DIR = os.path.join(APP_DIR, "app_data")

DEFAULT_DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
EXPORT_DIR = DEFAULT_DOWNLOADS_DIR if os.path.isdir(DEFAULT_DOWNLOADS_DIR) else os.path.join(APP_DIR, "exports")

MAIN_MENU_IMAGE_PATH = os.path.join(ASSETS_DIR, "cipher_text_and_key_with_pen.png")
INTERFACE_BG_IMAGE_PATH = os.path.join(ASSETS_DIR, "digital_keys_and_pens.png")
COMPUTE_HASH_BG_IMAGE_PATH = INTERFACE_BG_IMAGE_PATH

COMPUTE_HASH_TITLE_COLOR = "white"
COMPUTE_HASH_TITLE_STROKE_WIDTH = 3

# Default file picker start location. On Kali/WSL, /mnt/ lets you browse Windows drives.
# On normal Linux/macOS/Windows Python, it falls back to the user's home folder.
WINDOWS_MOUNT_DIR = "/mnt/" if os.path.exists("/mnt/") else os.path.expanduser("~")

ENCRYPTED_DECRYPTED_DIR = os.path.join(STORAGE_DIR, "encrypted_decrypted_files")
CERTIFIED_PUBLIC_KEYS_DIR = os.path.join(STORAGE_DIR, "certified_public_keys")
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(ENCRYPTED_DECRYPTED_DIR, exist_ok=True)
os.makedirs(CERTIFIED_PUBLIC_KEYS_DIR, exist_ok=True)


class NonRepudiationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPG Cryptographic Security Toolkit")
        self.root.geometry("980x760")
        self.current_frame = None
        self.scroll_container = None
        self.scroll_canvas = None
        self.scroll_content_frame = None
        self.scroll_window_id = None
        self.scroll_background_label = None
        self.scroll_background_photo = None
        self.scroll_canvas_background_photo = None
        self.scroll_canvas_bg_image_id = None
        self.scroll_background_path = None
        self.scroll_background_source_image = None
        self.scroll_top_pad = 0
        self.queued_files = []
        self.main_menu_image = None
        self.interface_bg_image = None
        self.signature_dynamic_widgets = []
        self.signed_dynamic_widgets = []
        self.encrypted_file_dynamic_widgets = []
        self.signature_list_frame = None
        self.signed_list_frame = None
        self.encrypted_list_frame = None
        self.verify_signature_file = None
        self.verify_hash_file = None
        self.verify_public_key_file = None
        self.verify_signature_value_label = None
        self.verify_hash_value_label = None
        self.verify_public_key_value_label = None
        self.verify_execute_button = None

        self.certify_public_key_file = None
        self.certify_public_key_fingerprint = None
        self.certify_public_key_details = ""
        self.certify_fingerprint_verified = False
        self.certify_public_key_completed = False
        self.certify_public_key_storage_path = None
        self.certify_public_key_storage_path = None
        self.certify_load_value_label = None
        self.certify_fingerprint_button = None
        self.certify_public_key_button = None
        self.certify_export_button = None

        self.show_main_menu()

    # ==================== UI Helpers ====================
    def clear_frame(self, use_black_background=False):
        if self.current_frame:
            self.current_frame.destroy()
        self.scroll_container = None
        self.scroll_canvas = None
        self.scroll_content_frame = None
        self.scroll_window_id = None
        self.scroll_background_label = None
        self.scroll_background_photo = None
        self.scroll_canvas_background_photo = None
        self.scroll_canvas_bg_image_id = None
        self.scroll_background_path = None
        self.scroll_background_source_image = None
        self.scroll_top_pad = 0
        self.signature_list_frame = None
        self.signed_list_frame = None
        self.encrypted_list_frame = None
        if use_black_background:
            self.current_frame = tk.Frame(self.root, bg="black")
        else:
            self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def setup_scrollable_body(self, top_pad=0, background_image_path=None):
        # No scrollbar is used here. This creates a normal body frame only.
        # The body frame gets its own matching background image so the interface
        # looks like the screenshot: title on top, controls directly over the image.
        body_bg = self.current_frame.cget("bg")
        self.scroll_top_pad = top_pad
        self.scroll_background_path = background_image_path if background_image_path and os.path.exists(background_image_path) else None
        self.scroll_background_source_image = None

        if self.scroll_background_path:
            try:
                self.scroll_background_source_image = Image.open(self.scroll_background_path).convert("RGB")
            except Exception:
                self.scroll_background_source_image = None

        self.scroll_container = tk.Frame(
            self.current_frame,
            bg=body_bg,
            bd=0,
            highlightthickness=0
        )
        self.scroll_container.pack(fill="both", expand=True, pady=(top_pad, 0))

        if self.scroll_background_source_image:
            self.scroll_background_label = tk.Label(self.scroll_container, bd=0, highlightthickness=0)
            self.scroll_background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.scroll_background_label.lower()
            self.scroll_container.bind("<Configure>", self.refresh_scroll_background)
            self.root.after_idle(self.refresh_scroll_background)

        self.scroll_content_frame = self.scroll_container
        return self.scroll_content_frame

    def update_scrollable_body(self, event=None):
        self.refresh_scroll_background()

    def resize_scrollable_body(self, event=None):
        self.refresh_scroll_background()

    def refresh_scroll_background(self, event=None):
        if not self.scroll_background_source_image:
            return

        if not (
            self.scroll_container
            and self.scroll_container.winfo_exists()
            and self.scroll_background_label
            and self.scroll_background_label.winfo_exists()
        ):
            return

        frame_width = max(1, self.scroll_container.winfo_width())
        frame_height = max(1, self.scroll_container.winfo_height())

        root_width = max(1, self.current_frame.winfo_width())
        root_height = max(1, self.current_frame.winfo_height())
        full_image = self.scroll_background_source_image.resize((root_width, root_height), Image.LANCZOS)

        top_pad = max(0, int(self.scroll_top_pad or 0))
        bottom = min(root_height, top_pad + frame_height)
        if bottom <= top_pad:
            cropped_image = self.scroll_background_source_image.resize((frame_width, frame_height), Image.LANCZOS)
        else:
            cropped_image = full_image.crop((0, top_pad, root_width, bottom))
            cropped_image = cropped_image.resize((frame_width, frame_height), Image.LANCZOS)

        self.scroll_background_photo = ImageTk.PhotoImage(cropped_image)
        self.scroll_background_label.config(image=self.scroll_background_photo)
        self.scroll_background_label.image = self.scroll_background_photo
        self.scroll_background_label.lower()

    def get_content_parent(self):
        if self.scroll_content_frame and self.scroll_content_frame.winfo_exists():
            return self.scroll_content_frame
        return self.current_frame

    def get_title_image_font(self, size):
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "C:/Windows/Fonts/arialbd.ttf",
            "arialbd.ttf",
        ]

        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue

        return ImageFont.load_default()

    def add_interface_background(
        self,
        title_text=None,
        image_path=INTERFACE_BG_IMAGE_PATH,
        title_fill="white",
        title_stroke_width=1
    ):
        try:
            if not os.path.exists(image_path):
                return False

            self.root.update_idletasks()
            frame_width = max(1, self.current_frame.winfo_width())
            frame_height = max(1, self.current_frame.winfo_height())

            if frame_width <= 1 or frame_height <= 1:
                frame_width = max(1, self.root.winfo_width() - 40)
                frame_height = max(1, self.root.winfo_height() - 40)

            image = Image.open(image_path)
            image = image.resize((frame_width, frame_height), Image.LANCZOS)

            if title_text:
                draw = ImageDraw.Draw(image)
                title_font = self.get_title_image_font(56)
                bbox = draw.textbbox((0, 0), title_text, font=title_font, stroke_width=title_stroke_width)
                text_width = bbox[2] - bbox[0]
                x = (frame_width - text_width) // 2
                y = 18
                draw.text(
                    (x, y),
                    title_text,
                    font=title_font,
                    fill=title_fill,
                    stroke_width=title_stroke_width,
                    stroke_fill="black"
                )

            self.interface_bg_image = ImageTk.PhotoImage(image)

            bg_label = tk.Label(self.current_frame, image=self.interface_bg_image, bd=0)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
            return True
        except Exception:
            self.interface_bg_image = None
            return False

    def create_outlined_title(self, parent, text, size=56, pady=(8, 18), fill_color="white", outline_width=1):
        title_font = tkfont.Font(family="Arial", size=size, weight="bold")
        outline_color = "black"
        padding_x = outline_width + 10
        padding_y = outline_width + 8

        text_width = title_font.measure(text)
        text_height = title_font.metrics("linespace")
        canvas_width = text_width + (padding_x * 2)
        canvas_height = text_height + (padding_y * 2)
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        canvas = tk.Canvas(
            parent,
            width=canvas_width,
            height=canvas_height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0
        )

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                canvas.create_text(
                    center_x + dx,
                    center_y + dy,
                    text=text,
                    font=title_font,
                    fill=outline_color
                )

        canvas.create_text(
            center_x,
            center_y,
            text=text,
            font=title_font,
            fill=fill_color
        )
        canvas.pack(pady=pady)
        return canvas

    def create_outlined_section_label(self, parent, text, size=38, padx=8, pady=(0, 8), anchor="w"):
        title_font = tkfont.Font(family="Arial", size=size, weight="bold")
        outline_color = "black"
        fill_color = "white"
        outline_width = 1
        padding_x = outline_width + 8
        padding_y = outline_width + 6

        text_width = title_font.measure(text)
        text_height = title_font.metrics("linespace")
        canvas_width = text_width + (padding_x * 2)
        canvas_height = text_height + (padding_y * 2)
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        canvas = tk.Canvas(
            parent,
            width=canvas_width,
            height=canvas_height,
            bg=parent.cget("bg"),
            highlightthickness=0,
            bd=0
        )

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                canvas.create_text(
                    center_x + dx,
                    center_y + dy,
                    text=text,
                    font=title_font,
                    fill=outline_color,
                    anchor="center"
                )

        canvas.create_text(
            center_x,
            center_y,
            text=text,
            font=title_font,
            fill=fill_color,
            anchor="center"
        )
        canvas.pack(anchor=anchor, padx=padx, pady=pady)
        return canvas

    def create_image_section_label(self, parent, text, image_path, size=38, padx=8, pady=(0, 8), anchor="w"):
        try:
            if not os.path.exists(image_path):
                return self.create_outlined_section_label(
                    parent,
                    text,
                    size=size,
                    padx=padx,
                    pady=pady,
                    anchor=anchor
                )

            font = self.get_title_image_font(size)
            temp_image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            draw = ImageDraw.Draw(temp_image)
            bbox = draw.textbbox((0, 0), text, font=font, stroke_width=1)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            label_width = text_width + 22
            label_height = text_height + 16

            bg_image = Image.open(image_path).convert("RGBA")
            bg_image = bg_image.resize((label_width, label_height), Image.LANCZOS)

            draw = ImageDraw.Draw(bg_image)
            draw.text(
                (11, 8),
                text,
                font=font,
                fill="white",
                stroke_width=1,
                stroke_fill="black"
            )

            photo = ImageTk.PhotoImage(bg_image)
            label = tk.Label(parent, image=photo, bd=0, highlightthickness=0)
            label.image = photo
            label.pack(anchor=anchor, padx=padx, pady=pady)
            return label
        except Exception:
            return self.create_outlined_section_label(
                parent,
                text,
                size=size,
                padx=padx,
                pady=pady,
                anchor=anchor
            )

    def create_large_interface_button(self, parent, text, command, width=None):
        button_options = {
            "text": text,
            "command": command,
            "font": ("Arial", 20, "bold"),
            "padx": 18,
            "pady": 14,
            "bd": 3,
            "relief": "raised",
            "cursor": "hand2",
        }
        if width is not None:
            button_options["width"] = width
        return tk.Button(parent, **button_options)

    def create_large_action_button(self, parent, text, command, width=10):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 16, "bold"),
            width=width,
            padx=12,
            pady=10,
            bd=3,
            relief="raised",
            cursor="hand2",
        )

    def create_file_display_box(self, parent, heading, default_text, pady=6, clear_command=None):
        card = tk.Frame(
            parent,
            bd=2,
            relief="solid",
            bg="white",
            padx=14,
            pady=12
        )
        card.pack(fill="x", pady=pady, padx=8)

        header_frame = tk.Frame(card, bg="white")
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text=heading,
            font=("Arial", 12, "bold"),
            justify="left",
            anchor="w",
            bg="white"
        ).pack(side="left", fill="x", expand=True)

        if clear_command is not None:
            tk.Button(
                header_frame,
                text="Clear",
                command=clear_command,
                font=("Arial", 10, "bold"),
                padx=10,
                pady=4,
                bd=2,
                relief="raised",
                cursor="hand2"
            ).pack(side="right", padx=(10, 0))

        value_label = tk.Label(
            card,
            text=default_text,
            font=("Arial", 11),
            justify="left",
            anchor="w",
            wraplength=1080,
            bg="white"
        )
        value_label.pack(fill="x", pady=(8, 0))
        return value_label

    def choose_from_list(self, title, prompt, options, geometry="900x500"):
        if not options:
            return None

        selected_value = {"value": None}
        selection_window = tk.Toplevel(self.root)
        selection_window.title(title)
        selection_window.geometry(geometry)
        selection_window.grab_set()

        tk.Label(
            selection_window,
            text=prompt,
            font=("Arial", 11),
            justify="left",
            wraplength=840
        ).pack(fill="x", padx=20, pady=(20, 12))

        list_frame = tk.Frame(selection_window)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 12))

        listbox = tk.Listbox(
            list_frame,
            font=("Arial", 11),
            activestyle="dotbox"
        )
        listbox.pack(side="left", fill="both", expand=True)

        for option in options:
            listbox.insert(tk.END, option)

        if options:
            listbox.selection_set(0)
            listbox.activate(0)

        def submit_selection(event=None):
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("No Selection", "Please select an option before continuing.")
                return
            selected_value["value"] = options[selected_index[0]]
            selection_window.destroy()

        def cancel_selection():
            selection_window.destroy()

        listbox.bind("<Double-Button-1>", submit_selection)

        button_frame = tk.Frame(selection_window)
        button_frame.pack(pady=(0, 18))

        tk.Button(button_frame, text="Select", command=submit_selection, width=14).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", command=cancel_selection, width=14).pack(side="left", padx=10)

        self.root.wait_window(selection_window)
        return selected_value["value"]

    def gpg_algorithm_name(self, algo_code):
        algorithm_map = {
            "1": "RSA",
            "16": "ELG",
            "17": "DSA",
            "18": "ECDH",
            "19": "ECDSA",
            "20": "ELG",
            "22": "EDDSA",
        }
        return algorithm_map.get(str(algo_code), "KEY")

    def get_gpg_key_entries(self, secret_only=False):
        command = [
            "gpg",
            "--list-secret-keys" if secret_only else "--list-keys",
            "--with-colons",
            "--fingerprint",
            "--keyid-format",
            "LONG",
        ]

        try:
            output = subprocess.check_output(command, text=True, stderr=subprocess.STDOUT)
        except Exception:
            return []

        entries = []
        current = None

        for raw_line in output.splitlines():
            parts = raw_line.split(":")
            if not parts:
                continue

            record_type = parts[0]

            if record_type in ("sec", "pub"):
                if current and current.get("keyid"):
                    entries.append(current)
                current = {
                    "type": record_type,
                    "status_code": parts[1].strip(),
                    "length": parts[2].strip(),
                    "algo_code": parts[3].strip(),
                    "keyid": parts[4].strip(),
                    "fingerprint": "",
                    "uid_text": "",
                }
            elif record_type == "fpr" and current and not current["fingerprint"]:
                current["fingerprint"] = parts[9].strip()
            elif record_type == "uid" and current and not current["uid_text"]:
                current["uid_text"] = parts[9].strip()

        if current and current.get("keyid"):
            entries.append(current)

        formatted_entries = []
        for entry in entries:
            algo_name = self.gpg_algorithm_name(entry["algo_code"])
            key_length = entry["length"] or "?"
            key_id = entry["keyid"] or "Unknown"
            display_id = f"{algo_name}{key_length}/{key_id}"
            uid_text = entry["uid_text"] or entry["fingerprint"] or "No user ID available"

            formatted_entries.append({
                **entry,
                "algo_name": algo_name,
                "display_id": display_id,
                "is_revoked": entry["status_code"] == "r",
                "uid_text": uid_text,
            })

        return formatted_entries

    def choose_key_entry(self, entries, title, prompt, key_label):
        if not entries:
            return None

        option_map = {}
        option_list = []

        for entry in entries:
            revoked_suffix = " [Revoked]" if entry.get("is_revoked") else ""
            option_text = f"{key_label}: {entry['display_id']}{revoked_suffix} - {entry['uid_text']}"
            option_map[option_text] = entry
            option_list.append(option_text)

        selected_option = self.choose_from_list(title, prompt, option_list)
        return option_map.get(selected_option)

    def prompt_for_passphrase(self, title, prompt):
        prompt_window = tk.Toplevel(self.root)
        prompt_window.title(title)
        prompt_window.geometry("460x190")
        prompt_window.grab_set()

        tk.Label(
            prompt_window,
            text=prompt,
            font=("Arial", 10),
            wraplength=410,
            justify="center"
        ).pack(pady=15)

        pass_entry = tk.Entry(prompt_window, show="*", width=42)
        pass_entry.pack(pady=10)
        pass_entry.focus_set()

        button_frame = tk.Frame(prompt_window)
        button_frame.pack(pady=10)

        def submit_passphrase():
            prompt_window.passphrase = pass_entry.get().strip()
            prompt_window.destroy()

        tk.Button(button_frame, text="OK", command=submit_passphrase, width=12).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", command=prompt_window.destroy, width=12).pack(side="left", padx=10)

        self.root.wait_window(prompt_window)
        return getattr(prompt_window, "passphrase", None)

    def build_encrypted_output_path(self, file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(file_path)
        name, ext = os.path.splitext(base_name)
        if not name:
            name = base_name or "file"
        return os.path.join(ENCRYPTED_DECRYPTED_DIR, f"encrypted_{name}_{timestamp}{ext}.gpg")

    def build_decrypted_output_path(self, file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(file_path)
        if base_name.lower().endswith(".gpg"):
            base_name = base_name[:-4]
        name, ext = os.path.splitext(base_name)
        if not name:
            name = base_name or "file"
        return os.path.join(ENCRYPTED_DECRYPTED_DIR, f"decrypted_{name}_{timestamp}{ext}")

    def get_gnupg_home(self):
        return os.environ.get("GNUPGHOME", os.path.expanduser("~/.gnupg"))

    def get_revocation_certificate_path(self, fingerprint):
        return os.path.join(
            self.get_gnupg_home(),
            "openpgp-revocs.d",
            f"{fingerprint.upper()}.rev"
        )

    def prepare_revocation_certificate_for_import(self, revocation_path):
        with open(revocation_path, "r", encoding="utf-8", errors="replace") as rev_file:
            original_lines = rev_file.read().splitlines()

        normalized_lines = []
        for line in original_lines:
            if line.startswith(":-----"):
                normalized_lines.append(line[1:])
            else:
                normalized_lines.append(line)

        temp_file = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            delete=False,
            suffix=".asc"
        )
        try:
            temp_file.write("\n".join(normalized_lines) + "\n")
            return temp_file.name
        finally:
            temp_file.close()

    def show_main_menu(self):
        self.clear_frame()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = min(1700, max(1180, screen_width - 80))
        window_height = min(1400, max(980, screen_height - 80))
        self.root.geometry(f"{window_width}x{window_height}")

        tk.Label(
            self.current_frame,
            text="GPG Cryptographic Security Toolkit",
            font=("Arial", 24, "bold")
        ).pack(pady=(0, 0))

        button_frame = tk.Frame(self.current_frame)
        button_frame.pack(pady=(0, 0))

        btn_style = {"font": ("Arial", 12), "width": 34, "pady": 10}

        tk.Button(button_frame, text="Compute SHA-256 Hash", command=self.show_compute_hash, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Stored Hash Files", command=self.show_stored_hashes, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Asymmetric Key Generation", command=self.show_key_generation, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Create Digital Signatures", command=self.show_create_signatures, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Digitally Signed Files", command=self.show_signed_files, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Verify & Certify Public Key", command=self.show_verify_certify_public_key, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Verify Digital Signature", command=self.show_verify_digital_signature, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Encrypting / Decrypting Files", command=self.show_encrypt_decrypt_menu, **btn_style).pack(pady=8)
        tk.Button(button_frame, text="Encrypted / Decrypted Files", command=self.show_encrypted_decrypted_files, **btn_style).pack(pady=8)

        self.add_main_menu_image()

    def add_main_menu_image(self):
        try:
            image_frame = tk.Frame(self.current_frame)
            image_frame.pack(fill="both", expand=True, pady=(10, 0))

            if not os.path.exists(MAIN_MENU_IMAGE_PATH):
                tk.Label(
                    image_frame,
                    text=f"Image not found: {MAIN_MENU_IMAGE_PATH}",
                    font=("Arial", 10),
                    fg="red"
                ).pack()
                return

            image = Image.open(MAIN_MENU_IMAGE_PATH)
            self.root.update_idletasks()
            frame_width = max(1, image_frame.winfo_width())
            frame_height = max(1, image_frame.winfo_height())

            if frame_width <= 1 or frame_height <= 1:
                frame_width = max(1, self.current_frame.winfo_width() - 40)
                frame_height = max(1, self.current_frame.winfo_height() - 40)

            available_width = max(1, frame_width - 10)
            available_height = max(1, frame_height - 10)

            # Match the main-menu image to the screenshot-confirmed size.
            target_box_width = 355
            target_box_height = 530

            final_width = min(available_width, target_box_width)
            final_height = min(available_height, target_box_height)

            image = image.resize((final_width, final_height), Image.LANCZOS)
            self.main_menu_image = ImageTk.PhotoImage(image)

            image_label = tk.Label(image_frame, image=self.main_menu_image, bd=0, highlightthickness=0)
            image_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            tk.Label(
                self.current_frame,
                text=f"Could not load image: {e}",
                font=("Arial", 10),
                fg="red"
            ).pack(pady=25)

    def run_gpg(self, args, input_text=None):
        return subprocess.run(
            args,
            input=input_text,
            text=True,
            capture_output=True
        )

    def show_text_window(self, title, content, height=18):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("900x500")
        text = tk.Text(win, wrap="word")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", content)
        text.config(state="disabled")

    def ask_yes_no(self, title, prompt):
        return messagebox.askyesno(title, prompt)

    def file_sha256_hex(self, file_path):
        hash_obj = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()

    def unique_hash_filename(self, base_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{base_name}.{timestamp}.sha256.txt"

    # ==================== Compute SHA-256 Hash Section ====================
    def show_compute_hash(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Compute SHA-256 Hash",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Compute SHA-256 Hash",
                size=56,
                pady=(10, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.queue_list = tk.Listbox(content_frame, height=12, width=100)
        self.queue_list.pack(pady=(0, 10))

        self.create_large_interface_button(
            content_frame,
            "Load File(s)",
            self.load_file_for_hash,
            width=16
        ).pack(pady=10)
        self.create_large_interface_button(
            content_frame,
            "Create Hash",
            self.confirm_create_hash,
            width=16
        ).pack(pady=10)
        self.create_large_interface_button(
            content_frame,
            "Clear Queue",
            self.clear_hash_queue,
            width=16
        ).pack(pady=10)
        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=24)

    def load_file_for_hash(self):
        file_paths = filedialog.askopenfilenames(
            title="Select file(s) to hash",
            initialdir=WINDOWS_MOUNT_DIR
        )
        for file_path in file_paths:
            if file_path and file_path not in self.queued_files:
                self.queued_files.append(file_path)
                self.queue_list.insert(tk.END, file_path)

    def clear_hash_queue(self):
        self.queued_files.clear()
        if hasattr(self, "queue_list"):
            self.queue_list.delete(0, tk.END)

    def confirm_create_hash(self):
        if not self.queued_files:
            messagebox.showwarning("No File", "Please load at least one file.")
            return

        if not self.ask_yes_no("Compute SHA-256 Hash", "Compute SHA-256 hash file(s)?"):
            return

        errors = []
        created = []
        for fpath in self.queued_files[:]:
            try:
                out_path = self.compute_and_store_hash(fpath)
                created.append(out_path)
            except Exception as e:
                errors.append(f"{fpath}: {e}")

        self.clear_hash_queue()

        if created:
            messagebox.showinfo(
                "Success",
                f"Created {len(created)} hash file(s) successfully."
            )
        if errors:
            self.show_text_window("Hash Errors", "\n".join(errors))

        self.show_stored_hashes()

    def compute_and_store_hash(self, file_path):
        file_hash = self.file_sha256_hex(file_path)
        base_name = os.path.basename(file_path)
        hash_filename = self.unique_hash_filename(base_name)
        hash_path = os.path.join(STORAGE_DIR, hash_filename)

        with open(hash_path, "w", newline="\n", encoding="utf-8") as f:
            f.write(f"SHA256({base_name}) = {file_hash}\n")

        return hash_path

    # ==================== Stored Hash Files ====================
    def show_stored_hashes(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Stored Hash Files",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Stored Hash Files",
                size=56,
                pady=(12, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.hash_frame = tk.Frame(content_frame)
        self.hash_frame.pack(fill="x")
        self.refresh_stored_hashes()

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=24)

    def refresh_stored_hashes(self):
        for widget in self.hash_frame.winfo_children():
            widget.destroy()

        hash_files = sorted(glob.glob(os.path.join(STORAGE_DIR, "*.sha256.txt")))
        if not hash_files:
            tk.Label(self.hash_frame, text="No stored hashes yet.", font=("Arial", 11)).pack(pady=12)
            return

        list_container = tk.Frame(self.hash_frame)
        list_container.pack(fill="x", anchor="n")

        for hfile in hash_files:
            fname = os.path.basename(hfile)

            card = tk.Frame(
                list_container,
                bd=2,
                relief="solid",
                bg="white",
                padx=14,
                pady=12
            )
            card.pack(fill="x", pady=6, padx=8)

            name_label = tk.Label(
                card,
                text=fname,
                font=("Arial", 11, "bold"),
                anchor="w",
                justify="left",
                wraplength=580,
                bg="white"
            )
            name_label.pack(side="left", fill="x", expand=True, padx=(0, 14))

            action_frame = tk.Frame(card, bg="white")
            action_frame.pack(side="right")

            self.create_large_action_button(
                action_frame,
                "Delete",
                lambda f=hfile: self.delete_hash(f),
                width=9
            ).pack(side="right", padx=(10, 0))
            self.create_large_action_button(
                action_frame,
                "Export",
                lambda f=hfile: self.export_hash(f),
                width=9
            ).pack(side="right", padx=(10, 0))
            self.create_large_action_button(
                action_frame,
                "View",
                lambda f=hfile: self.view_file(f),
                width=9
            ).pack(side="right")

    def view_file(self, fpath):
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            self.show_text_window(os.path.basename(fpath), content)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_hash(self, hfile):
        if not self.ask_yes_no("Delete Hash", f"Delete this hash file?\n\n{os.path.basename(hfile)}"):
            return
        try:
            os.remove(hfile)
            self.refresh_stored_hashes()
            messagebox.showinfo("Removed", "The hash file has been removed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_hash(self, hfile):
        try:
            dest = os.path.join(EXPORT_DIR, os.path.basename(hfile))
            shutil.copy2(hfile, dest)
            messagebox.showinfo("Exported", f"Hash exported to:\n{dest}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================== Asymmetric Key Generation ====================
    def show_key_generation(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Asymmetric Key Generation",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Asymmetric Key Generation",
                size=56,
                pady=(12, 18),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.create_large_interface_button(
            content_frame,
            "Create New Private/Public Key Pair",
            self.create_new_keypair
        ).pack(pady=(0, 14))
        self.create_large_interface_button(
            content_frame,
            "Revoke Public Key",
            self.revoke_public_key,
            width=20
        ).pack(pady=(0, 14))
        self.create_large_interface_button(
            content_frame,
            "Delete Key Pair",
            self.delete_key_pair,
            width=20
        ).pack(pady=(0, 14))
        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=(0, 22))

        self.key_list_frame = tk.Frame(content_frame)
        self.key_list_frame.pack(fill="x", pady=20)
        self.refresh_key_list()

    def parse_secret_key_blocks(self, gpg_output):
        blocks = []
        current_block = []

        for raw_line in gpg_output.splitlines():
            line = raw_line.rstrip()
            stripped = line.strip()

            if not stripped:
                continue

            # Ignore status, separator, and metadata lines until a real secret key block starts.
            if not current_block and not stripped.startswith("sec"):
                continue

            if stripped.startswith("sec") and current_block:
                if current_block[0].startswith("sec"):
                    blocks.append("\n".join(current_block))
                current_block = [stripped]
            else:
                current_block.append(stripped)

        if current_block and current_block[0].startswith("sec"):
            blocks.append("\n".join(current_block))

        return blocks

    def create_bordered_card(self, parent, text, font=("Arial", 11), wraplength=580, pady=6, padx=8):
        card = tk.Frame(
            parent,
            bd=2,
            relief="solid",
            bg="white",
            padx=14,
            pady=12
        )
        card.pack(fill="x", pady=pady, padx=padx)

        tk.Label(
            card,
            text=text,
            font=font,
            justify="left",
            anchor="w",
            wraplength=wraplength,
            bg="white"
        ).pack(fill="x", expand=True)

        return card

    def refresh_key_list(self):
        for widget in self.key_list_frame.winfo_children():
            widget.destroy()
        try:
            key_entries = self.get_gpg_key_entries(secret_only=True)
            if not key_entries:
                tk.Label(self.key_list_frame, text="No keys found or error listing keys.", font=("Arial", 11)).pack(pady=12)
                return

            list_container = tk.Frame(self.key_list_frame)
            list_container.pack(fill="x", anchor="n")

            for entry in key_entries:
                key_status = "Revoked" if entry.get("is_revoked") else "Active"
                key_summary = (
                    f"Key Pair: {entry['display_id']}\n"
                    f"User ID: {entry['uid_text']}\n"
                    f"Fingerprint: {entry['fingerprint'] or 'Unavailable'}\n"
                    f"Status: {key_status}"
                )
                self.create_bordered_card(
                    list_container,
                    key_summary,
                    font=("Courier New", 10),
                    wraplength=1000
                )
        except Exception:
            tk.Label(self.key_list_frame, text="No keys found or error listing keys.", font=("Arial", 11)).pack(pady=12)

    def create_new_keypair(self):
        password = self.get_key_password()
        if not password:
            return

        exp_win = tk.Toplevel(self.root)
        exp_win.title("Select Expiration Date")
        exp_win.geometry("420x420")

        cal = Calendar(
            exp_win,
            selectmode="day",
            year=datetime.now().year,
            month=datetime.now().month,
            day=datetime.now().day,
            mindate=datetime.now().date() + timedelta(days=1)
        )
        cal.pack(pady=20)

        no_exp_var = tk.BooleanVar(value=False)
        tk.Checkbutton(exp_win, text="No expiration", variable=no_exp_var).pack(pady=8)
        tk.Button(exp_win, text="Done", command=exp_win.destroy).pack(pady=10)
        self.root.wait_window(exp_win)

        expire_date = "0" if no_exp_var.get() else cal.get_date().replace("-", "")

        real_name = simpledialog.askstring("Real Name", "What's your real name to assign the key?")
        if not real_name:
            return
        email = simpledialog.askstring("Email", "What's your email to assign the key?")
        if not email:
            return
        comment = simpledialog.askstring("Comment", "Type a comment to assign to the key (optional):") or ""

        batch_input = f"""Key-Type: RSA
Key-Length: 4096
Subkey-Type: RSA
Subkey-Length: 4096
Expire-Date: {expire_date}
Name-Real: {real_name}
Name-Comment: {comment}
Name-Email: {email}
Passphrase: {password}
%commit
"""

        try:
            result = subprocess.run(
                ["gpg", "--batch", "--gen-key"],
                input=batch_input,
                text=True,
                capture_output=True
            )
            if result.returncode != 0:
                messagebox.showerror("Error", f"Key generation failed:\n{result.stderr}")
                return

            messagebox.showinfo("Success", "Keys successfully created.")
            self.refresh_key_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def revoke_public_key(self):
        key_entries = [
            entry for entry in self.get_gpg_key_entries(secret_only=True)
            if not entry.get("is_revoked")
        ]
        if not key_entries:
            messagebox.showwarning(
                "No Keys Available",
                "No non-revoked public keys were found for revocation."
            )
            return

        selected_key = self.choose_key_entry(
            key_entries,
            "Select Public Key",
            "Select the public key you would like to revoke. The matching RSA4096/private key identification is shown with each option.",
            "Public Key"
        )
        if not selected_key:
            return

        if not self.ask_yes_no(
            "Revoke Public Key",
            "Are you sure you would like to revoke this public key?\n\n"
            f"{selected_key['display_id']}"
        ):
            self.show_key_generation()
            return

        revocation_path = self.get_revocation_certificate_path(selected_key["fingerprint"])
        if not os.path.exists(revocation_path):
            messagebox.showerror(
                "Revocation Error",
                "The revocation certificate for this key pair was not found in the GnuPG revocation directory."
            )
            return

        temp_revocation_path = None
        try:
            temp_revocation_path = self.prepare_revocation_certificate_for_import(revocation_path)
            result = subprocess.run(
                ["gpg", "--batch", "--yes", "--import", temp_revocation_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                messagebox.showerror(
                    "Revocation Error",
                    (result.stderr or result.stdout or "The selected public key could not be revoked.").strip()
                )
                return

            self.refresh_key_list()
            messagebox.showinfo(
                "Revoked",
                f"The public key paired with {selected_key['display_id']} has been revoked."
            )
        except Exception as e:
            messagebox.showerror("Revocation Error", f"Unexpected error during revocation:\n{e}")
        finally:
            if temp_revocation_path and os.path.exists(temp_revocation_path):
                os.remove(temp_revocation_path)

    def delete_key_pair(self):
        key_entries = self.get_gpg_key_entries(secret_only=True)
        if not key_entries:
            messagebox.showwarning("No Keys Available", "No asymmetric key pairs were found to delete.")
            return

        selected_key = self.choose_key_entry(
            key_entries,
            "Select Key Pair",
            "Select the asymmetric key pair you would like to delete.",
            "Key Pair"
        )
        if not selected_key:
            return

        if not self.ask_yes_no(
            "Delete Key Pair",
            "Would you like to delete this key pair?\n\n"
            f"{selected_key['display_id']}"
        ):
            self.show_key_generation()
            return

        try:
            result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--delete-secret-and-public-key",
                    selected_key["fingerprint"],
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                messagebox.showerror(
                    "Delete Error",
                    (result.stderr or result.stdout or "The selected key pair could not be deleted.").strip()
                )
                return

            self.refresh_key_list()
            messagebox.showinfo(
                "Deleted",
                f"The key pair {selected_key['display_id']} has been deleted."
            )
        except Exception as e:
            messagebox.showerror("Delete Error", f"Unexpected error during key deletion:\n{e}")

    def get_key_password(self):
        pw_win = tk.Toplevel(self.root)
        pw_win.title("Private Key Password")
        pw_win.geometry("420x280")
        pw_win.grab_set()

        tk.Label(
            pw_win,
            text="Create a password for the private key and retype it below.",
            font=("Arial", 10),
            justify="center",
            wraplength=380
        ).pack(pady=20)

        tk.Label(pw_win, text="Password:").pack(anchor="w", padx=40)
        pass1 = tk.Entry(pw_win, show="*", width=40)
        pass1.pack(pady=5, padx=40)

        tk.Label(pw_win, text="Retype Password:").pack(anchor="w", padx=40)
        pass2 = tk.Entry(pw_win, show="*", width=40)
        pass2.pack(pady=5, padx=40)

        btn_frame = tk.Frame(pw_win)
        btn_frame.pack(pady=20)

        done_btn = tk.Button(btn_frame, text="Done", state="disabled", width=15)
        done_btn.pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=pw_win.destroy, width=15).pack(side="left", padx=10)

        def check_passwords(*args):
            p1 = pass1.get().strip()
            p2 = pass2.get().strip()
            done_btn.config(state="normal" if p1 and p1 == p2 else "disabled")

        pass1.bind("<KeyRelease>", check_passwords)
        pass2.bind("<KeyRelease>", check_passwords)

        def submit_password():
            password = pass1.get().strip()
            if password:
                pw_win.password = password
                pw_win.destroy()

        done_btn.config(command=submit_password)
        self.root.wait_window(pw_win)
        return getattr(pw_win, "password", None)

    # ==================== Create Digital Signatures ====================
    def show_create_signatures(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Create Digital Signatures",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Create Digital Signatures",
                size=56,
                pady=(12, 18),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.create_large_interface_button(
            content_frame,
            "Sign A Hash File",
            self.select_key_and_sign,
            width=16
        ).pack(pady=(0, 16))
        self.signature_list_frame = tk.Frame(content_frame)
        self.signature_list_frame.pack(fill="x")
        self.signature_dynamic_widgets = []
        self.refresh_signature_lists()

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=24)

    def refresh_signature_lists(self):
        for widget in self.signature_dynamic_widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.signature_dynamic_widgets = []

        parent = self.signature_list_frame if self.signature_list_frame and self.signature_list_frame.winfo_exists() else self.get_content_parent()

        key_label = self.create_image_section_label(
            parent,
            "Available Keys",
            COMPUTE_HASH_BG_IMAGE_PATH,
            size=38,
            padx=8,
            pady=(8, 8),
            anchor="w"
        )
        self.signature_dynamic_widgets.append(key_label)
        try:
            keys_output = subprocess.check_output(
                ["gpg", "--list-secret-keys", "--keyid-format", "LONG"],
                text=True,
                stderr=subprocess.STDOUT
            )
            key_blocks = self.parse_secret_key_blocks(keys_output)
            if key_blocks:
                for key_block in key_blocks:
                    card = self.create_bordered_card(
                        parent,
                        key_block,
                        font=("Courier New", 10),
                        wraplength=1000
                    )
                    self.signature_dynamic_widgets.append(card)
            else:
                no_keys_label = tk.Label(parent, text="No keys found.", font=("Arial", 11), bg=parent.cget("bg"))
                no_keys_label.pack(anchor="w", padx=8, pady=8)
                self.signature_dynamic_widgets.append(no_keys_label)
        except Exception:
            no_keys_label = tk.Label(parent, text="No keys found.", font=("Arial", 11), bg=parent.cget("bg"))
            no_keys_label.pack(anchor="w", padx=8, pady=8)
            self.signature_dynamic_widgets.append(no_keys_label)

        hash_label = self.create_image_section_label(
            parent,
            "Available Hash Files",
            COMPUTE_HASH_BG_IMAGE_PATH,
            size=38,
            padx=8,
            pady=(18, 8),
            anchor="w"
        )
        self.signature_dynamic_widgets.append(hash_label)
        hash_files = sorted(glob.glob(os.path.join(STORAGE_DIR, "*.sha256.txt")))
        if not hash_files:
            no_hashes_label = tk.Label(parent, text="No stored hash files available to sign.", font=("Arial", 11), bg=parent.cget("bg"))
            no_hashes_label.pack(anchor="w", padx=8, pady=8)
            self.signature_dynamic_widgets.append(no_hashes_label)
            return

        for hfile in hash_files:
            card = self.create_bordered_card(
                parent,
                os.path.basename(hfile),
                font=("Arial", 11, "bold"),
                wraplength=1000
            )
            self.signature_dynamic_widgets.append(card)

    def get_valid_key_id(self):
        secret_keys = [
            entry for entry in self.get_gpg_key_entries(secret_only=True)
            if not entry.get("is_revoked")
        ]
        if not secret_keys:
            messagebox.showwarning("No Private Keys", "No available private keys were found for signing.")
            return None

        selected_key = self.choose_key_entry(
            secret_keys,
            "Select Private Key",
            "Select a private key to sign with.",
            "Private Key"
        )
        if not selected_key:
            return None

        return selected_key.get("fingerprint") or selected_key.get("keyid")

    def choose_hash_file(self):
        hash_files = sorted(glob.glob(os.path.join(STORAGE_DIR, "*.sha256.txt")))
        if not hash_files:
            messagebox.showwarning("No Hashes", "No stored hash files to sign.")
            return None

        option_map = {}
        option_list = []
        for path in hash_files:
            option_text = os.path.basename(path)
            option_map[option_text] = path
            option_list.append(option_text)

        selected_hash = self.choose_from_list(
            "Select Hash",
            "Which hash file would you like to sign?",
            option_list,
            geometry="760x420"
        )
        return option_map.get(selected_hash)

    def get_signing_password(self):
        return self.prompt_for_passphrase(
            "Enter Private Key Passphrase",
            "Enter the passphrase to unlock the private key for signing:"
        )

    # ==================== Encrypting / Decrypting Files ====================
    def show_encrypt_decrypt_menu(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Encrypting / Decrypting Files",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Encrypting / Decrypting Files",
                size=56,
                pady=(12, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.create_large_interface_button(
            content_frame,
            "Asymmetric Encryption",
            self.start_asymmetric_encryption_flow,
            width=26
        ).pack(pady=(0, 14))

        self.create_large_interface_button(
            content_frame,
            "Asymmetric Decryption",
            self.start_asymmetric_decryption_flow,
            width=26
        ).pack(pady=(0, 14))

        self.create_large_interface_button(
            content_frame,
            "Symmetric Encryption",
            self.start_symmetric_encryption_flow,
            width=26
        ).pack(pady=(0, 14))

        self.create_large_interface_button(
            content_frame,
            "Symmetric Decryption",
            self.start_symmetric_decryption_flow,
            width=26
        ).pack(pady=(0, 14))

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=(8, 20))

    def get_symmetric_encryption_passphrase(self):
        pw_win = tk.Toplevel(self.root)
        pw_win.title("Create Symmetric Encryption Passphrase")
        pw_win.geometry("500x280")
        pw_win.grab_set()

        tk.Label(
            pw_win,
            text="Create the password/passphrase you will use for encrypting and decrypting this file. Type it exactly the same twice.",
            font=("Arial", 10),
            justify="center",
            wraplength=440
        ).pack(pady=20)

        tk.Label(pw_win, text="Password / Passphrase:").pack(anchor="w", padx=45)
        pass1 = tk.Entry(pw_win, show="*", width=45)
        pass1.pack(pady=5, padx=45)

        tk.Label(pw_win, text="Retype Password / Passphrase:").pack(anchor="w", padx=45)
        pass2 = tk.Entry(pw_win, show="*", width=45)
        pass2.pack(pady=5, padx=45)

        button_frame = tk.Frame(pw_win)
        button_frame.pack(pady=20)

        done_btn = tk.Button(button_frame, text="Done", state="disabled", width=15)
        done_btn.pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", command=pw_win.destroy, width=15).pack(side="left", padx=10)

        def check_passwords(event=None):
            p1 = pass1.get().strip()
            p2 = pass2.get().strip()
            done_btn.config(state="normal" if p1 and p1 == p2 else "disabled")

        pass1.bind("<KeyRelease>", check_passwords)
        pass2.bind("<KeyRelease>", check_passwords)

        def submit_password():
            password = pass1.get().strip()
            if password:
                pw_win.passphrase = password
                pw_win.destroy()

        done_btn.config(command=submit_password)
        pass1.focus_set()
        self.root.wait_window(pw_win)
        return getattr(pw_win, "passphrase", None)

    def import_public_key_file_for_encryption(self, public_key_file):
        show_result = subprocess.run(
            [
                "gpg",
                "--batch",
                "--yes",
                "--with-colons",
                "--with-fingerprint",
                "--import-options",
                "show-only",
                "--import",
                public_key_file,
            ],
            capture_output=True,
            text=True
        )

        parse_source = "\n".join(
            part for part in [show_result.stdout.strip(), show_result.stderr.strip()] if part
        )
        fingerprint = self.extract_primary_public_key_fingerprint(parse_source)

        if not fingerprint:
            human_result = subprocess.run(
                ["gpg", "--show-keys", "--with-fingerprint", public_key_file],
                capture_output=True,
                text=True
            )
            fingerprint = self.extract_fingerprint_from_human_output(
                "\n".join(
                    part for part in [human_result.stdout.strip(), human_result.stderr.strip()] if part
                )
            )

        import_result = subprocess.run(
            ["gpg", "--batch", "--yes", "--import", public_key_file],
            capture_output=True,
            text=True
        )

        import_output = "\n".join(
            part for part in [import_result.stderr.strip(), import_result.stdout.strip()] if part
        ).strip()

        if import_result.returncode != 0:
            raise RuntimeError(import_output or "GPG could not import the selected public key file.")

        if not fingerprint:
            fingerprint = self.extract_primary_public_key_fingerprint(import_output)

        if not fingerprint:
            raise RuntimeError("The public key was imported, but the primary fingerprint could not be detected.")

        return fingerprint

    def start_asymmetric_encryption_flow(self):
        messagebox.showinfo(
            "Asymmetric Encryption",
            "Please load the public key file that was shared with you to begin the encryption."
        )

        public_key_file = filedialog.askopenfilename(
            title="Select public key file for encryption",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[
                ("ASCII-armored public key files", "*.asc"),
                ("Public key files", "*.pub"),
                ("All files", "*.*"),
            ]
        )
        if not public_key_file:
            self.show_encrypt_decrypt_menu()
            return

        try:
            recipient_fingerprint = self.import_public_key_file_for_encryption(public_key_file)
        except Exception as e:
            messagebox.showerror("Public Key Import Error", str(e))
            self.show_encrypt_decrypt_menu()
            return

        file_path = filedialog.askopenfilename(
            title="Select file to encrypt",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[("All files", "*.*")]
        )
        if not file_path:
            self.show_encrypt_decrypt_menu()
            return

        if not self.ask_yes_no(
            "Asymmetric Encryption",
            f"Would you like to encrypt this file?\n\n{os.path.basename(file_path)}"
        ):
            self.show_encrypt_decrypt_menu()
            return

        output_path = self.build_encrypted_output_path(file_path)

        try:
            result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--trust-model",
                    "always",
                    "--recipient",
                    recipient_fingerprint,
                    "--output",
                    output_path,
                    "--encrypt",
                    file_path,
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                if os.path.exists(output_path):
                    os.remove(output_path)
                messagebox.showerror(
                    "Encryption Error",
                    (result.stderr or result.stdout or "GPG encryption failed.").strip()
                )
                return

            messagebox.showinfo("Success", "Your file has been successfully encrypted.")
            self.show_encrypted_decrypted_files()
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            messagebox.showerror("Encryption Error", f"Unexpected error during encryption:\n{e}")

    def start_asymmetric_decryption_flow(self):
        key_entries = [
            entry for entry in self.get_gpg_key_entries(secret_only=True)
            if not entry.get("is_revoked")
        ]
        if not key_entries:
            messagebox.showwarning(
                "No Private Keys Available",
                "No private keys were found. Please create a private/public key pair first."
            )
            return

        selected_key = self.choose_key_entry(
            key_entries,
            "Select Private Key",
            "Select which private key you would like to use for decryption.",
            "Private Key"
        )
        if not selected_key:
            self.show_encrypt_decrypt_menu()
            return

        continue_with_file = self.ask_yes_no(
            "Confirm Private Key",
            "Would you like to continue to select a file to decrypt with the private key "
            f"{selected_key['display_id']}?"
        )
        if not continue_with_file:
            self.show_encrypt_decrypt_menu()
            return

        file_path = filedialog.askopenfilename(
            title="Select file to decrypt",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[("GPG encrypted files", "*.gpg"), ("All files", "*.*")]
        )
        if not file_path:
            self.show_encrypt_decrypt_menu()
            return

        passphrase = self.prompt_for_passphrase(
            "Enter Private Key Passphrase",
            f"Enter the passphrase for the private key {selected_key['display_id']} to decrypt the file."
        )
        if not passphrase:
            messagebox.showinfo("Cancelled", "Decryption cancelled.")
            self.show_encrypt_decrypt_menu()
            return

        output_path = self.build_decrypted_output_path(file_path)

        try:
            result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--pinentry-mode",
                    "loopback",
                    "--passphrase",
                    passphrase,
                    "--try-secret-key",
                    selected_key["fingerprint"] or selected_key["keyid"],
                    "--output",
                    output_path,
                    "--decrypt",
                    file_path,
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                if os.path.exists(output_path):
                    os.remove(output_path)
                error_text = (result.stderr or result.stdout or "GPG decryption failed.").strip()
                if "Bad passphrase" in error_text or "bad passphrase" in error_text or "BAD_PASSPHRASE" in error_text:
                    messagebox.showerror("Decryption Error", "Incorrect passphrase. Please try again.")
                else:
                    messagebox.showerror("Decryption Error", error_text)
                return

            messagebox.showinfo("Success", "The file was decrypted successfully.")
            self.show_encrypted_decrypted_files()
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            messagebox.showerror("Decryption Error", f"Unexpected error during decryption:\n{e}")

    def start_symmetric_encryption_flow(self):
        messagebox.showinfo(
            "Symmetric Encryption",
            "Which file would you like to encrypt?"
        )

        file_path = filedialog.askopenfilename(
            title="Select file to encrypt",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[("All files", "*.*")]
        )
        if not file_path:
            self.show_encrypt_decrypt_menu()
            return

        if not self.ask_yes_no(
            "Symmetric Encryption",
            f"Would you like to encrypt this file?\n\n{os.path.basename(file_path)}"
        ):
            self.show_encrypt_decrypt_menu()
            return

        passphrase = self.get_symmetric_encryption_passphrase()
        if not passphrase:
            messagebox.showinfo("Cancelled", "Symmetric encryption cancelled.")
            self.show_encrypt_decrypt_menu()
            return

        output_path = self.build_encrypted_output_path(file_path)

        try:
            result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--pinentry-mode",
                    "loopback",
                    "--passphrase",
                    passphrase,
                    "--cipher-algo",
                    "AES256",
                    "--output",
                    output_path,
                    "--symmetric",
                    file_path,
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                if os.path.exists(output_path):
                    os.remove(output_path)
                messagebox.showerror(
                    "Symmetric Encryption Error",
                    (result.stderr or result.stdout or "GPG symmetric encryption failed.").strip()
                )
                return

            messagebox.showinfo("Success", "Your file has been successfully encrypted.")
            self.show_encrypted_decrypted_files()
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            messagebox.showerror("Symmetric Encryption Error", f"Unexpected error during symmetric encryption:\n{e}")

    def start_symmetric_decryption_flow(self):
        messagebox.showinfo(
            "Symmetric Decryption",
            "Which file would you like to decrypt?"
        )

        file_path = filedialog.askopenfilename(
            title="Select file to decrypt",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[("GPG encrypted files", "*.gpg"), ("All files", "*.*")]
        )
        if not file_path:
            self.show_encrypt_decrypt_menu()
            return

        if not self.ask_yes_no(
            "Symmetric Decryption",
            f"Would you like to decrypt this file?\n\n{os.path.basename(file_path)}"
        ):
            self.show_encrypt_decrypt_menu()
            return

        passphrase = self.prompt_for_passphrase(
            "Enter Symmetric Decryption Passphrase",
            "Enter the password/passphrase that was originally used to encrypt this file."
        )
        if not passphrase:
            messagebox.showinfo("Cancelled", "Symmetric decryption cancelled.")
            self.show_encrypt_decrypt_menu()
            return

        output_path = self.build_decrypted_output_path(file_path)

        try:
            result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--pinentry-mode",
                    "loopback",
                    "--passphrase",
                    passphrase,
                    "--output",
                    output_path,
                    "--decrypt",
                    file_path,
                ],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                if os.path.exists(output_path):
                    os.remove(output_path)
                error_text = (result.stderr or result.stdout or "GPG symmetric decryption failed.").strip()
                if (
                    "Bad passphrase" in error_text
                    or "bad passphrase" in error_text
                    or "BAD_PASSPHRASE" in error_text
                    or "Bad session key" in error_text
                    or "bad session key" in error_text
                ):
                    messagebox.showerror("Symmetric Decryption Error", "Incorrect passphrase. Please try again.")
                else:
                    messagebox.showerror("Symmetric Decryption Error", error_text)
                return

            messagebox.showinfo("Success", "The file was decrypted successfully.")
            self.show_encrypted_decrypted_files()
        except Exception as e:
            if os.path.exists(output_path):
                os.remove(output_path)
            messagebox.showerror("Symmetric Decryption Error", f"Unexpected error during symmetric decryption:\n{e}")

    # Backward-compatible method names in case another part of the application still calls them.
    def start_encrypt_file_flow(self):
        self.start_asymmetric_encryption_flow()

    def start_decrypt_file_flow(self):
        self.start_asymmetric_decryption_flow()


    # ==================== Verify & Certify Public Key ====================
    def show_verify_certify_public_key(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Verify & Certify Public Key",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Verify & Certify Public Key",
                size=52,
                pady=(12, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.reset_verify_certify_public_key_state(update_widgets=False)

        self.create_large_interface_button(
            content_frame,
            "Load Public Key File",
            self.load_public_key_file_for_certification,
            width=28
        ).pack(pady=(0, 10))

        self.certify_fingerprint_button = self.create_large_interface_button(
            content_frame,
            "Verify Fingerprint",
            self.verify_loaded_public_key_fingerprint,
            width=28
        )
        self.certify_fingerprint_button.pack(pady=(10, 10))

        self.certify_public_key_button = self.create_large_interface_button(
            content_frame,
            "Certify Public Key File",
            self.certify_loaded_public_key_file,
            width=28
        )
        self.certify_public_key_button.pack(pady=(10, 10))

        self.certify_export_button = self.create_large_interface_button(
            content_frame,
            "Export Certified Public Key File",
            self.confirm_export_certified_public_key_file,
            width=28
        )
        self.certify_export_button.pack(pady=(10, 12))

        self.certify_load_value_label = self.create_file_display_box(
            content_frame,
            "Loaded Public Key File",
            "No public key file loaded.",
            pady=10
        )

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=18)

        self.refresh_verify_certify_public_key_buttons()

    def reset_verify_certify_public_key_state(self, update_widgets=True):
        self.certify_public_key_file = None
        self.certify_public_key_fingerprint = None
        self.certify_public_key_details = ""
        self.certify_fingerprint_verified = False
        self.certify_public_key_completed = False

        if update_widgets:
            if self.certify_load_value_label and self.certify_load_value_label.winfo_exists():
                self.certify_load_value_label.config(text="No public key file loaded.")
            self.refresh_verify_certify_public_key_buttons()

    def refresh_verify_certify_public_key_buttons(self):
        if self.certify_fingerprint_button and self.certify_fingerprint_button.winfo_exists():
            self.certify_fingerprint_button.config(
                state="normal" if self.certify_public_key_file else "disabled"
            )

        if self.certify_public_key_button and self.certify_public_key_button.winfo_exists():
            self.certify_public_key_button.config(
                state="normal" if self.certify_fingerprint_verified else "disabled"
            )

        if self.certify_export_button and self.certify_export_button.winfo_exists():
            self.certify_export_button.config(
                state="normal" if self.certify_public_key_completed else "disabled"
            )

    def load_public_key_file_for_certification(self):
        file_path = filedialog.askopenfilename(
            title="Select public key file",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[
                ("ASCII-armored public key files", "*.asc"),
                ("Public key files", "*.pub"),
                ("All files", "*.*"),
            ]
        )
        if not file_path:
            return

        # Loading a new public key always resets the step-by-step queue.
        self.certify_public_key_file = file_path
        self.certify_public_key_fingerprint = None
        self.certify_public_key_details = ""
        self.certify_fingerprint_verified = False
        self.certify_public_key_completed = False
        self.certify_public_key_storage_path = None

        if self.certify_load_value_label and self.certify_load_value_label.winfo_exists():
            self.certify_load_value_label.config(text=file_path)

        try:
            show_result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--with-colons",
                    "--with-fingerprint",
                    "--import-options",
                    "show-only",
                    "--import",
                    file_path,
                ],
                capture_output=True,
                text=True
            )

            parse_source = "\n".join(
                part for part in [show_result.stdout.strip(), show_result.stderr.strip()] if part
            )

            fingerprint = self.extract_primary_public_key_fingerprint(parse_source)
            if not fingerprint:
                human_result = subprocess.run(
                    ["gpg", "--show-keys", "--with-fingerprint", file_path],
                    capture_output=True,
                    text=True
                )
                fingerprint = self.extract_fingerprint_from_human_output(
                    "\n".join(
                        part for part in [human_result.stdout.strip(), human_result.stderr.strip()] if part
                    )
                )

            import_result = subprocess.run(
                ["gpg", "--batch", "--yes", "--import", file_path],
                capture_output=True,
                text=True
            )

            import_output = "\n".join(
                part for part in [import_result.stderr.strip(), import_result.stdout.strip()] if part
            ).strip()

            if import_result.returncode != 0:
                self.reset_verify_certify_public_key_state(update_widgets=True)
                self.show_text_window(
                    "Public Key Import Error",
                    import_output or "GPG could not import the selected public key file.",
                    height=20
                )
                return

            if not fingerprint:
                fingerprint = self.extract_primary_public_key_fingerprint(import_output)

            if not fingerprint:
                self.reset_verify_certify_public_key_state(update_widgets=True)
                self.show_text_window(
                    "Public Key Fingerprint Error",
                    "The public key was imported, but the primary fingerprint could not be detected.",
                    height=20
                )
                return

            self.certify_public_key_fingerprint = fingerprint
            messagebox.showinfo(
                "Public Key Loaded",
                "The public key file has been loaded and imported.\n\n"
                "You can now press Verify Fingerprint."
            )
        except Exception as e:
            self.reset_verify_certify_public_key_state(update_widgets=True)
            messagebox.showerror("Public Key Load Error", f"Unexpected error while loading the public key:\n{e}")
            return

        self.refresh_verify_certify_public_key_buttons()

    def extract_primary_public_key_fingerprint(self, gpg_text):
        current_record_is_public_key = False

        for raw_line in gpg_text.splitlines():
            parts = raw_line.split(":")
            if not parts:
                continue

            record_type = parts[0]
            if record_type == "pub":
                current_record_is_public_key = True
            elif record_type in ("sub", "sec", "ssb"):
                current_record_is_public_key = False
            elif record_type == "fpr" and current_record_is_public_key and len(parts) > 9:
                fingerprint = parts[9].strip()
                if fingerprint:
                    return fingerprint

        return None

    def extract_fingerprint_from_human_output(self, gpg_text):
        for raw_line in gpg_text.splitlines():
            compact_line = raw_line.strip().replace(" ", "")
            if len(compact_line) >= 40 and all(ch in "0123456789ABCDEFabcdef" for ch in compact_line):
                return compact_line.upper()
        return None

    def verify_loaded_public_key_fingerprint(self):
        if not self.certify_public_key_file or not self.certify_public_key_fingerprint:
            messagebox.showwarning(
                "No Public Key Loaded",
                "Please load a public key file before verifying the fingerprint."
            )
            return

        try:
            # Show the fingerprint/details from the normal GPG keyring after import.
            # This is important because certification and later verification must use
            # the same normal GPG keyring, not a temporary disposable keyring.
            details_result = subprocess.run(
                [
                    "gpg",
                    "--list-keys",
                    "--with-fingerprint",
                    "--with-subkey-fingerprint",
                    "--keyid-format",
                    "LONG",
                    self.certify_public_key_fingerprint,
                ],
                capture_output=True,
                text=True
            )

            details_output = "\n".join(
                part for part in [details_result.stdout.strip(), details_result.stderr.strip()] if part
            ).strip()

            if details_result.returncode != 0:
                self.show_text_window(
                    "Fingerprint Verification Error",
                    details_output or "GPG could not display the imported public key details from the normal keyring.",
                    height=20
                )
                return

            compact_details = details_output.replace(" ", "")
            if self.certify_public_key_fingerprint not in compact_details:
                details_output += (
                    "\n\nDetected Primary Fingerprint:\n"
                    f"{self.certify_public_key_fingerprint}"
                )

            self.certify_public_key_details = details_output or "No public key details were returned by GPG."
            self.certify_fingerprint_verified = True
            self.certify_public_key_completed = False
            self.certify_public_key_storage_path = None
            self.refresh_verify_certify_public_key_buttons()
            self.show_text_window("Public Key Fingerprint / Identity Details", self.certify_public_key_details, height=22)
        except Exception as e:
            messagebox.showerror("Fingerprint Error", f"Unexpected error while verifying the fingerprint:\n{e}")

    def certify_loaded_public_key_file(self):
        if not self.certify_fingerprint_verified or not self.certify_public_key_fingerprint:
            messagebox.showwarning(
                "Fingerprint Not Verified",
                "Please verify the public key fingerprint before certifying the public key file."
            )
            return

        key_entries = [
            entry for entry in self.get_gpg_key_entries(secret_only=True)
            if not entry.get("is_revoked")
        ]
        if not key_entries:
            messagebox.showwarning(
                "No Private Keys Available",
                "No non-revoked private keys were found. Please create a private/public key pair first."
            )
            return

        selected_key = self.choose_key_entry(
            key_entries,
            "Which Private Key would you like to certify with?",
            "Which Private Key would you like to certify with?",
            "Private Key"
        )
        if not selected_key:
            return

        passphrase = self.prompt_for_passphrase(
            "Enter Private Key Passphrase",
            f"Enter the passphrase for the private key {selected_key['display_id']} to certify this public key."
        )
        if not passphrase:
            messagebox.showinfo("Cancelled", "Public key certification cancelled.")
            return

        try:
            certify_result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--pinentry-mode",
                    "loopback",
                    "--passphrase",
                    passphrase,
                    "--local-user",
                    selected_key["fingerprint"] or selected_key["keyid"],
                    "--quick-sign-key",
                    self.certify_public_key_fingerprint,
                ],
                capture_output=True,
                text=True
            )

            certify_output = "\n".join(
                part for part in [certify_result.stderr.strip(), certify_result.stdout.strip()] if part
            ).strip()

            if certify_result.returncode != 0:
                if "Bad passphrase" in certify_output or "bad passphrase" in certify_output or "BAD_PASSPHRASE" in certify_output:
                    messagebox.showerror("Certification Error", "Incorrect passphrase. Please try again.")
                else:
                    self.show_text_window(
                        "Certification Error",
                        certify_output or "GPG could not certify the selected public key.",
                        height=20
                    )
                return

            self.certify_public_key_completed = True
            self.refresh_verify_certify_public_key_buttons()
            messagebox.showinfo(
                "Public Key Certified",
                "The selected public key has been certified with the selected private key.\n\n"
                "You can now export the certified public key file."
            )
        except Exception as e:
            messagebox.showerror("Certification Error", f"Unexpected error while certifying the public key:\n{e}")

    def confirm_export_certified_public_key_file(self):
        if not self.certify_public_key_completed or not self.certify_public_key_fingerprint:
            messagebox.showwarning(
                "Public Key Not Certified",
                "Please certify the public key before exporting it."
            )
            return

        export_confirm_window = tk.Toplevel(self.root)
        export_confirm_window.title("Export Certified Public Key")
        export_confirm_window.geometry("520x210")
        export_confirm_window.grab_set()

        tk.Label(
            export_confirm_window,
            text="Would you like to export the certified public key file?",
            font=("Arial", 12, "bold"),
            wraplength=460,
            justify="center"
        ).pack(pady=(28, 24))

        button_frame = tk.Frame(export_confirm_window)
        button_frame.pack(pady=8)

        user_choice = {"answer": None}

        def choose_yes():
            user_choice["answer"] = True
            export_confirm_window.destroy()

        def choose_no():
            user_choice["answer"] = False
            export_confirm_window.destroy()

        tk.Button(button_frame, text="Yes", command=choose_yes, width=14, font=("Arial", 11, "bold")).pack(side="left", padx=14)
        tk.Button(button_frame, text="No", command=choose_no, width=14, font=("Arial", 11, "bold")).pack(side="left", padx=14)

        self.root.wait_window(export_confirm_window)

        if user_choice["answer"] is not True:
            self.refresh_verify_certify_public_key_buttons()
            return

        self.export_certified_public_key_file()

    def export_certified_public_key_file(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"certified_public_key_{self.certify_public_key_fingerprint[-16:]}_{timestamp}.asc"

        # Save a certified public key copy inside the GUI storage folder and
        # also export a copy into the user's Windows Downloads folder.
        try:
            os.makedirs(EXPORT_DIR, exist_ok=True)
            os.makedirs(CERTIFIED_PUBLIC_KEYS_DIR, exist_ok=True)
        except Exception as e:
            messagebox.showerror(
                "Export Error",
                "Could not access or create one of the export directories.\n\n"
                f"Windows Downloads directory:\n{EXPORT_DIR}\n\n"
                f"GUI certified public key storage directory:\n{CERTIFIED_PUBLIC_KEYS_DIR}\n\n"
                f"Error:\n{e}"
            )
            return

        storage_path = os.path.join(CERTIFIED_PUBLIC_KEYS_DIR, default_name)
        export_path = os.path.join(EXPORT_DIR, default_name)

        try:
            # Export from the normal GPG keyring because this is where the key was
            # imported and certified. The exported file includes the public key and
            # the certification signature created by the selected private key.
            export_result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--armor",
                    "--output",
                    storage_path,
                    "--export",
                    self.certify_public_key_fingerprint,
                ],
                capture_output=True,
                text=True
            )

            export_output = "\n".join(
                part for part in [export_result.stderr.strip(), export_result.stdout.strip()] if part
            ).strip()

            if export_result.returncode != 0:
                self.show_text_window(
                    "Export Error",
                    export_output or "GPG could not export the certified public key from the normal keyring.",
                    height=20
                )
                return

            shutil.copy2(storage_path, export_path)
            self.certify_public_key_storage_path = storage_path

            messagebox.showinfo(
                "Exported",
                "The certified public key file was saved in both locations.\n\n"
                f"Windows Downloads copy:\n{export_path}\n\n"
                f"GUI storage copy:\n{storage_path}"
            )

            # After a successful export, clear the queue and return to the start of the process.
            self.reset_verify_certify_public_key_state(update_widgets=True)
        except Exception as e:
            if os.path.exists(storage_path) and not os.path.getsize(storage_path):
                try:
                    os.remove(storage_path)
                except Exception:
                    pass
            messagebox.showerror("Export Error", f"Unexpected error while exporting the certified public key:\n{e}")


    # ==================== Verify Digital Signature ====================
    def show_verify_digital_signature(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Verify Digital Signature",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Verify Digital Signature",
                size=56,
                pady=(12, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.verify_signature_file = None
        self.verify_hash_file = None
        self.verify_public_key_file = None

        self.create_large_interface_button(
            content_frame,
            "Load Signature File (.asc)",
            self.load_signature_file_for_verification,
            width=24
        ).pack(pady=(0, 10))

        self.create_large_interface_button(
            content_frame,
            "Load Hash File (.sha256.txt)",
            self.load_hash_file_for_verification,
            width=24
        ).pack(pady=(10, 10))

        self.create_large_interface_button(
            content_frame,
            "Load Public Key File",
            self.load_public_key_file_for_verification,
            width=24
        ).pack(pady=(10, 10))

        self.verify_execute_button = self.create_large_interface_button(
            content_frame,
            "Verify Digital Signature",
            self.confirm_verify_loaded_signature,
            width=24
        )
        self.verify_execute_button.pack(pady=12)
        self.verify_execute_button.config(state="disabled")

        self.verify_signature_value_label = self.create_file_display_box(
            content_frame,
            "Loaded Signature File",
            "No signature file loaded.",
            pady=10,
            clear_command=self.clear_signature_file_for_verification
        )

        self.verify_hash_value_label = self.create_file_display_box(
            content_frame,
            "Loaded Hash File",
            "No hash file loaded.",
            pady=6,
            clear_command=self.clear_hash_file_for_verification
        )

        self.verify_public_key_value_label = self.create_file_display_box(
            content_frame,
            "Loaded Public Key File",
            "No public key file loaded.",
            pady=6,
            clear_command=self.clear_public_key_file_for_verification
        )

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=18)

    def load_signature_file_for_verification(self):
        file_path = filedialog.askopenfilename(
            title="Select digitally signed file",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[
                ("ASCII-armored signature files", "*.asc"),
                ("All files", "*.*"),
            ]
        )
        if not file_path:
            return

        self.verify_signature_file = file_path
        if self.verify_signature_value_label and self.verify_signature_value_label.winfo_exists():
            self.verify_signature_value_label.config(text=file_path)
        self.refresh_verify_digital_signature_button()

    def load_hash_file_for_verification(self):
        file_path = filedialog.askopenfilename(
            title="Select SHA-256 hash file",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[
                ("SHA-256 hash files", "*.sha256.txt"),
                ("Text files", "*.txt"),
                ("All files", "*.*"),
            ]
        )
        if not file_path:
            return

        self.verify_hash_file = file_path
        if self.verify_hash_value_label and self.verify_hash_value_label.winfo_exists():
            self.verify_hash_value_label.config(text=file_path)
        self.refresh_verify_digital_signature_button()

    def load_public_key_file_for_verification(self):
        file_path = filedialog.askopenfilename(
            title="Select public key file",
            initialdir=WINDOWS_MOUNT_DIR,
            filetypes=[
                ("ASCII-armored public key files", "*.asc"),
                ("Public key files", "*.pub"),
                ("All files", "*.*"),
            ]
        )
        if not file_path:
            return

        self.verify_public_key_file = file_path
        if self.verify_public_key_value_label and self.verify_public_key_value_label.winfo_exists():
            self.verify_public_key_value_label.config(text=file_path)
        self.refresh_verify_digital_signature_button()

    def clear_signature_file_for_verification(self):
        self.verify_signature_file = None
        if self.verify_signature_value_label and self.verify_signature_value_label.winfo_exists():
            self.verify_signature_value_label.config(text="No signature file loaded.")
        self.refresh_verify_digital_signature_button()

    def clear_hash_file_for_verification(self):
        self.verify_hash_file = None
        if self.verify_hash_value_label and self.verify_hash_value_label.winfo_exists():
            self.verify_hash_value_label.config(text="No hash file loaded.")
        self.refresh_verify_digital_signature_button()

    def clear_public_key_file_for_verification(self):
        self.verify_public_key_file = None
        if self.verify_public_key_value_label and self.verify_public_key_value_label.winfo_exists():
            self.verify_public_key_value_label.config(text="No public key file loaded.")
        self.refresh_verify_digital_signature_button()

    def refresh_verify_digital_signature_button(self):
        if not self.verify_execute_button or not self.verify_execute_button.winfo_exists():
            return

        is_ready = bool(
            self.verify_signature_file
            and self.verify_hash_file
            and self.verify_public_key_file
        )
        self.verify_execute_button.config(state="normal" if is_ready else "disabled")

    def confirm_verify_loaded_signature(self):
        if not self.verify_signature_file or not self.verify_hash_file or not self.verify_public_key_file:
            messagebox.showwarning(
                "Missing Files",
                "Please load the signature file, hash file, and public key file before verifying."
            )
            return

        if not self.ask_yes_no("Verify Digital Signature", "Would you like to verify this digital signature?"):
            return

        self.run_loaded_signature_verification()

    def run_loaded_signature_verification(self):
        try:
            # Import the selected public key into the normal GPG keyring instead of
            # a temporary keyring. This allows GPG to see any certifications/trust
            # that were created in the Verify & Certify Public Key interface.
            import_result = subprocess.run(
                [
                    "gpg",
                    "--batch",
                    "--yes",
                    "--import",
                    self.verify_public_key_file,
                ],
                capture_output=True,
                text=True
            )

            import_output = "\n".join(
                part for part in [import_result.stderr.strip(), import_result.stdout.strip()] if part
            ).strip()

            if import_result.returncode != 0:
                if not import_output:
                    import_output = "GPG could not import the selected public key file."
                self.show_text_window("Public Key Import Error", import_output, height=20)
                return

            verify_result = subprocess.run(
                [
                    "gpg",
                    "--verify",
                    self.verify_signature_file,
                    self.verify_hash_file,
                ],
                capture_output=True,
                text=True
            )

            verification_output = "\n".join(
                part for part in [verify_result.stderr.strip(), verify_result.stdout.strip()] if part
            ).strip()

            if import_output:
                verification_output = "Public key import output:\n" + import_output + "\n\nVerification output:\n" + verification_output

            if not verification_output:
                verification_output = "No verification output was returned by GPG."

            self.show_text_window("Verification Result", verification_output, height=20)
        except Exception as e:
            messagebox.showerror("Verification Error", f"Unexpected error during verification:\n{e}")

    def select_key_and_sign(self):
        key_id = self.get_valid_key_id()
        if not key_id:
            return

        hash_path = self.choose_hash_file()
        if not hash_path:
            return

        if not self.ask_yes_no("Confirm Sign", f"Digitally sign this file?\n\n{os.path.basename(hash_path)}"):
            return

        passphrase = self.get_signing_password()
        if not passphrase:
            messagebox.showinfo("Cancelled", "Signing cancelled.")
            return

        signed_path = hash_path + ".asc"
        pub_path = hash_path + ".pub.asc"

        try:
            result = subprocess.run([
                "gpg",
                "--batch",
                "--yes",
                "--armor",
                "--output", signed_path,
                "--detach-sign",
                "--local-user", key_id,
                "--pinentry-mode", "loopback",
                "--passphrase", passphrase,
                hash_path,
            ], capture_output=True, text=True)

            if result.returncode != 0:
                err = (result.stderr or "").strip()
                if "Bad passphrase" in err or "BAD_PASSPHRASE" in err:
                    messagebox.showerror("Signing Error", "Incorrect passphrase. Please try again.")
                else:
                    messagebox.showerror("Signing Error", f"GPG failed:\n{err}")
                return

            export_result = subprocess.run([
                "gpg",
                "--batch",
                "--yes",
                "--armor",
                "--output", pub_path,
                "--export", key_id
            ], capture_output=True, text=True)

            if export_result.returncode != 0:
                messagebox.showerror("Public Key Export Error", export_result.stderr.strip())
                return

            verify_result = subprocess.run([
                "gpg",
                "--verify",
                signed_path,
                hash_path
            ], capture_output=True, text=True)

            if verify_result.returncode != 0:
                messagebox.showerror(
                    "Verification Error",
                    "The signature file was created, but immediate verification failed.\n\n"
                    + (verify_result.stderr or "")
                )
                return

            messagebox.showinfo(
                "Success",
                "The hash file has been successfully digitally signed and verified."
            )
            self.show_signed_files()

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during signing:\n{e}")

    # ==================== Digitally Signed Files ====================
    def show_signed_files(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Digitally Signed Files",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Digitally Signed Files",
                size=56,
                pady=(12, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.signed_list_frame = tk.Frame(content_frame)
        self.signed_list_frame.pack(fill="x")
        self.signed_dynamic_widgets = []
        self.refresh_signed_files()

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=(20, 24))

    def refresh_signed_files(self):
        for widget in self.signed_dynamic_widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.signed_dynamic_widgets = []

        parent = self.signed_list_frame if self.signed_list_frame and self.signed_list_frame.winfo_exists() else self.get_content_parent()

        sig_files = sorted(glob.glob(os.path.join(STORAGE_DIR, "*.sha256.txt.asc")))
        if not sig_files:
            no_signed_label = tk.Label(parent, text="No digitally signed files yet.", font=("Arial", 11), bg=parent.cget("bg"))
            no_signed_label.pack(anchor="w", padx=8, pady=(0, 12))
            self.signed_dynamic_widgets.append(no_signed_label)
            return

        for sfile in sig_files:
            fname = os.path.basename(sfile)

            card = self.create_bordered_card(
                parent,
                fname,
                font=("Arial", 11, "bold"),
                wraplength=580,
                pady=6
            )
            self.signed_dynamic_widgets.append(card)

            content_label = card.winfo_children()[0]
            content_label.pack_forget()
            content_label.pack(side="left", fill="x", expand=True, padx=(0, 14))

            action_frame = tk.Frame(card, bg="white")
            action_frame.pack(side="right")

            self.create_large_action_button(
                action_frame,
                "Delete",
                lambda f=sfile: self.remove_signed(f),
                width=9
            ).pack(side="right", padx=(10, 0))
            self.create_large_action_button(
                action_frame,
                "Export Set",
                lambda f=sfile: self.export_signed_set(f),
                width=10
            ).pack(side="right", padx=(10, 0))
            self.create_large_action_button(
                action_frame,
                "Verify",
                lambda f=sfile: self.verify_signed_pair(f),
                width=9
            ).pack(side="right")

    def verify_signed_pair(self, sig_file):
        base_hash_file = sig_file[:-4] if sig_file.endswith(".asc") else None
        if not base_hash_file or not os.path.exists(base_hash_file):
            messagebox.showerror("Missing Hash File", "The matching hash file was not found.")
            return

        result = subprocess.run(["gpg", "--verify", sig_file, base_hash_file], capture_output=True, text=True)
        msg = (result.stderr or result.stdout or "").strip()
        if result.returncode == 0:
            messagebox.showinfo("Verification Result", msg)
        else:
            messagebox.showerror("Verification Failed", msg)

    def export_signed_set(self, sig_file):
        try:
            base_hash_file = sig_file[:-4] if sig_file.endswith(".asc") else None
            pub_path = base_hash_file + ".pub.asc" if base_hash_file else None

            copied = []
            for path in [base_hash_file, sig_file, pub_path]:
                if path and os.path.exists(path):
                    dest = os.path.join(EXPORT_DIR, os.path.basename(path))
                    shutil.copy2(path, dest)
                    copied.append(dest)

            if not copied:
                messagebox.showwarning("Nothing Exported", "No matching files were found to export.")
                return

            messagebox.showinfo("Exported", "Exported these files:\n\n" + "\n".join(copied))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def remove_signed(self, sig_file):
        if not self.ask_yes_no("Delete", f"Delete this signature set?\n\n{os.path.basename(sig_file)}"):
            return

        try:
            base_hash_file = sig_file[:-4] if sig_file.endswith(".asc") else None
            pub_path = base_hash_file + ".pub.asc" if base_hash_file else None

            removed = []
            for path in [sig_file, pub_path]:
                if path and os.path.exists(path):
                    os.remove(path)
                    removed.append(path)

            messagebox.showinfo("Removed", "Removed selected signature file(s).")
            self.refresh_signed_files()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ==================== Encrypted / Decrypted Files ====================
    def show_encrypted_decrypted_files(self):
        self.clear_frame(use_black_background=True)
        has_bg = self.add_interface_background(
            "Encrypted / Decrypted Files",
            COMPUTE_HASH_BG_IMAGE_PATH,
            title_fill=COMPUTE_HASH_TITLE_COLOR,
            title_stroke_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
        )
        if not has_bg:
            self.create_outlined_title(
                self.current_frame,
                "Encrypted / Decrypted Files",
                size=56,
                pady=(12, 20),
                fill_color=COMPUTE_HASH_TITLE_COLOR,
                outline_width=COMPUTE_HASH_TITLE_STROKE_WIDTH
            )

        content_frame = self.setup_scrollable_body(
            top_pad=110 if has_bg else 0,
            background_image_path=COMPUTE_HASH_BG_IMAGE_PATH if has_bg else None
        )

        self.encrypted_list_frame = tk.Frame(content_frame)
        self.encrypted_list_frame.pack(fill="x")
        self.encrypted_file_dynamic_widgets = []
        self.refresh_encrypted_decrypted_files()

        self.create_large_interface_button(
            content_frame,
            "Back to Main Menu",
            self.show_main_menu,
            width=18
        ).pack(pady=(20, 24))

    def refresh_encrypted_decrypted_files(self):
        for widget in self.encrypted_file_dynamic_widgets:
            if widget.winfo_exists():
                widget.destroy()
        self.encrypted_file_dynamic_widgets = []

        parent = self.encrypted_list_frame if self.encrypted_list_frame and self.encrypted_list_frame.winfo_exists() else self.get_content_parent()

        managed_files = sorted(
            path for path in glob.glob(os.path.join(ENCRYPTED_DECRYPTED_DIR, "*"))
            if os.path.isfile(path)
        )

        if not managed_files:
            empty_label = tk.Label(
                parent,
                text="No encrypted or decrypted files have been saved yet.",
                font=("Arial", 11),
                bg=parent.cget("bg")
            )
            empty_label.pack(anchor="w", padx=8, pady=(0, 12))
            self.encrypted_file_dynamic_widgets.append(empty_label)
            return

        for file_path in managed_files:
            file_name = os.path.basename(file_path)

            card = self.create_bordered_card(
                parent,
                file_name,
                font=("Arial", 11, "bold"),
                wraplength=580,
                pady=6
            )
            self.encrypted_file_dynamic_widgets.append(card)

            content_label = card.winfo_children()[0]
            content_label.pack_forget()
            content_label.pack(side="left", fill="x", expand=True, padx=(0, 14))

            action_frame = tk.Frame(card, bg="white")
            action_frame.pack(side="right")

            self.create_large_action_button(
                action_frame,
                "Delete",
                lambda f=file_path: self.remove_encrypted_decrypted_file(f),
                width=9
            ).pack(side="right", padx=(10, 0))

            self.create_large_action_button(
                action_frame,
                "Export",
                lambda f=file_path: self.export_encrypted_decrypted_file(f),
                width=9
            ).pack(side="right")

    def export_encrypted_decrypted_file(self, file_path):
        if not self.ask_yes_no(
            "Export File",
            f"Would you like to export this file?\n\n{os.path.basename(file_path)}"
        ):
            return

        try:
            export_path = os.path.join(EXPORT_DIR, os.path.basename(file_path))
            shutil.copy2(file_path, export_path)
            messagebox.showinfo("Exported", f"File exported to:\n{export_path}")
            self.show_encrypted_decrypted_files()
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def remove_encrypted_decrypted_file(self, file_path):
        if not self.ask_yes_no(
            "Delete File",
            f"Would you like to delete this file?\n\n{os.path.basename(file_path)}"
        ):
            return

        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            messagebox.showinfo("Removed", "The selected file has been deleted.")
            self.refresh_encrypted_decrypted_files()
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = NonRepudiationApp(root)
    root.mainloop()
