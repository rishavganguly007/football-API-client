from footballAPIClient import footballAPI


def main():
    fp = footballAPI.FootballAPI("b8739683c92735d420273b664380febc")
    # print(fp.get_timezone())
    print(fp.get_leagues_seasons())


if __name__ == "__main__":
    main()
