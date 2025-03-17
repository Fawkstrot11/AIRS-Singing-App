import inputProcessor, inputGrader, outputFormatter, noteUtils, database

def execute(temp_id, target):
    output = target # ['C4', "C5"]
    inputs = inputProcessor.detect_notes(str(temp_id)+".mp3")
    print(inputs)
    grades = inputGrader.input_grading(output, inputs)

    print([noteUtils.note_to_order(x) for x in inputs])

    outputFormatter.create(
        [noteUtils.note_to_order(x) for x in output],
        [noteUtils.note_to_order(x) for x in inputs], name=str(temp_id)+".png"
    )

    conn = database.create_connection("airs_app.db")
    database.add_grade(conn, 1, 1, int(grades[0]*100))

    return grades
