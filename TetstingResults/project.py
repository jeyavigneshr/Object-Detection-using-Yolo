# library imports
import pandas as pd
import numpy as np

# read csv and excel file
ground_truth = pd.read_excel('Ground_truth.xlsx')
final_bk = pd.read_csv('response.csv')

# creating a dummy dataframe with full of zeros
columns = ['Frame_Number', 'Sedan_Black', 'Sedan_Silver', 'Sedan_Red', 'Sedan_White', 'Sedan_Blue', 'Hatchback_Black', 'Hatchback_Silver', 'Hatchback_Red', 'Hatchback_White', 'Hatchback_Blue', 'Total_Cars']
truth_dataframe = pd.DataFrame(0, index=np.arange(1495), columns=columns)

truth_dataframe

# function to split the colors
def get_separate_colours(color_string):
  return color_string.split('|')

for index, row in final_bk.iterrows():
    car_type = str(row['car_type'])
    colours_detected = str(row['colours_detected'])
    color_list = get_separate_colours(colours_detected)
    if (car_type != "nan") and (colours_detected != "nan"):
      if (len(color_list) > 1):
        for color in color_list:
          column_to_fill = car_type.capitalize() + "_" + color.capitalize()
          truth_dataframe.at[index, column_to_fill] = 1
          truth_dataframe.at[index, 'Frame_Number'] = index
          print(index, column_to_fill)
      else:
        column_to_fill = car_type.capitalize() + "_" + color_list[0].capitalize()
        truth_dataframe.at[index, column_to_fill] = 1
        truth_dataframe.at[index, 'Frame_Number'] = index
        print(index, column_to_fill)
    truth_dataframe.at[index, 'Frame_Number'] = index

truth_dataframe['Total_Cars'] = truth_dataframe['Sedan_Black'] + truth_dataframe['Sedan_Silver']+ truth_dataframe['Sedan_Red'] + truth_dataframe['Sedan_White'] + truth_dataframe['Sedan_Blue'] + truth_dataframe['Hatchback_Black'] + truth_dataframe['Hatchback_Silver'] + truth_dataframe['Hatchback_Red'] + truth_dataframe['Hatchback_White'] + truth_dataframe['Hatchback_Blue']

truth_dataframe

truth_dataframe.to_csv('result.csv')

