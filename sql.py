import pymysql
import os
import datetime

def repeat_rows_based_on_task_id():
    # Connect to the MySQL database
    connection = pymysql.connect(user='root',
        host='34.131.103.82',
        password='123_!Atellp#',
        database='ht_dp_mdo',
        cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            # Get today's date and day of the week (6 = Sunday, 0 = Monday, ...)
            today = datetime.datetime.now()
            day_of_week = today.weekday()

            # Check if today is Wednesday (day_of_week = 2)
            if day_of_week == 3:
                # Define the task_id to repeat
                task_to_repeat = "MDO.01.IN"

                # Find the last value in the "sno" column and set it as the starting point for sno
                cursor.execute("SELECT MAX(sno) FROM `mdo`")
                last_sno = cursor.fetchone()["MAX(sno)"] or 0
                # last_sno += 1
                # Create an array to hold the rows to repeat
                rows_to_repeat = []

                # Query existing rows with the specified task_id
                cursor.execute("SELECT * FROM `mdo` WHERE `task_id` = %s", (task_to_repeat,))
                existing_rows = cursor.fetchall()

                for i in range(len(existing_rows)):
                    if existing_rows[i]['task_id'] == task_to_repeat:  # Assuming task_id is in the second column (index 1)
                        sno = last_sno + i +1
                        ln_id = f"{existing_rows[i]['task_id']}.{sno}"

                        # Check if a row with the same sno and ln_id already exists in the table
                        row_exists = any(existing_row['sno'] == sno and existing_row['ln_id'] == ln_id for existing_row in existing_rows)

                        if not row_exists:
                            new_row = {
                                "sno": sno,
                                "task_id": existing_rows[i]['task_id'],
                                "ln_id": ln_id,
                                "Planned": today.strftime("%Y-%m-%d"),
                                "Actual": "",
                                "Status": "Pending",
                                # You can add other columns as needed
                            }
                            rows_to_repeat.append(new_row)

                # Insert the unique rows to repeat into the table
                if rows_to_repeat:
                    insert_query = "INSERT INTO `mdo` (`sno`, `task_id`, `ln_id`, `Planned`, `Actual`, `Status`) " \
                                   "VALUES (%(sno)s, %(task_id)s, %(ln_id)s, %(Planned)s, %(Actual)s, %(Status)s)"
                    cursor.executemany(insert_query, rows_to_repeat)
                    connection.commit()

if __name__ == "__main__":
    repeat_rows_based_on_task_id()
