DOCUMENTATION:

The AIRS singing app is a web-based Flask server, with backend written in Python and an SQLite3 database. This document will tell you everything you need to know about deploying, using, upkeeping, and modifying the application.

- DEPLOYMENT:
Flask apps are suprisingly *particular* about their deployment. Not hard, but particular. We used PythonAnywhere, which is cheap and robust. Many other options exist but most of them don't allow the use of SQL Databases. Deployment is simple; git pull into the console, then set the WSGI configuration to this:

import sys

if path not in sys.path:
    sys.path.append(path)
import database
database.setup()

from app import app as application
You can generate a venv from the requirements.txt, but be careful, as it's a little finnicky. You may have to uninstall and reinstall a couple libraries.


- USING:
Once deployed, the application is accessible through the web. There are 3 buttons visible, for three main options:
- Practice: the main function of the app, this allows "Note Sequences" to be generated, then grades the user's response.
- Watch: A simple section that contains videos, designed to provide motivation or useful tips
- Review: Shows feedback for the user's performance in Practice.

The site is account-based- users carry progression accross devices, and all sequences are saved to their account for easy analysis. Note that while there is no native password recovery feature, passwords can be manually updated from the database if needed. The easiest way is to use the werkzeug.security.generate_password_hash(password_here) function in python, then copy/paste the output in the user's password field with an SQLite editor of your choice. You *can* do this via provided Database methods but it's likely more complicated than it's worth.

User profiles consist of 4 major elements: an ID, a name, a password, and a *theme*. This determines the style used on the website- a feature requested by clients in order to a/b test different demographics. Three exist by default: "standard", "princess", and "rock". By default, the user's theme is randomly generated when the account is created (with a bias to standard), but this can be easily changed. Sample code is left commented in the code to allow the user to select their own theme at creation.

Audio input is handled locally in the website, using the built-in functions of the browser itself. It is then handed to challenge.py, which converts it into a .wav file and then then hands it to part2.py for processing and grading. 

**IMPORTANT: Note that some mobile phones do not like the current deployment, as it lacks an HTTPS certificate. They do not like to send audio without it. This is an easy fix, but an HTTPS certificate is not cheap, and I did not want to pay for it if it was not going to be needed immediately.**

- UPKEEP:
The server requires minimal manual upkeep. When you wish to access the data, simply download it from the source it is deployed from. SQLite3 Databases are simple to navigate, and a number of tools exist that can assist in analysis. They can also be converted into a CSV, to analyize in a Spreadsheet-like form.

Due to the nature of the server, the database should be resilient to crashes, and is not publically accessible, so it should not be able to be tampered with. I would  recommend keeping a backup every once and a while to be safe, but that's more of a universal precaution.

- MODIFICATION:
This is the important part of this document. This app was designed to be as modular as possible, and almost every feature is able to be adjusted as necessary. I will cover what I deem to be the important ones.

-- Grading Schema: The default grading scheme is a linear scale, which gives points for each note based on how close you got to the target. This can be easily adjusted- the inputGrader.py file contains the "input_grading" function. Any algorithm that takes the two lists (original_notes, aka the target, and input_notes, aka the response) and gives a numerical value value per note can be substituted into this point. Be mindful that each note must recieve a score, not just a final score for the whole sequence- this is needed to tune the generator towards your strong suits.

-- Tone Generation: The means by which a random tune is generated is controlled by noteSelector.py. It has a number of variables that can be adjusted. Many of these are tuned automatically in the "part1.py" script, and the degree by which this occurs can be manually adjusted, too. Key elements are the upper and lower bound, which determine how high or low the sequence can start, which are set to adapt to the notes the user is good at (note that it is only the starting note: the sequence may proceed to move out of comfortable range a little, allowing the user to gradually grow their range and the bounds as they improve). There is also the sequence length, which scales with a user's average accuracy- as the user is more accurate, they get harder and harder tones (in the sense that hitting multiple notes is harder than hitting one). There is also the step, determining the shift in notes at a time (from C-C# is step 1; C-D is step 2, etc.) The manner in which notes generate can be be further changed by adjusting the "next_note" formula. As is, the next note is calculated by "next_note = random.randint(-1, 1) * step", meaning it cannot move less than the step. It can be adjusted to randint(-step, step) to allow numbers in between, or random.randint(0,step) to only allow the sequences to increase.

-- Output Image: This is generated by outputFormatter.py, and is a little more complex. Fundamentally it takes two lists; the short one is your target notes, the long one is input. There are a lot of little nobs you can turn, such as color and size. You can also just fully replace it as long as you have something spit out an image named appropriately- it's extremely non-critical in implementation.

-- Input Processing: This is the most technical function in the entire app, and cannot be easily tweaked. That said, other solutions to this goal exist. We found librosa to be the most accurate, but it also produces really really long lists, which can make data a little fuzzy. This is most clearly seen in the generated images, as they get really crowded with dots. While this was deemed as the best option available, replacing it is as easy as replacing this single file.

-- Account Creation/Database fields: Account details such as age and gender were excluded, as it is unclear what information will be allowed to be collected, and it's easier to add than remove. That said, adding a field like this is very easy, but slightly involved. Note that this guide assumes you are working with a fresh setup of the database. If you have data that exists prior to modifications to the database, it is still possible to tweak the database, but its much more of a case-by-case process than I can cover here. Since this is SQLite3, there are many helpful guides online. The steps are as follows:
--- First, go to database.py, and find the create_tables function. The table at the top is the users table. Adding a field there adds it to the database when constructed; reference the existing fields for formatting.
--- Then, go to the add_user function, down a lil bit. It has a parameter for each table entry. Note how theme has a default value; this is not necessary but can be helpful. Add your new parameter, and include it int the list of variables in the cursor.execute() call. Make sure you get the order right! You'll also want to adjust the dummy call to add_user (with John and his password "Password") to match your new one, so it runs properly.
--- Next, go to the signup.py file. Here is where you determine where the data for this field comes from. You can see how the theme variable is random, by default, but the rest (including the alternate theme choice) uses request.form.get(variable_name). If you want the user to set this field, you'll want to copy this format.
--- Lastly, if you want to let the user select, you need to give them a field to select it in. Go to signup.html, and scroll down to the form field. HTML forms can be quite complex, but you can also just copy the formatting of username and change the word username to your new variable.
And thats all! Run the test function at the bottom of database.py to generate a new database file (you can do this other ways, but this is the easiest). If you really want to avoid the sample data, un-comment all the deletions, or comment out the additions, but I recommend leaving it just so you have an easy reference if you forget the structure.
