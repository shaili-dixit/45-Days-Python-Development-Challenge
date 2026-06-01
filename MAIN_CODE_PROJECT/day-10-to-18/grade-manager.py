"""
Student Grade Management System with Report Card Generator
Stores student names, subjects, scores; calculates stats and generates formatted report cards.
"""

from statistics import mean, median


GRADE_THRESHOLDS = [
    (90, 'A+', 'Outstanding'),
    (80, 'A',  'Excellent'),
    (70, 'B',  'Good'),
    (60, 'C',  'Average'),
    (50, 'D',  'Below Average'),
    (0,  'F',  'Fail'),
]


def letter_grade(score):
    for threshold, grade, remark in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade, remark
    return 'F', 'Fail'


def student_stats(scores: dict):
    values = list(scores.values())
    if not values:
        return {}
    avg = round(mean(values), 2)
    grade, remark = letter_grade(avg)
    return {
        'scores': scores,
        'average': avg,
        'highest': max(values),
        'lowest': min(values),
        'median': round(median(values), 2),
        'total': sum(values),
        'grade': grade,
        'remark': remark,
        'passed': avg >= 50,
        'best_subject': max(scores, key=scores.get),
        'weak_subject': min(scores, key=scores.get),
    }


def print_report_card(name, stats):
    line = "═" * 55
    thin = "─" * 55
    print(f"\n  {line}")
    print(f"  {'REPORT CARD':^53}")
    print(f"  {line}")
    print(f"  Student  : {name}")
    print(f"  Overall  : {stats['grade']} — {stats['remark']}")
    print(f"  Result   : {'✓ PASSED' if stats['passed'] else '✗ FAILED'}")
    print(f"  {thin}")
    print(f"  {'Subject':<25} {'Score':>7}  {'Grade':<5}  {'Remark'}")
    print(f"  {thin}")

    for subject, score in sorted(stats['scores'].items()):
        g, r = letter_grade(score)
        bar = "▓" * int(score / 10) + "░" * (10 - int(score / 10))
        print(f"  {subject:<25} {score:>7.1f}  {g:<5}  {r}")

    print(f"  {thin}")
    print(f"  {'Average':<25} {stats['average']:>7.2f}  {stats['grade']:<5}  {stats['remark']}")
    print(f"  {'Highest Score':<25} {stats['highest']:>7.1f}")
    print(f"  {'Lowest Score':<25} {stats['lowest']:>7.1f}")
    print(f"  {'Median Score':<25} {stats['median']:>7.2f}")
    print(f"  {'Total Marks':<25} {stats['total']:>7.1f}")
    print(f"  {thin}")
    print(f"  Best Subject : {stats['best_subject']}")
    print(f"  Weak Subject : {stats['weak_subject']}")
    print(f"  {line}\n")


def class_summary(students_data):
    """Print a class-wide summary table."""
    print(f"\n  {'═'*70}")
    print(f"  {'CLASS SUMMARY':^68}")
    print(f"  {'═'*70}")
    print(f"  {'Name':<22} {'Average':>8}  {'Grade':<5}  {'Best Subject':<20}  {'Status'}")
    print(f"  {'─'*70}")

    averages = []
    for name, stats in students_data.items():
        avg = stats['average']
        averages.append(avg)
        status = '✓ Pass' if stats['passed'] else '✗ Fail'
        print(f"  {name:<22} {avg:>8.2f}  {stats['grade']:<5}  {stats['best_subject']:<20}  {status}")

    print(f"  {'─'*70}")
    class_avg = round(mean(averages), 2)
    top_student = max(students_data, key=lambda n: students_data[n]['average'])
    print(f"  Class Average : {class_avg}")
    print(f"  Top Student   : {top_student} ({students_data[top_student]['average']})")
    passed = sum(1 for s in students_data.values() if s['passed'])
    print(f"  Pass Rate     : {passed}/{len(students_data)} ({passed/len(students_data)*100:.1f}%)")
    print(f"  {'═'*70}\n")


def subject_leaderboard(students_data, subjects):
    print(f"\n  Subject-wise Leaderboard:")
    for subject in subjects:
        scores = {
            name: students_data[name]['scores'].get(subject, 0)
            for name in students_data
        }
        top = sorted(scores.items(), key=lambda x: -x[1])
        print(f"\n  {subject}:")
        for rank, (name, score) in enumerate(top, 1):
            g, _ = letter_grade(score)
            print(f"    {rank}. {name:<20} {score:.1f}  ({g})")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Grade Management System v1.0           ║")
    print("╚══════════════════════════════════════════╝")

    subjects = ["Mathematics", "Science", "English", "History", "Computer Science"]

    raw_data = {
        "Alice Sharma":  [92, 88, 76, 81, 95],
        "Bob Verma":     [67, 72, 58, 65, 80],
        "Carol Singh":   [45, 50, 63, 49, 55],
        "David Kumar":   [88, 91, 85, 90, 78],
        "Eve Patel":     [73, 69, 82, 77, 88],
        "Frank Nair":    [55, 48, 60, 52, 45],
    }

    students_data = {}
    for name, marks in raw_data.items():
        scores = dict(zip(subjects, marks))
        students_data[name] = student_stats(scores)

    for name, stats in students_data.items():
        print_report_card(name, stats)

    class_summary(students_data)
    subject_leaderboard(students_data, subjects)


if __name__ == "__main__":
    main()
