from PIL import Image, UnidentifiedImageError
from threading import Thread
import subprocess as sp
import os
import sys
import time
from pathlib import Path
from termcolor.termcolor import colored


def get_filename(path):
    filename = path.split('/').pop()
    return filename  # , *(filename.split('.'))


def list_files(folder_path):
    run = sp.run(['find', folder_path], capture_output=True)
    return run.stdout.decode('utf-8').strip().split('\n')


def get_destination_file(base_path, file_path):
    new_dest = f'{base_path}/adjusted'
    return f"{new_dest}{file_path.replace(base_path, '')}"


def readjust_image(base_path, img_path, quality=50, dpi=(72, 72), format='', size='', verbose=False):
    try:
        with Image.open(img_path) as img:
            img_size = size or img.size
            img_format = format or img.format

            destination_file = get_destination_file(base_path, img_path)

            # create destination folder if not exist
            path = Path(destination_file)
            path = path.parent
            path.mkdir(parents=True, exist_ok=True)

            img = img.resize(img_size, Image.Resampling.LANCZOS)
            img.save(destination_file, img_format, optimize=True, quality=quality, dpi=dpi, lossless=False)

            if verbose:
                text = f"{img_path} >> {destination_file}"
                print(colored(text, 'green'))

    except UnidentifiedImageError:
        text = f"Un-Processable: {img_path}"
        print(colored(text, 'red'))


def help_text():
    return '''
        ImageCompressor <source_folder> <verbose>(opt) <quality>(opt)
        e.g.: ImageCompressor /home/doruk/Pictures -v 80 
'''


def execute_in_threads(folder_path, quality, verbose):
    total_threads = 8

    files = list_files(folder_path)

    total_threads = min(len(files), total_threads)
    chunk_size = len(files) // total_threads
    threads = []

    def perform_task(start_index, end_index):
        for fl_index in range(start_index, end_index):
            fl = files[fl_index]

            if os.path.isfile(fl):
                readjust_image(folder_path, fl, quality=int(quality), verbose=verbose, dpi=(300, 300))

    for i in range(0, total_threads):
        start_pos = i * chunk_size
        end_pos = (start_pos + chunk_size + len(files) % total_threads) \
            if (i == total_threads - 1) \
            else start_pos + chunk_size

        threads.append(
            Thread(target=perform_task, args=(start_pos, end_pos))
        )

    for item in threads:
        item.start()

    for item in threads:
        item.join()


def execute(folder_path, quality, verbose):
    for fl in list_files(folder_path):
        if os.path.isfile(fl):
            readjust_image(folder_path, fl, quality=int(quality), verbose=verbose, dpi=(300, 300))


def main():
    args = sys.argv
    if len(args) < 2:
        print(help_text())
        exit('no source directory given')

    folder_path = args[1][0:-1] if args[1][-1] == '/' else args[1]

    quality = args[2] if len(args) > 2 else 80
    verbose = '-v' in args
    parallel = '--threads' in args

    if (not os.path.exists(folder_path)) or (not os.path.isdir(folder_path)):
        exit('given path must be a directory')

    # create destination folder if not exist
    dest_path = f"{folder_path}/adjusted"
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    start = time.time()
    if parallel:
        execute_in_threads(folder_path, quality, verbose)
    else:
        execute(folder_path, quality, verbose)
    end = time.time()

    print(f'Completed in: {end - start} Seconds')


if __name__ == "__main__":
    main()

