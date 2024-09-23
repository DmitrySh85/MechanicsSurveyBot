import asyncio
import os

import pandas as pd
from sqlalchemy import delete

from db import get_session
from models.models import Question


async def populate_db_from_file():
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
        row_values = [None if pd.isna(value) else value for value in row.values.tolist()]
        text = row_values[1]
        first_answer = str(row_values[2]) if row_values[2] else ""
        second_answer = str(row_values[3]) if row_values[3] else ""
        third_answer = str(row_values[4]) if row_values[4] else ""
        fourth_answer = str(row_values[5]) if row_values[5] else ""
        valid_answer_number = int(row_values[6])
        description = row_values[7]
        data.append({

            "text": text,
            "first_answer": first_answer,
            "second_answer": second_answer,
            "third_answer": third_answer,
            "fourth_answer": fourth_answer,
            "valid_answer_number": valid_answer_number,
            "description": description
        })
        print({
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
    file_name = "files/modified_survey.xlsx"
    df = pd.read_excel(file_name)
    return df


if __name__ == "__main__":
    asyncio.run(populate_db_from_file())