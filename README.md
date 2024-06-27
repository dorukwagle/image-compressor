Installation:
create a python virtual environment
then run 
pip install -r requirements.txt

**Useage:**

Takes 2 necessary arguments;
first argument must be the folder path
second argument must be the compression quality (0 to 100)

e.g.
To compress the images in the entire folder to quality 75 run:

_python3 ImageCompressor.py /path/to/images/folder 75_

To See what's really happening, use -v arg <br>
_python3 ImageCompressor.py /path/to/images/folder 75 -v_

To run the process in multiple threads (is faster) <br>
_python3 ImageCompressor.py /path/to/images/folder 75 -v --threads_

By default png images aren't compressed. you can convert them to webp and then compress
<br>
_python3 ImageCompressor.py /path/to/images/folder 75 -v --threads --convert_


