from import_applicants import import_applicants
import app

def main():
    print("STEP 1: Importing applicants...")
    print("=" * 60)
    import_applicants()

    print("\nSTEP 2: Scoring applicants...")
    print("=" * 60)
    app.main()

if __name__ == "__main__":
    main()