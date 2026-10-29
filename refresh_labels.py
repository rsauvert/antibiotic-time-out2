"""Weekly refresh of labels.json from openFDA (FDA's public drug label API).

For each antibiotic, looks up its current label by DailyMed set ID and records:
the label's effective date, whether it carries a boxed warning (and its opening
words), and the opening words of Indications and Usage. Warning section headings
are kept as last reviewed. Every change is logged in labels.json -> "changes".
No API key is needed at this volume.
"""
import json, urllib.request, urllib.parse, datetime, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATH = ROOT / "labels.json"
API = "https://api.fda.gov/drug/label.json?search=set_id:%22{}%22&limit=1"

def first_words(text, n=110):
    text = " ".join(text.split())
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0]

def pretty(yyyymmdd):
    try:
        return datetime.datetime.strptime(yyyymmdd, "%Y%m%d").strftime("%B %-d, %Y")
    except Exception:
        return yyyymmdd

def fetch(setid):
    with urllib.request.urlopen(API.format(urllib.parse.quote(setid)), timeout=30) as r:
        res = json.load(r).get("results") or []
    return res[0] if res else None

def main():
    data = json.loads(PATH.read_text())
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    changes = []
    for drug, lab in data["labels"].items():
        try:
            rec = fetch(lab["setid"])
        except Exception as e:
            changes.append(f"{drug}: label could not be reached ({e.__class__.__name__})")
            continue
        if not rec:
            changes.append(f"{drug}: no openFDA record for set ID {lab['setid']}")
            continue
        updated = pretty(rec.get("effective_time", ""))
        boxed_text = " ".join(rec.get("boxed_warning", []))
        boxed = bool(boxed_text.strip())
        ind = " ".join(rec.get("indications_and_usage", []))
        notes = []
        if updated and updated != lab.get("updated"):
            notes.append(f"label date {lab.get('updated')} -> {updated}")
            lab["updated"] = updated
        if boxed != lab.get("boxed"):
            notes.append("boxed warning " + ("ADDED" if boxed else "removed"))
            lab["boxed"] = boxed
        if boxed:
            lab["boxedQuote"] = first_words(boxed_text.replace("WARNING:", "").strip())
        if ind and not lab.get("indicationQuote"):
            lab["indicationQuote"] = first_words(ind)
        lab["retrievedAt"] = now
        lab["source"] = "openFDA (DailyMed set ID)"
        if notes:
            changes.append(f"{drug}: " + "; ".join(notes) + " - review the curated card")
    data["lastRun"] = now
    entries = [{"date": now, "text": c} for c in changes] or [{"date": now, "text": "No label changes"}]
    data["changes"] = (data.get("changes", []) + entries)[-52:]
    PATH.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    print("\n".join(c["text"] for c in entries))

if __name__ == "__main__":
    sys.exit(main())
