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
import json
from typing import Dict, Any
import grouper
import course
import criterion
import survey


def _load_criterion(data: Dict[str, Any]) -> criterion.Criterion:
    """ Return a criterion created using the information in <data> """
    args = data.get('args', [])
    criterion_ = getattr(criterion, data['class'])(*args)
    return criterion_


def load_survey(data: Dict[str, Any]) -> survey.Survey:
    """Return a survey created using the information in <data>"""
    questions = {}
    criteria = {}
    weights = {}
    for q_data in data['questions']:
        args = q_data['question'].get('args', [])
        question = getattr(survey, q_data['question']['class'])(*args)
        questions[question.id] = question
        weight = q_data.get('weight')
        crit_data = q_data.get('criterion')
        if crit_data is not None:
            criteria[question.id] = _load_criterion(crit_data)
        if weight is not None:
            weights[question.id] = weight

    survey_ = survey.Survey(list(questions.values()))
    for id_, criterion_ in criteria.items():
        survey_.set_criterion(criterion_, questions[id_])
    for id_, weight in weights.items():
        survey_.set_criterion(questions[id_], weight)

    return survey_


def load_course(data: Dict[str, Any]) -> course.Course:
    """Return a course created using the information in <data>"""
    course_name = data['name']
    course_ = course.Course(course_name)
    students = [course.Student(s_data['id'], s_data['name'])
                for s_data in data['students']]
    course_.enroll_students(students)
    return course_


def load_data(json_filename: str) -> Dict[str, Any]:
    """Return data extracted from <json_filename> which is a json file"""
    with open(json_filename) as f:
        data = json.load(f)
    return data


def answer_questions(survey_: survey.Survey,
                     course_: course.Course,
                     data: Dict[str, Any]) -> None:
    """
    Answer the questions in <survey_> by assigning answers to the
    student in <course_> accoding to the data in <data>
    """
    students = {s.id: s for s in course_.get_students()}
    questions = {q.id: q for q in survey_.get_questions()}
    for s_data in data['students']:
        student = students[s_data['id']]
        for a_data in s_data['answers']:
            question = questions[a_data['question_id']]
            answer = survey.Answer(a_data['answer'])
            student.set_answer(question, answer)


if __name__ == '__main__':
    course_file = 'example_course.json'
    survey_file = 'example_survey.json'

    course_data = load_data(course_file)
    survey_data = load_data(survey_file)

    new_survey = load_survey(survey_data)
    new_course = load_course(course_data)
    answer_questions(new_survey, new_course, course_data)

    # change the two variables below to test your code with different group
    # sizes and grouper types.
    group_size = 2
    grouper_type = grouper.AlphaGrouper

    grouping = grouper_type(group_size).make_grouping(new_course, new_survey)
    score = new_survey.score_grouping(grouping)
    print(f'Grouper Type: {grouper_type.__name__}',
          f'Grouping:\n{grouping}',
          f'Score: {score}',
          sep='\n\n')
