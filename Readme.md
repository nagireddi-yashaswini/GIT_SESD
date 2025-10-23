E-Learning Platform Design Document
This document outlines the software design principles applied in developing an E-Learning Platform, covering its conceptual design, modular structure, and security considerations.

Phase 1: Conceptual Design & Applying the Principles
This is the most critical phase. Before writing any code, we thought through the design to ensure robustness and maintainability.

Step 1: Apply Abstraction (Defining Roles)
Abstraction means focusing on essential features while hiding unnecessary complexity. Here, we abstract the different users of the system into distinct roles, each with specific permissions and responsibilities.

Action: The following roles are defined for the E-Learning Platform:

Student: Can register/login, browse courses, enroll in courses, watch video lectures, attempt quizzes, view their progress, and download certificates. They cannot upload content or manage other users.

Instructor: Can register/login, upload course content, create quizzes, and track the performance of students in their courses. They cannot enroll in courses as a student or manage system users.

Administrator: Can register/login, manage all user accounts (add/remove students, instructors), and manage the entire course catalog (add/update/delete courses). Has the highest level of system access.

Guest User: Can browse courses with limited access (e.g., view course titles, descriptions, and instructors, but not access lecture content or quizzes). They cannot log in, enroll, or interact with personalized features.

Step 2: Apply Decomposition and Modularity (Subsystems)
Decomposition is breaking a large system into smaller, manageable parts. Modularity is the result, where these parts (modules) are organized logically, making the system easier to understand, develop, and maintain.

Action: The E-Learning Platform is decomposed into the following subsystems (modules):

Authentication Module: Handles all user registration, login, logout, and credential verification processes.

Course Management Module: Manages the creation, updating, and deletion of courses, including their descriptions, prerequisites, and associated instructors. It also handles course browsing and enrollment logic.

Content Management Module: Manages the storage, upload, and delivery of all course materials, such as video lectures, readings, and supplementary files.

Quiz Engine Module: Handles the creation, administration, attempt tracking, and automatic evaluation of quizzes. It stores questions and correct answers securely.

Certification Module: Manages the generation, storage, and retrieval of digital certificates upon course completion.

User Management Module: (Often integrated with Authentication for admins) Allows administrators to view, add, modify, or delete user accounts (students, instructors).

Performance Tracking Module: Gathers and displays student progress data, quiz scores, and course completion status, primarily for instructors and students themselves.

Step 3: Apply Cohesion and Coupling
High Cohesion: Each module should be highly focused on a single task. A cohesive module performs one job well.
Low Coupling: Modules should be as independent as possible. A change in one module should not require major changes in another.

Action: Here's how cohesion and coupling are justified in our design:

Justify Cohesion:

The Quiz Engine Module is highly cohesive because its sole responsibility is everything related to quizzes: creating, evaluating, and storing quiz data (questions, answers, student attempts). It does not, for example, handle user registration or course content storage.

The Certification Module is highly cohesive as it only focuses on generating and managing certificates, without dealing with course content or student enrollment specifics.

Justify Coupling:

The Course Management Module needs to know which students are enrolled in a course. Instead of directly accessing the internal enrolled_courses list of a Student object, it interacts by calling a method like student.enroll_course(course_obj). This means the Course Management Module is loosely coupled from the Student's internal data structure. If Student's internal enrollment mechanism changes, Course Management might not need to change as long as the enroll_course method's interface remains stable.

When an Instructor creates a Quiz (part of the Quiz Engine), the Instructor module doesn't need to know the internal mechanism of how the Quiz stores its questions or evaluates answers. It simply calls quiz.create_quiz(...) or quiz.evaluate_quiz(). This maintains low coupling between the instructor's actions and the quiz's internal implementation.

Step 4: Apply Information Hiding (Security)
Information Hiding means concealing the internal state and implementation details of an object, only exposing what is necessary through public interfaces. This is crucial for security, data integrity, and maintainability.

Action: Our strategy for Information Hiding and security involves:

Sensitive Data Protection:

User Passwords: Within the User class (and its subclasses like Student, Instructor, Administrator), the __password attribute (using __ prefix in Python) is treated as private. In a real application, this would store a hashed version of the password, never the plaintext. Access to verify login credentials is only via the public login() method.

Quiz Correct Answers: Within the Quiz class, the __correct_answers attribute is kept private. It can only be accessed internally by the evaluate_quiz() method. Students attempting the quiz (and even instructors after quiz creation, for security) cannot directly inspect the correct answers.

Access Control via Methods:

All sensitive data (e.g., student grades, quiz answers, private course content) is accessed or modified only through well-defined public methods (e.g., attempt_quiz(), track_student_performance(), download_certificate()).

These methods inherently contain logic to verify the user's role and permissions. For example, Instructor.track_student_performance() would first check if the requesting instructor is actually associated with the student's course. Student.download_certificate() would verify if the student has completed the course and earned the certificate. Unauthorized access attempts are denied, enforcing data security.