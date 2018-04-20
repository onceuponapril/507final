# 507final
1.Data sources used:Yelp website, google place map, Lyft.
For yelp, because it is web crawling there is no need for api. For google place map, you need api(had better be the unlimited use because text search counts 10 for once https://developers.google.com/places/web-service/get-api-key?authuser=1). For Lyft, you need  API and clienr secrets because it uses Oauth2,https://developer.lyft.com/docs/overview. Format can check "secrets.py".)

Including instructions for a user to access the data sources (e.g., API keys or client secrets needed, along with a pointer to instructions on how to obtain these and instructions for how to incorporate them into your program (e.g., secrets.py file format))
Any other information needed to run the program (e.g., pointer to getting started info for plotly)

Brief description of how your code is structured, including the names of significant data processing functions (just the 2-3 most important functions--not a complete list) and class definitions. If there are large data structures (e.g., lists, dictionaries) that you create to organize your data for presentation, briefly describe them.
The cache file is designed in the beginning. There is a function to create the sql database (create_first_table) but you donnot need to invoke it unless you wanna check how it runs. The one important class called Yelpeat().lyft_data()  if you 
Brief user guide, including how to run the program and how to choose presentation options.
