import os

def group_files_by_suffix(folder_path):
    # 1) Build a mapping: suffix -> list of file names
    suffix_map = {}
    for fname in os.listdir(folder_path):
        full = os.path.join(folder_path, fname)
        if not os.path.isfile(full):
            continue

        base, ext = os.path.splitext(fname)
        if '-' not in base:
            continue  # no hyphen: skip

        # suffix is everything after the last hyphen
        suffix = base.rsplit('-', 1)[-1]
        suffix_map.setdefault(suffix, []).append(fname)

    # 2) For each suffix group, create folder & move files
    for suffix, files in suffix_map.items():
        if len(files) < 2:
            continue  # only group if 2+ files share this suffix

        target_dir = os.path.join(folder_path, suffix)
        os.makedirs(target_dir, exist_ok=True)

        for fname in files:
            src = os.path.join(folder_path, fname)
            dst = os.path.join(target_dir, fname)
            # rename will move across directories on the same drive
            os.rename(src, dst)
            print(f"Moved {fname} → {suffix}{os.sep}")

if __name__ == "__main__":
    # ← change this to the folder you want to organize
    folder = r"C:\Users\ayashar\OneDrive - Lincoln IT\Documents\Microsoft Price Increase\Reminder Emails"
    group_files_by_suffix(folder)
