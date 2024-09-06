from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from transliterate import to_cyrillic, to_latin
from uzwords import words
from difflib import get_close_matches
import re

# Directly define your API token here
API_TOKEN = "7292739885:AAFDFtMehMLGa3hYVGiWkdzBXxZJwkVBlaI"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def checkWords(word, words=words):
    word = word.lower()
    matches = set(get_close_matches(word, words))
    available = False

    if word in matches:
        available = True
        matches = {word}
    else:
        if "ҳ" in word:
            word_with_x = word.replace("ҳ", "x")
            matches.update(get_close_matches(word_with_x, words))
        if "x" in word:
            word_with_ҳ = word.replace("x", "ҳ")
            matches.update(get_close_matches(word_with_ҳ, words))

    return {"available": available, "matches": matches}


def is_cyrillic(text):
    # Check if text contains Cyrillic characters
    return bool(re.search(r"[а-яА-Я]", text))


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    username = message.from_user.username
    xabar = f"Assalom alaykum, {username} Kirill-Lotin-Kirill botiga xush kelibsiz!"
    xabar += "\nMatningizni yuboring."
    await message.reply(xabar)


@dp.message_handler(commands=["help"])
async def send_help(message: types.Message):
    xabar = """Send any Uzbek text, and I’ll check each word for spelling errors.
        Correct words will be marked ✅.
        For incorrect words, I’ll suggest alternatives.
        Use /start to begin and /help for assistance."""
    await message.reply(xabar)


@dp.message_handler(lambda message: message.text)  # Updated filter
async def translit_and_check(message: types.Message):
    msg = message.text

    if is_cyrillic(msg):
        # Handle Cyrillic text
        words_to_check = msg.split()
        correct_words = []
        incorrect_words = []

        for word in words_to_check:
            result = checkWords(word)
            if result["available"]:
                correct_words.append(f"✅ {word.capitalize()}")
            else:
                suggestions = "\n".join(
                    [f"✅ {match.capitalize()}" for match in result["matches"]]
                )
                if suggestions:
                    incorrect_words.append(
                        f"❌ {word.capitalize()}\nSuggestions:\n{suggestions}"
                    )
                else:
                    incorrect_words.append(
                        f"❌ {word.capitalize()} (No suggestions found)"
                    )

        response = ""
        if correct_words:
            response += "Correct words:\n" + "\n".join(correct_words) + "\n"
        if incorrect_words:
            response += "\nIncorrect words and suggestions:\n" + "\n\n".join(
                incorrect_words
            )

        await message.reply(response)

    else:
        # Handle Latin text
        cyrillic_msg = to_cyrillic(msg)
        words_to_check = cyrillic_msg.split()
        correct_words = []
        incorrect_words = []

        for word in words_to_check:
            result = checkWords(word)
            if result["available"]:
                correct_words.append(f"✅ {to_latin(word.capitalize())}")
            else:
                suggestions = "\n".join(
                    [
                        f"✅ {to_latin(match.capitalize())}"
                        for match in result["matches"]
                    ]
                )
                if suggestions:
                    incorrect_words.append(
                        f"❌ {to_latin(word.capitalize())}\nSuggestions:\n{suggestions}"
                    )
                else:
                    incorrect_words.append(
                        f"❌ {to_latin(word.capitalize())} (No suggestions found)"
                    )

        response = ""
        if correct_words:
            response += "Correct words:\n" + "\n".join(correct_words) + "\n"
        if incorrect_words:
            response += "\nIncorrect words and suggestions:\n" + "\n\n".join(
                incorrect_words
            )

        await message.reply(response)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
