import random
from static_text.static_data import REMINDERS


def get_survey_reminder_text():
    index = random.randint(0, len(REMINDERS)-1)
    return REMINDERS[index]