import itertools
import random
import unittest

from criterion import *
from survey import *
from course import *
from grouper import *


def no_public(class_name, instance, public_attrs, public_methods):
    methods = class_name.__dict__
    attrs = instance.__dict__
    temp_methods = list(filter(lambda x: x[0] != "_", methods))
    temp_attrs = list(filter(lambda x: x[0] != "_", attrs))
    assert sorted(temp_methods) == sorted(public_methods)
    assert sorted(temp_attrs) == sorted(public_attrs)


class TestStudent(unittest.TestCase):
    def setUp(self) -> None:
        self.s1 = Student(1, "A")
        self.s2 = Student(2, "B")
        self.s3 = Student(3, "C")
        self.q1 = Question(1, "Question1")
        self.q100 = Question(100, "Question100")
        self.a1 = Answer("Answer for q1")
        self.a2 = Answer("Answer for q100")
        self.a3 = Answer("A")
        self.m3 = MultipleChoiceQuestion(3, "Multiple Choice Question 3", ["A", "B", "C", "D"])
        no_public(Student, self.s1, ["id", "name"], ["has_answer", "set_answer", "get_answer"])

    def tearDown(self) -> None:
        self.s1 = Student(1, "A")
        self.s2 = Student(2, "B")
        self.s3 = Student(3, "C")

    def test_get_answer_1(self):
        self.assertIsNone(self.s1.get_answer(self.q1), "Student doesn't have an answer for the question")

    def test_get_answer_2(self):
        self.s1.set_answer(self.q1, self.a1)
        self.assertTrue(self.s1.get_answer(self.q1) == self.a1,
                        "Student has an answer for the Question get answer does not care about the validate answer")
        self.s1.set_answer(self.q1, self.a2)
        self.assertTrue(self.s1.get_answer(self.q1) == self.a2,
                        "You should overwrite the existing answer when set is called more than once")
        self.s1.set_answer(self.q1, self.a1)
        self.assertIsNone(self.s1.get_answer(self.q100), "Student doesnt't have an answer for the question")

    def test_has_answer(self):
        self.assertFalse(self.s1.has_answer(self.q1), "Student doesnt have the answer for the question")

    def test_has_answer_2(self):
        self.s1.set_answer(self.m3, self.a3)
        self.assertTrue(self.s1.has_answer(self.m3),
                        "Student has the answer for the question and the question is valid")
        self.s1.set_answer(self.m3, self.a1)
        self.assertFalse(self.s1.has_answer(self.m3), "Student has the answer but answer is invalid")


class TestCourse(unittest.TestCase):
    def setUp(self) -> None:
        self.c1 = Course("CSC148")
        self.c2 = Course("CSC207")
        self.s1 = Student(1, "A")
        self.s2 = Student(2, "B")
        self.s3 = Student(3, "C")
        self.q1 = Question(1, "Question1")
        self.q100 = Question(100, "Question100")
        self.a1 = Answer("Answer for q1")
        self.a2 = Answer("Answer for q100")
        self.a3 = Answer("A")
        self.m3 = MultipleChoiceQuestion(3, "Multiple Choice Question 3", ["A", "B", "C", "D"])
        self.n3 = NumericQuestion(4, "Numerical Question", 1, 2)
        self.survey1 = Survey([self.m3])
        self.survey2 = Survey([self.m3, self.n3])
        no_public(Course, self.c1, ["name", "students"], ["enroll_students", "all_answered", "get_students"])

    def tearDown(self) -> None:
        self.c1 = Course("CSC148")
        self.c2 = Course("CSC207")
        self.s1 = Student(1, "A")
        self.s2 = Student(2, "B")
        self.s3 = Student(3, "C")
        self.q1 = Question(1, "Question1")
        self.q100 = Question(100, "Question100")
        self.a1 = Answer("Answer for q1")
        self.a2 = Answer("Answer for q100")
        self.a3 = Answer("A")
        self.m3 = MultipleChoiceQuestion(3, "Multiple Choice Question 3", ["A", "B", "C", "D"])
        self.n3 = NumericQuestion(4, "Numerical Question", 1, 2)
        self.survey1 = Survey([self.m3])
        self.survey2 = Survey([self.m3, self.n3])
        no_public(Course, self.c1, ["name", "students"], ["enroll_students", "all_answered", "get_students"])

    def test_enroll_students(self):
        self.c1.enroll_students([self.s1, self.s2])
        self.assertCountEqual(self.c1.students, [self.s1, self.s2], "You should add two students to the students of c1")

    def test_enroll_students_2(self):
        self.c1.enroll_students([self.s1, self.s2])
        temp = self.c1.students
        self.c1.enroll_students([self.s1, self.s3])
        self.assertListEqual(temp, self.c1.students, "You should not add any existing students")

    def test_get_students(self):
        self.assertTupleEqual(self.c1.get_students(), ())

    def test_get_students_2(self):
        self.c1.enroll_students([self.s2, self.s1, self.s3])
        self.assertTupleEqual(self.c1.get_students(), (self.s1, self.s2, self.s3))

    def test_get_students_3(self):
        students = [Student(i, str(i)) for i in range(100)]
        random.shuffle(students)
        self.c2.enroll_students(list(students))
        self.assertTupleEqual(self.c2.get_students(), tuple(sorted(students, key=lambda x: x.id)))

    def test_all_answered(self):
        self.assertTrue(self.c1.all_answered(self.survey1), "If the course has no students this should return True")
        self.c1.enroll_students([self.s1])
        self.assertTrue(self.c1.all_answered(Survey([])),
                        "If there is no question on the survey this should also return True")
        self.assertTrue(self.c2.all_answered(Survey([])),
                        "If there is no question in the survey this should also return True")

    def test_all_answered_survey_with_single_question(self):
        self.s1.set_answer(self.m3, self.a1)
        self.c1.enroll_students([self.s1])
        self.assertFalse(self.c1.all_answered(self.survey1),
                         "There is one student and he doesnot have a valid answer for the question")
        self.c1.students = []
        self.s1.set_answer(self.m3, self.a3)
        self.c1.enroll_students([self.s1])
        self.assertTrue(self.c1.all_answered(self.survey1),
                        "There is one student and he has a valid an answer for the question")
        self.c1.enroll_students([self.s2])
        self.assertFalse(self.c1.all_answered(self.survey1),
                         "There are two students but one of them does not have an answer for the survey")
        self.c1.students[-1].set_answer(self.m3, self.a1)
        self.assertFalse(self.c1.all_answered(self.survey1),
                         "There are two students but one of them does not valid answer of the question")
        self.c1.students[-1].set_answer(self.m3, self.a3)
        self.assertTrue(self.c1.all_answered(self.survey1),
                        "There are two students and both of them have validate answer of the survey")

    def test_all_answered_survey_with_multiple_questions(self):
        numerical_sol = Answer(1)
        numerical_att = Answer(3)
        self.s1.set_answer(self.m3, self.a3)
        self.c1.enroll_students([self.s1])
        self.assertFalse(self.c1.all_answered(self.survey2),
                         "There is one student but he has only answer for the survey")
        self.c1.students[-1].set_answer(self.n3, numerical_att)
        self.assertFalse(self.c1.all_answered(self.survey2),
                         "There is one student but he does not have a valid answer for the second question of survey")
        self.c1.students[-1].set_answer(self.n3, numerical_sol)
        self.assertTrue(self.c1.all_answered(self.survey2))
        self.s2.set_answer(self.m3, self.a3)
        self.c1.enroll_students([self.s2])
        self.assertFalse(self.c1.all_answered(self.survey2),
                         "There are two students but one of them does not have answer for the second question of the survey")
        self.c1.students[-1].set_answer(self.n3, numerical_att)
        self.assertFalse(self.c1.all_answered(self.survey2),
                         "There are two students but one of them does not have a valid answer for the second question of survey")
        self.c1.students[-1].set_answer(self.n3, numerical_sol)
        self.assertTrue(self.c1.all_answered(self.survey2))


class TestQuestion(unittest.TestCase):
    def setUp(self) -> None:
        self.q = Question(1, "Q")
        self.assertTrue(len(Question.__mro__) == 2)

    def test_SubclassInheritance(self):
        subclasses = [MultipleChoiceQuestion, NumericQuestion, CheckboxQuestion, YesNoQuestion]
        all_are_questions = all([Question in i.__mro__ for i in subclasses])
        at_least_one = any([len(i.__mro__) > 3 for i in subclasses])
        self.assertTrue(all_are_questions)
        self.assertTrue(at_least_one)


class TestMultipleChoiceQuestion(unittest.TestCase):
    def setUp(self) -> None:
        self.options = ["OptionA", "OptionB", "OptionC", "OptionD"]
        self.m1 = MultipleChoiceQuestion(1, "Choose one of four possible option",
                                         self.options)
        self.s1 = Student(1, "A")
        self.a1 = Answer("OptionA")
        self.a2 = Answer("Bool")
        no_public(MultipleChoiceQuestion, self.m1, ["id", "text"], ["validate_answer", "get_similarity"])

    def tearDown(self) -> None:
        self.options = ["OptionA", "OptionB", "OptionC", "OptionD"]
        self.m1 = MultipleChoiceQuestion(1, "Choose one of four possible option",
                                         self.options)
        self.s1 = Student(1, "A")
        self.a1 = Answer("OptionA")
        self.a2 = Answer("Bool")

    def test_inheritance(self):
        mro = MultipleChoiceQuestion.__mro__
        mandatory_types = [MultipleChoiceQuestion, object]
        inheritances = list(filter(lambda x: x not in mandatory_types, mro))
        self.assertTrue(len(inheritances) >= 1)

    def test_str(self):
        options = ["OptionA", "OptionB", "OptionC", "OptionD"]
        self.assertTrue("Choose one of four possible option" in str(self.m1))
        self.assertTrue(all([opt in str(self.m1) for opt in options]))

    def test_validate(self):
        self.assertTrue(self.m1.validate_answer(self.a1))
        self.assertFalse(self.m1.validate_answer(self.a2))

    def test_similarity(self):
        exp = [1.0, 0.0, 0.0, 0.0]
        act = [self.m1.get_similarity(self.a1, Answer(opt)) for opt in self.options]
        self.assertTrue(all([exp[i] == act[i] for i in range(4)]))


class TestNumericQuestion(unittest.TestCase):
    def setUp(self) -> None:
        self.n1 = NumericQuestion(1, "N1", -2, 2)
        self.a1 = Answer(1)
        self.a2 = Answer("1")

    def test_inheritance(self):
        mro = NumericQuestion.__mro__
        mandatory_types = [NumericQuestion, object]
        inheritances = list(filter(lambda x: x not in mandatory_types, mro))
        self.assertTrue(len(inheritances) >= 1)

    def test_str(self):
        self.assertTrue("N1" in str(self.n1))
        self.assertTrue("-2" in str(self.n1))
        self.assertTrue("2" in str(self.n1))

    def test_validate(self):
        self.assertFalse(self.n1.validate_answer(self.a2))
        self.assertTrue(self.n1.validate_answer(Answer(1)))
        valid_sols = [Answer(i) for i in range(-2, 3)]
        self.assertTrue(all([self.n1.validate_answer(ans) for ans in valid_sols]))
        invalid_sols = [Answer(i) for i in range(-10, -2)] + [Answer(j) for j in range(3, 10)]
        self.assertFalse(any([self.n1.validate_answer(ans) for ans in invalid_sols]))

    def test_similarity(self):
        # 1 - (absolute_diff / (max_val - min_val))
        exp = [1 - (abs(j - i) / 4) for i in range(-2, 3) for j in range(-2, 3)]
        act = [self.n1.get_similarity(Answer(i), Answer(j)) for i in range(-2, 3) for j in range(-2, 3)]
        self.assertTrue(all([exp[i] == act[i] for i in range(25)]))


class TestYesNoQuestion(unittest.TestCase):
    def setUp(self) -> None:
        self.y1 = YesNoQuestion(1, "YesNo")
        self.a1 = Answer(True)
        self.a2 = Answer(1)

    def test_inheritance(self):
        mro = NumericQuestion.__mro__
        mandatory_types = [YesNoQuestion, object]
        inheritances = list(filter(lambda x: x not in mandatory_types, mro))
        self.assertTrue(len(inheritances) >= 1)

    def test_validate(self):
        self.assertTrue(self.y1.validate_answer(self.a1))
        self.assertTrue(self.y1.validate_answer(Answer(False)))
        self.assertFalse(self.y1.validate_answer(self.a2))

    def test_similarity(self):
        self.assertEqual(self.y1.get_similarity(self.a1, Answer(False)), 0.0)
        self.assertEqual(self.y1.get_similarity(self.a1, Answer(True)), 1.0)
        self.assertEqual(self.y1.get_similarity(Answer(False), Answer(True)), 0.0)
        self.assertEqual(self.y1.get_similarity(Answer(False), Answer(False)), 1.0)


class TestCheckboxQuestion(unittest.TestCase):
    def setUp(self) -> None:
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.y1 = CheckboxQuestion(1, "Checkbox", ["OptA", "OptB", "OptC", "OptD"])
        self.a1 = Answer(True)
        self.a2 = Answer(1)

    def tearDown(self) -> None:
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.y1 = CheckboxQuestion(1, "Checkbox", ["OptA", "OptB", "OptC", "OptD"])
        self.a1 = Answer(True)
        self.a2 = Answer(1)

    def test_inheritance(self):
        mro = NumericQuestion.__mro__
        mandatory_types = [CheckboxQuestion, Question, object]
        inheritances = list(filter(lambda x: x not in mandatory_types, mro))
        self.assertTrue(len(inheritances) >= 1)

    def test_validate(self):
        permutations = list(itertools.permutations(self.opts, 2))
        self.assertFalse(self.y1.validate_answer(self.a1))
        self.assertFalse(self.y1.validate_answer(self.a2))
        self.assertFalse(self.y1.validate_answer(Answer([])))
        act1 = [self.y1.validate_answer(Answer([opt])) for opt in self.opts]
        self.assertTrue(all(act1))
        act2 = [self.y1.validate_answer(Answer([opt[0], opt[1]])) for opt in permutations]
        self.assertTrue(all(act2))
        act3 = [self.y1.validate_answer(Answer([opt, opt])) for opt in self.opts]
        self.assertFalse(any(act3), "Non unique")
        act4 = [self.y1.validate_answer(Answer([str(i)])) for i in range(10)]
        self.assertFalse(any(act4), "Non possible")
        act5 = [self.y1.validate_answer(Answer([self.opts[i], str(i)])) for i in range(len(self.opts))]
        self.assertFalse(any(act5), "Non possible")

    def test_similarity(self):
        permutations = list(itertools.permutations(self.opts, 2))
        act1 = [self.y1.get_similarity(Answer([i]), Answer([i])) for i in self.opts]
        self.assertTrue(all([i == 1.0 for i in act1]))
        act2 = [self.y1.get_similarity(Answer([opt[0]]), Answer([opt[1]])) for opt in permutations]
        self.assertTrue(all([i == 0.0 for i in act2]))
        q = CheckboxQuestion(2, "Checkbox", ["O", "p", "t", "A", "B", "C", "D"])
        act3 = [q.get_similarity(Answer(list(opt[0])), Answer(list(opt[1]))) for opt in permutations]
        self.assertTrue(all([i == 0.6 for i in act3]))


class TestCriterion(unittest.TestCase):
    def setUp(self) -> None:
        self.c = Criterion
        self.assertTrue(len(self.c.__mro__) == 2)

    def test_Inheritance(self):
        subclasses = [HomogeneousCriterion, HeterogeneousCriterion, LonelyMemberCriterion]
        all_criterion = all([self.c in i.__mro__ for i in subclasses])
        self.assertTrue(all_criterion)
        at_least_one = any([len(i.__mro__) > 3 for i in subclasses])
        self.assertTrue(at_least_one)
        no_init = all(["__init__" not in i.__mro__ for i in subclasses])
        self.assertTrue(no_init)


class TestHomogeneousCriterion(unittest.TestCase):
    def setUp(self) -> None:
        self.choices = ["A", "B", "C", "D"]
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.c = HomogeneousCriterion()
        self.q1 = MultipleChoiceQuestion(1, "M", self.choices)
        self.q2 = NumericQuestion(2, "N", 1, 5)
        self.q3 = YesNoQuestion(3, "Y")
        self.q4 = CheckboxQuestion(4, "Checkbox", self.opts)

    def tearDown(self) -> None:
        self.choices = ["A", "B", "C", "D"]
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.c = HomogeneousCriterion()
        self.q1 = MultipleChoiceQuestion(1, "M", self.choices)
        self.q2 = NumericQuestion(2, "N", 1, 5)
        self.q3 = YesNoQuestion(3, "Y")
        self.q4 = CheckboxQuestion(4, "Checkbox", self.opts)

    def test_score_single_element(self):
        self.assertTrue(all([self.c.score_answers(self.q1, [Answer(choice)]) == 1.0 for choice in self.choices]))
        self.assertTrue(all([self.c.score_answers(self.q2, [Answer(num)]) == 1.0 for num in range(1, 6)]))
        self.assertTrue(all([self.c.score_answers(self.q3, [Answer(boolean)]) == 1.0 for boolean in [True, False]]))
        self.assertTrue(all([self.c.score_answers(self.q4, [Answer([opt])]) == 1.0 for opt in self.opts]))

    def test_score_multiple_elements(self):
        self.assertEqual(self.c.score_answers(self.q1, [Answer(choice) for choice in self.choices]), 0.0)
        self.assertEqual(self.c.score_answers(self.q2, [Answer(num) for num in range(1, 6)]),  0.5)
        self.assertEqual(self.c.score_answers(self.q3, [Answer(boolean) for boolean in [True, False]]), 0.0)
        self.assertEqual(self.c.score_answers(self.q4, [Answer([opt]) for opt in self.opts]), 0.0)

    def test_score_single_element_invalid(self):
        invalid_args = list(range(1, 6)) + [True, False] + [[opt] for opt in self.opts]
        for invalid_arg in invalid_args:
            self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q1,
                              [Answer(invalid_arg)])
        invalid_args2 = self.choices + [True, False] + [[opt] for opt in self.opts]
        for invalid_arg in invalid_args2:
            self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q2,
                              [Answer(invalid_arg)])
        invalid_args3 = self.choices + list(range(1, 6)) + [[opt] for opt in self.opts]
        for invalid_arg in invalid_args3:
            self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q3,
                              [Answer(invalid_arg)])
        invalid_args4 = self.choices + list(range(1, 6)) + [True, False]
        for invalid_arg in invalid_args4:
            self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q4,
                              [Answer(invalid_arg)])

    def test_score_mix_invalid_element(self):
        invalid_args = [Answer(choice) for choice in self.choices] + [Answer(True)]
        self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q1, invalid_args)
        invalid_args2 = [Answer(num) for num in range(1, 6)] + [Answer("A")]
        self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q2, invalid_args2)
        invalid_args3 = [Answer(True)] + [Answer(1)]
        self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q3, invalid_args3)
        invalid_args4 = [Answer([opt]) for opt in self.opts] + [Answer(True)]
        self.assertRaises(InvalidAnswerError, HomogeneousCriterion.score_answers, self.c, self.q4, invalid_args4)

    def test_score_with_multiple_choice(self):
        answers = [Answer(i) for i in self.choices]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_one_duplicate), 1 / 6, "1 / 4C2 = 1 / 6")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_two_set_duplicate), 2 / 6, "2 / 4C2 = 1 / 3")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_three_duplicate), 1 / 2, "3 / 4C2 = 1 / 2")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q1, answer_with_four_duplicate), 1.0)

    def test_score_with_numerical_answer(self):
        answers = [Answer(i) for i in range(1, 6)]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:4] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_one_duplicate), 0.6,
                         " sum of [0.75, 0.5, 0.25, 1.0, 0.75, 0.5, 0.75, 0.75, 0.5, 0.25] / 10")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2] + [answers[1]]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_two_set_duplicate), 0.85,
                         " sum of [0.75, 1.0, 0.75, 0.75, 0.75, 1.0, 1.0, 0.75, 0.75, 1.0] / 10")
        answer_with_three_duplicates = [answer_copy[0]] * 3 + [answer_copy[1]] * 2
        self.assertEqual(self.c.score_answers(self.q2, answer_with_three_duplicates), 0.85,
                         " sum of [1.0, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 0.75, 0.75, 1.0] / 10")
        answer_with_four_duplicates = [answer_copy[0]] * 4 + [answer_copy[-1]]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_four_duplicates), 0.6,
                         " sum of [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0] / 10")
        answer_with_all_duplicates = [answer_copy[0]] * 5
        self.assertEqual(self.c.score_answers(self.q2, answer_with_all_duplicates), 1.0,
                         " sum of [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] / 10")

    def test_score_with_yes_no(self):
        answers = [Answer(True), Answer(False), Answer(True), Answer(False)]
        self.assertEqual(self.c.score_answers(self.q3, answers), 1 / 3, "2 / 4C2 = 1 / 3")
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q3, answer_with_one_duplicate), 0.5, "3 / 4C2 = 1 / 2")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q3, answer_with_four_duplicate), 1.0)

    def test_score_with_checkbox(self):
        answers = [Answer([i]) for i in self.opts]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_one_duplicate), 1 / 6, "1 / 4C2 = 1 / 6")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_two_set_duplicate), 2 / 6, "2 / 4C2 = 1 / 3")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_three_duplicate), 1 / 2, "3 / 4C2 = 1 / 2")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q4, answer_with_four_duplicate), 1.0)

    def test_score_with_checkbox_2(self):
        self.q4 = CheckboxQuestion(4, "C", list("OptABCD"))
        answers = [Answer(list(i)) for i in self.opts]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_one_duplicate), 2 / 3,
                         "sum of [0.6, 0.6, 1.0, 0.6, 0.6, 0.6] / 6")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_two_set_duplicate), 4.4 / 6,
                         "sum of [0.6, 1.0, 0.6, 0.6, 1.0, 0.6]")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_three_duplicate), 4.8 / 6,
                         "sum of [1.0, 1.0, 0.6, 1.0, 0.6, 0.6] / 6")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q4, answer_with_four_duplicate), 1.0)


class TestHeterogeneousCriterion(TestHomogeneousCriterion):
    def setUp(self) -> None:
        super().setUp()
        self.c = HeterogeneousCriterion()

    def tearDown(self) -> None:
        super().tearDown()
        self.c = HeterogeneousCriterion()

    def test_score_multiple_elements(self):
        self.assertEqual(self.c.score_answers(self.q1, [Answer(choice) for choice in self.choices]), 1.0)
        self.assertEqual(self.c.score_answers(self.q2, [Answer(num) for num in range(1, 6)]), 0.5)
        self.assertEqual(self.c.score_answers(self.q3, [Answer(boolean) for boolean in [True, False]]), 1.0)
        self.assertEqual(self.c.score_answers(self.q4, [Answer([opt]) for opt in self.opts]), 1.0)

    def test_score_single_element(self):
        self.assertTrue(all([self.c.score_answers(self.q1, [Answer(choice)]) == 0.0 for choice in self.choices]))
        self.assertTrue(all([self.c.score_answers(self.q2, [Answer(num)]) == 0.0 for num in range(1, 6)]))
        self.assertTrue(all([self.c.score_answers(self.q3, [Answer(boolean)]) == 0.0 for boolean in [True, False]]))
        self.assertTrue(all([self.c.score_answers(self.q4, [Answer([opt])]) == 0.0 for opt in self.opts]))

    def test_score_with_checkbox(self):
        answers = [Answer([i]) for i in self.opts]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_one_duplicate), 1 - (1 / 6), "1 - 1 / 4C2 = 5 / 6")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_two_set_duplicate), 1 - (2 / 6), "1 - 2 / 4C2 = 2 / 3")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_three_duplicate), 1 / 2, "1 - 3 / 4C2 = 1 / 2")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q4, answer_with_four_duplicate), 0.0)

    def test_score_with_checkbox_2(self):
        self.q4 = CheckboxQuestion(4, "C", list("OptABCD"))
        answers = [Answer(list(i)) for i in self.opts]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_one_duplicate), 1 - (2 / 3),
                         "1 - sum of [0.6, 0.6, 1.0, 0.6, 0.6, 0.6] / 6")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_two_set_duplicate), 1 - (4.4 / 6),
                         "1 - sum of [0.6, 1.0, 0.6, 0.6, 1.0, 0.6]")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_three_duplicate), 1 - (4.8 / 6),
                         "1 - sum of [1.0, 1.0, 0.6, 1.0, 0.6, 0.6] / 6")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q4, answer_with_four_duplicate), 0.0)

    def test_score_with_multiple_choice(self):
        answers = [Answer(i) for i in self.choices]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_one_duplicate), 1 - (1 / 6), "1 - 1 / 4C2 = 5 / 6")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_two_set_duplicate), 1 - (2 / 6), "2 / 4C2 = 2 / 3")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_three_duplicate), 1 / 2, "1 - 3 / 4C2 = 1 / 2")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q1, answer_with_four_duplicate), 0.0)

    def test_score_with_numerical_answer(self):
        answers = [Answer(i) for i in range(1, 6)]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:4] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_one_duplicate), 1 - 0.6,
                         "1 - sum of [0.75, 0.5, 0.25, 1.0, 0.75, 0.5, 0.75, 0.75, 0.5, 0.25] / 10")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2] + [answers[1]]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_two_set_duplicate), 1 - 0.85,
                         "1 - sum of [0.75, 1.0, 0.75, 0.75, 0.75, 1.0, 1.0, 0.75, 0.75, 1.0] / 10")
        answer_with_three_duplicates = [answer_copy[0]] * 3 + [answer_copy[1]] * 2
        self.assertEqual(self.c.score_answers(self.q2, answer_with_three_duplicates), 1 - 0.85,
                         "1 - sum of [1.0, 1.0, 0.75, 0.75, 1.0, 0.75, 0.75, 0.75, 0.75, 1.0] / 10")
        answer_with_four_duplicates = [answer_copy[0]] * 4 + [answer_copy[-1]]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_four_duplicates), 1 - 0.6,
                         "1 - sum of [1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0] / 10")
        answer_with_all_duplicates = [answer_copy[0]] * 5
        self.assertEqual(self.c.score_answers(self.q2, answer_with_all_duplicates), 0.0,
                         "1 - sum of [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] / 10")

    def test_score_with_yes_no(self):
        answers = [Answer(True), Answer(False), Answer(True), Answer(False)]
        self.assertEqual(self.c.score_answers(self.q3, answers), 1 - (1 / 3), "1 - 2 / 4C2 = 2 / 3")
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q3, answer_with_one_duplicate), 0.5, "1 - 3 / 4C2 = 1 / 2")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q3, answer_with_four_duplicate), 0.0)


class TestLonelyMemberCriterion(TestHeterogeneousCriterion):
    def setUp(self) -> None:
        super().setUp()
        self.c = LonelyMemberCriterion()

    def tearDown(self) -> None:
        super().tearDown()
        self.c = LonelyMemberCriterion()

    def test_score_multiple_elements(self):
        self.assertEqual(self.c.score_answers(self.q1, [Answer(choice) for choice in self.choices]), 0.0)
        self.assertEqual(self.c.score_answers(self.q2, [Answer(num) for num in range(1, 6)]), 0.0)
        self.assertEqual(self.c.score_answers(self.q3, [Answer(boolean) for boolean in [True, False]]), 0.0)
        self.assertEqual(self.c.score_answers(self.q4, [Answer([opt]) for opt in self.opts]), 0.0)

    def test_score_with_checkbox(self):
        answers = [Answer([i]) for i in self.opts]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_one_duplicate), 0, "opta, optb, optc, opta")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_two_set_duplicate), 1 , "opta, optb, opta, optb")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_three_duplicate), 0, "opta, opta, opta, optb")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q4, answer_with_four_duplicate), 1, "opta, opta, opta, opta")

    def test_score_with_checkbox_2(self):
        self.q4 = CheckboxQuestion(4, "C", list("OptABCD"))
        answers = [Answer(list(i)) for i in self.opts]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_one_duplicate), 0,
                         "[[O,p,t,A], [O,p,t,B], [O,p,t,C], [O,p,t,A]]")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_two_set_duplicate), 1,
                         "[[O,p,t,A], [O,p,t,B], [O,p,t,A], [O,p,t,B]]")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q4, answer_with_three_duplicate), 0,
                         "[[O,p,t,A], [O,p,t,A], [O,p,t,A], [O,p,t,B]]")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q4, answer_with_four_duplicate), 1)

    def test_score_with_multiple_choice(self):
        answers = [Answer(i) for i in self.choices]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_one_duplicate), 0, "A, B, C, A")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_two_set_duplicate), 1, "A, B, A, B")
        answer_with_three_duplicate = [answer_copy[0]] * 3 + answer_copy[1: 2]
        self.assertEqual(self.c.score_answers(self.q1, answer_with_three_duplicate), 0, "A, A, A, B")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q1, answer_with_four_duplicate), 1)

    def test_score_with_numerical_answer(self):
        answers = [Answer(i) for i in range(1, 6)]
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:4] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_one_duplicate), 0,
                         "1, 2, 3, 4, 1")
        answer_with_two_set_duplicate = answer_copy[:2] + answer_copy[:2] + [answers[1]]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_two_set_duplicate), 1,
                         "1, 2, 1, 2, 2")
        answer_with_three_duplicates = [answer_copy[0]] * 3 + [answer_copy[1]] * 2
        self.assertEqual(self.c.score_answers(self.q2, answer_with_three_duplicates), 1,
                         "1, 1, 1, 2, 2")
        answer_with_four_duplicates = [answer_copy[0]] * 4 + [answer_copy[-1]]
        self.assertEqual(self.c.score_answers(self.q2, answer_with_four_duplicates), 0,
                         "1, 1, 1, 1, 5")
        answer_with_all_duplicates = [answer_copy[0]] * 5
        self.assertEqual(self.c.score_answers(self.q2, answer_with_all_duplicates), 1,
                         "1, 1, 1, 1, 1")

    def test_score_with_yes_no(self):
        answers = [Answer(True), Answer(False), Answer(True), Answer(False)]
        self.assertEqual(self.c.score_answers(self.q3, answers), 1, "T, F, T, F")
        answer_copy = answers[:]
        answer_with_one_duplicate = answer_copy[:3] + answer_copy[0:1]
        self.assertEqual(self.c.score_answers(self.q3, answer_with_one_duplicate), 0, "T, F, T, T")
        answer_with_four_duplicate = [answer_copy[0]] * 4
        self.assertEqual(self.c.score_answers(self.q3, answer_with_four_duplicate), 1, "T T T T")


class TestGroup(unittest.TestCase):
    def setUp(self) -> None:
        self.students = [Student(i, str(i)) for i in range(10)]
        random.shuffle(self.students)
        self.group = Group(self.students)

    def tearDown(self) -> None:
        self.students = [Student(i, str(i)) for i in range(10)]
        random.shuffle(self.students)
        self.group = Group(self.students)

    def test_len(self):
        self.assertEqual(len(self.group), 10)

    def test_str(self):
        self.assertTrue("\n" not in str(self.group))
        self.assertTrue(all([str(i) in str(self.group) for i in range(10)]))

    def test_in(self):
        self.assertTrue(all([student in self.group for student in self.students]))
        self.assertTrue(all([Student(i, str(i)) not in self.group for i in range(11, 21)]))

    def test_get_student(self):
        act = self.group.get_members()
        self.assertTrue(id(self.students) != id(act))
        self.assertCountEqual(act, self.students)


class TestGrouping(unittest.TestCase):
    def setUp(self) -> None:
        self.group1 = Group([Student(i, "Student" + str(i)) for i in range(3)])
        self.group2 = Group([Student(i, "Student" + str(i)) for i in range(3, 6)])
        self.group3 = Group([Student(i, "Student" + str(i)) for i in range(6, 10)])
        self.grouping = Grouping()

    def tearDown(self) -> None:
        self.group1 = [Student(i, "Student" + str(i)) for i in range(3)]
        self.group2 = [Student(i, "Student" + str(i)) for i in range(3, 6)]
        self.group3 = [Student(i, "Student" + str(i)) for i in range(6, 10)]
        self.grouping = Grouping()

    def test_str(self):
        self.grouping.add_group(self.group1)
        self.grouping.add_group(self.group2)
        self.assertTrue("\n" in str(self.grouping))
        temp = str(self.grouping)
        info = temp.split("\n")
        desire_line = list(filter(lambda x: "Student1" in x, info))
        desire_line2 = list(filter(lambda x: "Student4" in x, info))
        self.assertTrue(any(["Student0" in line and "Student1" in line and "Student2" in line for line in desire_line]))
        self.assertTrue(
            any(["Student3" in line and "Student4" in line and "Student5" in line for line in desire_line2]))

    def test_add_1(self):
        student_comb = list(itertools.combinations([Student(i, "Student" + str(i)) for i in range(3)], 2))
        self.assertTrue(self.grouping.add_group(self.group1))
        self.assertTrue(self.grouping.get_groups() != [])
        self.assertFalse(self.grouping.add_group(Group([])))
        self.assertFalse(any([self.grouping.add_group(Group([])) for _ in range(10)]))
        self.assertFalse(any([self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in student_comb]))

    def test_add_2(self):
        group1_comb = list(itertools.combinations([Student(i, "Student" + str(i)) for i in range(3)], 2))
        group2_comb = list(itertools.combinations([Student(i, "Student" + str(i)) for i in range(3, 6)], 2))
        group3_comb = list(itertools.combinations([Student(i, "Student" + str(i)) for i in range(6, 10)], 2))
        self.assertTrue(self.grouping.add_group(self.group1))
        self.assertFalse(any([self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in group1_comb]))
        self.assertTrue(self.grouping.add_group(self.group2))
        self.assertFalse(any([self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in group2_comb]))
        self.assertFalse(any([self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in group2_comb + group1_comb]))
        self.assertTrue(self.grouping.add_group(self.group3))
        self.assertFalse(any(
            [self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in group3_comb]))
        self.assertFalse(any([self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in
                              group3_comb + group2_comb]))
        self.assertFalse(any([self.grouping.add_group(Group([student_tuple[0], student_tuple[1]])) for student_tuple in
                              group3_comb + group2_comb + group1_comb]))

    def test_get_group(self):
        self.grouping.add_group(self.group1)
        student_ids = [student.id for group in self.grouping.get_groups() for student in group.get_members()]
        self.assertCountEqual(student_ids, [i for i in range(3)])
        self.grouping.add_group(self.group2)
        student_ids2 = [student.id for group in self.grouping.get_groups() for student in group.get_members()]
        self.assertCountEqual(student_ids2, [i for i in range(6)])
        self.grouping.add_group(self.group3)
        student_ids3 = [student.id for group in self.grouping.get_groups() for student in group.get_members()]
        self.assertCountEqual(student_ids3, [i for i in range(10)])


class TestSurvey(unittest.TestCase):
    def setUp(self) -> None:
        self.choices = ["A", "B", "C", "D"]
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.c1 = HomogeneousCriterion()
        self.c2 = HeterogeneousCriterion()
        self.c3 = LonelyMemberCriterion()
        self.q1 = MultipleChoiceQuestion(1, "M", self.choices)
        self.q2 = NumericQuestion(2, "N", 1, 5)
        self.q3 = YesNoQuestion(3, "Y")
        self.q4 = CheckboxQuestion(4, "Checkbox", self.opts)
        self.students = [Student(i, "Student{}".format(i)) for i in range(4)]
        self.questions = [self.q1, self.q2, self.q3, self.q4]
        self.criterion = [self.c1, self.c2, self.c3]
        self.survey = Survey(self.questions)
        self.set_answer = lambda question, answers: [self.students[i].set_answer(question, answers[i]) for i in range(len(self.students))]

    def tearDown(self) -> None:
        self.choices = ["A", "B", "C", "D"]
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.c1 = HomogeneousCriterion()
        self.c2 = HeterogeneousCriterion()
        self.c3 = LonelyMemberCriterion()
        self.q1 = MultipleChoiceQuestion(1, "M", self.choices)
        self.q2 = NumericQuestion(2, "N", 1, 5)
        self.q3 = YesNoQuestion(3, "Y")
        self.q4 = CheckboxQuestion(4, "Checkbox", self.opts)
        self.students = [Student(i, "Student{}".format(i)) for i in range(4)]
        self.questions = [self.q1, self.q2, self.q3, self.q4]
        self.criterion = [self.c1, self.c2, self.c3]
        self.survey = Survey(self.questions)
        self.set_answer = lambda question, answers: map(lambda student_index: self.students[student_index].set_answer(question, answers[student_index]), [i for i in range(4)])

    def test_len(self):
        self.assertEqual(len(self.survey), 4)
        self.survey._questions = {}
        self.assertEqual(len(self.survey), 0)
        self.survey._questions = {i: Question(i, str(i)) for i in range(10)}
        self.assertEqual(len(self.survey), 10)

    def test_contain(self):
        self.assertTrue(all(Question(i, str(i)) in self.survey for i in range(1, 5)))

    def test_score_invalid(self):
        self.survey._questions = {self.q1.id: self.q1}
        self.set_answer(self.q1, [Answer([opt]) for opt in self.opts])
        self.assertEqual(self.survey.score_students(self.students), 0.0)
        self.survey._questions = {self.q2.id: self.q2}
        self.set_answer(self.q2, [Answer(choice) for choice in self.choices])
        self.assertEqual(self.survey.score_students(self.students), 0.0, "")
        self.survey._questions = {self.q3.id: self.q3}
        self.set_answer(self.q3, [Answer(num) for num in range(1, 6)])
        self.assertEqual(self.survey.score_students(self.students), 0.0, "")
        self.survey._questions = {self.q4.id: self.q4}
        self.set_answer(self.q4, [Answer(boolean) for boolean in [True, False, True, False]])
        self.assertEqual(self.survey.score_students(self.students), 0, "")

    def test_score_students_with_single_question(self):
        self.survey._questions = {}
        self.assertEqual(self.survey.score_students(self.students), 0.0)
        self.survey._questions = {self.q1.id: self.q1}
        self.set_answer(self.q1, [Answer(choice) for choice in self.choices])
        self.assertEqual(self.survey.score_students(self.students), 0.0)
        self.survey._questions = {self.q2.id: self.q2}
        self.set_answer(self.q2, [Answer(num) for num in range(1, 6)])
        self.assertEqual(self.survey.score_students(self.students), 3.5 / 6, "(sum of [0.75, 0.5, 0.25, 0.75, 0.5, 0.75] / 6) / 1")
        self.survey._questions = {self.q3.id: self.q3}
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False]])
        self.assertEqual(self.survey.score_students(self.students), 1/3, "(sum of [0.0, 1.0, 0.0, 0.0, 1.0, 0.0] / 6) / 1")
        self.survey._questions = {self.q4.id: self.q4}
        self.set_answer(self.q4, [Answer([opt]) for opt in self.opts])
        self.assertEqual(self.survey.score_students(self.students), 0, "")

    def test_score_students_with_two_questions(self):
        self.survey._questions = {self.q1.id: self.q1, self.q2.id: self.q2}
        self.survey.set_criterion(self.c2, self.q2)
        self.survey.set_weight(2, self.q2)
        self.set_answer(self.q1, [Answer(choice) for choice in self.choices])
        self.set_answer(self.q2, [Answer(num) for num in range(1, 6)])
        self.assertAlmostEqual(self.survey.score_students(self.students), 5 / 12, 3, "(0 + (2.5/ 6) * 2) / 2")
        self.survey._questions = {self.q2.id: self.q2, self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q2)
        self.survey.set_criterion(self.c2, self.q3)
        self.survey.set_weight(2, self.q2)
        self.survey.set_weight(4, self.q3)
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False]])
        self.assertAlmostEqual(self.survey.score_students(self.students), 8/6, 3, "(0 + (2/3) * 4) / 2")

    def test_score_grouping_single_member(self):
        self.assertEqual(self.survey.score_grouping(Grouping()), 0)
        self.set_answer(self.q1, [Answer(choice) for choice in self.choices])
        gr1, gr2, gr3, gr4 = Group([self.students[0]]), Group([self.students[1]]), Group([self.students[2]]), Group([self.students[3]])
        group_lis = [gr1, gr2, gr3, gr4]
        grouping = Grouping()
        for group in group_lis:
            grouping.add_group(group)
        self.survey._questions = {self.q1.id: self.q1}
        self.assertEqual(self.survey.score_grouping(grouping), 1)

    def test_score_grouping_two_groups(self):
        self.set_answer(self.q1, [Answer(choice) for choice in self.choices])
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False]])
        gr1, gr2 = Group([self.students[0], self.students[1]]), Group([self.students[2], self.students[3]])
        group_lis = [gr1, gr2]
        grouping = Grouping()
        for group in group_lis:
            grouping.add_group(group)
        self.survey.set_weight(3, self.q3)
        self.survey.set_criterion(self.c2, self.q3)
        self.survey._questions = {self.q1.id: self.q1, self.q3.id: self.q3}
        self.assertEqual(self.survey.score_grouping(grouping), 1.5, "((0 + 1 * 3) / 2 + (0 + 1 * 3) / 2) / 2")

    def test_score_grouping_unbalanced(self):
        self.set_answer(self.q2, [Answer(num) for num in [1, 1, 3, 3]])
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, True, True, False]])
        gr1, gr2 = Group([self.students[0], self.students[1], self.students[2]]), Group([self.students[3]])
        self.survey.set_criterion(self.c3, self.q3)
        self.survey.set_criterion(self.c2, self.q2)
        group_lis = [gr1, gr2]
        grouping = Grouping()
        for group in group_lis:
            grouping.add_group(group)
        self.survey._questions = {self.q2.id: self.q2, self.q3.id: self.q3}
        self.assertAlmostEqual(self.survey.score_grouping(grouping), 1/3, 3, "((1/3 + 1) / 2 + (0 + 0) / 2) / 2")


class TestSlice(unittest.TestCase):
    def setUp(self) -> None:
        self.l1 = [3, 4, 6, 2, 3]

    def tearDown(self) -> None:
        self.l1 = [3, 4, 6, 2, 3]

    def test_slice(self):
        self.assertTrue(all([slice_list([], i) == [] for i in range(100)]))
        self.assertTrue(all(slice_list([1] * i, 0) == [] for i in range(100)))
        act = slice_list(self.l1, 1)
        exp = [[i] for i in self.l1]
        self.assertEqual(act, exp)
        act2 = slice_list(self.l1, 2)
        exp2 = [[3, 4], [6, 2], [3]]
        self.assertEqual(act2, exp2)
        act3 = slice_list(self.l1, 3)
        exp3 = [[3, 4, 6], [2, 3]]
        self.assertEqual(act3, exp3)
        act4 = slice_list(self.l1, 4)
        exp4 = [[3, 4, 6, 2], [3]]
        self.assertEqual(act4, exp4)
        act5 = slice_list(self.l1, len(self.l1))
        exp5 = [self.l1]
        self.assertEqual(act5, exp5)


class TestWindow(unittest.TestCase):
    def setUp(self) -> None:
        self.l1 = [3, 4, 6, 2, 3]

    def tearDown(self) -> None:
        self.l1 = [3, 4, 6, 2, 3]

    def test_window(self):
        self.assertTrue(all([slice_list([], i) == [] for i in range(100)]))
        self.assertTrue(all(slice_list([1] * i, 0) == [] for i in range(100)))
        act1 = windows(self.l1, 1)
        exp1 = [[i] for i in self.l1]
        self.assertEqual(act1, exp1)
        act2 = windows(self.l1, 2)
        exp2 = [[3, 4], [4, 6], [6, 2], [2, 3]]
        self.assertEqual(act2, exp2)
        act3 = windows(self.l1, 3)
        exp3 = [[3, 4, 6], [4, 6, 2], [6, 2, 3]]
        self.assertEqual(act3, exp3)
        act4 = windows(self.l1, 4)
        exp4 = [[3, 4, 6, 2], [4, 6, 2, 3]]
        self.assertEqual(act4, exp4)
        self.assertEqual([self.l1], windows(self.l1, len(self.l1)))


class TestGrouper(unittest.TestCase):
    def setUp(self) -> None:
        self.choices = ["A", "B", "C", "D"]
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.c1 = HomogeneousCriterion()
        self.c2 = HeterogeneousCriterion()
        self.c3 = LonelyMemberCriterion()
        self.q1 = MultipleChoiceQuestion(1, "M", self.choices)
        self.q2 = NumericQuestion(2, "N", 1, 5)
        self.q3 = YesNoQuestion(3, "Y")
        self.q4 = CheckboxQuestion(4, "Checkbox", self.opts)
        self.students = [Student(i, "Student{}".format(i)) for i in range(4)]
        self.questions = [self.q1, self.q2, self.q3, self.q4]
        self.criterion = [self.c1, self.c2, self.c3]
        self.survey = Survey(self.questions)
        self.set_answer = lambda question, answers: [self.students[i].set_answer(question, answers[i]) for i in
                                                     range(len(self.students))]
        self.grouper = Grouper(2)
        self.assertGrouplen = lambda x, y: self.assertEqual(len(x), y)
        self.assertSubGrouplen = lambda x, y: self.assertTrue(all(len(x[i]) == y[i] for i in range(len(x))))

    def tearDown(self) -> None:
        self.choices = ["A", "B", "C", "D"]
        self.opts = ["OptA", "OptB", "OptC", "OptD"]
        self.c1 = HomogeneousCriterion()
        self.c2 = HeterogeneousCriterion()
        self.c3 = LonelyMemberCriterion()
        self.q1 = MultipleChoiceQuestion(1, "M", self.choices)
        self.q2 = NumericQuestion(2, "N", 1, 5)
        self.q3 = YesNoQuestion(3, "Y")
        self.q4 = CheckboxQuestion(4, "Checkbox", self.opts)
        self.students = [Student(i, "Student{}".format(i)) for i in range(4)]
        self.questions = [self.q1, self.q2, self.q3, self.q4]
        self.criterion = [self.c1, self.c2, self.c3]
        self.survey = Survey(self.questions)
        self.set_answer = lambda question, answers: [self.students[i].set_answer(question, answers[i]) for i in
                                                     range(len(self.students))]
        self.grouper = Grouper(2)
        self.assertGrouplen = lambda x, y: self.assertEqual(len(x), y)
        self.assertSubGrouplen = lambda x, y: self.assertTrue(all(len(x[i]) == y[i] for i in range(len(x))))


class TestAlphaGrouper(TestGrouper):
    def setUp(self) -> None:
        super().setUp()
        self.grouper = AlphaGrouper(2)

    def tearDown(self) -> None:
        super().tearDown()
        self.grouper = AlphaGrouper(2)

    def test_make_grouping(self):
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        grouping = self.grouper.make_grouping(course, Survey([]))
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2, 2])
        student_names = [student.name for group in grouping.get_groups() for student in group.get_members()]
        exp = [student.name for student in self.students]
        self.assertEqual(student_names, exp)

    def test_make_grouping_2(self):
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        self.grouper.group_size = 3
        grouping = self.grouper.make_grouping(course, Survey([]))
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [3, 1])
        student_names = [student.name for group in grouping.get_groups() for student in group.get_members()]
        exp = [student.name for student in self.students]
        self.assertEqual(student_names, exp)

    def test_make_grouping_3(self):
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        for i in range(4, 10):
            self.grouper.group_size = i
            grouping = self.grouper.make_grouping(course, Survey([]))
            self.assertGrouplen(grouping, 1)
            self.assertSubGrouplen(grouping.get_groups(), [4])
            student_names = [student.name for group in grouping.get_groups() for student in group.get_members()]
            exp = [student.name for student in self.students]
            self.assertEqual(student_names, exp)


class TestRandomGrouper(TestGrouper):
    def setUp(self) -> None:
        super().setUp()
        self.grouper = RandomGrouper(2)

    def tearDown(self) -> None:
        super().tearDown()
        self.grouper = RandomGrouper(2)

    def test_make_grouping(self):
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        grouping = self.grouper.make_grouping(course, Survey([]))
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2, 2])
        student_names = [student.name for group in grouping.get_groups() for student in group.get_members()]
        exp = [student.name for student in self.students]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_2(self):
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        self.grouper.group_size = 3
        grouping = self.grouper.make_grouping(course, Survey([]))
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [3, 1])
        student_names = [student.name for group in grouping.get_groups() for student in group.get_members()]
        exp = [student.name for student in self.students]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_3(self):
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        for i in range(4, 10):
            self.grouper.group_size = i
            grouping = self.grouper.make_grouping(course, Survey([]))
            self.assertGrouplen(grouping, 1)
            self.assertSubGrouplen(grouping.get_groups(), [4])
            student_names = [student.name for group in grouping.get_groups() for student in group.get_members()]
            exp = [student.name for student in self.students]
            self.assertCountEqual(student_names, exp)


class TestGreedyGrouper(TestGrouper):
    def setUp(self) -> None:
        super().setUp()
        self.grouper = GreedyGrouper(2)

    def tearDown(self) -> None:
        super().setUp()
        self.grouper = GreedyGrouper(2)

    def test_make_grouping_tie(self):
        self.grouper.group_size = 2
        course = Course("C1")
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, False, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2] * 2)
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[0].name, self.students[1].name}, {self.students[2].name, self.students[3].name}]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_full(self):
        for i in range(4, 10):
            self.grouper.group_size = i
            course = Course("C1")
            self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, False, False]])
            course.enroll_students(self.students[::-1])
            self.survey._questions = {self.q3.id: self.q3}
            self.survey.set_criterion(self.c3, self.q3)
            grouping = self.grouper.make_grouping(course, self.survey)
            self.assertGrouplen(grouping, 1)
            self.assertSubGrouplen(grouping.get_groups(), [4])
            student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
            exp = [set(student.name for student in self.students)]
            self.assertCountEqual(student_names, exp)

    def test_make_grouping_greedy_1(self):
        self.grouper.group_size = 2
        course = Course("C1")
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2] * 2)
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[0].name, self.students[2].name}, {self.students[1].name, self.students[3].name}]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_greedy_2(self):
        self.grouper.group_size = 3
        course = Course("C1")
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [3, 1])
        student_names = [student.name for group in grouping.get_groups()[0:1] for student in group.get_members()]
        exp = [student.name for student in [self.students[0], self.students[2], self.students[1]]]
        self.assertCountEqual(student_names, exp)
        last_student = grouping.get_groups()[1].get_members()[0]
        self.assertEqual(last_student.name, self.students[-1].name)

    def test_make_grouping_greedy_3(self):
        self.students.append(Student(4, str(4)))
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False, True]])
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 3)
        self.assertSubGrouplen(grouping.get_groups(), [2, 2, 1])
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[0].name, self.students[2].name}, {self.students[1].name, self.students[3].name}, {self.students[-1].name}]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_greedy_4(self):
        """
        This case is interesting this shows that your greedy algorithm does not provide the best solution
        Since you start with the first student and using lonely criterion as the criteria, thus the group you obtain can
        only be {0, 1, 2} & {3, 4} which only gives a score of 0.5.  However the optimal solution for this problem is
        {1, 3, 4} & {0, 2} which gives a score of 1.   If your solution is {1, 3, 4} & {0, 2} you are using wrong greedy
        :return:
        """
        self.grouper.group_size = 3
        self.students.append(Student(4, str(4)))
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, True, False, False]])
        course = Course("C1")
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [3, 2])
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[0].name, self.students[2].name, self.students[1].name}, {self.students[3].name, self.students[4].name}]
        self.assertCountEqual(student_names, exp)


class TestWindowGrouper(TestGrouper):
    def setUp(self) -> None:
        super().setUp()
        self.grouper = WindowGrouper(2)

    def tearDown(self) -> None:
        super().tearDown()
        self.grouper = WindowGrouper(2)

    def test_make_grouping(self):
        self.grouper.group_size = 2
        course = Course("C1")
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, True, False, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2] * 2)
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[0].name, self.students[1].name}, {self.students[3].name, self.students[2].name}]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_2(self):
        self.grouper.group_size = 2
        course = Course("C1")
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, False, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2] * 2)
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[2].name, self.students[1].name}, {self.students[3].name, self.students[0].name}]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_3(self):
        self.grouper.group_size = 3
        course = Course("C1")
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, False, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [3, 1])
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[2].name, self.students[1].name, self.students[3].name}, {self.students[0].name}]
        self.assertCountEqual(student_names, exp)

    def test_make_grouping_4(self):
        self.grouper.group_size = 2
        course = Course("C1")
        self.students.pop()
        self.set_answer(self.q3, [Answer(boolean) for boolean in [True, False, False]])
        course.enroll_students(self.students[::-1])
        self.survey._questions = {self.q3.id: self.q3}
        self.survey.set_criterion(self.c3, self.q3)
        grouping = self.grouper.make_grouping(course, self.survey)
        self.assertGrouplen(grouping, 2)
        self.assertSubGrouplen(grouping.get_groups(), [2, 1])
        student_names = [set(student.name for student in group.get_members()) for group in grouping.get_groups()]
        exp = [{self.students[2].name, self.students[1].name}, {self.students[0].name}]
        self.assertCountEqual(student_names, exp)


if __name__ == '__main__':
    unittest.main(exit=False)
