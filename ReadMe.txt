This is the data&code garbage for the article named "Unraveling Environmental Risk Awareness in China over Four Decades from Mass Media and Academic Archives".

A new methodological framework, integrating NLP techniques with web news and academic archives, to extract environmental risk awareness of people over extended periods and large spatial scales was put forward here. And by applying geographic entity and focus extraction, coupled with environmental risk quantification, we examined nearly four decades of environmental risk awareness among the Chinese.The researhch results also confirm the validity of our methods.

Requirements
The codes are based on Python 3.9. 

File Descriptions:
The main codes for implementing the algorithm are stored in the GetLocationInfo.py script.
In this file, detailed location information will be extracted from the text. And the whole process will be divided into four parts: location  extraction, place name information sheets establishment, provincial information sheets establishment and geoencoding.
input: Chinese news texts/Academic archives->string
*** the input text contains context and ten times of title. So the text should be "context"+"title"*10.
output: 
(1)location_coor->dataframe
It contains the detailed geographic information in texts, including detailed and accurate place names (entire), unnormalized weights of each place name (weight) and the longitude and latitude of each place name (longitude & latitude).
(2)pro_pd ->dataframe
It's the aggregation by province of location_coor. It contains the provinces extracted from the text and their unnormalized weights.
(3)confidence -> float
It refers the confidence that the extracted place names are the geographic information contained in the entire article.

Other Scripts:
LocationInfoGrasper.py
It offers three methods, which are Baidu-based geocoding, Gaode-based geocoding and obtaining detailed geographical name information from national database for geographical names of China. 
delete_locations.py
It helps clear the useless locations or place names that cannot be processed for our research, such as place names abroad or place names beyond provincial administrations.
Stack.py
It's the script for stack, which is used in place name information sheets establishment in GetLocationInfo.py.

Some Necessary Files:
bbd_word_country.json
It contains names of countries in the world and their major cities, which is used in delete_lcoation.py.
administrative_weight.json
It helps convert administrative level to its corresponding PAI.
corpus.txt
It's used in word segmentation by LAC, which ensures that the words we need are not incorrectly segmented.
province_name_modification.json
It helps modify the province name, making the province name complete. For example, it helps convert 湖北 (Hubei, incomplete province name)  to 湖北省 (Hubei Province, complete province name).   
province_to_capital.json
It helps convert province name to their capital's name, making it convenient to locate these provinces.
WebNewsSamples.csv & AcademicArchivesSamples.csv
Our research data samples.
It includes: title, content, date (issued date), keyword/weight (weight is the ratio of the occurence of the keyword of the the sum of the occurence the keywords, but actually it's not mentioned in this research), source and id.