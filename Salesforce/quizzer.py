"""
quizzer.py: Creates a quiz and allows user input to answer quiz questions
"""


import sys
import json
import random
import itertools 
import textwrap


class String:
    """
    Holds variable string messages because I'm too lazy to change each string
    """
    question = "\nQ: {}"
    invalid = "Invalid input: expected {}\n"
    choice = "{}. {}"
    answer = "\rAnswer: "
    early_exit = "Early Exit"


def get_answer():
    """
    User input that allows early exit on ctrl-C
    """
    error = False
    try:
        i = input('\r'+String.answer)
    except KeyboardInterrupt:
        error = True
        exit(String.early_exit)
    else:
        if i == '\x04': # ^D pressed
            error = True
    finally:
        if error:
            exit(String.early_exit)
        return i

class Question:
    """
    Base class for each of the unique question types
    """
    immediate_answer = False
    questions = set()
    
    @classmethod
    def options(cls, immediate_answer=False):
        if immediate_answer:
            cls.immediate_answer = immediate_answer
    
    @staticmethod
    def grade():
        """
        Returns number of correct answers out of total questions
        """
        return sum(int(q.check()) for q in Question.questions)
    
    def __init__(self, question, answer, qtype, choices):
        """
        Holds all variables needed to complete the question
        """
        self.question = question
        self.qtype = qtype
        self.choices = dict()
        if isinstance(answer, list):
            self.answer = set(answer)
        else:
            self.answer = {answer, }
        self.populate(choices)
        Question.questions.add(self)
    
    def populate(self, choices):
        """
        Maps into choices dict both choice and 1 based index to correct answer
        """
        random.shuffle(choices)
        for i, answer in enumerate(choices):
            answer_index = str(i + 1)
            self.choices[answer_index] = answer
            # self.choices[answer] = answer
    
    def check(self):
        """
        Determines if answer given is correct
        """
        return all(
            self.choices[a].lower() in self.answer 
                for a in self.answer_given.split()
        )
        # return self.answer.lower() == self.choices[self.answer_given].lower()

    def format_question(self):
        return String.question.format('\n   '.join(textwrap.wrap(self.question, 77)))

    def present(self):
        """
        Outputs question, choices, and user input messages in that order.
        TODO: remove the key handling to outside the class function?
        """
        # Question message
        print(self.format_question())

        # All possible choices
        for i, a in self.choices.items():
            if i is not a:
                print(String.choice.format(i, a))

        # generates whitelisted inputs from user and refreshes on bad input
        if self.qtype == "multi_choice":
            err_keys_allowed = [" ".join(c)
                for i in range(len(self.answer))
                for c in itertools.combinations([
                        str(i) for i in range(len(self.answer))
                    ], i+1)
            ]
        else:
            err_keys_allowed = list(self.choices.keys())
        
        self.answer_given = get_answer()
        while self.answer_given not in err_keys_allowed:
            print('\r' + String.invalid.format(', '.join(err_keys_allowed)), end='')
            self.answer_given = get_answer()
        
        if Question.immediate_answer:
            print("Correct" if self.check() else "Incorrect")
            if not self.check():
                for a in self.answer:
                    print(String.choice.format(0, a))


class TrueFalse(Question):
    """
    Helper class of Question class. Handles user input and display
    """
    choices = ['True', 'False']
    
    def __init__(self, question, answer, qtype="true_false", choices=None):
        """
        Initialization to make it easier to create T/F type questions
        """
        if not choices:
            choices = TrueFalse.choices
        
        super().__init__(
            question=question,
            answer=answer,
            qtype=qtype,
            choices=choices
        )


if __name__ == "__main__":
    Question.options(True)
    with open('QA.json') as data:
        questions = json.load(data)
    
    # print(len(questions))
    
    random.shuffle(questions)
    # every question created is saved to the internal question set
    for question in questions:
        if question['qtype'] == "true_false":
            TrueFalse(
                question=question['question'], 
                answer=question['answer']
            )
        else:
            Question(
                question=question['question'], 
                answer=question['answer'], 
                qtype=question['qtype'],
                choices=question['choices']
            )
    
    for q in Question.questions:
        q.present()
    
    print()
    print(f"Questions : {len(Question.questions)}")
    print(f"Correct   : {Question.grade()}")
    
    for q in Question.questions:
        if not q.check():
            print(q.format_question())
            print()
            print(q.format_answer())
            # print()
            # print(q.handle_input())

