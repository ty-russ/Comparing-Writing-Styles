import os
import re
import html
import pandas as pd

# ---------------------------------------------------
# Helper: extract first match of a regex or return ""
# ---------------------------------------------------
def get_first(pattern, text, default=""):
    m = re.search(pattern, text, flags=re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else default

# ---------------------------------------------------
# Parse a single .sgm Reuters file
# ---------------------------------------------------
def parse_reuters_sgm(path):
    with open(path, "r", errors="ignore") as f:
        raw = f.read()

    # Each <REUTERS ...> ... </REUTERS> block is one article
    blocks = re.findall(
        r"<REUTERS[^>]*>.*?</REUTERS>",
        raw,
        flags=re.DOTALL | re.IGNORECASE,
    )

    rows = []

    for b in blocks:
        # --- Basic metadata ---
        newid = get_first(r'NEWID="(\d+)"', b)
        date = get_first(r"<DATE>(.*?)</DATE>", b)

        # --- Text fields inside <TEXT> ---
        title = html.unescape(get_first(r"<TITLE>(.*?)</TITLE>", b))
        author = html.unescape(get_first(r"<AUTHOR>(.*?)</AUTHOR>", b))
        dateline = html.unescape(get_first(r"<DATELINE>(.*?)</DATELINE>", b))
        body = html.unescape(get_first(r"<BODY>(.*?)</BODY>", b))

        # Some "BRIEF" items may not have <BODY>, only <TEXT>
        if not body:
            body = html.unescape(get_first(r"<TEXT[^>]*>(.*?)</TEXT>", b))

        # --- PLACES (for our region-based project) ---
        places_block = get_first(r"<PLACES>(.*?)</PLACES>", b)
        places_list = re.findall(r"<D>(.*?)</D>", places_block, flags=re.DOTALL | re.IGNORECASE)
        places = ";".join(places_list)  # e.g. "usa;uk;japan"

        # --- TOPICS (optional but useful later) ---
        topics_block = get_first(r"<TOPICS>(.*?)</TOPICS>", b)
        topics_list = re.findall(r"<D>(.*?)</D>", topics_block, flags=re.DOTALL | re.IGNORECASE)
        topics = ";".join(topics_list)

        # --- Build one clean article_text field ---
        if dateline and body:
            article_text = f"{dateline}\n\n{body}"
        else:
            # fallback: just body or title
            article_text = body or title

        # Append row
        rows.append(
            {
                "id": int(newid) if newid else None,
                "date": date,
                "article_title": title,
                "article_text": article_text,
                "author": author,
                "places": places,
                "topics": topics,
            }
        )

    return rows

# ---------------------------------------------------
# Parse all reut2-XXX.sgm files in a folder
# ---------------------------------------------------
def parse_all_sgm(data_dir, output_csv="reuters_regions.csv"):
    all_rows = []

    # Look for files like reut2-000.sgm, reut2-001.sgm, ..., reut2-021.sgm
    for fname in sorted(os.listdir(data_dir)):
        if re.match(r"reut2-\d+\.sgm$", fname):
            path = os.path.join(data_dir, fname)
            print(f"Parsing {path} ...")
            rows = parse_reuters_sgm(path)
            all_rows.extend(rows)

    # Build DataFrame and save to CSV
    df = pd.DataFrame(all_rows)
    df = df.sort_values("id")  # keep chronological order
    df.to_csv(output_csv, index=False)
    print(f"Saved {len(df)} rows to {output_csv}")
    return df

# ---------------------------------------------------
# Run as script
# ---------------------------------------------------
if __name__ == "__main__":
 
    DATA_DIR = "./reuters21578"  
    OUTPUT_CSV = "./reuters_regions.csv"

    parse_all_sgm(DATA_DIR, OUTPUT_CSV)
