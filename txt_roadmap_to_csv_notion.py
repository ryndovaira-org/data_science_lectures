new_file = ""
new_first_line = "1, 2, 3, 4\n"
with open("C:/Users/Mi/Desktop/roadmap.txt", "r") as file:
    for line in file.readlines():
        path = line.strip()
        tmp = path.replace("/", ", ", 2).split(", ")
        github_link = (
            f"https://github.com/ryndovaira-org/data_science_notes/tree/main/{path}"
        )
        new_file += f"{tmp[0]}, {tmp[2]}, {tmp[1]}, {github_link}\n"

with open("C:/Users/Mi/Desktop/roadmap_new.csv", "w") as file:
    file.write(new_first_line + new_file)
