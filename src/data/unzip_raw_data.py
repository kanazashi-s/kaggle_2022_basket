import zipfile
import pathlib


def main():
    input_path = pathlib.Path("data", "raw", "mens-march-mania-2022.zip")

    output_path = pathlib.Path("data", "raw")
    with zipfile.ZipFile(input_path, 'r') as f:
        f.extractall(output_path)

if __name__ == "__main__":
    main()