import random, part1, part2, database
import shutil

# Go run the database main file first to make sure a database.... exists.
#Actually if you create a connection and no databse exists then it is created, and the code for the
#database tables and insertions can be added here no problem
conn = database.create_connection("airs_app.db")

user_id = 1 # should be whoever the user is. 1 is John, for testing.

id = random.randint(1000,10000)
sequence = part1.execute(id)
# tones generated. go get the audio.


shutil.copyfile("C Single Note.mp3", str(id)+".mp3")

# assume the audio is gotten now. Must be (id.mp3)
grade = part2.execute(id, sequence)
print(grade[0])

