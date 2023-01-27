import requests
import os
import pandas as pd
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime, timedelta, time

#get json from twitter api call
def get_twitter_json(relevant_date_start, relevant_date_end, num_of_tweets,query):
  url = "https://api.twitter.com/2/tweets/search/recent?start_time={date_start}&end_time={date_end}&max_results={count}&tweet.fields=created_at,author_id,lang&query={q}".format(date_start=relevant_date_start, date_end=relevant_date_end, count=num_of_tweets, q=query)

  payload={}
  headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMrGkwEAAAAA9bB7QZaUkh5C%2FYrIRMKkURf7gvo%3DIO6r4pTU1v7qK0f7lKCqE2jh6RG1nqCdjsQDcZzYwnb8fmF9xX',
    'Cookie': 'guest_id=v1%3A167338319723204849'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()

#get json from twitter api call without end date -> end date = current timestamp
def get_twitter_json_without_end(relevant_date_start, num_of_tweets,query):
  url = "https://api.twitter.com/2/tweets/search/recent?start_time={date_start}&max_results={count}&tweet.fields=created_at,author_id,lang&query={q}".format(date_start=relevant_date_start, count=num_of_tweets, q=query)

  payload={}
  headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMrGkwEAAAAA9bB7QZaUkh5C%2FYrIRMKkURf7gvo%3DIO6r4pTU1v7qK0f7lKCqE2jh6RG1nqCdjsQDcZzYwnb8fmF9xX',
    'Cookie': 'guest_id=v1%3A167338319723204849'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()

#twitter api call if next_token in last api response
def get_twitter_json_next_page(relevant_date_start, relevant_date_end, num_of_tweets,query,next_token):
  url = "https://api.twitter.com/2/tweets/search/recent?start_time={date_start}&end_time={date_end}&max_results={count}&tweet.fields=created_at,author_id,lang&query={q}&next_token={next_page}".format(date_start=relevant_date_start, date_end=relevant_date_end, count=num_of_tweets, q=query, next_page=next_token)

  payload={}
  headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMrGkwEAAAAA9bB7QZaUkh5C%2FYrIRMKkURf7gvo%3DIO6r4pTU1v7qK0f7lKCqE2jh6RG1nqCdjsQDcZzYwnb8fmF9xX',
    'Cookie': 'guest_id=v1%3A167338319723204849'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()

#twitter api call if next_token in last api response without end date -> end date = current timestamp
def get_twitter_json_next_page_without_end(relevant_date_start, num_of_tweets,query,next_token):
  url = "https://api.twitter.com/2/tweets/search/recent?start_time={date_start}&max_results={count}&tweet.fields=created_at,author_id,lang&query={q}&next_token={next_page}".format(date_start=relevant_date_start, count=num_of_tweets, q=query, next_page=next_token)

  payload={}
  headers = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAMrGkwEAAAAA9bB7QZaUkh5C%2FYrIRMKkURf7gvo%3DIO6r4pTU1v7qK0f7lKCqE2jh6RG1nqCdjsQDcZzYwnb8fmF9xX',
    'Cookie': 'guest_id=v1%3A167338319723204849'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  return response.json()

#create a pandas DataFrame from json
def create_df_from_json(json):
  columns = ['tweet_id', 'tweet_user_id', 'tweet_lang', 'tweet_text', 'tweet_created_at']
  collected_data = []
  for t in json["data"]:
    collected_data.append([t["id"],t["author_id"],t["lang"],t["text"],t["created_at"]])

  return pd.DataFrame(collected_data, columns=columns)

#create excel file from df or append
#https://stackoverflow.com/questions/38074678/append-existing-excel-sheet-with-new-dataframe-using-python-pandas
def append_df_to_excel(df, excel_path):
  if os.path.isfile(excel_path):  #if file already exists append to existing file
      workbook = openpyxl.load_workbook(excel_path)  #load workbook if already exists
      sheet = workbook['all_tweets']  #declare the active sheet 

      #append the dataframe results to the current excel file
      for row in dataframe_to_rows(df, header = False, index = False):
          sheet.append(row)
      workbook.save(excel_path)  #save workbook
      workbook.close()  #close workbook
  else:  #create the excel file if doesn't already exist
      with pd.ExcelWriter(path = excel_path, engine = 'openpyxl') as writer:
          df.to_excel(writer, index = False, sheet_name = 'all_tweets')

#other method to create excel file from df or append
def append_df_to_excel2(df, excel_path):
    excel_df = pd.read_excel(excel_path) #read excel to dataframe
    res = pd.concat([df, excel_df], ignore_index=True) #concat both dataframes
    res.to_excel(excel_path, index=False) #write complete dataframe to excel

#function to creat excel sheet
def create_excel_sheet(relevant_date_start,relevant_date_end,num_of_tweets,query,num_of_repeats):
  tweets_json = get_twitter_json(relevant_date_start=relevant_date_start,relevant_date_end=relevant_date_end,num_of_tweets=num_of_tweets,query=query) #get json
  df = create_df_from_json(json=tweets_json) #create dataframe from json
  append_df_to_excel(df=df, excel_path='data/tweets.xlsx') #write dataframe to excel or append if excel table already exists

  #pagination on twitter searches -> api call returns next_token which indicates that there is still more data for the given query (100 tweets pery api call)
  if tweets_json["meta"]["next_token"]:
    next_token = tweets_json["meta"]["next_token"]
    for _ in range(num_of_repeats): # number of times you want to get new results from same query
      next_json = get_twitter_json_next_page(relevant_date_start=relevant_date_start,relevant_date_end=relevant_date_end,num_of_tweets=num_of_tweets,query=query,next_token=next_token)
      next_df = create_df_from_json(json=next_json)
      append_df_to_excel(df=next_df, excel_path='data/tweets.xlsx')

      #stop if there are no more pages
      if not tweets_json["meta"]["next_token"]:
        break

#function to creat excel sheet without end date -> end date = current timestamp
def create_excel_sheet_without_end(relevant_date_start,num_of_tweets,query,num_of_repeats):
  tweets_json = get_twitter_json_without_end(relevant_date_start=relevant_date_start,num_of_tweets=num_of_tweets,query=query) #get json
  df = create_df_from_json(json=tweets_json) #create dataframe from json
  append_df_to_excel(df=df, excel_path='data/tweets.xlsx') #write dataframe to excel or append if excel table already exists

  #pagination on twitter searches -> api call returns next_token which indicates that there is still more data for the given query (100 tweets pery api call)
  if tweets_json["meta"]["next_token"]:
    next_token = tweets_json["meta"]["next_token"]
    for _ in range(num_of_repeats): # number of times you want to get new results from same query
      next_json = get_twitter_json_next_page_without_end(relevant_date_start=relevant_date_start,num_of_tweets=num_of_tweets,query=query,next_token=next_token)
      next_df = create_df_from_json(json=next_json)
      append_df_to_excel(df=next_df, excel_path='data/tweets.xlsx')

      #stop if there are no more pages
      if not tweets_json["meta"]["next_token"]:
        break


#starting creation of excel sheet

#necessary ISO-8601 timestamps for twitter api
relevant_date_start = datetime.combine((datetime.now() - timedelta(0)), time.min).isoformat(timespec="seconds")+"Z"
relevant_date_end = datetime.combine((datetime.now() - timedelta(1)), time.max).isoformat(timespec="seconds")+"Z"
custom_time = (datetime.now()-timedelta(7)).isoformat(timespec="seconds")+"Z" #get the oldest possible time for the free twitter API, used with 'create_excel_sheet_without_end'

num_of_tweets = 100 #10-100 tweets per api call
query = "TSLA -has:links" #search query
num_of_repeats = 6 #how many more requests if next_token (more pages) in api call
#-> num_of_tweets + (num_of_repeats*num_of_tweets) = number of tweets | 100 + (6*100) = 700

##call main function -> 'create_excel_sheet' for past days, 'create_excel_sheet_without_end' for the present day

#create_excel_sheet(relevant_date_start=relevant_date_start,relevant_date_end=relevant_date_end,num_of_tweets=num_of_tweets,query=query,num_of_repeats=num_of_repeats)
create_excel_sheet_without_end(relevant_date_start=relevant_date_start,num_of_tweets=num_of_tweets,query=query,num_of_repeats=num_of_repeats)