import aiogram
from loader import dp, Bot, types
from Data.config import api_token

bot = Bot(token=api_token)

quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "Berlin", "Madrid", "Rome"],
        "correct_answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Venus", "Jupiter"],
        "correct_answer": "Mars"
    },
    # Add more questions
]

# Initialize a list to store poll IDs
poll_ids = []


async def send_quiz_questions(user_id, quiz_data):
    for quiz_item in quiz_data:
        question_text = quiz_item["question"]
        options = quiz_item["options"]
        correct_answer = quiz_item["correct_answer"]

        poll = await bot.send_poll(
            chat_id=user_id,
            question=question_text,
            options=options,
            is_anonymous=False
        )
        # Store poll IDs for later reference
        poll_ids.append(poll.poll.id)


@dp.poll_answer_handler()
async def process_quiz_answer(quiz_answer: types.PollAnswer):
    user_id = quiz_answer.user.id
    poll_id = quiz_answer.poll_id
    user_selected_option = quiz_answer.option_ids[0]

    # Retrieve correct answer from quiz_data
    correct_answer = next(item["correct_answer"] for item in quiz_data if item["question"] == question_text)

    if user_selected_option == quiz_data[poll_ids.index(poll_id)]["options"].index(correct_answer):
        await bot.send_message(user_id, "Correct! 🎉")
    else:
        await bot.send_message(user_id, f"Sorry, the correct answer was: {correct_answer}")
