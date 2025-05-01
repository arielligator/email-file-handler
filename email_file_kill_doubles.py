import os

def remove_adjacent_duplicates(base_name: str) -> str:
    """
    Split the base name on hyphens and remove any token
    that is identical to the one immediately before it.
    """
    parts = base_name.split('-')
    deduped = []
    for part in parts:
        if not deduped or part != deduped[-1]:
            deduped.append(part)
    return '-'.join(deduped)

def dedupe_filenames_in_folder(folder_path: str):
    """
    Walks through folder_path and renames any file whose
    base name contains adjacent duplicate hyphen-separated tokens.
    """
    for fname in os.listdir(folder_path):
        old_path = os.path.join(folder_path, fname)
        if not os.path.isfile(old_path):
            continue

        base, ext = os.path.splitext(fname)
        new_base = remove_adjacent_duplicates(base)
        if new_base == base:
            # no change needed
            continue

        new_fname = new_base + ext
        new_path = os.path.join(folder_path, new_fname)

        # avoid clobbering an existing file
        if os.path.exists(new_path):
            print(f"⚠️  Skipping rename of {fname}: {new_fname} already exists")
            continue

        os.rename(old_path, new_path)
        print(f"Renamed:\n  {fname}\n→ {new_fname}\n")

if __name__ == "__main__":
    # <-- change this to the folder you want to clean up
    target_folder = r"C:\Users\ayashar\OneDrive - Lincoln IT\Documents\Microsoft Price Increase\Reminder Email 1"
    dedupe_filenames_in_folder(target_folder)
