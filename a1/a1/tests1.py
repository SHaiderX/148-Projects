
import survey
import criterion
from grouper import *
from course import *

import pytest
from typing import List, Set, FrozenSet

def test_mc_str() -> None:
    MC = survey.MultipleChoiceQuestion(1, 'first letter', ['a', 'b', 'c'])
    assert 'a' in MC.__str__()
    assert 'b' in MC.__str__()
    assert 'c' in MC.__str__()

def test_MC_validate_answer() -> None:
    MC = survey.MultipleChoiceQuestion(1, 'first letter', ['a', 'b', 'c'])
    assert MC.id == 1
    assert MC.text == 'first letter'
    ans = survey.Answer('a')
    wrong = survey.Answer('d')
    assert MC.validate_answer(ans)
    assert not MC.validate_answer(wrong)

def test_MC_similarity() -> None:
    MC = survey.MultipleChoiceQuestion(1, 'first letter', ['a', 'b', 'c'])
    ans = survey.Answer('a')
    ans1 = survey.Answer('a')
    ans2 = survey.Answer('d')
    assert MC.get_similarity(ans, ans1) == 1.0
    assert MC.get_similarity(ans, ans2) == 0.0

def test_numeric_str() -> None:
    Numeric = survey.NumericQuestion(1, 'How much do you like uni?', 1, 10)
    assert Numeric.__str__() == \
           "Question:How much do you like uni?" + \
           "\nAnswer: Any integer between 1 and 10 inclusive"

def test_numeric_validate() -> None:
    Numeric = survey.NumericQuestion(1, 'How much do you like uni?', 1, 10)
    ans = survey.Answer(4)
    ans1 = survey.Answer(1)
    ans2 = survey.Answer(10)
    ans3 = survey.Answer(0)
    ans4 = survey.Answer(11)
    assert Numeric.validate_answer(ans)
    assert Numeric.validate_answer(ans1)
    assert Numeric.validate_answer(ans2)
    assert not Numeric.validate_answer(ans3)
    assert not Numeric.validate_answer(ans4)

def test_numeric_similarity() -> None:
    Numeric = survey.NumericQuestion(1, 'How much do you like uni?', 1, 10)
    ans = survey.Answer(4)
    ans1 = survey.Answer(1)
    ans2 = survey.Answer(10)
    assert Numeric.get_similarity(ans, ans) == 1.0
    assert Numeric.get_similarity(ans1, ans2) == 0.0
    assert Numeric.get_similarity(ans, ans2) == 1.0 - abs(10 - 4)/9

def test_YesNo_str() -> None:
    YN = survey.YesNoQuestion(1, "Do you like university?")
    assert YN.__str__() ==  "Question: Do you like university?" +\
        "\nAnswer: Yes or No"

def test_YesNo_Validate() -> None:
    YN = survey.YesNoQuestion(1, "Do you like university?")
    ans = survey.Answer(True)
    ans1 = survey.Answer(False)
    ans2 = survey.Answer(12)
    assert YN.validate_answer(ans)
    assert YN.validate_answer(ans1)
    assert not YN.validate_answer(ans2)

def test_YesNo_similarity() -> None:
    YN = survey.YesNoQuestion(1, "Do you like university?")
    ans = survey.Answer(True)
    ans1 = survey.Answer(False)
    ans2 = survey.Answer(True)
    assert YN.get_similarity(ans, ans1) == 0.0
    assert YN.get_similarity(ans, ans2) == 1.0

def test_checkbox_str() -> None:
    check = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    assert 'pizza' in check.__str__()
    assert 'cake' in check.__str__()
    assert 'apple' in check.__str__()

def test_checkbox_validate() -> None:
    check = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    ans = survey.Answer(['pizza'])
    ans1 = survey.Answer(['cake', 'apple'])
    ans2 = survey.Answer(['tomatoes'])
    assert check.validate_answer(ans)
    assert check.validate_answer(ans1)
    assert not check.validate_answer(ans2)

def test_checkbox_similarity() -> None:
    check = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    ans = survey.Answer(['pizza'])
    ans1 = survey.Answer(['cake', 'apple'])
    ans2 = survey.Answer(['pizza', 'cake', 'apple'])
    ans3 = survey.Answer(['cake', 'pizza', 'apple'])
    ans4 = survey.Answer(['apple', 'cake'])
    assert check.get_similarity(ans, ans) == 1.0
    assert check.get_similarity(ans, ans1) == 0.0
    assert check.get_similarity(ans1, ans2) == 2/3
    assert check.get_similarity(ans3, ans2) == 1.0
    assert check.get_similarity(ans1, ans4) == 1.0

def test_homogenous_crit_score() -> None:
    Criterion = criterion.HomogeneousCriterion()
    check = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    ans = survey.Answer(['pizza'])
    ans1 = survey.Answer(['cake', 'apple'])
    ans2 = survey.Answer(['pizza', 'cake', 'apple'])
    ans3 = survey.Answer(['cake', 'pizza', 'apple'])
    wrong = survey.Answer(['Beans'])
    ans4 = survey.Answer(['apple', 'cake'])
    assert Criterion.score_answers(check, [ans2, ans3]) == 1.0
    assert Criterion.score_answers(check, [ans]) == 1.0

    with pytest.raises(criterion.InvalidAnswerError):
        Criterion.score_answers(check, [ans2, wrong])
        Criterion.score_answers(check, [wrong])

    assert Criterion.score_answers(check, [ans1, ans]) == 0.0
    assert Criterion.score_answers(check, [ans4, ans]) == 0.0
    assert Criterion.score_answers(check, [ans1, ans, ans4]) == (1.0)/(3.0)

def test_HeterogeneousCriterion_score() -> None:
    Criterion = criterion.HeterogeneousCriterion()
    check = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    ans = survey.Answer(['pizza'])

    assert Criterion.score_answers(check, [ans]) == 0.0

def test_LonelyMemberCriterion_score() -> None:
    Criterion = criterion.LonelyMemberCriterion()
    check = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    ans = survey.Answer(['pizza'])
    ans1 = survey.Answer(['cake', 'apple'])
    ans2 = survey.Answer(['pizza', 'cake', 'apple'])
    ans3 = survey.Answer(['cake', 'pizza', 'apple'])

    assert Criterion.score_answers(check, [ans]) == 0.0
    assert Criterion.score_answers(check, [ans2, ans3]) == 1.0
    assert Criterion.score_answers(check, [ans2, ans3, ans1]) == 0.0

def test_answer_is_valid() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    a1 = survey.Answer(['cake'])
    a2 = survey.Answer(['beans'])
    a3 = survey.Answer(10)
    assert a1.is_valid(q1)
    assert not a2.is_valid(q1)
    assert not a3.is_valid(q1)

def test_survey_len() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    assert len(Survey) == 4

def test_survey_contains() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3])
    assert q1 in Survey
    assert q2 in Survey
    assert not q4 in Survey

def test_survey_str() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    for q in [q1, q2, q3, q4]:
        assert q.text in str(Survey)

def test_survey_get_question() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    assert Survey.get_questions() == [q1, q2, q3, q4]

def test_survey_get_criterion() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    assert isinstance(Survey._get_criterion(q1), criterion.HomogeneousCriterion)

def test_survey_get_weight() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    assert Survey._get_weight(q1) == 1

def test_survey_set_weight() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    q5 = survey.YesNoQuestion(6, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    assert Survey._get_weight(q3) == 1
    assert Survey.set_weight(10, q3)
    assert not Survey.set_weight(10, q5)
    assert Survey._get_weight(q3) == 10
    assert Survey._get_weight(q4) == 1

def test_survey_set_criterion() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    q5 = survey.YesNoQuestion(6, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])
    assert isinstance(Survey._get_criterion(q1), criterion.HomogeneousCriterion)
    assert Survey.set_criterion(criterion.HeterogeneousCriterion(), q1)
    assert isinstance(Survey._get_criterion(q1), criterion.HeterogeneousCriterion)
    assert not Survey.set_criterion(criterion.HeterogeneousCriterion(), q5)

def test_survey_score_students() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])

    s1 = Student(1, 'Kaido')
    s2 = Student(2, 'Griffith')
    s3 = Student(3, 'Shin')
    s4 = Student(4, 'Levi')

    a1 = survey.Answer(['cake'])
    a2 = survey.Answer('b')
    a3 = survey.Answer(2)
    a4 = survey.Answer(True)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s1.set_answer(q3, a3)
    s1.set_answer(q4, a4)

    a12 = survey.Answer(['pizza'])
    a22 = survey.Answer('a')
    a32 = survey.Answer(1)
    a42 = survey.Answer(True)
    s2.set_answer(q1, a12)
    s2.set_answer(q2, a22)
    s2.set_answer(q3, a32)
    s2.set_answer(q4, a42)

    a13 = survey.Answer(['cake', 'pizza'])
    a23 = survey.Answer('a')
    a33 = survey.Answer(3)
    a43 = survey.Answer(False)
    s3.set_answer(q1, a13)
    s3.set_answer(q2, a23)
    s3.set_answer(q3, a33)
    s3.set_answer(q4, a43)

    a1 = survey.Answer(['cake'])
    a2 = survey.Answer('b')
    a3 = survey.Answer(2)
    a4 = survey.Answer(True)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s1.set_answer(q3, a3)
    s1.set_answer(q4, a4)

    a14 = survey.Answer(['cake', 'pizza', 'apple'])
    a24 = survey.Answer('b')
    a34 = survey.Answer(1)
    a44 = survey.Answer(True)
    s4.set_answer(q1, a14)
    s4.set_answer(q2, a24)
    s4.set_answer(q3, a34)
    s4.set_answer(q4, a44)

    assert round(Survey.score_students([s1, s2, s3, s4]), 2) == 0.41

def test_score_grouping() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])

    s1 = Student(1, 'Kaido')
    s2 = Student(2, 'Griffith')

    a1 = survey.Answer(['cake'])
    a2 = survey.Answer('b')
    a3 = survey.Answer(2)
    a4 = survey.Answer(True)
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)
    s1.set_answer(q3, a3)
    s1.set_answer(q4, a4)

    a12 = survey.Answer(['pizza'])
    a22 = survey.Answer('a')
    a32 = survey.Answer(1)
    a42 = survey.Answer(2)
    s2.set_answer(q1, a12)
    s2.set_answer(q2, a22)
    s2.set_answer(q3, a32)
    s2.set_answer(q4, a42)

    assert Survey.score_students([s1, s2]) == 0.0

def test_alpha_grouper_make_grouping() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])

    s1 = Student(1, 'Aron')
    s2 = Student(2, 'Ben')
    s3 = Student(3, 'Charlie')
    s4 = Student(4, 'Zack')
    g1 = Group([s1, s2])
    g2 = Group([s3, s4])
    G = Grouping()
    G.add_group(g1)
    G.add_group(g2)

    csc = Course('148')
    csc.enroll_students([s4, s3, s2, s1])

    A = AlphaGrouper(2)
    final_group = A.make_grouping(csc, Survey)
    FG = []
    for f in final_group.get_groups():
        FG.append(f.get_members())

    FG2 = []
    for f2 in G.get_groups():
        FG2.append(f2.get_members())

    assert FG == FG2

def test_random_grouper_make_grouping_every_student_present() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    q3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
    q4 = survey.YesNoQuestion(4, 'Yes or No')
    Survey = survey.Survey([q1, q2, q3, q4])

    s1 = Student(1, 'Aron')
    s2 = Student(2, 'Ben')
    s3 = Student(3, 'Charlie')
    s4 = Student(4, 'Zack')

    csc = Course('148')
    csc.enroll_students([s4, s3, s2, s1])

    A = AlphaGrouper(2)
    final_group = A.make_grouping(csc, Survey)
    FG = []
    for f in final_group.get_groups():
        FG.append(f.get_members())

    for group in FG:
        assert len(group) == 2
        assert s1 in group or s2 in group or s3 in group

def test_greedy_grouper_make_grouping() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    Survey = survey.Survey([q1, q2])

    s1 = Student(1, 'Aron')
    s2 = Student(2, 'Ben')
    s3 = Student(3, 'Charlie')
    s4 = Student(4, 'Zack')
    g1 = Group([s1, s3])
    g2 = Group([s2, s4])
    G = Grouping()
    G.add_group(g1)
    G.add_group(g2)

    a1 = survey.Answer(['cake'])
    a2 = survey.Answer('b')
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)

    a12 = survey.Answer(['pizza'])
    a22 = survey.Answer('a')
    s2.set_answer(q1, a12)
    s2.set_answer(q2, a22)

    a13 = survey.Answer(['cake'])
    a23 = survey.Answer('b')
    s3.set_answer(q1, a13)
    s3.set_answer(q2, a23)

    a14 = survey.Answer(['pizza'])
    a24 = survey.Answer('a')
    s4.set_answer(q1, a14)
    s4.set_answer(q2, a24)

    csc = Course('148')
    csc.enroll_students([s4, s3, s2, s1])

    A = GreedyGrouper(2)
    final_group = A.make_grouping(csc, Survey)
    FG = []
    for f in final_group.get_groups():
        FG.append(f.get_members())

    FG2 = []
    for f2 in G.get_groups():
        FG2.append(f2.get_members())

    assert FG == FG2

def test_windowed_grouper_make_grouping() -> None:
    q1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
    q2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
    Survey = survey.Survey([q1, q2])

    s1 = Student(1, 'Aron')
    s2 = Student(2, 'Ben')
    s3 = Student(3, 'Charlie')
    s4 = Student(4, 'Zack')
    g1 = Group([s1, s2])
    g2 = Group([s3, s4])
    G = Grouping()
    G.add_group(g1)
    G.add_group(g2)

    a1 = survey.Answer(['cake'])
    a2 = survey.Answer('b')
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)

    a12 = survey.Answer(['cake'])
    a22 = survey.Answer('b')
    s2.set_answer(q1, a12)
    s2.set_answer(q2, a22)

    a13 = survey.Answer(['pizza'])
    a23 = survey.Answer('a')
    s3.set_answer(q1, a13)
    s3.set_answer(q2, a23)

    a14 = survey.Answer(['pizza'])
    a24 = survey.Answer('a')
    s4.set_answer(q1, a14)
    s4.set_answer(q2, a24)

    csc = Course('148')
    csc.enroll_students([s4, s3, s2, s1])

    A = WindowGrouper(2)
    final_group = A.make_grouping(csc, Survey)
    FG = []
    for f in final_group.get_groups():
        FG.append(f.get_members())

    FG2 = []
    for f2 in G.get_groups():
        FG2.append(f2.get_members())

    assert FG == FG2

s = Student(1, 'test')
q1 = survey.CheckboxQuestion(1, 'foods?', ['pizza', 'cake', 'apple'])
q2 = survey.CheckboxQuestion(1, 'foods?', ['lemon', 'bread', 'beans'])

a1 = survey.Answer(['cake'])
a2 = survey.Answer(['beans'])
a3 = survey.Answer(10)

s.set_answer(q1, a1)


def test_student_str() -> None:
    assert 'test' in str(s)


def test_student_has_answer() -> None:
    assert s.has_answer(q1)


def test_student_set_answer() -> None:
    s.set_answer(q2, a2)
    assert q2 in s.qs_
    assert s.qs_[q2] == a2


def test_student_get_answer() -> None:
    assert s.get_answer(q1) == a1


# Course Test


def test_course_enroll_students() -> None:
    c = Course('testCourse')
    s1 = Student(1, 'one')
    s2 = Student(2, 'two')
    s3 = Student(3, 'three')
    lst = [s1, s2, s3]
    c.enroll_students(lst)
    assert c.students == [s1, s2, s3]


def test_course_all_answered() -> None:
    c = Course('testCourse')
    surv = survey.Survey([q1, q2])

    s1 = Student(1, 'bad1')
    s2 = Student(2, 'bad2')
    c.enroll_students([s1, s2])

    a1 = survey.Answer(['cake'])
    a2 = survey.Answer(['lemon'])
    s1.set_answer(q1, a1)
    s1.set_answer(q2, a2)

    a12 = survey.Answer(['pizza'])
    a22 = survey.Answer(['lemon'])
    s2.set_answer(q1, a12)
    s2.set_answer(q2, a22)

    assert c.all_answered(surv)


def test_course_get_students() -> None:
    c = Course('testCourse')
    s1 = Student(1, 'bad1')
    s2 = Student(2, 'bad2')
    c.enroll_students([s1, s2])
    assert c.get_students() == tuple([s1, s2])


# Grouper Tests

# list operation tests
def test_slice_list() -> None:
    lst = [3, 4, 6, 2, 3]
    assert slice_list(lst, 2) == [[3, 4], [6, 2], [3]]


def test_windows() -> None:
    lst = [3, 4, 6, 2, 3]
    assert windows(lst, 2) == [[3, 4], [4, 6], [6, 2], [2, 3]]


# Grouper tests
# alpha grouper test
que1 = survey.CheckboxQuestion(1, 'fav foods?', ['pizza', 'cake', 'apple'])
que2 = survey.MultipleChoiceQuestion(2, 'a, b, or c', ['a', 'b', 'c'])
que3 = survey.NumericQuestion(3, '1, 2, or 3', 1, 3)
que4 = survey.YesNoQuestion(4, 'Yes or No')
sur1 = survey.Survey([que1, que2, que3, que4])

# def test_alpha_grouper() -> None:
#     c = Course('testCourse')
#     s1 = Student(1, 'apple')
#     s2 = Student(2, 'banana')
#     s3 = Student(3, 'cake')
#     s4 = Student(4, 'dank')
#     s5 = Student(5, 'eat')
#     c.enroll_students([s1, s2, s3, s4, s5])
#
#
#     g = Grouping()
#     g.add_group(Group([s1, s2]))
#     g.add_group(Group([s3, s4]))
#     g.add_group(Group([s5]))
#
#
#     grper = AlphaGrouper(2)
#
#     # assert grper.make_grouping(c, sur1) == g


# Group Tests
s1 = Student(1, 'bad1')
s2 = Student(2, 'bad2')


def test_group_len() -> None:
    g = Group([s1, s2])
    assert len(g) == 2


def test_group_contains() -> None:
    g = Group([s1, s2])
    assert s1 in g


def test_group_str() -> None:
    g = Group([s1, s2])
    assert str(g) == 'bad1, bad2, '


def test_group_get_members() -> None:
    g = Group([s1, s2])
    assert g.get_members() == [s1, s2]


# Grouping Tests
s12 = Student(1, 'bad1')
s22 = Student(2, 'bad2')
s32 = Student(3, 'bad3')
s42 = Student(4, 'bad4')
grp1 = Group([s12, s22])
grp2 = Group([s32, s42])


def test_grouping_len() -> None:
    grping = Grouping()
    grping.add_group(grp1)
    grping.add_group(grp2)
    assert len(grping) == 2


def test_grouping_str() -> None:
    grping = Grouping()
    grping.add_group(grp1)
    grping.add_group(grp2)
    assert 'bad1' in str(grping)


def test_grouping_add_group() -> None:
    grping = Grouping()
    grping.add_group(grp1)
    grping.add_group(grp2)
    s52 = Student(5, 'bad5')
    grp3 = Group([s52])
    assert grping.add_group(grp3)


def test_grouping_get_groups() -> None:
    grping = Grouping()
    grping.add_group(grp1)
    grping.add_group(grp2)
    assert grping.get_groups() == [grp1, grp2]


if __name__ == '__main__':
    pytest.main(['tests.py'])
