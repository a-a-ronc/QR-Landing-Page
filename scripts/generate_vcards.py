#!/usr/bin/env python3
import os

# === CONFIG ===
NETLIFY_BASE = "https://intralog-contact-card.netlify.app"
PHOTO_DIR    = "assets/photos"
LOGO_FILE    = "intralog-logo.jpg"
VCARDS_DIR   = "vcards"

staff = [
    {
        "first": "Aaron",
        "last":  "Cendejas",
        "title": "Sr. Systems Engineer",
        "tel":   "+1-385-500-3952",
        "email": "aaron@intralog.io",
        "url":   "https://www.linkedin.com/in/aaron-cendejas-577b67223/",
    },
    {
        "first": "Michael",
        "last":  "Schulte",
        "title": "Partner",
        "tel":   "+1-385-500-3956",
        "email": "michael@intralog.io",
        "url":   "https://www.linkedin.com/in/michaeldschulte/",
    },
    {
        "first": "Bryson",
        "last":  "Westover",
        "title": "Partner",
        "tel":   "+1-385-500-3959",
        "email": "bryson@intralog.io",
        "url":   "https://www.linkedin.com/in/brysonwestover/",
    },
    {
        "first": "Mark",
        "last":  "Westover",
        "title": "President",
        "tel":   "+1-385-500-3950",
        "email": "mark@intralog.io",
        "url":   "https://www.linkedin.com/in/markcwestover/",
    },
    {
        "first": "Indigo",
        "last":  "Allen",
        "title": "Sr. Sales Associate",
        "tel":   "+1-385-500-3957",
        "email": "indigo@intralog.io",
        "url":   "https://www.linkedin.com/in/indigo-allen-98799b114/",
    }

]

os.makedirs(VCARDS_DIR, exist_ok=True)
shared_photo_url = f"{NETLIFY_BASE}/{PHOTO_DIR}/{LOGO_FILE}"

for p in staff:
    person   = f"{p['first']}-{p['last']}"
    vcf_path = os.path.join(VCARDS_DIR, f"{person}.vcf")

    with open(vcf_path, "w", newline="\r\n") as f:
        f.write("BEGIN:VCARD\n")
        f.write("VERSION:3.0\n")
        f.write(f"N:{p['last']};{p['first']};;;\n")
        f.write(f"FN:{p['first']} {p['last']}\n")
        f.write("ORG:Intralog\n")
        f.write(f"TITLE:{p['title']}\n")
        f.write(f"TEL;TYPE=CELL,VOICE:{p['tel']}\n")
        f.write(f"EMAIL;TYPE=WORK:{p['email']}\n")
        f.write(f"URL:{p['url']}\n")
        f.write(
            "ADR;TYPE=WORK:;;5215 Wiley Post Way Ste. 160;Salt "
            "Lake City;UT;84116;USA\n"
        )
        f.write(f"PHOTO;VALUE=URI;TYPE=JPEG:{shared_photo_url}\n")
        f.write("END:VCARD\n")

    print(f"✅ Wrote {vcf_path}")

print("All vCards generated! 🎉")
