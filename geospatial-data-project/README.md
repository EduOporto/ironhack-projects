In order to find the perfect spot for our company's office I will consider the following aspects:

 - A young and cheerful place: as the ages of all our employees are comprised between 25 and 40 year-old, I will look for a place with a low median age, where the percentage of people on that range is high, and where the leisure offer is so.
 - Forthcoming families friendly: as 30% or our employees would need schools or kindergardens around, and some others could in the future, I will check on the schooling levels of the places, as well as how close and convenient those could be from the candidate office.
 - Tech startups and design companies around: as more than 60% of our employees work in the development and design sections, I will try to sorround them with a creative vibe, looking that the area is close to other tech companies, so they can share, learn and improve their skills and knowledge.
 - Well-connected: as our executives will need to travel around the continent, and also most of our employees, I will take care on how connected the place is with other points of the geography. Giving our employees the chance of traveling, either for work purposes or leisure, could be a good point, above all for those who could be relocated from far away.

As the dataset of the possible offices is very dense, I will first divide it in two: one with all the offices located in the USA; and another with the ones located in European countries. 

Once this division is done, I will first focus my research in the USA offices. As the resultant collection does not have all the data I could require for filter and point a few candidates, I will need to enrich it with some data about demographics, schooling, surrounding businesses or transports. 

### Demographic data

Thanks to the extense databases that belong to the [United States Census Bureau](https://www.census.gov/en.html), I will have access to massive amounts of demographic data of each of the places where the offices are located. What I will need from this site is the median age of a given place, the rate of residents that belong to the group of age between 25 and 44 year-old, scholarization ratios and the education level of its population. 

All the data mentioned above can be found in the [American Community Survey (ACS)](https://www.census.gov/data/developers/data-sets/acs-5year.html), an ongoing survey that provides data every year, and that covers a broad range of topics about social, economic, demographic, and housing characteristics of the U.S. More specifically, I will take data from the 5-year results publication, as it offers "period" estimates that represent data collected over a period of time. The primary advantage of using multiyear estimates is the increased statistical reliability of the data for less populated areas and small population subgroups. The 5-year estimates are available for all geographies down to the block group level.  In total, there are 87 different summary levels available with over 578,000 geographic areas. Unlike the 1-year estimates, geographies do not have to meet a particular population threshold in order to be published.

From the four kinds of data shelled from the survey, I will choose the Data Profiles, as they contain over 1,000 variables about topics related to broad social, economic, housing, and demographic information; and the data is presented as population counts and percentages.

In order to extract all the data I will need, I will be assisted by [*census*](https://pypi.org/project/census/), a python wrapper built for those means. It is so simple that I will just need the zip code of the location, and it will give me back the data I'm interested in from the different tables I selected. 

(A relation between the name of the tables and the data they gather is available here:

 - [Age data](https://api.census.gov/data/2018/acs/acs5/profile/groups/DP05.html)
 - [Scholing data](https://api.census.gov/data/2018/acs/acs5/profile/groups/DP02.html)

### Leisure offer

Through the [Foursquare Places API](https://developer.foursquare.com/places) I will be aware that nightlife is granted for our employees, checking that our new office has enough venues in a 10-kilometer radius.

### Schooling offer

Together with the data extracted from the American Community Survey, I will get some more data from [Google's Places API](https://developers.google.com/places/web-service/overview) about the number of schools that surround the candidate office in a 4-kilometer radius, as this would make things much easier for our employees with children. 

About 

# Links & documentation for CEE research

Querys link: http://ec.europa.eu/eurostat/wdds/rest/data/v2.1/json/en/

 - Median age by region: demo_r_pjanind3?geoLevel=nuts3&indic_de=MEDAGEPOP&precision=1&unit=YR&time=2019
 - Proportions of population (0-14 / 25-44): demo_r_pjanind3?geoLevel=nuts3&indic_de=PC_Y0_14&indic_de=PC_Y25_44&precision=2&unit=PC&time=2019
 - Pupils and students enrolled by education level: educ_uoe_enra11?geoLevel=nuts2&precision=2&sex=T&unit=NR&isced11=ED0&isced11=ED1&isced11=ED2&time=2018
 - Participation rates in up to early secondary education levels at regional level: educ_uoe_enra15?geoLevel=nuts2&precision=2&unit=RT&isced11=ED02-8&isced11=ED1_2&time=2018
 - Participation rates of 4 year old children in education at regional level: educ_uoe_enra14?geoLevel=nuts2&precision=2&unit=RT&time=2018&age=Y4

# Some other API's

 - Foursquare: https://foursquare.com/developers/
 - Google API console: https://console.cloud.google.com/google/maps-apis/
 