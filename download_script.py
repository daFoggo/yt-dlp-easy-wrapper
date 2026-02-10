import json
import subprocess
import os
import sys

# --- Utilities for UI ---
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("="*60)
    print("      YT-DLP EASY WRAPPER      ")
    print("="*60)

def print_step(title):
    print(f"\n[+] {title}")

# --- Config & Setup ---
def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        return None
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_yt_dlp_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yt_dlp_exe = os.path.join(current_dir, "yt-dlp.exe")
    return yt_dlp_exe if os.path.exists(yt_dlp_exe) else "yt-dlp"

def ensure_download_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# --- Interactions ---
def get_user_choice(options, title="Select Option"):
    print(f"\n--- {title} ---")
    for i, opt in enumerate(options):
        print(f" {i + 1}. {opt['name']}")
    
    while True:
        choice = input(f"\n>> Select (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print("Invalid selection. Try again.")

def get_multi_choice(options, filter_type=None):
    # Filter options based on type compatibility
    valid_options = []
    for opt in options:
        # If no compatible_types field, assume compatible with all
        compat = opt.get('compatible_types', ['video', 'audio'])
        if filter_type and filter_type in compat:
            valid_options.append(opt)
        elif not filter_type: # Fallback
            valid_options.append(opt)

    if not valid_options:
        return []

    print(f"\n--- Select Additional Features (Comma separated, e.g. 1,2) ---")
    print(" 0. None (Default)")
    
    # Map display index to original valid_option index
    for i, opt in enumerate(valid_options):
        print(f" {i + 1}. {opt['name']}")
    print(f" A. All of the above")
    
    choice = input("\n>> Select features: ").strip().lower()
    
    selected_args = []
    
    if choice == '0' or choice == '':
        return []
    
    if choice == 'a':
        for opt in valid_options:
            selected_args.extend(opt['args'])
        return selected_args

    try:
        indices = [int(x.strip()) for x in choice.split(',')]
        for idx in indices:
            if 1 <= idx <= len(valid_options):
                selected_args.extend(valid_options[idx-1]['args'])
    except ValueError:
        print("Invalid input ignored.")
        
    return selected_args

# --- Main Logic ---
def main():
    config = load_config()
    if not config:
        print("Error: config.json missing.")
        return

    settings = config.get("settings", {})
    output_tmpl = settings.get("output_template", "%(title)s.%(ext)s")
    dl_dir = settings.get("download_dir", "downloads")
    ffmpeg_loc = settings.get("ffmpeg_location")

    ensure_download_dir(dl_dir)
    yt_dlp_path = get_yt_dlp_path()

    while True:
        clear_screen()
        print_header()
        
        url = input("\n>> Paste Link (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
        if not url: 
            continue

        # 1. Config Resolution
        res_config = get_user_choice(config.get("resolutions", []), "Video Quality / Format")
        res_type = res_config.get("type", "video") # Default to video if missing
        
        # 2. Config Features (Filtered)
        extra_args = get_multi_choice(config.get("features", []), filter_type=res_type)

        # 3. Execution
        cmd = [yt_dlp_path, url] + res_config["args"] + extra_args
        
        # Paths setting
        full_output_tmpl = os.path.join(dl_dir, output_tmpl)
        cmd.extend(["-o", full_output_tmpl])
        
        if ffmpeg_loc:
            cmd.extend(["--ffmpeg-location", ffmpeg_loc])

        print_step("Downloading...")
        try:
            subprocess.run(cmd, check=True)
            print("\n" + "="*60)
            print("SUCCESS! Download Complete.")
            print(f"Folder: {os.path.abspath(dl_dir)}")
            print("="*60)
            os.startfile(dl_dir)
        except subprocess.CalledProcessError as e:
            print(f"\n[!] Error: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
