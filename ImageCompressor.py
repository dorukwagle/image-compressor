from PIL import Image
import os
import sys
import time
from threading import Thread


def get_parent_dir(path):
    pth = path.split('/')
    pth.pop()
    return '/'.join(pth)


def get_filename(path):
    filename = path.split('/').pop()
    return filename  # , *(filename.split('.'))


def readjust_image(img_path, quality=50, dpi=(72, 72), format='', size='', verbose=False):
    with Image.open(img_path) as img:
        img_size = size or img.size
        img_format = format or img.format

        parent_dir = get_parent_dir(img_path)
        filename = get_filename(img_path)
        new_path = parent_dir + '/adjusted'

        if not os.path.exists(new_path):
            os.mkdir(new_path)

        destination_file = f'{new_path}/{filename}'

        img = img.resize(img_size, Image.Resampling.LANCZOS)
        img.save(destination_file, img_format, optimize=True, quality=quality, dpi=dpi, lossless=False)

        if verbose:
            print(img_path, ' >> ', destination_file)


def help():
    return '''
        ImageCompressor <source_folder> <verbose>(opt) <quality>(opt)
        e.g.: ImageCompressor /home/doruk/Pictures -v 80 
'''


def execute_in_threads(folder_path, quality, verbose):
    total_threads = 8

    files = os.listdir(folder_path)

    total_threads = min(len(files), total_threads)
    chunk_size = len(files) // total_threads
    threads = []

    def perform_task(start_index, end_index):
        for fl_index in range(start_index, end_index):
            fl = f'{folder_path}/{files[fl_index]}'

            if os.path.isfile(fl):
                readjust_image(fl, quality=int(quality), verbose=verbose, dpi=(300, 300))

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
    for fl in os.listdir(folder_path):
        fl = f'{folder_path}/{fl}'

        if os.path.isfile(fl):
            readjust_image(fl, quality=int(quality), verbose=verbose, dpi=(300, 300))


def main():
    args = sys.argv
    if len(args) < 2:
        print(help())
        exit('no source directory given')

    folder_path = args[1]
    quality = args[2] if len(args) > 2 else 80
    verbose = '-v' in args
    parallel = '--threads' in args

    if (not os.path.exists(folder_path)) or (not os.path.isdir(folder_path)):
        exit('given path must be a directory')

    start = time.time()
    if parallel:
        execute_in_threads(folder_path, quality, verbose)
    else:
        execute(folder_path, quality, verbose)
    end = time.time()

    print(f'Completed in: {end - start} Seconds')


if __name__ == "__main__":
    main()

