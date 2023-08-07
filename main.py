import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import random

# List of programs
programs = [
    "Bachelor of Science, Computer Science",
    "Bachelor of Science, Cybersecurity and Information Assurance",
    "Bachelor of Science, Data Analytics",
    "Bachelor of Science, Network Engineering and Security",
    "Bachelor of Science, Software Engineering",
    "Bachelor of Science, Cloud Computing",
    "Bachelor of Science, Information Technology",
    "Master of Science, Cybersecurity and Information Assurance",
    "Master of Science, Data Analytics",
    "Master of Science, Information Technology Management"
]

def get_recommendations(user_scores, student_status):
    # Calculate the match score for each program based on user scores
    match_scores = {}
    for program, scores in user_scores.items():
        total_score = sum(score.get() for score in scores.values())
        match_scores[program] = total_score

    # Filter programs based on student status
    if student_status == "Undergraduate":
        filtered_programs = [program for program in match_scores if "Master of Science" not in program]
    elif student_status == "Graduate":
        filtered_programs = [program for program in match_scores if "Master of Science" in program]
    else:
        raise ValueError("Invalid student status.")

    # Sort the filtered programs based on match scores in descending order
    sorted_programs = sorted(filtered_programs, key=lambda x: match_scores[x], reverse=True)

    # Create a list of recommended programs along with their percentage fit
    recommended_programs_with_percentage = []
    for program in sorted_programs:
        # Calculate the highest possible score for the program
        highest_possible_score = (len(user_scores[program]) * 5) - len(user_scores[program])
        # Calculate the adjusted total score
        adjusted_total_score = match_scores[program] - len(user_scores[program])
        # Calculate the percentage fit
        percentage_fit = round((adjusted_total_score / highest_possible_score) * 100) if highest_possible_score else 0
        recommended_programs_with_percentage.append((program, percentage_fit))

    return recommended_programs_with_percentage

def show_recommendations(user_scores, student_status, container):
    recommended_programs_with_percentage = get_recommendations(user_scores, student_status)

    for widget in container.winfo_children():
        widget.destroy()

    for rank, (program, percentage_fit) in enumerate(recommended_programs_with_percentage, start=1):
        program_label = ttk.Label(container, text=f"{rank}. {program} - {int(percentage_fit)}% fit")
        program_label.pack(pady=5)

        # Create a canvas for custom progress bar
        canvas = tk.Canvas(container, width=300, height=20)
        canvas.pack(pady=5)

        # Calculate the width of the progress bar, ensuring a minimum width of 5
        progress_bar_width = max(percentage_fit * 3, 5)

        if percentage_fit == 0:
            canvas.create_rectangle(0, 0, progress_bar_width, 20, fill="red", outline="red")
        else:
            if percentage_fit <= 50:
                red_part = 255
                green_part = (percentage_fit * 5.1)
            else:
                red_part = 255 - ((percentage_fit - 50) * 5.1)
                green_part = 255

            gradient_color = f'#{int(red_part):02x}{int(green_part):02x}00'
            canvas.create_rectangle(0, 0, progress_bar_width, 20, fill=gradient_color, outline=gradient_color)

# Create a centered label with padding
def centered_label(parent, text, font=("Helvetica", 12), wraplength=None):
    label = ttk.Label(parent, text=text, font=font, wraplength=wraplength)
    return label

# Call the survey function to display the GUI and conduct the survey
def conduct_survey():
    user_scores = {}
    flattened_questions = []
    root = tk.Tk()
    root.title("Degree Program Interest Survey")
    root.geometry("800x600")
    root.resizable(False, False)

    # Custom styles
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TFrame", background="#f0f0f0")
    style.configure("TLabel", background="#f0f0f0")
    style.configure("TRadiobutton", background="#f0f0f0")

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg="#f0f0f0")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create a frame to contain the content
    content_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=content_frame, anchor=tk.CENTER)

    # Center the content frame within the root window
    content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # Stdent status selection
    student_status_var = tk.StringVar(value="Undergraduate")  # Default to Undergraduate
    status_frame = ttk.Frame(content_frame)
    status_frame.pack()

    # Title text above the label
    student_status_title_label = ttk.Label(status_frame, text="Welcome to Cooper's WGU COIT Program Recommender!", font=("Helvetica", 18, "bold"))
    student_status_title_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Label for the buttons (using the centered_label function)
    status_label = centered_label(status_frame, "Please select your student status to begin the survey:")
    status_label.grid(row=1, column=0, columnspan=2, pady=10) 

    # Student status selection buttons
    ttk.Radiobutton(status_frame, text="Undergraduate", variable=student_status_var, value="Undergraduate").grid(row=2, column=0, padx=5, pady=10, sticky="e")
    ttk.Radiobutton(status_frame, text="Graduate", variable=student_status_var, value="Graduate").grid(row=2, column=1, padx=5, pady=10, sticky="w")

    program_questions = {
        "Bachelor of Science, Computer Science": [
            "I am intrigued by the inner workings of computers and algorithms.",
            "I am enthusiastic about solving complex problems using programming.",
            "I am drawn to the idea of designing efficient computational systems.",
            "I am inquisitive and methodical, driven by the desire to uncover the mechanics behind digital systems.",
            "I am tenacious and analytical, finding joy in solving complex puzzles and logical challenges."
        ],
        "Bachelor of Science, Cybersecurity and Information Assurance": [
            "I am interested in protecting digital information from unauthorized access.",
            "I am passionate about understanding and thwarting cyber threats.",
            "I am committed to maintaining the integrity and confidentiality of digital data.",
            "I am vigilant and detail-oriented, committed to maintaining the integrity of confidential systems.",
            "I value trust and discretion, ensuring safety in every online interaction."
        ],
        "Bachelor of Science, Data Analytics": [
            "I am fascinated by the power of data to reveal insights and drive decisions.",
            "I am eager to apply statistical techniques to interpret large data sets.",
            "I am inclined towards transforming raw data into meaningful information.",
            "I am curious and precise, with a knack for finding meaning in abstract information.",
            "I prioritize clarity and insight, striving to turn raw numbers into actionable knowledge."
        ],
        "Bachelor of Science, Network Engineering and Security": [
            "I am keen on designing and managing secure computer networks.",
            "I am attracted to the complexity of ensuring seamless communication between devices.",
            "I am determined to build resilient network infrastructures.",
            "I am resourceful and adaptive, thriving on the ever-changing landscape of interconnected systems.",
            "I am systematic and vigilant, specifically ensuring the reliability and integrity of connections across various platforms."
        ],
        "Bachelor of Science, Software Engineering": [
            "I am excited about creating high-quality software that meets user needs.",
            "I am motivated by the challenge of developing and maintaining robust software systems.",
            "I am devoted to applying engineering principles to software development.",
            "I am creative and resilient, driven to find unique solutions to intricate challenges.",
            "I am methodical and attentive, dedicated to building flawless digital tools."
        ],
        "Bachelor of Science, Cloud Computing": [
            "I am drawn to the potential of cloud platforms in hosting and managing services.",
            "I am curious about optimizing resource usage in distributed environments.",
            "I am interested in exploring the scalability and flexibility of cloud solutions.",
            "I am proactive and visionary, eager to explore the horizons of scalable online solutions.",
            "I am adaptable and forward-thinking, staying ahead of shifts in virtual infrastructure."
        ],
        "Bachelor of Science, Information Technology": [
            "I am enthusiastic about integrating technology to support organizational goals.",
            "I am inclined to understand how technology interfaces with business processes.",
            "I am focused on leveraging technology to solve real-world challenges.",
            "I am pragmatic and solution-oriented, making technology serve people's unique needs.",
            "I am a mediator, bridging the gap between technical complexity and everyday use."
        ],
        "Master of Science, Cybersecurity and Information Assurance": [
            "I am committed to advancing my knowledge in cybersecurity and risk management.",
            "I am interested in the strategic aspects of information assurance in organizations.",
            "I am dedicated to contributing to the field of cybersecurity through research and practice.",
            "I am committed to principles, deepening my expertise to ensure online safety and privacy.",
            "I prioritize proactive thinking, always ready to defend against unseen threats."
        ],
        "Master of Science, Data Analytics": [
            "I am passionate about diving deeper into data-driven decision-making processes.",
            "I am eager to explore advanced techniques in machine learning and data mining.",
            "I am focused on uncovering hidden patterns in complex data sets.",
            "I am investigative and discerning, driven to make sense of multifaceted information.",
            "I am relentless and insightful, digging deep to reveal hidden truths in the data."
        ],
        "Master of Science, Information Technology Management": [
            "I am interested in leading technology projects and aligning IT with business strategy.",
            "I am inclined towards understanding the managerial aspects of information technology.",
            "I am driven to enhance my leadership skills in managing technology and innovation.",
            "I have a leadership mindset, aligning technological innovation with organizational goals.",
            "I am adept at bridging diverse teams, ensuring seamless collaboration across different domains."
        ]
    }

    likert_labels = {
        1: "Strongly Disagree",
        2: "Disagree",
        3: "Neutral",
        4: "Agree",
        5: "Strongly Agree"
    }

    current_question_index = 0

    programs = list(program_questions.keys())
    random.shuffle(programs)
    current_program_index = 0
    current_question_index = 0

    def get_flattened_questions(student_status):
        # Get the filtered programs based on student status
        if student_status == "Undergraduate":
            filtered_programs = [program for program in programs if "Master of Science" not in program]
        elif student_status == "Graduate":
            filtered_programs = [program for program in programs if "Master of Science" in program]
        else:
            raise ValueError("Invalid student status.")

        # Flatten questions for the filtered programs
        flattened_questions = []
        for program in filtered_programs:
            for question in program_questions[program]:
                flattened_questions.append((program, question))

        return flattened_questions

    def start_survey():
        nonlocal flattened_questions
        flattened_questions = get_flattened_questions(student_status_var.get())
        random.shuffle(flattened_questions)
        show_question()

    def show_question():
        nonlocal current_question_index

        # Get the current program and question
        program, question = flattened_questions[current_question_index]

        for widget in content_frame.winfo_children():
            widget.destroy()

        question_label = centered_label(content_frame, f"{question}", font=("Helvetica", 14, "bold"), wraplength=800)
        question_label.pack(pady=10)  # Use pack to place the label
        question_label.config(background="#e0e0e0")

        question_var = tk.IntVar(value=0)  # Initialize with 0

        likert_frame = ttk.Frame(content_frame)
        likert_frame.pack(pady=10)

        for score, label in likert_labels.items():
            rb = ttk.Radiobutton(likert_frame, text=label, variable=question_var, value=score)
            rb.grid(row=0, column=score - 1, padx=10)

        user_scores.setdefault(program, {})
        user_scores[program][question] = question_var

        navigation_frame = ttk.Frame(content_frame)
        navigation_frame.pack(pady=10)

        if current_question_index > 0:
            back_button = ttk.Button(navigation_frame, text="Back", command=prev_question)
            back_button.pack(side="left")

        next_button = ttk.Button(navigation_frame, text="Next Question", command=next_question)
        next_button.pack(side="right")
        next_button.config(state=tk.DISABLED)  # Disable the button initially

        def enable_next_button(*args):
            next_button.config(state=tk.NORMAL)

        # Enable the Next button once a selection has been made
        question_var.trace_add("write", enable_next_button)

    def prev_question():
        nonlocal current_question_index

        if current_question_index > 0:
            current_question_index -= 1
            show_question()

    def next_question():
        nonlocal current_question_index

        # Get the current program and question
        program, question = flattened_questions[current_question_index]

        # Check if an option has or has not been selected
        if user_scores[program][question].get() == 0:
            centered_label(content_frame, "Please select an answer.", font=("Helvetica", 10, "bold"), fg="red")
            return

        current_question_index += 1

        if current_question_index >= len(flattened_questions):
            show_survey_completed()
            return

        show_question()

    def show_survey_completed():
        for widget in content_frame.winfo_children():
            widget.destroy()
        centered_label(content_frame, "Survey Completed!", font=("Helvetica", 16, "bold"))
        show_recommendations(user_scores, student_status_var.get(), canvas)

    ttk.Button(content_frame, text="Start Survey", command=start_survey).pack() # Call start_survey when button is clicked

    result_label = ttk.Label(content_frame, text="", font=("Helvetica", 12))
    result_label.pack()

    root.mainloop()
    
# Call the survey function to display the GUI and conduct the survey
conduct_survey()