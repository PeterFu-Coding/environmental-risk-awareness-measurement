# Environmental-Risk-Awareness-Measurement
This is the data&code depository for the article named ***"Unraveling Environmental Risk Awareness in China over Four Decades from Mass Media and Academic Archives"***.

A new methodological framework, integrating NLP techniques with web news and academic archives, to extract environmental risk awareness of people over extended periods and large spatial scales was put forward here. And by applying geographic entity and focus extraction, coupled with environmental risk quantification, we examined nearly four decades of environmental risk awareness among the Chinese.The researhch results also confirmed the validity of our methods.

# Requirements
The codes are based on Python 3.9. 

# File Description

## 1. Environmental Risk Extraction

## *Main File Descriptions:*
The main codes for implementing the algorithm are stored in the ***GetLocationInfo.py*** script.
In this file, detailed location information will be extracted from the text. And the whole process will be divided into four parts: location  extraction, place name information sheets establishment, provincial information sheets establishment and geoencoding.

### input: 
*Chinese news texts/Academic archives->string*

the input text contains context and ten times of title. So the text should be "context"+"title"*10.

### output: 
*(1) location_coor->dataframe*

It contains the detailed geographic information in texts, including detailed and accurate place names (entire), unnormalized weights of each place name (weight) and the longitude and latitude of each place name (longitude & latitude).

*(2) pro_pd ->dataframe*

It's the aggregation by province of location_coor. It contains the provinces extracted from the text and their unnormalized weights.

*(3) confidence -> float*

It refers the confidence that the extracted place names are the geographic information contained in the entire article.

## *Other Scripts:*
### LocationInfoGrasper.py
It offers three methods, which are Baidu-based geocoding, Gaode-based geocoding and obtaining detailed geographical name information from national database for geographical names of China. 
### delete_locations.py
It helps clear the useless locations or place names that cannot be processed for our research, such as place names abroad or place names beyond provincial administrations.
### Stack.py
It's the script for stack, which is used in place name information sheets establishment in GetLocationInfo.py.

## *Some Necessary Files Used in this Section:*
### bbd_word_country.json
It contains names of countries in the world and their major cities, which is used in delete_lcoation.py. The file originates from https://github.com/dongrixinyu/location_detect, which has been cited in our manuscript.
administrative_weight.json
It helps convert administrative level to its corresponding PAI.
### corpus.txt
It's used in word segmentation by LAC, which ensures that the words we need are not incorrectly segmented.
### province_name_modification.json
It helps modify the province name, making the province name complete. For example, it helps convert 北京 (Beijing, incomplete province name)  to 北京市 (Beijing City, complete province name).   
### province_to_capital.json
It helps convert province name to their capital's name, making it convenient to locate these provinces.
### WebNewsSamples.csv & AcademicArchivesSamples.csv
Our research data samples.

It includes: title, content, date (issued date), keyword/weight (weight is the ratio of the occurence of the keyword of the the sum of the occurence the keywords, but actually it's not mentioned in this research), source and id.
### ResultExample.csv
The example of the result of environmental risk extraction.

## 2. Result Analysis and Figure Output
## *Figure Generation Scirpts*
### DrawMaps/DrawHeatMap.py
It helps generate heat maps about environmental risk awareness. The maps has been displayed in Fig.4 in our manuscript.
### DrawMaps/DrawLineChart.py
It helps generate line charts about environmental risk awareness, which helps us analyse changing trends about four kinds of environmental risk awareness. The charts has been displayed in Fig.5 in our manuscript.
### DrawMaps/DrawWordMap.py
It helps generate word cloud maps of the keywords that extracted the data the most. The word cloud maps has been displayed in Fig.6 in our manuscript.
### DrawMaps/GetCoorByERE.py
It helps extract the coordinates of environmental risk events, which are used to draw scatter plots in ArcMap. The scatter plots have been displayed in Fig.7 in our manuscript.
### DrawMaps/DrawLineGraphForERE.py
It helps extract the trends of environmental risk events and display them in the form of line charts. The ERVs are normalized by the year of ERV. The chart has been displayed in Fig.8 in our manuscirpt. 
## *Other Scripts:*
### dataTransmission/GetDataFromdb.py
It helps get neccessary data from database. It was used in all figure generation scripts except DrawWordMap.py.
### PoliticalEffects.py
It helps analyse the effects of political factors.
## *Neccessary Files Used in this Section:*
### DrawMaps/WordCloudData.csv
It's the data of the word cloud maps. It contains the keywords that extracted the data the most, the amount of data and the categories of keyword. The first three columns are the results of web news and the others are the results of the academic archives. They were extracted from database through SQL.

# How to use these codes?
## 1. Environmental Risk Awareness Extraction
You just need to call the ***Get_key_location()*** in the GetLocationInfo.py file. When you send a text into it, maybe a piece of news or an academic archive, we could get the required geographic information. By the way, all the results are stored as ResultExample.csv.
## 2. Draw Maps
You just need to call map drawing functions in corresponding files. Maybe the paths needs to be revised. 

