import os

import inputProcessor, inputGrader, outputFormatter, noteUtils, database

def execute(temp_id, target, uid=1):
    output = target # ['C4', "C5"]
    inputs = inputProcessor.detect_notes(os.path.join("inputs", str(temp_id)+"_user.wav"))
    print(inputs)
    grades = inputGrader.input_grading(output, inputs)

    print([noteUtils.note_to_order(x) for x in inputs])

    outputFormatter.create(
        [noteUtils.note_to_order(x) for x in output],
        [noteUtils.note_to_order(x) for x in inputs], name=str(temp_id)+".png"
    )

    average, per_note_grades = inputGrader.input_grading(output, inputs)

    conn = database.create_connection("airs_app.db")
    user_id = uid #need to find a way to make dynamic

    for o, i, g in zip(output, inputs, per_note_grades):
        if i is not None and g > 0:
            if noteUtils.note_to_order(o) == noteUtils.note_to_order(i):
                database.update_user_note_score(conn, user_id, o, True)
            else:
                database.update_user_note_score(conn, user_id, o, False)

    print([noteUtils.note_to_order(x) for x in inputs])

    print("Output Formatter Start")
    outputFormatter.create(
        [noteUtils.note_to_order(x) for x in output],
        [noteUtils.note_to_order(x) for x in inputs], name=str(temp_id)+".png"
    )
    print("Output Formatter End")

    database.add_grade(conn, user_id, 1, int(average * 100))
    print("User Note Accuracy Overview")
    all_note_stats = database.get_user_notes_scores(conn, user_id)

    report = []
    for note, success, attempts in all_note_stats:
        if attempts == 0:
            accuracy = 0
        else:
            accuracy = round(success / attempts * 100, 2)
        report.append((note, accuracy, success, attempts))

    #Sort by accuracy descending
    report.sort(key=lambda x: -x[1])

    for note, acc, s, a in report:
        marker = "Great" if acc >= 90 else "Bad" if acc < 40 else "Good"
        print(f"{marker} {note}: {acc}% ({s}/{a})")
    print("Database status")
    #Print Results
    print("Users: ", database.get_users(conn))
    print("Exercise: ", database.get_exercises(conn))
    print("Grade for user 1: ", database.get_grades_of_user(conn, 1))
    print("User progression: ", database.get_user_progress(conn, 1))

    return [average, per_note_grades]
