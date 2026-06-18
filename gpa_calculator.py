GRADE_POINTS = {
    "A":  4.000,
    "A-": 3.667,
    "B+": 3.333,
    "B":  3.000,
    "B-": 2.667,
    "C+": 2.333,
    "C":  2.000,
    "F":  0.000,
}

def main():
    courses = []

    print("NYU GPA Calculator")
    print("Type 'done' when finished entering courses.\n")

    while True:
        course_code = input("Enter course code: ").strip()
        if course_code.lower() == "done":
            break

        while True:
            grade = input(f"Enter grade for {course_code}: ").strip().upper()
            if grade in GRADE_POINTS:
                break
            else:
                valid = ", ".join(GRADE_POINTS.keys())
                print(f"  Invalid grade '{grade}'. Valid grades: {valid}")

        while True:
            raw = input(f"Enter credit hours for {course_code}: ").strip()
            try:
                credits = float(raw)
                if credits > 0:
                    break
                else:
                    print("  Credit hours must be a positive number.")
            except ValueError:
                print("  Invalid input. Please enter a number (e.g. 3 or 1.5).")

        courses.append((course_code, grade, GRADE_POINTS[grade], credits))

    if not courses:
        print("\nNo courses entered.")
        return

    print("\n--- Courses ---")
    for code, grade, points, credits in courses:
        print(f"  {code}: {grade} | {credits:g} credits | quality points {points:.3f}")

    total_credits = sum(c for _, _, _, c in courses)
    gpa = sum(p * c for _, _, p, c in courses) / total_credits
    print(f"\nGPA: {gpa:.3f}")

if __name__ == "__main__":
    main()
