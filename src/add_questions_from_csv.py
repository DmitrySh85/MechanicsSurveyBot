import pandas as pd
import asyncio
from db import get_session
from models.models import Question


def process_csv_to_xlsx():
    df = pd.read_csv("files/questions.csv")
    df.to_excel("files/26082024.xlsx")


async def process_data_to_db():
    df = pd.read_csv("files/questions.csv")
    data = process_df_to_dict(df)
    print(data)
    await insert_data_to_db(data)


def process_df_to_dict(df: pd.DataFrame) -> dict:
    data = []
    for _, row in df.iterrows():
        row_values = row.values.tolist()
        text = row[0]
        answers = list(map(lambda x: x.strip(), str(row[1]).split(",")))
        first_answer = answers[0]
        second_answer = answers[1]
        third_answer = answers[2]
        fourth_answer = answers[3]

        valid_answer = row[2].strip()
        valid_answer_number = answers.index(valid_answer) + 1
        description = row[3]
        data.append({
            "text": text,
            "first_answer": first_answer,
            "second_answer": second_answer,
            "third_answer": third_answer,
            "fourth_answer": fourth_answer,
            "valid_answer_number": valid_answer_number,
            "description": description
        })
    return data

async def insert_data_to_db(data: dict):
    async with get_session() as session:
        await session.execute(Question.__table__.insert(), data)
        await session.commit()

if __name__ == "__main__":
    #process_csv_to_xlsx()
    asyncio.run(process_data_to_db())
