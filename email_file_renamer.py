import os
import re
import time
import extract_msg

def clean_filename(filename):
    base, ext = os.path.splitext(filename)
    # strip any trailing " (123)"
    base = re.sub(r'\s*\(\d+\)$', '', base)
    return base, ext

def extract_domain(msg_path):
    msg = extract_msg.Message(msg_path)
    try:
        to_field = msg.to or msg.header.get('To', '')
        # capture username and full domain.tld
        m = re.search(r'([\w\.-]+)@([\w\.-]+\.\w+)', to_field)
        if not m:
            return 'unknown'
        username, full_domain = m.group(1), m.group(2).lower()

        if full_domain == 'gmail.com':
            # for Gmail addresses, return the username instead
            return username.lower()
        else:
            # otherwise return only the first label of the domain
            return full_domain.split('.')[0]
    finally:
        msg.close()

def safe_rename(src, dst, retries=5, delay=1):
    for _ in range(retries):
        try:
            os.rename(src, dst)
            return True
        except PermissionError:
            time.sleep(delay)
    return False

def rename_msgs_in_folder(folder):
    for fname in os.listdir(folder):
        if not fname.lower().endswith('.msg'):
            continue

        old_path = os.path.join(folder, fname)
        base, ext = clean_filename(fname)
        domain_or_user = extract_domain(old_path)
        new_fname = f"{base}-{domain_or_user}{ext}"
        new_path  = os.path.join(folder, new_fname)

        if old_path == new_path:
            continue

        if safe_rename(old_path, new_path):
            print(f"Renamed:\n  {fname}\n→ {new_fname}\n")
        else:
            print(f"Failed to rename {fname}: still in use.")

if __name__ == "__main__":
    folder = r"C:\Users\ayashar\OneDrive - Lincoln IT\Documents\Microsoft Price Increase\Reminder Email 3"
    rename_msgs_in_folder(folder)
