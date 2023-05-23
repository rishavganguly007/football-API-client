from footballAPIClient import footballAPI


def main():
    fp = footballAPI.FootballAPI("API_KEY")
    print(fp.get_countries())


if __name__ == "__main__":
    main()
