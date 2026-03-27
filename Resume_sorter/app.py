from db import supabase
from scorer import score_applicant

def get_all_applicants():
    return supabase.table("applicants").select("*").execute().data

def get_job_opening(job_opening_id):
    return supabase.table("job_openings").select("*").eq("id", job_opening_id).execute().data[0]

def get_scoring_profile(scoring_profile_id):
    return supabase.table("scoring_profiles").select("*").eq("id", scoring_profile_id).execute().data[0]

def delete_old_scores(applicant_id, job_opening_id):
    supabase.table("applicant_scores") \
        .delete() \
        .eq("applicant_id", applicant_id) \
        .eq("job_opening_id", job_opening_id) \
        .execute()

def insert_score(applicant, job, profile, result):
    supabase.table("applicant_scores").insert({
        "applicant_id": applicant["id"],
        "job_opening_id": job["id"],
        "scoring_profile_id": profile["id"],
        "total_score": result["total_score"],
        "hard_fail": result["hard_fail"],
        "score_breakdown_json": result["score_breakdown_json"],
        "explanation_json": result["explanation_json"]
    }).execute()

def score_all_applicants():
    applicants = get_all_applicants()

    if not applicants:
        return []

    ranked_results = []

    for applicant in applicants:
        job = get_job_opening(applicant["job_opening_id"])
        profile = get_scoring_profile(job["scoring_profile_id"])

        result = score_applicant(applicant, profile)

        delete_old_scores(applicant["id"], job["id"])
        insert_score(applicant, job, profile, result)

        ranked_results.append({
            "full_name": applicant["full_name"],
            "email": applicant["email"],
            "job_title": job["title"],
            "score": result["total_score"],
            "hard_fail": result["hard_fail"],
            "strengths": ", ".join(result["explanation_json"]["strengths"]),
            "gaps": ", ".join(result["explanation_json"]["gaps"])
        })

    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    return ranked_results

def main():
    ranked_results = score_all_applicants()

    if not ranked_results:
        print("No applicants found.")
        return

    print("\nFINAL RANKING")
    print("=" * 60)

    for i, candidate in enumerate(ranked_results, start=1):
        status = "❌ HARD FAIL" if candidate["hard_fail"] else "✅"

        print(f"{i}. {candidate['full_name']} — {candidate['score']} {status}")
        print(f"   Job: {candidate['job_title']}")
        print(f"   Hard Fail: {candidate['hard_fail']}")
        print(f"   Strengths: {candidate['strengths']}")
        print(f"   Gaps: {candidate['gaps']}")
        print("-" * 60)

if __name__ == "__main__":
    main()