# Mark E. Markov

AI improvisation buddy. You play music, Mark listens to you and plays something similar back in real time.

## Feature extraction

Mark uses Librosa to pull pitch, beat and tempo data from the audio stream.

### Pitch

Onsets are calculated. Using pyin, Mark determines if the note is voiced and its average frequency.

### Tempo

Tempos are windowed and averaged so as to smooth out any abrupt changes.

### Beat

Using librosa's beat_track, Mark knows when the last beat is played within a given chunk. That information + tempo are used to calculate the theoretical next beat when playing back a response.

## Musical Response

Like the name suggest, Mark uses Markov chains to create a musical response using data provided by the improviser.

### Transition Matrix

Before generating the response, a transition matrix is created using the last X pitches recorded. This way the response is always informed by the latest information from the improviser.

### Phrases

Mark responds with quarter note phrases of differing lengths. The tempo is an average of the last X recorded tempos. Instead of playing the phrase directly after it is created the program waits (using pygame's time delay) for the start of the next beat.

## Thank you

I will continue to refine this application. Please reach out if you have any suggestions/thoughts/advice.
