new_file = ""
new_first_line = "Title, Group, GitHub\n"
with open("./roadmap.txt", "r") as file:
    for line in file.readlines():
        path = line.strip()
        group, title = path.rsplit("/", 1)
        github_link = (
            f"https://github.com/ryndovaira-org/data_science_notes/tree/main/{path}"
        )
        group_num, group_name = group.split("_", 1)
        title_num, title_name = title.split("_", 1)
        if len(group_num) == 0 or len(title_num) == 0:
            continue
        new_file += f"{title}, {group}, {github_link}\n"

with open("./roadmap_notion.csv", "w") as file:
    file.write(new_first_line + new_file)
