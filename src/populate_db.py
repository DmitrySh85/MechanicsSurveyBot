import asyncio
import os

import pandas as pd
from sqlalchemy import delete

from db import get_session
from models.models import Question


async def populate_db_from_file():
    async with get_session() as session:
        stmt = delete(Question)
        await session.execute(stmt)
        await session.commit()
    folder_path = "files/"
    for file_name in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file_name)) and file_name.endswith(".xlsx"):
            df = process_file_to_df()
            data = process_df_to_dict(df)
            await insert_data_to_db(data)


async def insert_data_to_db(data: dict):
    async with get_session() as session:
        await session.execute(Question.__table__.insert(), data)
        await session.commit()

def process_df_to_dict(df: pd.DataFrame) -> dict:
    data = []
    for _, row in df.iterrows():
        row_values = row.values.tolist()
        text = row[0]
        first_answer = row[1]
        second_answer = row[2]
        third_answer = row[3]
        fourth_answer = row[4]
        valid_answer_number = int(row[5]) - 1
        description = row[6]
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


def process_file_to_df():
    file_name = "files/survey.xlsx"
    df = pd.read_excel(file_name)
    return df


if __name__ == "__main__":
    asyncio.run(populate_db_from_file())