# e_learning_platform.py

# ==============================================================================
# ABSTRACTION: Base class for all user roles
# ==============================================================================
class User:
    def __init__(self, user_id, username, password, email, role):
        self.user_id = user_id
        self.username = username
        # Information Hiding: Password should ideally be hashed, not stored in plain text.
        # For demonstration, we'll keep it simple, but note the principle.
        self.__password = password 
        self.email = email
        self.role = role

    def login(self, username, password):
        if self.username == username and self.__password == password:
            print(f"User {self.username} logged in successfully.")
            return True
        print("Invalid credentials.")
        return False

    def logout(self):
        print(f"User {self.username} logged out.")
        return True

    def update_profile(self, new_email=None):
        if new_email:
            self.email = new_email
            print(f"Profile updated for {self.username}. New email: {self.email}")
            return True
        print("No updates provided.")
        return False

class Student(User):
    def __init__(self, user_id, username, password, email):
        super().__init__(user_id, username, password, email, "student")
        self.enrolled_courses = []
        self.completed_quizzes = {} # {quiz_id: score}
        self.certificates = []

    # Cohesion: Student class handles student-specific actions
    def enroll_course(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            print(f"Student {self.username} enrolled in course: {course.title}")
            return True
        print(f"Student {self.username} is already enrolled in: {course.title}")
        return False

    # Coupling: Interacts with Quiz object without knowing its internal logic
    def attempt_quiz(self, quiz):
        if quiz.course_id in [c.course_id for c in self.enrolled_courses]:
            print(f"Student {self.username} is attempting quiz: {quiz.quiz_id}")
            # Simulate quiz attempt and getting a score
            score = quiz.evaluate_quiz() # Quiz class handles evaluation
            self.completed_quizzes[quiz.quiz_id] = score
            print(f"Quiz {quiz.quiz_id} completed with score: {score}")
            return True
        print(f"Student {self.username} is not eligible to attempt quiz {quiz.quiz_id}.")
        return False

    def download_certificate(self, certificate):
        if certificate.student_id == self.user_id and certificate.course_id in [c.course_id for c in self.enrolled_courses]:
            self.certificates.append(certificate)
            print(f"Certificate for course {certificate.course_id} downloaded by {self.username}.")
            return True
        print(f"Cannot download certificate for {self.username}. Eligibility criteria not met.")
        return False

class Instructor(User):
    def __init__(self, user_id, username, password, email, expertise):
        super().__init__(user_id, username, password, email, "instructor")
        self.expertise = expertise
        self.created_courses = []

    # Cohesion: Instructor class handles instructor-specific actions
    def upload_course_content(self, course, content):
        if course in self.created_courses:
            course.add_content(content)
            print(f"Instructor {self.username} uploaded content to {course.title}.")
            return True
        print(f"Instructor {self.username} does not manage course {course.title}.")
        return False

    # Coupling: Creates Quiz object, but Quiz manages its own internal questions/answers
    def create_quiz(self, course, quiz_id, questions_data):
        if course in self.created_courses:
            new_quiz = Quiz(quiz_id, course.course_id, questions_data)
            course.add_quiz(new_quiz)
            print(f"Instructor {self.username} created quiz {quiz_id} for {course.title}.")
            return new_quiz
        print(f"Instructor {self.username} does not manage course {course.title}.")
        return None

    def track_student_performance(self, student, course):
        if course in self.created_courses:
            print(f"Instructor {self.username} tracking {student.username}'s performance in {course.title}.")
            # In a real system, this would retrieve data from a database
            print(f"Completed quizzes for {student.username}: {student.completed_quizzes}")
            return True
        print(f"Instructor {self.username} does not manage course {course.title}.")
        return False

class Administrator(User):
    def __init__(self, user_id, username, password, email):
        super().__init__(user_id, username, password, email, "admin")

    # Cohesion: Administrator class handles system-wide management
    def manage_users(self, platform_system, action, user_obj=None):
        if action == "add_student" and user_obj:
            platform_system.register_student(user_obj.user_id, user_obj.username, user_obj._User__password, user_obj.email)
            print(f"Admin added student {user_obj.username}.")
        elif action == "remove_student" and user_obj:
            if user_obj.user_id in platform_system.students:
                del platform_system.students[user_obj.user_id]
                print(f"Admin removed student {user_obj.username}.")
        # ... similar logic for instructors
        else:
            print("Admin user management action not recognized or user object missing.")

    def manage_courses(self, platform_system, action, course_obj=None, instructor_obj=None):
        if action == "create_course" and course_obj and instructor_obj:
            platform_system.create_course(course_obj.course_id, course_obj.title, course_obj.description, instructor_obj)
            print(f"Admin created course {course_obj.title}.")
        elif action == "delete_course" and course_obj:
            if course_obj.course_id in platform_system.courses:
                del platform_system.courses[course_obj.course_id]
                print(f"Admin deleted course {course_obj.title}.")
        else:
            print("Admin course management action not recognized or objects missing.")

# ==============================================================================
# COHESION & INFORMATION HIDING: Course content and management
# ==============================================================================
class Course:
    def __init__(self, course_id, title, description, instructor):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.instructor_id = instructor.user_id
        self.video_lectures = []
        self.quizzes = []

    def add_content(self, content):
        self.video_lectures.append(content)
        print(f"Content added to {self.title}.")
        return True

    def update_course(self, new_description):
        self.description = new_description
        print(f"Course {self.title} updated.")
        return True

    def delete_course(self):
        print(f"Course {self.title} deleted.")
        # In a real system, this would involve database deletion
        return True

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)
        print(f"Quiz {quiz.quiz_id} added to course {self.title}.")
        return True

# ==============================================================================
# COHESION & INFORMATION HIDING: Quiz logic and answers
# ==============================================================================
class Quiz:
    def __init__(self, quiz_id, course_id, questions_data):
        self.quiz_id = quiz_id
        self.course_id = course_id
        self.questions = [q['question'] for q in questions_data]
        # Information Hiding: Correct answers are hidden within the Quiz object
        self.__correct_answers = {q['question']: q['answer'] for q in questions_data}

    def evaluate_quiz(self):
        print(f"Evaluating quiz {self.quiz_id}...")
        # Simulate evaluation - in a real app, student answers would be compared
        score = len(self.questions) * 0.8 # Simulate 80% score for simplicity
        return score

    def get_score(self, student_id):
        # In a real app, retrieve student's specific score
        return "Score unavailable without student's submission."

# ==============================================================================
# COHESION: Certificate generation
# ==============================================================================
class Certificate:
    def __init__(self, certificate_id, student_id, course_id, issue_date):
        self.certificate_id = certificate_id
        self.student_id = student_id
        self.course_id = course_id
        self.issue_date = issue_date

    def generate_certificate(self):
        print(f"Generating certificate {self.certificate_id} for student {self.student_id} for course {self.course_id}.")
        # In a real system, this would create a PDF or digital document
        return f"Certificate URL for {self.certificate_id}"

# ==============================================================================
# MODULARITY & DECOMPOSITION: High-level system to manage all components
# ==============================================================================
class ELearningPlatform:
    def __init__(self):
        self.users = {} # Stores all users (students, instructors, admins)
        self.courses = {}
        self.quizzes = {}
        self.certificates = {}

    # Coupling: Manages users but user objects handle their own login/profile updates
    def register_user(self, user_type, user_id, username, password, email, extra_data=None):
        if user_id in self.users:
            print(f"User with ID {user_id} already exists.")
            return None
        
        if user_type == "student":
            new_user = Student(user_id, username, password, email)
        elif user_type == "instructor":
            new_user = Instructor(user_id, username, password, email, extra_data['expertise'])
        elif user_type == "admin":
            new_user = Administrator(user_id, username, password, email)
        else:
            print("Invalid user type.")
            return None
        
        self.users[user_id] = new_user
        print(f"Registered new {user_type}: {username}")
        return new_user

    def create_course(self, course_id, title, description, instructor):
        if course_id in self.courses:
            print(f"Course with ID {course_id} already exists.")
            return None
        if not isinstance(instructor, Instructor):
            print("Only an Instructor can create a course.")
            return None
        
        new_course = Course(course_id, title, description, instructor)
        self.courses[course_id] = new_course
        instructor.created_courses.append(new_course)
        print(f"Course '{title}' created by {instructor.username}.")
        return new_course

# ==============================================================================
# DEMONSTRATION OF DESIGN PRINCIPLES
# ==============================================================================
if __name__ == "__main__":
    platform = ELearningPlatform()

    print("--- 1. User Registration (Abstraction & Modularity) ---")
    admin_user = platform.register_user("admin", "adm001", "admin_user", "admin@elearn.com", "adminpass")
    inst_alice = platform.register_user("instructor", "inst001", "Alice", "alice@elearn.com", "alicelpass", {'expertise': 'Programming'})
    std_bob = platform.register_user("student", "std001", "Bob", "bob@elearn.com", "bobpass")
    std_charlie = platform.register_user("student", "std002", "Charlie", "charlie@elearn.com", "charliepass")
    print("\n")

    print("--- 2. Instructor Creating & Uploading Course (Cohesion & Coupling) ---")
    course_py = platform.create_course("c101", "Python Basics", "Learn Python from scratch", inst_alice)
    if course_py:
        inst_alice.upload_course_content(course_py, "Intro to Python Video.mp4")
        inst_alice.upload_course_content(course_py, "Python Loops.pdf")
    print("\n")

    print("--- 3. Student Enrolling & Watching (Cohesion & Coupling) ---")
    if course_py:
        std_bob.enroll_course(course_py)
        # Simulate watching content
        print(f"Student {std_bob.username} watching 'Intro to Python Video.mp4' in {course_py.title}")
    print("\n")

    print("--- 4. Instructor Creating & Student Attempting Quiz (Information Hiding & Cohesion) ---")
    quiz_data = [
        {'question': 'What is Python?', 'answer': 'A programming language'},
        {'question': 'What is a loop?', 'answer': 'A sequence of instructions repeated'}
    ]
    if course_py:
        quiz_py_basics = inst_alice.create_quiz(course_py, "q101", quiz_data)
        if quiz_py_basics:
            std_bob.attempt_quiz(quiz_py_basics)
            print(f"Bob's score for quiz {quiz_py_basics.quiz_id}: {std_bob.completed_quizzes.get(quiz_py_basics.quiz_id)}")
    print("\n")

    print("--- 5. Information Hiding Demo (Quiz Answers) ---")
    # Attempt to directly access quiz answers (should be 'hidden' from direct access)
    try:
        print(f"Attempting to access correct answers for quiz {quiz_py_basics.quiz_id}: {quiz_py_basics.__correct_answers}")
    except AttributeError as e:
        print(f"Failed to access hidden answers directly: {e}. (Demonstrates Information Hiding)")
    print("\n")

    print("--- 6. Certificate Generation (Cohesion) ---")
    if std_bob.completed_quizzes.get("q101") and course_py: # Assuming passing score
        cert_bob_py = Certificate("cert001", std_bob.user_id, course_py.course_id, "2023-10-27")
        cert_bob_py.generate_certificate()
        std_bob.download_certificate(cert_bob_py)
    print("\n")

    print("--- 7. Administrator Actions (Modularity) ---")
    # Admin manages users
    new_student_data = Student("std003", "Eve", "evepass", "eve@elearn.com") # Temp object for data transfer
    admin_user.manage_users(platform, "add_student", new_student_data)
    # Admin manages courses (e.g., could delete one)
    # admin_user.manage_courses(platform, "delete_course", course_py)
    print("\n")

    print("--- 8. Guest User (Limited Access - conceptual in this code) ---")
    # Guest User functionality is implicitly handled by not requiring login for "browsing"
    # For a simple demo, a guest can conceptually "browse" by checking course existence
    print(f"Guest browsing: Is 'Python Basics' available? {'Yes' if 'c101' in platform.courses else 'No'}")