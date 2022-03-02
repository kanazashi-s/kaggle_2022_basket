import data.unzip_raw_data
import data.make_base_csv


def main():
    data.unzip_raw_data.main()

    data.make_base_csv.make_train()
    data.make_base_csv.make_test()


if __name__ == '__main__':
    main()
