from app.agents.interview_agent.generator import (
    InterviewGenerator,
)

from app.agents.interview_agent.evaluator import (
    InterviewEvaluator,
)

from app.agents.interview_agent.feedback import (
    InterviewFeedbackGenerator,
)

from app.agents.interview_agent.scoring import (
    InterviewScoreCalculator,
)

from app.models.interview import InterviewSession

from app.repositories.interview_repository import (
    InterviewRepository,
)


class InterviewService:

    @staticmethod
    def start_interview(
        db,
        user_id: int,
        request,
    ):
        question_set = InterviewGenerator.generate(
            target_role=request.target_role,
            company=request.company,
            difficulty=request.difficulty,
            interview_type=request.interview_type,
        )

        interview = InterviewSession(
            user_id=user_id,
            target_role=request.target_role,
            company=request.company,
            difficulty=request.difficulty,
            interview_type=request.interview_type,
            questions=question_set.model_dump(),
            answers=[],
            feedback={},
            overall_score=0,
            status="In Progress",
        )

        return InterviewRepository.create(
            db,
            interview,
        )

    @staticmethod
    def get_interview(
        db,
        interview_id,
    ):
        return InterviewRepository.get_by_id(
            db,
            interview_id,
        )

    @staticmethod
    def get_user_interviews(
        db,
        user_id,
    ):
        return InterviewRepository.get_user_interviews(
            db,
            user_id,
        )

    @staticmethod
    def delete_interview(
        db,
        interview,
    ):
        InterviewRepository.delete(
            db,
            interview,
        )

    @staticmethod
    def submit_answer(
        db,
        interview,
        request,
    ):
        questions_data = interview.questions or {}

        questions = questions_data.get("questions", [])

        if not isinstance(questions, list):
            raise ValueError(
                "Invalid interview questions format."
            )

        requested_question_number = int(
            request.question_number
        )

        question = None

        for q in questions:
            if not isinstance(q, dict):
                continue

            question_number = q.get(
                "question_number"
            )

            if question_number is None:
                continue

            try:
                question_number = int(
                    question_number
                )
            except (TypeError, ValueError):
                continue

            if (
                question_number
                == requested_question_number
            ):
                question = q
                break

        if question is None:
            raise ValueError(
                f"Question {requested_question_number} not found."
            )

        answers = list(
            interview.answers or []
        )

        existing_answer = next(
            (
                item
                for item in answers
                if int(
                    item.get(
                        "question_number",
                        -1,
                    )
                )
                == requested_question_number
            ),
            None,
        )

        # Evaluate the candidate's answer
        evaluation = InterviewEvaluator.evaluate(
            question=question["question"],
            answer=request.answer,
        )

        # Generate feedback
        feedback = InterviewFeedbackGenerator.generate(
            question=question["question"],
            answer=request.answer,
            evaluation=evaluation,
        )

        # Store answer
        answer_record = {
            "question_number": requested_question_number,
            "question": question["question"],
            "answer": request.answer,
            "score": evaluation.score,
            "feedback": feedback,
        }

        if existing_answer:
            answers[answers.index(existing_answer)] = answer_record
        else:
            answers.append(answer_record)

        interview.answers = answers

        # Calculate overall score
        scores = [
            item["score"]
            for item in answers
            if "score" in item
        ]

        result = InterviewScoreCalculator.calculate(
            scores,
        )

        interview.overall_score = result[
            "overall_score"
        ]

        interview.feedback = result

        # Complete interview when all questions
        # have been answered
        if len(answers) == len(questions):
            interview.status = "Completed"

        return InterviewRepository.update(
            db,
            interview,
        )

    @staticmethod
    def update_status(
        db,
        interview,
        status,
    ):
        interview.status = status

        return InterviewRepository.update(
            db,
            interview,
        )