import tkinter as tk
from tkinter import messagebox
import json

# ---------- Load the data ----------
with open("data.json") as f:
    data = json.load(f)

questions = data["question"]
options = data["options"]
answers = data["answer"]


def get_correct_text(q_no):
    """Return the correct answer as text.
    Works if the JSON stores the text, or a number (1-based) pointing to the option."""
    ans = answers[q_no]
    if isinstance(ans, int):
        return options[q_no][ans - 1]
    return ans


# ---------- Main window ----------
root = tk.Tk()
root.title("Quiz App")
root.geometry("700x450")

q_no = 0          # current question number
score = 0
selected = tk.StringVar(value="")   # holds the option the user picked

question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=650, justify="left")
question_label.pack(pady=20)

# Four radio buttons for the options
radio_buttons = []
for _ in range(4):
    rb = tk.Radiobutton(root, text="", variable=selected, value="", font=("Arial", 13))
    rb.pack(anchor="w", padx=40, pady=5)
    radio_buttons.append(rb)

feedback_label = tk.Label(root, text="", font=("Arial", 12))
feedback_label.pack(pady=10)


def show_question():
    """Put the current question and its options on the screen."""
    selected.set("")
    feedback_label.config(text="")
    question_label.config(text=f"Q{q_no + 1}. {questions[q_no]}")
    for i, rb in enumerate(radio_buttons):
        rb.config(text=options[q_no][i], value=options[q_no][i])


def check_answer():
    """Check the chosen option, show feedback, then move on."""
    global q_no, score

    if selected.get() == "":
        messagebox.showwarning("Warning", "Please select an option first.")
        return

    correct = get_correct_text(q_no)
    if selected.get() == correct:
        score += 1
        messagebox.showinfo("Result", "Correct!")
    else:
        messagebox.showinfo("Result", f"Wrong! The correct answer is: {correct}")

    q_no += 1
    if q_no < len(questions):
        show_question()
    else:
        messagebox.showinfo("Quiz Finished", f"Your score: {score} / {len(questions)}")
        root.destroy()


next_button = tk.Button(root, text="Submit", font=("Arial", 13), command=check_answer)
next_button.pack(pady=20)

show_question()
root.mainloop()