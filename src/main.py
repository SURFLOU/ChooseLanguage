from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
from sklearn import preprocessing
from itertools import combinations
from sqlhandling import connect_to_db, read_query, insert_func_into_table, create_tables
import data


def number_of_total_speakers(language):
    df = pd.read_csv("../data/toplanguages.csv", header=0)
    return int(df.loc[df["Language"] == language, 'Total Speakers'].item())


def number_of_job_offers(language):  # based on pracuj.pl
    result = ""
    while result == "":
        url = "https://www.pracuj.pl/praca/" + data.languagesTranslation[language] + ";kw"
        page = requests.get(url)

        soup = BeautifulSoup(page.content, "html.parser")
        results = str(soup.find_all("span", class_='results-header-listing__offer-count-text-number'))
        string = re.sub('<.*?>', '', results)
        result = string.lstrip(string[0]).rstrip(string[-1])

    return int(result)


def type_of_family(language):
    df = pd.read_csv("../data/europeanlanguagesfamily.csv", header=0, sep=";")
    return str(df.loc[df["Language"] == language, "Family"].item())


def number_of_hours(language):
    df = pd.read_csv("../data/FSIdifficulty.csv", header=0, sep=";")
    return df.loc[df['Language'] == language, 'Number of hours'].item()


def lexical_similarity(language_list, language):
    df = pd.read_csv("../data/lexicalsimilarity.csv", header=0, sep=';')
    x = []
    for elems in language_list:
        x.append([elems, language, df.loc[df['Language'] == elems, language].item()])
    max_numb = 0
    max_lang_native = ""
    for elem in x:
        if float(elem[2]) > max_numb:
            max_numb = float(elem[2])
            max_lang_native = str(elem[0])
    return max_numb, max_lang_native


def get_total_score(language_list, connect):
    lex_similarity = []
    num_of_hours = []
    total_speakers = []
    job_offers = []
    language_family = []
    for lang in data.all_languages:
        if lang in language_list:
            continue
        common_family = 0
        for elem in language_list:
            if type_of_family(elem) == type_of_family(lang):
                common_family = 1
        lex_similarity.append(lexical_similarity(language_list, lang)[0])
        language_family.append(common_family)
        num_of_hours.append((read_query(connect, f"SELECT number_of_hours FROM job WHERE language = '{lang}'")[0][0]) * (-1))  # The higher value than worse that's why * -1
        total_speakers.append(read_query(connect, f"SELECT number_of_speakers FROM job WHERE language = '{lang}'")[0][0])
        job_offers.append(read_query(connect, f"SELECT job_offers FROM job WHERE language = '{lang}'")[0][0])

    languages = [x for x in data.all_languages if x not in language_list]

    df = {
        'Language': languages,
        'Lexical_similarity': lex_similarity,
        'Family_of_language': language_family,
        'Number_of_hours': num_of_hours,
        'Total_speakers': total_speakers,
        'Amount_of_job_offers': job_offers
    }

    df = pd.DataFrame(df)

    return df


def create_raport(language):
    print('Given your wages you should learn {lang}. '.format(lang=language))
    print("It should take you approximately {hours} hours to be fluent in {lang}".format(
        hours=number_of_hours(language),
        lang=language))
    print("There are {joboffs} job offerts with your foreign language online".format(
        joboffs=number_of_job_offers(language)))
    print("There are {natives} people speaking this language".format(natives=number_of_total_speakers(language)))


def permutate_languages(languages):
    language_len = len(languages)
    counter = 0
    for i in range(2, language_len):
        comb = combinations(languages, i)
        for elems in list(comb):
            print(elems)
            counter += 1


def find_best_lang(df):
    max_value = df["Total sum"].max()
    best_lang = df.loc[df['Total sum'] == max_value, "Language"].item()

    return best_lang, max_value


def normalize_df(language_list, connect):
    df = get_total_score(language_list, connect)
    column_names_to_normalize = ["Lexical_similarity", "Family_of_language", "Number_of_hours",
                                 "Total_speakers", "Amount_of_job_offers"]
    min_max_scaler = preprocessing.MinMaxScaler()
    x = df[column_names_to_normalize].values

    x_scaled = min_max_scaler.fit_transform(x)
    df_temp = pd.DataFrame(x_scaled, columns=column_names_to_normalize, index=df.index)
    df[column_names_to_normalize] = df_temp


    return df


def set_wages(df, wages_list):
    # wages_list = [similarity, family, difficulty, number of speakers, job offers]
    for i in range(len(df)):
        df.at[i, "Lexical_similarity"] = df.loc[i, "Lexical_similarity"] * wages_list[0]
        df.at[i, "Family_of_language"] = df.loc[i, "Family_of_language"] * wages_list[1]
        df.at[i, "Number_of_hours"] = df.loc[i, "Number_of_hours"] * wages_list[2]
        df.at[i, "Total_speakers"] = df.loc[i, "Total_speakers"] * wages_list[3]
        df.at[i, "Amount_of_job_offers"] = df.loc[i, "Amount_of_job_offers"] * wages_list[4]

    df.loc[:, 'Total sum'] = df.sum(numeric_only=True, axis=1) # Create Total sum col to sum all values

    return df




