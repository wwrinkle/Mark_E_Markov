# Mark E. Markov

AI improvisation buddy. You play music, Mark listens to you and plays something similar back to you in real time.

## Feature extraction

Mark uses Librosa to pull pitch, beat and tempo data from the audio stream.

### Pitch

Onsets are calculated. Using pyin we determine if the note is voiced and it's average frequency.

### Tempo

Tempos are windowed and averaged so as to smooth out any changes.

### Beat

Using librosa's beat_track, Mark knows when the last beat played in a given chunk. That information + tempo are used to calculate the theorical next beat when playing back a response.

## Musical Response

Like the name suggest, Mark uses Markov chains to create a musical response using data provided by the improviser. 

### Transition Matrix

Before generating the response, a transition matrix is created using the last X pitches recorded. This way the reponse is always informed by the latest information from the improviser.

### Phrases

Mark responds with quarter note phrases of differing lengths. The tempo is an average of the last X recorded tempos. Before the prhasse is played, the program waits (using pygame's time delay) for the start of another beat instead of just plaing directly after being created.

## Thank you

I will continue to refine this application. Feel free to reach out if you have any questions and please reach out if you have suggestions/advice.


