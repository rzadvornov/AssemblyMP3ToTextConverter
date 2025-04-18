from pathlib import Path
from typing import Union

__all__ = [
    'clear_directory_files',
]


def clear_directory_files(
    directory_path: Union[str, Path],
    empty_subfolders: bool = False
) -> list:
    """Irreversibly removes all files inside the specified directory. Optionally
    clears subfolders from files too. Returns a list with paths Python lacks
    permission to delete."""
    if empty_subfolders:
        directory_items = Path(directory_path).rglob("*")
    else:
        directory_items = Path(directory_path).glob("*")

    erroneous_paths = []

    for file_path in (path_object for path_object in directory_items
                      if path_object.is_file()):
        try:
            file_path.unlink()
        except PermissionError:
            erroneous_paths.append(file_path)
    return erroneous_paths
