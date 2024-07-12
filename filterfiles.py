import pathlib
from typing import List, Callable


class FileFilter:
    def __init__(self, root_dir: pathlib.Path = pathlib.Path.cwd()):
        self.root_dir = root_dir
        self.files = []
        self.filter_engine: Callable = None

    def scan_dir(self):
        for path in self.root_dir.rglob('*'):
            if path.is_file() and self.filter_engine(path):
                self.files.append(path)

    def set_filter_engine(self, engine: Callable):
        self.filter_engine = engine

    def start(self):
        if self.filter_engine is None:
            raise ValueError('Filter engine is not set.')
        self.files.clear()
        self.scan_dir()

    def get_files(self) -> List[pathlib.Path]:
        return self.files


def filter_engine_for_bigsize_videos(file_path: pathlib.Path) -> bool:
    video_extensions = ('.mp4', '.avi', '.mov', '.wmv', '.3gp', '.rmvb', '.flv')
    file_size_1mb = 1024 * 1024  # Correct definition of 1 MB
    return file_path.suffix.lower() in video_extensions and file_path.stat().st_size > file_size_1mb * 600


def move_files(destination: pathlib.Path, sources: List[pathlib.Path]):
    destination.mkdir(parents=True, exist_ok=True)

    print(f'Found {len(sources)} files in total.')
    for index, source in enumerate(sources, start=1):
        print(f'Moving {index}: {source.name}...')
        # destination.joinpath(source.name).write_bytes(source.read_bytes())
        source.rename(destination.joinpath(source.name))


def main():
    root_dir = pathlib.Path('.')
    dest_dir = pathlib.Path('video')
    file_filter = FileFilter(root_dir=root_dir)
    file_filter.set_filter_engine(filter_engine_for_bigsize_videos)
    file_filter.start()
    move_files(dest_dir, file_filter.get_files())
    print('Operation completed successfully.')


if __name__ == '__main__':
    main()