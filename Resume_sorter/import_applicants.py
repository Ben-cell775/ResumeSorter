import csv
from db import supabase

CSV_FILE = "applicants.csv"

def applicant_exists(email):
    response = supabase.table("applicants").select("*").eq("email", email).execute()
    return len(response.data) > 0

def import_applicants(csv_file=CSV_FILE):
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        count = 0
        skipped = 0

        for row in reader:
            email = row["email"]

            if applicant_exists(email):
                skipped += 1
                continue

            payload = {
                "company_id": int(row["company_id"]),
                "job_opening_id": int(row["job_opening_id"]),
                "full_name": row["full_name"],
                "email": row["email"],
                "resume_text": row["resume_text"]
            }

            supabase.table("applicants").insert(payload).execute()
            count += 1

        return {
            "imported": count,
            "skipped": skipped
        }

if __name__ == "__main__":
    result = import_applicants()
    print(result)