Installation:
create a python virtual environment
then run 
pip install -r requirements.txt

Useage:

Takes 2 necessary arguments;
first argument must be the folder path
second argument must be the compression quality (0 to 100)

e.g.
To compress the images in the entire folder to quality 75 run:

python3 ImageCompressor.py /path/to/images/folder 75

To See what's really happening, use -v arg
python3 ImageCompressor.py /path/to/images/folder 75 -v

To run the process in multiple threads (is faster)
python3 ImageCompressor.py /path/to/images/folder 75 -v --threads

By default png images aren't compressed. you can convert them to webp and then compress

python3 ImageCompressor.py /path/to/images/folder 75 -v --threads --convert


