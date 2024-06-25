import pandas as pd
import json
from tqdm import tqdm
from src.server import forecasting_constants as constants
import math


def load_data(contracts_data_path, item_property_store):
    zakupki_df = pd.read_excel(contracts_data_path)
    zakupki_df = zakupki_df.dropna(how='all')
    zakupki_df = zakupki_df[zakupki_df['Статус контракта'] == 'Исполнен']

    with open(item_property_store, 'r', encoding='utf-8') as file:
        spgz_store = json.load(file)
    return zakupki_df, spgz_store

def process_dara(zakupki_df):
    common_data = zakupki_df[["ID СПГЗ", "Наименование СПГЗ", "Реестровый номер в РК", "Срок исполнения с", "Срок исполнения по", "Цена ГК, руб.", "Конечный код КПГЗ"]]
    common_data["ID СПГЗ"] = common_data["ID СПГЗ"].astype("int")
    common_data["is_service"] = common_data["Конечный код КПГЗ"].map(is_service)
    common_data['Срок исполнения с'] = pd.to_datetime(common_data['Срок исполнения с'], format='%d.%m.%Y')
    common_data['Срок исполнения по'] = pd.to_datetime(common_data['Срок исполнения по'], format='%d.%m.%Y')
    common_data["Наименование СПГЗ"] = common_data["Наименование СПГЗ"].apply(lambda x: x.strip())



    common_data_items = common_data.query("is_service == False")

    common_data_items['is_used_in_2022'] = common_data_items['Срок исполнения с'].dt.year == 2022

    common_data_items['is_used_in_last_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 10 and x.month <= 12)
    common_data_items['is_used_in_last_2_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 6 and x.month <= 12)

    common_data_items['is_ended_in_last_quarter_2022'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2022 and x.month >= 10 and x.month <= 12)
    common_data_items['is_ended_in_1_quarter_2023'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 1 and x.month <= 3)
    common_data_items['is_ended_in_next_2_quarter_2023'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 1 and x.month <= 6)

    common_data_items['is_ended_in_next_1st_quarter_2023'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 1 and x.month <= 3)
    common_data_items['is_ended_in_next_2nd_quarter_2023'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 4 and x.month <= 6)
    common_data_items['is_ended_in_next_3rd_quarter_2023'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 7 and x.month <= 9)
    common_data_items['is_ended_in_next_4rd_quarter_2023'] = common_data_items['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 9 and x.month <= 12)
    common_data_items['is_used_in_1st_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 1 and x.month <= 3)
    common_data_items['is_used_in_2st_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 4 and x.month <= 6)
    common_data_items['is_used_in_3st_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 8 and x.month <= 9)
    common_data_items['is_used_in_4st_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 10 and x.month <= 12)
    common_data_items['is_used_in_first_2st_quarter_2022'] = common_data_items['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 1 and x.month <= 6)



    common_data_items["used_count"] = common_data_items['Наименование СПГЗ'].map(common_data_items['Наименование СПГЗ'].value_counts())


    mask = (common_data_items["Срок исполнения с"] >= "2022-01-01") & (common_data_items["Срок исполнения с"] <= "2022-03-31")
    filtered_df = common_data_items[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_1st_quarts_2022")
    common_data_items = common_data_items.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_items["count_1st_quarts_2022"] = common_data_items["count_1st_quarts_2022"].fillna(0).astype(int)

    mask = (common_data_items["Срок исполнения с"] >= "2022-04-01") & (common_data_items["Срок исполнения с"] <= "2022-06-30")
    filtered_df = common_data_items[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_2st_quarts_2022")
    common_data_items = common_data_items.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_items["count_2st_quarts_2022"] = common_data_items["count_2st_quarts_2022"].fillna(0).astype(int)

    mask = (common_data_items["Срок исполнения с"] >= "2022-07-01") & (common_data_items["Срок исполнения с"] <= "2022-09-30")
    filtered_df = common_data_items[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_3st_quarts_2022")
    common_data_items = common_data_items.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_items["count_3st_quarts_2022"] = common_data_items["count_3st_quarts_2022"].fillna(0).astype(int)

    mask = (common_data_items["Срок исполнения с"] >= "2022-09-01") & (common_data_items["Срок исполнения с"] <= "2022-12-31")
    filtered_df = common_data_items[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_4st_quarts_2022")
    common_data_items = common_data_items.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_items["count_4st_quarts_2022"] = common_data_items["count_4st_quarts_2022"].fillna(0).astype(int)


    common_data_service= common_data.query("is_service == True")

    common_data_service['is_used_in_2022'] = common_data_service['Срок исполнения с'].dt.year == 2022

    common_data_service['is_used_in_last_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 10 and x.month <= 12)
    common_data_service['is_used_in_last_2_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 6 and x.month <= 12)

    common_data_service['is_ended_in_last_quarter_2022'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2022 and x.month >= 10 and x.month <= 12)
    common_data_service['is_ended_in_1_quarter_2023'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 1 and x.month <= 3)
    common_data_service['is_ended_in_next_2_quarter_2023'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 1 and x.month <= 6)

    common_data_service['is_ended_in_next_1st_quarter_2023'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 1 and x.month <= 3)
    common_data_service['is_ended_in_next_2nd_quarter_2023'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 4 and x.month <= 6)
    common_data_service['is_ended_in_next_3rd_quarter_2023'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 7 and x.month <= 9)
    common_data_service['is_ended_in_next_4rd_quarter_2023'] = common_data_service['Срок исполнения по'].apply(lambda x: x.year == 2023 and x.month >= 9 and x.month <= 12)
    common_data_service['is_used_in_1st_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 1 and x.month <= 3)
    common_data_service['is_used_in_2st_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 4 and x.month <= 6)
    common_data_service['is_used_in_3st_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 8 and x.month <= 9)
    common_data_service['is_used_in_4st_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 10 and x.month <= 12)
    common_data_service['is_used_in_first_2st_quarter_2022'] = common_data_service['Срок исполнения с'].apply(lambda x: x.year == 2022 and x.month >= 1 and x.month <= 6)

    common_data_service["used_count"] = common_data_service['Наименование СПГЗ'].map(common_data_service['Наименование СПГЗ'].value_counts())


    mask = (common_data_service["Срок исполнения с"] >= "2022-01-01") & (common_data_service["Срок исполнения с"] <= "2022-03-31")
    filtered_df = common_data_service[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_1st_quarts_2022")
    common_data_service = common_data_service.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_service["count_1st_quarts_2022"] = common_data_service["count_1st_quarts_2022"].fillna(0).astype(int)

    mask = (common_data_service["Срок исполнения с"] >= "2022-04-01") & (common_data_service["Срок исполнения с"] <= "2022-06-30")
    filtered_df = common_data_service[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_2st_quarts_2022")
    common_data_service = common_data_service.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_service["count_2st_quarts_2022"] = common_data_service["count_2st_quarts_2022"].fillna(0).astype(int)

    mask = (common_data_service["Срок исполнения с"] >= "2022-07-01") & (common_data_service["Срок исполнения с"] <= "2022-09-30")
    filtered_df = common_data_service[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_3st_quarts_2022")
    common_data_service = common_data_service.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_service["count_3st_quarts_2022"] = common_data_service["count_3st_quarts_2022"].fillna(0).astype(int)

    mask = (common_data_service["Срок исполнения с"] >= "2022-09-01") & (common_data_service["Срок исполнения с"] <= "2022-12-31")
    filtered_df = common_data_service[mask]
    count_df = filtered_df.groupby("Наименование СПГЗ").size().reset_index(name="count_4st_quarts_2022")
    common_data_service = common_data_service.merge(count_df, on="Наименование СПГЗ", how="left")
    common_data_service["count_4st_quarts_2022"] = common_data_service["count_4st_quarts_2022"].fillna(0).astype(int)

    common_data_service["amount_average"] = (common_data_service["count_1st_quarts_2022"] + common_data_service["count_2st_quarts_2022"] + common_data_service["count_3st_quarts_2022"] + common_data_service["count_4st_quarts_2022"]) / 4
    common_data_service["amount_average"] = common_data_service["amount_average"].apply(lambda x: math.ceil(x))

    return common_data_service, common_data_items


def calcucate_score_common(row, quartal: int = 1, type = "item"):
    score = 0.0
    explanation = []

    if row["is_used_in_first_2st_quarter_2022"]:
        score += 0.5
        if quartal < 3:
            score += 0.5
        if type == "item":
            explanation.append("Контракт по товару заключался в первой половине 2022 года")
        else:
            explanation.append("Услуга использовалась в первой половине 2022 года")

    if row["is_used_in_1st_quarter_2022"] and quartal == 1:
        score += 1.0
        if type == "item":
            explanation.append("Контракт по товару заключался в первом квартале 2022 года")
        else:
            explanation.append("Услуга использовалась в первом квартале 2022 года")

    elif row["is_used_in_2st_quarter_2022"] and quartal == 2:
        score += 1.0
        if type == "item":
            explanation.append("Контракт по товару заключался во втором квартале 2022 года")
        else:
            explanation.append("Услуга использовалась во втором квартале 2022 года")
    elif row["is_used_in_3st_quarter_2022"] and quartal == 3:
        score += 1.0
        if type == "item":
            explanation.append("Контракт по товару заключался в третьем квартале 2022 года")
        else:
            explanation.append("Услуга использовалась в третьем квартале 2022 года")
    elif row["is_used_in_4st_quarter_2022"] and quartal == 4:
        score += 1.0
        if type == "item":
            explanation.append("Контракт по товару заключался в четвертом квартале 2022 года")
        else:
            explanation.append("Услуга использовалась в четвертом квартале 2022 года")


    if row["is_ended_in_next_1st_quarter_2023"] and quartal == 1:
        score += 3.0
        if type == "item":
            explanation.append("Контракт по товару истекает в первом квартале 2023 года")
        else:
            explanation.append("Услуга истекает в первом квартале 2023 года")
    if row["is_ended_in_next_2nd_quarter_2023"] and quartal == 2:
        score += 3.0
        if type == "item":
            explanation.append("Контракт по товару истекает во втором квартале 2023 года")
        else:
            explanation.append("Услуга истекает во втором квартале 2023 года")
    if row["is_ended_in_next_3rd_quarter_2023"] and quartal == 3:
        score += 3.0
        if type == "item":
            explanation.append("Контракт по товару истекает в третьем квартале 2023 года")
        else:
            explanation.append("Услуга истекает в третьем квартале 2023 года")
    if row["is_ended_in_next_4rd_quarter_2023"] and quartal == 4:
        score += 3.0
        if type == "item":
            explanation.append("Контракт по товару истекает в четвертом квартале 2023 года")
        else:
            explanation.append("Услуга истекает в четвертом квартале 2023 года")
    if row["count_1st_quarts_2022"] >= 3:
        score += 1.0
        if quartal == 1:
            score += 2.0
        if type == "item":
            explanation.append(f"Контракт по товару заключался {row['count_1st_quarts_2022']} раз в первом квартале 2022 года")
        else:
            explanation.append(f"Услуга заключалась {row['count_1st_quarts_2022']} раз в первом квартале 2022 года")
    if row["count_2st_quarts_2022"] >= 3:
        score += 1.0
        if quartal == 2:
            score += 2.0
        if type == "item":
            explanation.append(f"Контракт по товару заключался {row['count_2st_quarts_2022']} раз во втором квартале 2022 года")
        else:
            explanation.append(f"Услуга заключалась {row['count_2st_quarts_2022']} раз во втором квартале 2022 года")
    if row["count_3st_quarts_2022"] >= 3:
        score += 1.0
        if quartal == 3:
            score += 2.0
        if type == "item":
            explanation.append(f"Контракт по товару заключался {row['count_3st_quarts_2022']} раз в третьем квартале 2022 года")
        else:
            explanation.append(f"Услуга заключалась {row['count_3st_quarts_2022']} раз в третьем квартале 2022 года")
    if row["count_4st_quarts_2022"] >= 3:
        score += 1.0
        if quartal == 4:
            score += 2.0
        if type == "item":
            explanation.append(f"Контракт по товару заключался {row['count_4st_quarts_2022']} раз в четвертом квартале 2022 года")
        else:
            explanation.append(f"Услуга заключалась {row['count_4st_quarts_2022']} раз в четвертом квартале 2022 года")

    if row["used_count"] >= 7:
        score += 2.0
        if type == "item":
            explanation.append(f"Товар приобретался {row['used_count']} раз")

    return score, explanation


def is_service(kpgz_code):
    code = kpgz_code.split(".")[0]
    if code == "01":
        return False
    elif code == "02" or code == "03":
        return True
    else:
        None

def find_dict_by_name(dict_list, query, explanation):
    """
    Функция находит и возвращает первый словарь из списка, где значение ключа 'name' совпадает с query.

    :param dict_list: Список словарей, содержащих ключ 'name'
    :param query: Строка для поиска в ключе 'name'
    :return: Словарь, если значение найдено, иначе None
    """
    for d in dict_list:
        if d.get('name').lower().replace(",", "").replace(" ", "").replace(".", "") == query.lower().replace(",", "").replace(" ", "").replace(".", ""):
            d["Объяснение"] = explanation
            return d
    return None

def predictions(common_data_service, common_data_items, spgz_store):
    common_data_items[["score", "explanation"]] = common_data_items.apply(lambda row: pd.Series(calcucate_score_common(row, 1)), axis=1)
    recs_items_1rst_quartal = common_data_items.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    recs_items_1rst_quartal_filtered = recs_items_1rst_quartal[:50]
    recs_items_1rst_quartal_filtered = recs_items_1rst_quartal_filtered.query("score > 0.0")


    common_data_items[["score", "explanation"]] = common_data_items.apply(lambda row: pd.Series(calcucate_score_common(row, 2)), axis=1)
    recs_items_2nd_quartal = common_data_items.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    used = set(recs_items_1rst_quartal["Наименование СПГЗ"][:50].tolist())
    recs_items_2nd_quartal_filtered = recs_items_2nd_quartal[~recs_items_2nd_quartal["Наименование СПГЗ"].isin(set(recs_items_1rst_quartal["Наименование СПГЗ"][:50].tolist()))].sort_values("score", ascending=False)[:50]
    recs_items_2nd_quartal_filtered = recs_items_2nd_quartal_filtered.query("score > 0.0")

    common_data_items[["score", "explanation"]] = common_data_items.apply(lambda row: pd.Series(calcucate_score_common(row, 3)), axis=1)
    recs_items_3rd_quartal = common_data_items.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    used = set(recs_items_2nd_quartal_filtered["Наименование СПГЗ"][:50].tolist()) | set(recs_items_1rst_quartal["Наименование СПГЗ"][:50].tolist())
    recs_items_3rd_quartal_filtered = recs_items_3rd_quartal[~recs_items_3rd_quartal["Наименование СПГЗ"].isin(used)].sort_values("score", ascending=False)[:50]
    recs_items_3rd_quartal_filtered = recs_items_3rd_quartal_filtered.query("score > 0.0")


    common_data_items[["score", "explanation"]] = common_data_items.apply(lambda row: pd.Series(calcucate_score_common(row, 4)), axis=1)
    used = set(recs_items_2nd_quartal_filtered["Наименование СПГЗ"][:50].tolist()) | set(recs_items_1rst_quartal["Наименование СПГЗ"][:50].tolist()) | set(recs_items_3rd_quartal_filtered["Наименование СПГЗ"][:50].tolist())
    recs_items_4th_quartal = common_data_items.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    recs_items_4th_quartal_filtered = recs_items_4th_quartal[~recs_items_4th_quartal["Наименование СПГЗ"].isin(used)].sort_values("score", ascending=False)[:50]
    recs_items_4th_quartal_filtered = recs_items_4th_quartal_filtered.query("score > 0.0")



    common_data_service[["score", "explanation"]] = common_data_service.apply(lambda row: pd.Series(calcucate_score_common(row, 1, "service")), axis=1)
    recs_service_1rst_quartal = common_data_service.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    recs_service_1rst_quartal_filtered = recs_service_1rst_quartal[:50]
    recs_service_1rst_quartal_filtered = recs_service_1rst_quartal_filtered.query("score > 0.0")

    common_data_service[["score", "explanation"]] = common_data_service.apply(lambda row: pd.Series(calcucate_score_common(row, 2, "service")), axis=1)
    recs_service_2nd_quartal = common_data_service.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    used = set(recs_service_1rst_quartal_filtered["Наименование СПГЗ"][:50].tolist())
    recs_service_2nd_quartal_filtered = recs_service_2nd_quartal[~recs_service_2nd_quartal["Наименование СПГЗ"].isin(set(recs_service_1rst_quartal["Наименование СПГЗ"][:50].tolist()))].sort_values("score", ascending=False)[:50]
    recs_service_2nd_quartal_filtered = recs_service_2nd_quartal_filtered.query("score > 0.0")

    common_data_service[["score", "explanation"]] = common_data_service.apply(lambda row: pd.Series(calcucate_score_common(row, 3, "service")), axis=1)
    recs_serivce_3rd_quartal = common_data_service.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    used = set(recs_service_2nd_quartal_filtered["Наименование СПГЗ"][:50].tolist()) | set(recs_service_1rst_quartal_filtered["Наименование СПГЗ"][:50].tolist())
    recs_serivce_3rd_quartal_filtered = recs_serivce_3rd_quartal[~recs_serivce_3rd_quartal["Наименование СПГЗ"].isin(used)].sort_values("score", ascending=False)[:50]
    recs_serivce_3rd_quartal_filtered = recs_serivce_3rd_quartal_filtered.query("score > 0.0")



    common_data_service[["score", "explanation"]] = common_data_service.apply(lambda row: pd.Series(calcucate_score_common(row, 4, "service")), axis=1)
    used = set(recs_service_2nd_quartal_filtered["Наименование СПГЗ"][:50].tolist()) | set(recs_service_1rst_quartal_filtered["Наименование СПГЗ"][:50].tolist()) | set(recs_serivce_3rd_quartal_filtered["Наименование СПГЗ"][:50].tolist())
    recs_service_4th_quartal = common_data_service.sort_values("score", ascending=False).drop_duplicates("Наименование СПГЗ", keep="first").reset_index(drop=True)
    recs_service_4th_quartal_filtered = recs_service_4th_quartal[~recs_service_4th_quartal["Наименование СПГЗ"].isin(used)].sort_values("score", ascending=False)[:50]
    recs_service_4th_quartal_filtered = recs_service_4th_quartal_filtered.query("score > 0.0")



    res_json_1q_i = do_json_object(recs_items_1rst_quartal_filtered, spgz_store, constants.prices_items, constants.price_services)
    res_json_2q_i = do_json_object(recs_items_2nd_quartal_filtered,  spgz_store, constants.prices_items, constants.price_services)
    res_json_3q_i = do_json_object(recs_items_3rd_quartal_filtered,  spgz_store, constants.prices_items, constants.price_services)
    res_json_4q_i = do_json_object(recs_items_4th_quartal_filtered,  spgz_store, constants.prices_items, constants.price_services)

    res_json_1q_s = do_json_object(recs_service_1rst_quartal_filtered, spgz_store, constants.prices_items, constants.price_services, "service")
    res_json_2q_s = do_json_object(recs_service_2nd_quartal_filtered,  spgz_store, constants.prices_items, constants.price_services, "service")
    res_json_3q_s = do_json_object(recs_serivce_3rd_quartal_filtered,  spgz_store, constants.prices_items, constants.price_services, "service")
    res_json_4q_s = do_json_object(recs_service_4th_quartal_filtered,  spgz_store, constants.prices_items, constants.price_services, "service")

    res_json_1q = res_json_1q_i + res_json_1q_s
    res_json_2q = res_json_2q_i + res_json_2q_s
    res_json_3q = res_json_3q_i + res_json_3q_s
    res_json_4q = res_json_4q_i + res_json_4q_s

    return (res_json_1q, res_json_2q, res_json_3q,res_json_4q)


def do_json_object(recs, spgz_store, prices_items, services_price, type = "item"):
    json_res = []
    for idx, row in tqdm(recs.iterrows()):
        name = row["Наименование СПГЗ"]
        explanation = row["explanation"]
        matching_dict = find_dict_by_name(spgz_store, name, explanation)
        if matching_dict:
            matching_dict["amount"] = constants.item2count.get(name, 1)
            if type == "service":
                matching_dict["amount"] = max(row["amount_average"], 1)
            matching_dict["type"] = type
            if type == "item":
                # if row["Наименование СПГЗ"] not in prices_items:
                #     print("Miss item", row["Наименование СПГЗ"])
                matching_dict["price"] = prices_items.get(name, row["Цена ГК, руб."]) * matching_dict["amount"]
                # print("Should be", name, prices_items.get(name, row["Цена ГК, руб."]) * 1, "amount", matching_dict["amount"])
            else:
                # if row["Наименование СПГЗ"] not in services_price:
                    # print("Miss service", row["Наименование СПГЗ"])
                # print("Should be", name, services_price.get(row["Наименование СПГЗ"], row["Цена ГК, руб."]) * 1)
                matching_dict["price"] = services_price.get(row["Наименование СПГЗ"], row["Цена ГК, руб."]) * 1
            if matching_dict["okpd2Code"] in constants.cluster_1:
                matching_dict["cluster"] = 1
            elif matching_dict["okpd2Code"] in constants.cluster_2:
                matching_dict["cluster"] = 2
            elif matching_dict["okpd2Code"] in constants.cluster_3:
                matching_dict["cluster"] = 3
            elif matching_dict["okpd2Code"] in constants.cluster_4:
                matching_dict["cluster"] = 4
            elif matching_dict["okpd2Code"] in constants.cluster_5:
                matching_dict["cluster"] = 5
            elif matching_dict["okpd2Code"] in constants.cluster_6:
                matching_dict["cluster"] = 6
            elif matching_dict["okpd2Code"] in constants.cluster_7:
                matching_dict["cluster"] = 7
            elif matching_dict["okpd2Code"] in constants.cluster_8:
                matching_dict["cluster"] = 8
            else:
                matching_dict["cluster"] = 0
            json_res.append(matching_dict)
    return json_res



def get_predictions(contracts_data_path: str, item_property_store: str) -> list[dict, dict, dict, dict]:
    zakupki_df, spgz_store = load_data(contracts_data_path, item_property_store)
    common_data_service, common_data_items = process_dara(zakupki_df)
    res_json_1q, res_json_2q, res_json_3q,res_json_4q = predictions(common_data_service, common_data_items, spgz_store)
    return res_json_1q, res_json_2q, res_json_3q,res_json_4q

if __name__ == "__main__":
    preidcitons = get_predictions("../data/2. ГКУ/Выгрузка контрактов по Заказчику.xlsx", "../data/spgz.json")
    print(len(preidcitons[0]), len(preidcitons[1]), len(preidcitons[2]), len(preidcitons[3]), )
    print(preidcitons[0][0]["name"], preidcitons[0][0]["price"])
    print(preidcitons[1][0]["name"], preidcitons[1][0]["price"])
    print(preidcitons[2][0]["name"], preidcitons[2][0]["price"])
    print(preidcitons[3][0]["name"], preidcitons[3][0]["price"])