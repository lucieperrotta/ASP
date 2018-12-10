ASP Project: Designing an Auto-Wah for guitar
Lucie Perrotta and Simon Guilloud

Abstract
In this project, we design and implement an Auto-Wah effect for music instruments. The Auto-Wah effect gained popularity in the early 70s as many rock guitar players and Jazz trumpet players used it live, allowing them to activate the pedal and move on the scene, giving considerable practicality over the famous traditional Wah pedal which needs the player to tune-it using a foot switch while using it. On top of that it can variate much more rapidly than what a human can do. The Auto-Wah, as known as dynamic filter, is a time-varying bandpass filter, and is here synthetized using an IIR Dynamic Filter tuned according to the envelope of the signal: the louder the signal, the higher the peak and cutoff frequency of the lowpass filter.

Use
You have three main ways to use our Algorithm. You can either use the jupyter notebook, import the file AutoWah or directly run AutoWahExecute to have an interface to modify your file without code.
In the first two cases, doc is included in the files.

If you use the graphic module, here are the parameters explanations.
Parameters:
    Input File = The filename (or path) of a wav file.
	Save To = The filename (or path) you want to save the result to.
    maximum = The maximum value (in herz) the filter will cut too. Everything higher than that will always be cut.
    minimum = The minimum value (in herz) the filter will cut too. Everything lower than that will never be cut.
    peak = Uncheck if you want the filter will only be lowpass without the resonante component.
    p = Height of the peak. It set to zero, equivalent to peak unchecked