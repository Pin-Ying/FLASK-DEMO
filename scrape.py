import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_stocks():
    try:
        url = "https://histock.tw/%E5%9C%8B%E9%9A%9B%E8%82%A1%E5%B8%82"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text.split("<h3>今年以來</h3>")[1], "lxml")
        trs = soup.find("div", class_="index-list").find_all("tr")
        datas = []
        for tr in trs:
            data = []
            for th in tr.find_all("th"):
                # print(th.text)
                data.append(th.text)
            for td in tr.find_all("td"):
                # print(td.text)
                data.append(td.text)
            datas.append(data)
        return datas
    except Exception as e:
        print(e)
    return None


def scrape_pm25(sort=False, ascending=True):
    try:
        url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=JSON"
        datas = requests.get(url).json()["records"]
        df = pd.DataFrame(datas)
        df = df[df["pm25"]!=""]
        df["pm25"] = df["pm25"].apply(lambda x: eval(x) if x else 0)

        if sort:
            df = df.sort_values("pm25", ascending=ascending)

        columns = df.columns
        values = df.values

        return columns, values
    except Exception as e:
        print(e)
    return None, 404


def get_pm25_json():
    values = scrape_pm25()[1]
    xdata = [value[0] for value in values]
    ydata = [value[2] for value in values]

    json_data = {"site": xdata, "pm25": ydata}
    return json_data


if __name__ == "__main__":
    print(scrape_pm25())
