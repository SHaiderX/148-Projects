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

=== Module Description ===

This file contains classes that describe a survey as well as classes that
described different types of questions that can be asked in a given survey.
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, List
from criterion import HomogeneousCriterion, InvalidAnswerError
if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """ An abstract class representing a question used in a survey

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """ Initialize a question with the text <text> """
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """
        Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        raise NotImplementedError

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """ Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion(Question):
    """ A question whose answers can be one of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _options: all the options to answer to the multiple choice question.

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    _options: List[str]

    def __init__(self, id_: int, text: str, options: List[str]) -> None:
        """
        Initialize a question with the text <text> and id <id> and
        possible answers <options>.

        === Precondition ===
        No two elements in <options> are the same string
        <options> contains at least two elements
        """
        Question.__init__(self, id_, text)
        self._options = options

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        #return ("Question: {}. \nChoices: {}").format(self.text, self._options)

        s = 'Question: {}\nChoices:'.format(self.text)
        for i in range(1, len(self._options)+1):
            s = s + "\n{}. {}".format(i, self._options[i-1])

        return s

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the possible answers to this
        question.
        """
        return answer.content in self._options

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question.
        """
        if isinstance(answer1.content, int) and answer1.content < \
                len(self._options) and isinstance(answer2.content, int) and \
                answer2.content < len(self._options):

            if self._options[answer1.content] == self._options[answer2.content]:
                return 1.0
            else:
             return 0.0

        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class NumericQuestion(Question):
    """ A question whose answer can be an integer between some
    minimum and maximum value (inclusive).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _min: the minimum value the integer answer can take
    _max: the maximum value the integer answer can take

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    _max: int
    _min: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """
        Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        === Precondition ===
        min_ < max_
        """
        Question.__init__(self, id_, text)
        self._min = min_
        self._max = max_

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return ("Question:{}\nAnswer: Any integer between {} and {} inclusive")\
            .format(self.text, self._min, self._max)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        if isinstance(answer.content, int):
            return answer.content <= self._max and answer.content >= self._min
        else:
            return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity calculated by:

        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximum
           and minimum possible answers.
        3. subtract the value from step 2 from 1.0

        Hint: this is the same calculation from the worksheet in lecture!

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        similarity = abs(answer1.content - answer2.content)
        similarity = similarity/(self._max - self._min)
        return 1.0 - similarity

class YesNoQuestion(Question):
    """ A question whose answer is either yes (represented by True) or
    no (represented by False).

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Representation Invariants ===
    text is not the empty string
    """

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return ("Question: {}\nAnswer: Yes or No").format(self.text)

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer>'s content is a boolean.
        """
        return answer.content is True or answer.content is False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return 1.0 iff <answer1>.content is equal to <answer2>.content and
        return 0.0 otherwise.

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        if answer1.content == answer2.content:
            return 1.0
        else:
            return 0.0


class CheckboxQuestion(Question):
    """ A question whose answers can be one or more of several options

    === Public Attributes ===
    id: the id of this question
    text: the text of this question

    === Private Attributes ===
    _options: all of the checkbox answers to the question

    === Representation Invariants ===
    text is not the empty string
    """

    id: int
    text: str
    _options: List[str]

    def __init__(self, id_: int, text: str, options: List[str]) -> None:
        """
        Initialize a question with the text <text> and id <id> and
        possible answers <options>.

        === Precondition ===
        No two elements in <options> are the same string
        <options> contains at least two elements
        """
        Question.__init__(self, id_, text)
        self._options = options

    def __str__(self) -> str:
        """
        Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        s = 'Question: {}\nChoices:'.format(self.text)
        for i in range(1, len(self._options)+1):
            s = s + "\n{}. {}".format(i, self._options[i-1])

        return s

    def validate_answer(self, answer: Answer) -> bool:
        """
        Return True iff <answer> is a valid answer to this question.

        An answer is valid iff its content is a non-empty list containing
        unique possible answers to this question.
        """
        if isinstance(answer.content, list):
            if len(answer.content) == 0:
                return False
            checker = []

            for ans in answer.content:
                if ans not in self._options or ans in checker:
                    return False
                else:
                    checker.append(ans)
            return True

        else:
            return False

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """
        Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer1>.content == ['c', 'b', 'd'], the strings that are common to
        both are ['c', 'b'] and the unique strings that appear in both are
        ['a', 'b', 'c', 'd'].

        === Precondition ===
        <answer1> and <answer2> are both valid answers to this question
        """
        unique = []
        similar = 0.0
        for ans1 in answer1.content:
            unique.append(ans1)
        for ans2 in answer2.content:
            if ans2 in unique:
                similar += 1.0
            else:
                unique.append(ans2)

        return similar/len(unique)


class Answer:
    """ An answer to a question used in a survey

    === Public Attributes ===
    content: an answer to a single question
    """
    content: Union[str, bool, int, List[str]]

    def __init__(self,
                 content: Union[str, bool, int, List[Union[str]]]) -> None:
        """Initialize an answer with content <content>"""
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff self.content is a valid answer to <question>"""
        return question.validate_answer(self)


class Survey:
    """
    A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    === Private Attributes ===
    _questions: a dictionary mapping each question's id to the question itself
    _criteria: a dictionary mapping a question's id to its associated criterion
    _weights: a dictionary mapping a question's id to a weight; an integer
              representing the importance of this criteria.
    _default_criterion: a criterion to use to evaluate a question if the
              question does not have an associated criterion in _criteria
    _default_weight: a weight to use to evaluate a question if the
              question does not have an associated weight in _weights

    === Representation Invariants ===
    No two questions on this survey have the same id
    Each key in _questions equals the id attribute of its value
    Each key in _criteria occurs as a key in _questions
    Each key in _weights occurs as a key in _questions
    Each value in _weights is greater than 0
    _default_weight > 0
    """

    _questions: Dict[int, Question]
    _criteria: Dict[int, Criterion]
    _weights: Dict[int, int]
    _default_criterion: Criterion
    _default_weight: int

    def __init__(self, questions: List[Question]) -> None:
        """
        Initialize a new survey that contains every question in <questions>.
        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        self._questions = {}
        self._criteria = {}
        self._weights = {}
        self._default_weight = 1
        self._default_criterion = HomogeneousCriterion()
        for q in questions:
            self._questions[q.id] = q
            self._weights[q.id] = self._default_weight
            self._criteria[q.id] = self._default_criterion

    def __len__(self) -> int:
        """ Return the number of questions in this survey """
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """
        Return True iff there is a question in this survey with the same
        id as <question>.
        """
        return question.id in self._questions

    def __str__(self) -> str:
        """
        Return a string containing the string representation of all
        questions in this survey

        You can choose the precise format of this string.
        """
        s = ''
        for q in self._questions:
            s = s + "{} \nWeight: {}\n\n".\
                format(self._questions[q].__str__(), self._weights[q])

        return s

    def get_questions(self) -> List[Question]:
        """ Return a list of all questions in this survey """
        questions = []
        for id_ in self._questions:
            questions.append(self._questions[id_])

        return questions

    def _get_criterion(self, question: Question) -> Criterion:
        """
        Return the criterion associated with <question> in this survey.

        Iff <question>.id does not appear in self._criteria, return the default
        criterion for this survey instead.

        === Precondition ===
        <question>.id occurs in this survey
        """
        return self._criteria[question.id]

    def _get_weight(self, question: Question) -> int:
        """
        Return the weight associated with <question> in this survey.

        Iff <question>.id does not appear in self._weights, return the default
        weight for this survey instead.

        === Precondition ===
        <question>.id occurs in this survey
        """
        return self._weights[question.id]

    def set_weight(self, weight: int, question: Question) -> bool:
        """
        Set the weight associated with <question> to <weight> and return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if question in self._questions.values():
            self._weights[question.id] = weight
            return True
        else:
            return False

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """
        Set the criterion associated with <question> to <criterion> and return
        True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if question.id in self._questions:
            self._criteria[question.id] = criterion
            return True
        else:
            return False

    def score_students(self, students: List[Student]) -> float:
        """
        Return a quality score for <students> calculated based on their answers
        to the questions in this survey, and the associated criterion and weight
        for each question .

        This score is determined using the following algorithm:

        1. For each question in <self>, find its associated criterion, weight,
           and <students> answers to this question. Use the score_answers method
           for this criterion to calculate a quality score. Multiply this
           quality score by the associated weight.
        2. Find the average of all quality scores from step 1.

        If an InvalidAnswerError would be raised by calling this method, or if
        there are no questions in <self>, this method should return zero.

        === Precondition ===
        All students in <students> have an answer to all questions in this
            survey
        """
        if len(self._questions) == 0:
            return 0.0

        total = []
        try:
            for id_ in self._questions:
                ans = []
                for student in students:
                    ans.append(student.get_answer(self._questions[id_]))
                t = self._get_criterion(self._questions[id_]).\
                    score_answers(self._questions[id_], ans)
                total.append(t * self._get_weight(self._questions[id_]))
        except InvalidAnswerError:
            return 0.0

        return sum(total)/len(total)

    def score_grouping(self, grouping: Grouping) -> float:
        """ Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> this score is 0.0. Otherwise, this
        score is determined using the following algorithm:

        1. For each group in <grouping>, get the score for the members of this
           group calculated based on their answers to the questions in this
           survey.
        2. Return the average of all the scores calculated in step 1.

        === Precondition ===
        All students in the groups in <grouping> have an answer to all questions
            in this survey
        """
        if len(grouping) == 0:
            return 0.0

        total = []
        for group in grouping.get_groups():
            students = group.get_members()
            total.append(Survey.score_students(self, students))

        return sum(total)/len(total)



if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper']})
