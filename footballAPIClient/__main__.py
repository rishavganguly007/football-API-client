from footballAPIClient import footballAPI


def main():
    fp = footballAPI.FootballAPI("b8739683c92735d420273b664380febc")
    # print(fp.get_timezone())
    print(fp.get_teams_information(id=4))


if __name__ == "__main__":
    main()
