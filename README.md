# Producer Consumer Lab

	Within this lab we were to use the files of ExtractFrames.py, ConvertToGrayscale.py, and DisplayFrames.py in order to obtain a video and have it play in greyscale. The assignment given consisted of the using of threads and locks in order to create an efficient process where as these files are able to play simeoltaneously, in an orderly fashion, of which I used the given code from the "ExtractAndDisplay.py" file and simply changed certain aspects of the file in order to create 3 seperate synchronized threads, which is basically the process of a Producer Consumer, where the Producer part consisted of the extraction and conversion, and the consumer consisted of the conversion and displaying the frames.
	
	The following resources were used in order for the attempt of this assignment:
		* Provided resource code for the video.
		* Using notes from given examples from Dr.Freudenthal's concerning locks and queues.
		* Used the following sites as references:
			- https://pymbook.readthedocs.io/en/latest/classes.html
			- https://docs.python.org/3.4/library/threading.html