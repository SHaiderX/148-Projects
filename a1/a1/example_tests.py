"""CSC148 Assignment 1

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh and Jaisie Sin
"""
import course
import survey
import criterion
import grouper
import pytest
from typing import List, Set, FrozenSet


@pytest.fixture
def empty_course() -> course.Course:
    return course.Course('csc148')


@pytest.fixture
def students() -> List[course.Student]:
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette')]


@pytest.fixture
def alpha_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def greedy_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def window_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[1]]))
    grouping.add_group(grouper.Group([students_with_answers[2],
                                      students_with_answers[3]]))
    return grouping


@pytest.fixture
def questions() -> List[survey.Question]:
    return [survey.MultipleChoiceQuestion(1, 'why?', ['a', 'b']),
            survey.NumericQuestion(2, 'what?', -2, 4),
            survey.YesNoQuestion(3, 'really?'),
            survey.CheckboxQuestion(4, 'how?', ['a', 'b', 'c'])]


@pytest.fixture
def criteria(answers) -> List[criterion.Criterion]:
    return [criterion.HomogeneousCriterion(),
            criterion.HeterogeneousCriterion(),
            criterion.LonelyMemberCriterion()]


@pytest.fixture()
def weights() -> List[int]:
    return [2, 5, 7]


@pytest.fixture
def answers() -> List[List[survey.Answer]]:
    return [[survey.Answer('a'), survey.Answer('b'),
             survey.Answer('a'), survey.Answer('b')],
            [survey.Answer(0), survey.Answer(4),
             survey.Answer(-1), survey.Answer(1)],
            [survey.Answer(True), survey.Answer(False),
             survey.Answer(True), survey.Answer(True)],
            [survey.Answer(['a', 'b']), survey.Answer(['a', 'b']),
             survey.Answer(['a']), survey.Answer(['b'])]]


@pytest.fixture
def students_with_answers(students, questions, answers) -> List[course.Student]:
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def course_with_students(empty_course, students) -> course.Course:
    empty_course.enroll_students(students)
    return empty_course


@pytest.fixture
def course_with_students_with_answers(empty_course,
                                      students_with_answers) -> course.Course:
    empty_course.enroll_students(students_with_answers)
    return empty_course


@pytest.fixture
def survey_(questions, criteria, weights) -> survey.Survey:
    s = survey.Survey(questions)
    for i, question in enumerate(questions):
        if i:
            s.set_weight(weights[i-1], question)
        if len(questions)-1 != i:
            s.set_criterion(criteria[i], question)
    return s


@pytest.fixture
def group(students) -> grouper.Group:
    return grouper.Group(students)


def get_member_ids(grouping: grouper.Grouping) -> Set[FrozenSet[int]]:
    member_ids = set()
    for group in grouping.get_groups():
        ids = []
        for member in group.get_members():
            ids.append(member.id)
        member_ids.add(frozenset(ids))
    return member_ids


def compare_groupings(grouping1: grouper.Grouping,
                      grouping2: grouper.Grouping) -> None:
    assert get_member_ids(grouping1) == get_member_ids(grouping2)


class TestHomogeneousCriterion:
    def test_score_answers(self, criteria, answers, questions) -> None:
        hom_criterion = criteria[0]
        score = hom_criterion.score_answers(questions[0], answers[0])
        assert round(score, 2) == 0.33


class TestHeterogeneousCriterion:
    def test_score_answers(self, criteria, answers, questions) -> None:
        het_criterion = criteria[1]
        score = het_criterion.score_answers(questions[1], answers[1])
        assert round(score, 2) == 0.44


class TestLonelyMemberCriterion:
    def test_score_answers(self, criteria, answers, questions) -> None:
        lon_criterion = criteria[2]
        assert lon_criterion.score_answers(questions[2], answers[2]) == 0.0




class TestSurvey:
    def test___len__(self, survey_) -> None:
        assert len(survey_) == 4

    def test___contains__(self, survey_, questions) -> None:
        for question in questions:
            assert question in survey_

    def test___str__(self, survey_, questions) -> None:
        for question in questions:
            assert str(question) in str(survey_)

    def test_get_questions(self, survey_, questions) -> None:
        q_ids = set()
        for question in questions:
            q_ids.add(question.id)
        for question in survey_.get_questions():
            assert question.id in q_ids

    def test__get_criterion(self, survey_, questions, criteria) -> None:
        criteria.append(criterion.HomogeneousCriterion())
        for i, question in enumerate(questions):
            assert isinstance(survey_._get_criterion(question),
                              type(criteria[i]))

    def test__get_weight(self, survey_, questions, weights) -> None:
        weights.insert(0, 1)
        for i, question in enumerate(questions):
            assert isinstance(survey_._get_weight(question), type(weights[i]))

    def test_set_weight(self, survey_, questions) -> None:
        survey_._weights = {}
        survey_.set_weight(999, questions[0])
        assert survey_._get_weight(questions[0]) == 999

    def test_set_criterion(self, survey_, questions) -> None:
        survey_._criteria = {}
        criterion_ = criterion.HomogeneousCriterion()
        survey_.set_criterion(criterion_, questions[0])
        assert survey_._get_criterion(questions[0]) == criterion_

    def test_score_students(self, survey_, students_with_answers) -> None:
        score = survey_.score_students(students_with_answers)
        assert round(score, 2) == 1.18

    def test_score_grouping(self, survey_, greedy_grouping) -> None:
        score = survey_.score_grouping(greedy_grouping)
        assert round(score, 2) == 1.92


class TestAnswer:
    def test_is_valid(self, questions, answers) -> None:
        for i, question in enumerate(questions):
            assert answers[i][0].is_valid(question)


class TestMultipleChoiceQuestion:
    def test___str__(self, questions) -> None:
        mc = questions[0]
        assert 'why?' in str(mc)

    def test_validate_answer(self, questions, answers) -> None:
        mc = questions[0]
        assert mc.validate_answer(answers[0][0])

    def test_get_similarity(self, questions, answers) -> None:
        mc = questions[0]
        assert mc.get_similarity(*answers[0][:2]) == 0.0


class TestNumericQuestion:
    def test___str__(self, questions) -> None:
        num = questions[1]
        assert 'what?' in str(num)

    def test_validate_answer(self, questions, answers) -> None:
        num = questions[1]
        assert num.validate_answer(answers[1][0])

    def test_get_similarity(self, questions, answers) -> None:
        num = questions[1]
        similarity = num.get_similarity(*answers[1][:2])
        assert round(similarity, 2) == 0.33


class TestYesNoQuestion:
    def test___str__(self, questions) -> None:
        yn = questions[2]
        assert 'really?' in str(yn)

    def test_validate_answer(self, questions, answers) -> None:
        yn = questions[2]
        assert yn.validate_answer(answers[2][0])

    def test_get_similarity(self, questions, answers) -> None:
        yn = questions[2]
        similarity = yn.get_similarity(*answers[2][:2])
        assert round(similarity, 2) == 0.0


class TestCheckboxQuestion:
    def test___str__(self, questions) -> None:
        check = questions[3]
        assert 'how?' in str(check)

    def test_validate_answer(self, questions, answers) -> None:
        check = questions[3]
        assert check.validate_answer(answers[3][0])

    def test_get_similarity(self, questions, answers) -> None:
        check = questions[3]
        similarity = check.get_similarity(*answers[3][2:])
        assert round(similarity, 2) == 0.0


if __name__ == '__main__':
    pytest.main(['example_tests.py'])
