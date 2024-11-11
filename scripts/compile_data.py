from icst.definitions import RESOURCES_DIR

if __name__ == "__main__":
    filepath = RESOURCES_DIR / "trials" / "raw_data_compressed" / "expansion"
    files = [file.name for file in filepath.rglob("*.txt") if file.is_file()]
    files = sorted(files, key=lambda x: int(x.split("_")[1].split(".")[0]))

    with open(RESOURCES_DIR / "statistics" / "stats.txt", 'w') as stats:
        for i in range(len(files) - 1):
            with open(filepath / files[i], "rb") as file:
                file.seek(-2, 2)
                while file.read(1) != b"\n":
                    file.seek(-2, 1)

                last_line = file.readline().decode()

            data = last_line.split(';')
            stats.write(data[1] + '\n')
