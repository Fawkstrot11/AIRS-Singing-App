# The structure that calls all the parts in sequence. This is subject to change if necessary (especially whether input should be read here or in the web portion)
import inputProcessor
import noteSelector
import toneGenerator

notes = noteSelector.getNotes()

toneGenerator.main(notes)

read_notes = inputProcessor.main()

# do grading here

# produce the cool graphic


