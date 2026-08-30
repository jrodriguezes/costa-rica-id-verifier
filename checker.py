import os
import urllib.request
import unicodedata
import urllib.error
import json
import time

# Configuration
API_URL = "https://api.hacienda.go.cr/fe/ae"

def load_lines(filename):
    lines = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    lines.append(line)
    return lines

def normalize_name(name):
    # Convert to uppercase and replace common accents if needed
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    return " ".join(name.upper().split())

def main():
    names = load_lines("names.txt")
    ids = load_lines("ids.txt")

    if not names:
        print("No names found in names.txt")
        return
    if not ids:
        print("No IDs found in ids.txt")
        return

    normalized_target_names = [normalize_name(name) for name in names]

    # Simple headers for Hacienda
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    match_counter = 0

    print(f"Starting check for {len(ids)} IDs using the FREE Hacienda API...")
    print("This is completely free and requires no API key!")
    print("-" * 50)

    for i, person_id in enumerate(ids, 1):
        print(f"[{i}/{len(ids)}] Checking ID {person_id}...", end="\r", flush=True)
        try:
            url = f"{API_URL}?identificacion={person_id}"
            
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    
                    full_name = data.get("nombre", "")

                    if full_name:
                        normalized_full_name = normalize_name(full_name)

                        # Check if this name matches any in our list
                        matched = False
                        for target_name in normalized_target_names:
                            target_parts = target_name.split()
                            # Check if ALL parts of the target name are in the full name
                            if all(part in normalized_full_name.split() for part in target_parts):
                                matched = True
                                match_counter += 1
                                print(f"[MATCH] Pos: {i} | Match #{match_counter} | Name: {full_name} | ID: {person_id}".ljust(90))
                                break
                    else:
                        print(f"ID {person_id} found but no name attached.")
                        
        except urllib.error.HTTPError as e:
            if e.code == 404 or e.code == 400:
                print(f"ID {person_id} not found in Hacienda.")
            else:
                print(f"Error querying ID {person_id}: HTTP {e.code}")

        except Exception as e:
            print(f"Exception checking ID {person_id}: {e}")
            
        # A small delay to be polite to the free government servers
        time.sleep(1.0)
        
    print("\n" + "-" * 50)
    print(f"Total Matches Found: {match_counter}")

if __name__ == "__main__":
    main()
