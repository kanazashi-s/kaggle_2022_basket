import data


def main():
    data.unzip_raw_data.main()

    data.make_base_csv.make_train()
    data.make_base_csv.make_test()
    data.make_base_csv.make_submission()

    data.make_switched_dataset.make_all()

if __name__ == '__main__':
    main()
