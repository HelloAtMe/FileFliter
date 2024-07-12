# -*- coding: utf-8 -*-
"""
@ File         : filterfiles.py
@ Author       : Wcy
@ Contact      : 
@ Date         : 2024-01-03 11:08:47
@ Description  : 
"""

import pathlib

FILE_SIZE_1MB = 1024 # megabytes = 1024 * bytes


class FileFilter:
    def __init__(self, root_dir=pathlib.Path.cwd()):
        '''
        Locate all eligible files in the specified
        root directory
        '''
        self._root_dir = root_dir
        self._files = []
        self._filter_engine = None

    def scan_dir(self, path: pathlib.Path):
        # Find videos in current directory
        for x in path.iterdir():
            if x.is_file():
                if self._filter_engine(x):
                    self._files.append(x)
            elif x.is_dir():
                self.scan_dir(x)
            else:
                pass

    def set_root_dir(self, root_dir: str| pathlib.Path):
        if isinstance(root_dir, str):
            root_dir = pathlib.Path(root_dir)
        self._root_dir = root_dir

    def set_filter_engine(self, engine: callable):
        self._filter_engine = engine

    def start(self):
        if self._filter_engine is None:
            raise Exception('There is no filter engine.')
        
        self._files = []
        self.scan_dir(self._root_dir)

    def result(self) -> list:
        return self._files


def filter_engine_for_bigsize_videos(fn: pathlib.Path) -> bool:
    if fn.suffix.lower() in ['.mp4', '.avi', '.mov', '.wmv', '3gp', '.rmvb', '.flv'] \
        and fn.stat().st_size > FILE_SIZE_1MB * 600:
        return True
    return False
    

def move_action(dest: pathlib.Path|str, srcs: list):
    # Copy the filtered files to the specified directory
    # create destination directory, if not exist
    dest.mkdir(511, True, True)

    print(f'Find {len(srcs)} files in total.')
    x: pathlib.Path
    for n, x in enumerate(srcs):
        print(f'Move {n+1} name: {x.name} ...')
        x.rename(dest / x.name)


def main():
    root_dir = pathlib.Path('.')
    dest_dir = pathlib.Path('video')
    obj_filter = FileFilter()
    print('Set root directory.')
    obj_filter.set_root_dir(root_dir)
    print('Set engine.')
    obj_filter.set_filter_engine(filter_engine_for_bigsize_videos)
    print('Start filtering files.')
    obj_filter.start()
    print('Move filtered files.')
    move_action(dest_dir, obj_filter.result())
    print('Success.')


def test():
    # Watch the file attributes
    fn = pathlib.Path(__file__)
    print(fn.stat())


if __name__ == '__main__':
    # test()
    main()
