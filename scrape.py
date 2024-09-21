import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://data.moenv.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate desc&format=JSON"
six_countys = ["臺北市", "新北市", "桃園市", "臺中市", "臺南市", "高雄市"]
df = None


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


def convert_value(num):
    try:
        return eval(num)
    except:
        # 將非正常數值轉換成None
        return None


def get_pm25_data():
    global df
    try:
        if df is None:
            datas = requests.get(url).json()["records"]
            df = pd.DataFrame(datas)
            df["pm25"] = df["pm25"].apply(convert_value)
            # 移除有None的數據
            df = df.dropna()
        return df
    except Exception as e:
        return str(e)


def scrape_six_pm25():
    pm25s = []
    try:
        df = get_pm25_data()
        datas = []
        for county in six_countys:
            pm25_avg = df.groupby("county").get_group(county)["pm25"].mean()
            pm25s.append(round(pm25_avg, 2))

        columns = six_countys
        values = pm25s

        return columns, values
    except Exception as e:
        print(e)
    return None, 404


def get_six_pm25_json():
    xdata, ydata = scrape_six_pm25()
    json_data = {"site": xdata, "pm25": ydata}
    return json_data


def scrape_pm25(sort=False, ascending=True):
    try:
        df = get_pm25_data()
        if sort:
            df = df.sort_values("pm25", ascending=ascending)
        columns = df.columns
        values = df.values

        return columns, values
    except Exception as e:
        print(e)
    return None, 404


def get_pm25_json():
    columns, values = scrape_pm25()
    xdata = [value[0] for value in values]
    ydata = [value[2] for value in values]

    json_data = {"site": xdata, "pm25": ydata}
    datas = list(zip(xdata, ydata))
    datas = sorted(datas, key=lambda x: x[1])

    json_data = {"site": xdata, "pm25": ydata, "highest": datas[-1], "lowest": datas[0]}
    return json_data


if __name__ == "__main__":
    print(get_pm25_json())
