import matplotlib.pyplot as plt
import os

student_score_map = {}
assignment_percent_map = {}
def load_students(file_name):
    students = {}
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            studentid = line[:3]
            studentname = line[3:].strip()
            student_score_map[studentid] = 0
            students[studentname] = studentid

    return students

def load_assignments(file_name):
    assignment_point_map = {}
    assignment_id_map = {}
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            assignmentname = lines[i].strip()
            assignmentid = lines[i+1].strip()
            assignmentpoints = float(lines[i+2].strip())
            assignment_point_map[assignmentid] = assignmentpoints
            assignment_id_map[assignmentname] = assignmentid

    return (assignment_point_map, assignment_id_map)

def load_submissions(submissions_folder, assignment_point_map):
    submissions = os.listdir('data/submissions')
    for file_name in submissions:
        with open("data/submissions/" + file_name, 'r') as file:
            line = file.readlines()[0].split('|')
            studentid = line[0]
            assignmentid = line[1]
            percentscore = float(line[2])
            assignment_point = assignment_point_map[assignmentid]
            student_score_map[studentid] = student_score_map[studentid] + percentscore/100 * assignment_point
            if assignmentid not in assignment_percent_map:
                assignment_percent_map[assignmentid] = []
            assignment_percent_map[assignmentid].append(percentscore)

def student_score(id):
    return round(student_score_map[id] / 10)

def assignment_statistics(assignment_name, assignmentidmap):
    assignment_id = assignmentidmap[assignment_name]
    if assignment_id is None:
        print("Assignment not found")
        return
    assignment_scores = assignment_percent_map[assignment_id]
    print(f"Min: {int(min(assignment_scores))}%")
    print(f"Avg: {int(sum(assignment_scores)/len(assignment_scores))}%")
    print(f"Max: {int(max(assignment_scores))}%")

def assignment_graph(assignment_name, assignmentidmap):
    assignment_id = assignmentidmap[assignment_name]
    if assignment_id is None:
        print("Assignment not found")
        return
    scores = assignment_percent_map[assignment_id]
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.show()

def main():
    students = load_students('data/students.txt')
    assignments = load_assignments('data/assignments.txt')
    assignmentpointmap = assignments[0]
    assignmentidmap = assignments[1]
    load_submissions('data/submissions', assignmentpointmap)
    print('''
1. Student grade
2. Assignment statistics
3. Assignment graph''')
    choice = int(input("Enter your selection: "))
    if choice == 1:
        name = input("What is the student's name: ")
        id = students[name]
        if id is None:
            print("Student not found")
            exit()
        score = student_score(id)
        print(f"{score}%")
    elif choice == 2:
        assignment = input("What is the assignment name: ")
        assignment_statistics(assignment,assignmentidmap)

    elif choice == 3:
        assignment = input("What is the assignment name: ")
        assignment_graph(assignment, assignmentidmap)
        
if __name__ == "__main__":
    main()