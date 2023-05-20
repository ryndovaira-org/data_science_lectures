from db_manager import DBManager


def option_table_list():
    ...


def option_table_data():
    ...


options = {'Show the table list': DBManager.show_table_list,
           'Show the table data': option_table_data}


def main():
    print('Введите номер варианта и нажмите Enter:')
    for i, option in enumerate(options):
        print(f'{i} - {option}')

    option_num = int(input())
    if 0 <= option_num < len(options):
        list(options.values())[option_num]()


if __name__ == '__main__':
    main()
