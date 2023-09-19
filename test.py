import pandas as pd

# df = pd.read_csv("id.csv", sep=';', encoding='cp1251')
#
# for value in range(len(df['id'])):
#     # print(df.loc[value, 'id'])
#     if df.loc[value, 'id'] == 855049328:
#         name_file = 'words_client_' + str(855049328) + '.csv'
#         df_user_words = pd.read_csv(name_file, sep=';', encoding='cp1251')
#         if (len(df_user_words['word'])) == 2:
#             print('You should to give me a word for learning. Press "I want to enlarge my vocabulary"')
#         elif (len(df_user_words['word'])) > 2:
#             print('It is better')
            # print(len(df_user_words['word']))
            # number_row_word = len(df_user_words['word'])
            # df_user_words.loc[number_row_word, 'word'] = 'word'  # бот вносить англійське слово
            # df_user_words.loc[number_row_word, 'ua_word'] = 'word_ukr'  # бот вносить англійське слово
            # df_user_words.loc[number_row_word, 'date'] = 1
            # df_user_words.loc[number_row_word, 'week_date'] = 1
            # df_user_words.loc[number_row_word, 'month_date'] = 1
            # df_user_words.loc[number_row_word, 'level'] = 1
            # df_user_words.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv

# if len(df_user_words['word']) == 2 and df_user_words.loc[0, 'word'] == 1 and df_user_words.loc[1, 'word'] == 1:
#     df_user_words.loc[0, 'word'] = 'word'  # бот вносить англійське слово
#     df_user_words.loc[0, 'ua_word'] = 'word_ukr'  # бот вносить англійське слово
#     df_user_words.loc[0, 'date'] = 1
#     df_user_words.loc[0, 'week_date'] = 1
#     df_user_words.loc[0, 'month_date'] = 1
#     df_user_words.loc[0, 'level'] = 1
#     df_user_words.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv
# elif len(df_user_words['word']) == 2 and df_user_words.loc[0, 'word'] != 1 and df_user_words.loc[1, 'word'] == 1:
#     df_user_words.loc[1, 'word'] = 'word'  # бот вносить англійське слово
#     df_user_words.loc[1, 'ua_word'] = 'word_ukr'  # бот вносить англійське слово
#     df_user_words.loc[1, 'date'] = 1
#     df_user_words.loc[1, 'week_date'] = 1
#     df_user_words.loc[1, 'month_date'] = 1
#     df_user_words.loc[1, 'level'] = 1
#     df_user_words.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv
# elif len(df_user_words['word']) == 2 and df_user_words.loc[0, 'word'] != 1 and df_user_words.loc[1, 'word'] != 1:
#     number_row_word = len(df_user_words['word'])
#     df_user_words.loc[number_row_word, 'word'] = 'word'  # бот вносить англійське слово
#     df_user_words.loc[number_row_word, 'ua_word'] = 'word_ukr'  # бот вносить англійське слово
#     df_user_words.loc[number_row_word, 'date'] = 1
#     df_user_words.loc[number_row_word, 'week_date'] = 1
#     df_user_words.loc[number_row_word, 'month_date'] = 1
#     df_user_words.loc[number_row_word, 'level'] = 1
#     df_user_words.to_csv(name_file, sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv


# a = 2
# b = 7
# a, b = (a + b) - a, (a + b) - b
# # b = (a + b) - a
# print(a, b)

# df_3000 = pd.read_csv('3000.csv', encoding='UTF-8')
# df_3001 = pd.read_csv('3001.csv', encoding='UTF-8')
# data = []
#
# for value_new in range(len(df_3000['transcription']) - 1):
#     new = ''
#     word = df_3000.loc[value_new, 'transcription']
#     for i in range(len(word)):
#         if word[i] != ']':
#             # print(new)
#             new += word[i]
#         elif word[i] == ']':
#             # print(i)
#             new += word[i]
#             break
#     print(new)
#     data.append(new)
#     df_3001.loc[value_new, 'transcription'] = new
#     df_3001.to_csv('3001.csv', sep=';', index=False, encoding='UTF-8')  # бот змінює дані в файлі csv
# df_3002 = pd.Series(data)
# df_3002.to_csv('3002.csv', sep=';', index=False, encoding='UTF-8')  # бот створює файл csv

# df_3000 = pd.read_csv('3000_words_2.csv', sep=';', encoding='cp1251')
# # print(len(df_3000['word']) - 1)
# collect = ''
# for i in df_3000['word']:
#     collect = i[:len(i)]
    # for k in i:
    #     collect =
    #     if k != ' ':
    #         collect += k
    #     elif k == ' ':
    #         break
    # print(collect)
    # df_3000.loc[i, 'word'] = collect
    # df_3000.to_csv('3000_words_2.csv', sep=';', index=False, encoding='cp1251')  # бот змінює дані в файлі csv