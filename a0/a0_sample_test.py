"""CSC148 Assignment 0: Sample tests

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Mario Badr, Christine Murad, Diane Horton, Misha Schwartz, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Christine Murad, Diane Horton, Misha Schwartz,
Sophia Huynh and Jaisie Sin
"""
from datetime import datetime
from gym import WorkoutClass, Instructor, Gym


def test_instructor_attributes() -> None:
    """Test the public attributes of a new instructor."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.get_id() == 5
    assert instructor.name == 'Matthew'


def test_instructor_one_certificate_get_certificates() -> None:
    """Test Instructor.get_num_certificates with a single certificate."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.add_certificate('Kickboxing')
    assert instructor.get_num_certificates() == 1
    #mine
    assert not instructor.add_certificate('Kickboxing')
    assert instructor.get_num_certificates() == 1
    assert instructor.add_certificate('Kickboxinffg')
    assert instructor.get_num_certificates() == 2


def test_instructor_one_certificate_can_teach() -> None:
    """Test Instructor.can_teach with a single satisfying certificate."""
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    assert instructor.add_certificate('Lifeguard')
    assert instructor.can_teach(swimming)
    #mine
    swimmingee = WorkoutClass('Swimmingee', ['Lifeguardee'])
    assert not instructor.can_teach(swimmingee)
    assert instructor.add_certificate('Lifeguardee')
    assert instructor.can_teach(swimmingee)

def test_gym_register_one_class() -> None:
    """Test Gym.register with a single user and class."""
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert instructor.add_certificate('Lifeguard')
    assert ac.add_workout_class(swimming)
    assert not ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert not ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert not ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert not ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert ac.register(jan_28_2020_11_00, 'Benjamin', 'Swimming')
    assert not ac.register(jan_28_2020_11_00, 'Benjamin', 'Swimming')


def test_gym_offerings_at_one_class() -> None:
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert instructor.add_certificate('Lifeguard')
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert ac.offerings_at(jan_28_2020_11_00) == \
        [('Matthew', 'Swimming', '25-yard Pool')]


def test_gym_one_instructor_one_hour_pay_no_certificates() -> None:
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', [])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    t1 = datetime(2020, 1, 17, 11, 0)
    t2 = datetime(2020, 1, 29, 13, 0)
    assert ac.payroll(t1, t2, 22.0) == [(5, 'Matthew', 1, 22)]

def test_Schedule_no_cert() -> None:
    t = Gym('Test')
    in1 = Instructor(1, 'one')
    in2 = Instructor(2, 'two')
    w1 = WorkoutClass('Wone', ['WoneC'])
    w2 = WorkoutClass('Tone', ['ToneC'])
    t.add_instructor(in1)
    t.add_instructor(in2)
    t.add_workout_class(w1)
    t.add_workout_class(w2)
    t.add_room("r1", 10)
    t.add_room("r2", 10)
    sep = datetime(2019, 9, 9, 12, 0)
    assert not t.schedule_workout_class(sep, "r1", "Wone", 1)
    in1.add_certificate("WoneC")
    in1.add_certificate("ToneC")
    in2.add_certificate("WoneC")
    assert t.schedule_workout_class(sep, "r1", "Wone", 1)

    #ins/room busy:
    assert not t.schedule_workout_class(sep, "r1", "Tone", 1)
    #ins busy
    assert not t.schedule_workout_class(sep, "r2", "Tone", 1)
    #room busy
    assert not t.schedule_workout_class(sep, "r1", "Tone", 2)

    assert t.schedule_workout_class(sep, "r2", "Wone", 2)

def test_register_break() -> None:
    t = Gym('Test')
    in1 = Instructor(1, 'one')
    in2 = Instructor(2, 'two')
    w1 = WorkoutClass('Wone', ['WoneC'])
    w2 = WorkoutClass('Tone', ['ToneC'])
    t.add_instructor(in1)
    t.add_instructor(in2)
    t.add_workout_class(w1)
    t.add_workout_class(w2)
    t.add_room("r1", 2)
    t.add_room("r2", 100)
    sep = datetime(2019, 9, 9, 12, 0)
    in1.add_certificate("WoneC")
    in1.add_certificate("ToneC")
    in2.add_certificate("ToneC")
    assert t.schedule_workout_class(sep, "r1", "Wone", 1)
    assert t.schedule_workout_class(sep, "r2", "Tone", 2)

    assert t.register(sep, 'John', 'Wone')
    assert t.register(sep, 'Lawn', 'Wone')
    assert t.register(sep, 'Sean', 'Tone')
    assert not t.register(sep, 'John', 'Tone')
    assert not t.register(sep, 'Lawn', 'Tone')
    assert not t.register(sep, 'Fawn', 'Wone')

    t.add_room("r3", 2)
    t.add_room("r4", 1)
    jan = datetime(2019, 1, 1, 12, 0)
    assert t.schedule_workout_class(jan, "r3", "Tone", 1)
    assert t.schedule_workout_class(jan, "r4", "Tone", 2)
    assert t.register(jan, 'John', 'Tone')
    assert t.register(jan, 'Lawn', 'Tone')
    assert t.register(jan, 'Sean', 'Tone')
    assert not t.register(jan, 'Rando', 'Tone')

def test_offering_none() -> None:
    t = Gym('Test')
    in1 = Instructor(1, 'one')
    in2 = Instructor(2, 'two')
    w1 = WorkoutClass('Wone', ['WoneC'])
    w2 = WorkoutClass('Tone', ['ToneC'])
    t.add_instructor(in1)
    t.add_instructor(in2)
    t.add_workout_class(w1)
    t.add_workout_class(w2)
    t.add_room("r1", 2)
    t.add_room("r2", 100)
    sep = datetime(2019, 9, 9, 12, 0)
    jan = datetime(2019, 1, 1, 12, 0)
    in1.add_certificate("WoneC")
    in2.add_certificate("ToneC")
    assert t.schedule_workout_class(sep, "r1", "Wone", 1)
    assert t.schedule_workout_class(sep, "r2", "Tone", 2)

    assert t.offerings_at(jan) == []
    assert t.offerings_at(sep) == [('one', "Wone", 'r1'), ('two', 'Tone', 'r2')]

    assert t.schedule_workout_class(jan, "r2", "Tone", 2)
    assert t.offerings_at(jan) == [('two', 'Tone', 'r2')]

def test_instr_hrs_no() -> None:
    t = Gym('Test')
    in1 = Instructor(1, 'one')
    in2 = Instructor(2, 'two')
    w1 = WorkoutClass('Wone', ['WoneC'])
    w2 = WorkoutClass('Tone', ['ToneC'])
    t.add_instructor(in1)
    t.add_instructor(in2)
    t.add_workout_class(w1)
    t.add_workout_class(w2)
    t.add_room("r1", 2)
    t.add_room("r2", 100)
    sep = datetime(2019, 9, 9, 12, 0)
    jan = datetime(2019, 1, 1, 12, 0)
    feb = datetime(2019, 2, 2, 12, 0)
    in1.add_certificate("WoneC")
    in2.add_certificate("ToneC")
    assert t.schedule_workout_class(sep, "r1", "Wone", 1)
    assert t.schedule_workout_class(sep, "r2", "Tone", 2)

    assert t.instructor_hours(jan, sep) == {1:1, 2:1}
    assert t.instructor_hours(jan, feb) == {1:0, 2:0}

    assert t.schedule_workout_class(jan, "r2", "Tone", 2)
    assert t.schedule_workout_class(feb, "r2", "Tone", 2)
    assert t.instructor_hours(jan, feb) == {1:0, 2:2}
    #TODO: could do more

def test_payroll_all()-> None:
    t = Gym('Test')
    in1 = Instructor(1, 'one')
    in2 = Instructor(2, 'two')
    in3 = Instructor(3, 'three')
    w1 = WorkoutClass('Wone', ['WoneC'])
    w2 = WorkoutClass('Tone', ['ToneC'])
    t.add_instructor(in1)
    t.add_instructor(in2)
    t.add_instructor(in3)
    t.add_workout_class(w1)
    t.add_workout_class(w2)
    t.add_room("r1", 2)
    t.add_room("r2", 100)
    sep = datetime(2019, 9, 9, 12, 0)
    jan = datetime(2019, 1, 1, 12, 0)
    feb = datetime(2019, 2, 2, 12, 0)
    in1.add_certificate("WoneC")
    in1.add_certificate("ToneC")
    in2.add_certificate("ToneC")

    assert t.payroll(jan, feb, 10) == [(1, 'one', 0, 0), (2, 'two', 0, 0), (3, 'three', 0, 0)]

    assert t.schedule_workout_class(sep, "r1", "Wone", 1)
    assert t.schedule_workout_class(sep, "r2", "Tone", 2)

    assert t.payroll(jan, feb, 10) == [(1, 'one', 0, 0), (2, 'two', 0, 0), (3, 'three', 0, 0)]
    assert t.payroll(jan, sep, 10) == [(1, 'one', 1, 13.0), (2, 'two', 1, 11.5), (3, 'three', 0, 0)]

    w3 = WorkoutClass('Zone', [])
    t.add_workout_class(w3)
    assert t.schedule_workout_class(jan, "r2", "Zone", 3)
    assert t.payroll(jan, sep, 10) == [(1, 'one', 1, 13.0), (2, 'two', 1, 11.5), (3, 'three', 1, 10)]
    in0 = Instructor(0, 'Zero')
    t.add_instructor(in0)
    assert t.payroll(jan, sep, 10) == [(0, 'Zero', 0, 0), (1, 'one', 1, 13.0), (2, 'two', 1, 11.5), (3, 'three', 1, 10)]

if __name__ == '__main__':
    import pytest
    pytest.main(['a0_sample_test.py'])
