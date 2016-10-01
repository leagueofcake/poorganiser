#!/usr/bin/env python3.5
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///porg.db', echo=False)
Base = declarative_base(bind=engine)

class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    text = Column(Unicode(100))
    numchoices = Column(Integer)
    preferential = Column(Boolean)
    yettovote = Column(Unicode(100))

    #SEPARATED, RELATED TABLE FOR NEW CLASS OPTION/CHOICE


    def __init__(self, text, users, choices=1, pref=False):
        self.id = None
        self.question_text = text
        self.choices = choices
        self.preferential = pref
        self.yet_to_vote = users

    def get_id(self):
        return self.id

    # TODO: Move to Poorganiser
    def get_options(self): #return options as text
        options_text = []
        for key in self.options:
            options_text.append(key)
        return self.options

    # TODO: Move to Poorganiser
    def add_option(self, option):
        if option not in self.options:
            self.options[option] = []

    # TODO: Move to Poorganiser
    def remove_option(self, option):
        if option in self.options:
            del(self.options[option])

    def get_text(self):
        return self.question_text

    def set_text(self, text):
        self.question_text = text

    # TODO: Move to Poorganiser
    def make_vote(self, user, option):
        self.options[option].append(user)
#print(self.options) #debug

    # TODO: Move to Poorganiser
    def get_result(self):
        for key in sorted(self.options, key=lambda k: len(self.options[k]), reverse = True): #sorted(self.options, key = len, reverse=False): #DEBUG PRINTING
            print (key, self.options[key], len(self.options[key]))
        ## FIX UP RETURN

    # TODO: Move to Poorganiser
    def has_voted(self, user):
        self.yet_to_vote.remove(user)
        if len(self.yet_to_vote) == 0: #everyone has voted
            self.get_result() #get the result

 #tests

def run_tests():
    test_get_text()
    test_set_text()
    test_add_option()
    test_get_options()


def test_get_text():
    q1 = Question("") # Empty case
    assert(q1.get_text() == "")

    q1 = Question(" ") # Whitespace case
    assert(q1.get_text() == " ")

    q1 = Question("Do you lickadickaday?") # normal case
    assert(q1.get_text() == "Do you lickadickaday?")


def test_set_text():
    q1 = Question("test")
    q1.set_text("Do you lickadickaday?")
    assert(q1.get_text() == "Do you lickadickaday?")
    q1.set_text(" ")
    assert(q1.get_text() == " ")
    q1.set_text("")
    assert(q1.get_text() == "")

def test_add_option():
    q1 = Question("test")
    assert(q1.get_options() == {})
    q1.add_option("Yes")
    assert(q1.get_options()["Yes"] == 0)
    q1.add_option("No")
    assert(q1.get_options()["No"] == 0)

def test_get_options():
    q1 = Question("")
    assert(q1.get_options() == {})

    q1 = Question("test")
    assert(q1.get_options() == {})


# run_tests()

q = Question("Please answer", ["Dom", "Dennis", "Jeremy"], 1, False)
q.add_option("A")
q.add_option("B")
q.add_option("C")
q.make_vote("Dom", "C")
q.has_voted("Dom")
q.make_vote("Jeremy", "B")
q.has_voted("Jeremy")
q.make_vote("Dennis", "B")
q.has_voted("Dennis")
