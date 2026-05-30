import os
import pathlib

print(os.getcwd())

first_level_dir_path = pathlib.Path("M2/Session12/first_level")
second_level_dir_path = first_level_dir_path / "second_level"

os.makedirs(second_level_dir_path, exist_ok=True)

print(os.listdir(first_level_dir_path))

second_level_dir_path.rmdir()