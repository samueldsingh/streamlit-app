# Interactive webmap using Python Streamlit - Agriculture Production in India

Python can be used to convert an ordinary csv file into an [interactive web map](https://samueldsingh-streamlit-app-streamlit-app-ha3455.streamlit.app/). 
My goal was to visualize agriculture crop production of India across different 
years and for different crops. I obtained the crop data from the government 
website, Ministry of Agriculture and Farmers welfare.

For creating the map, I'll use the Python Folium Library, and for boundary I'll use the [India GeoJSON file](https://github.com/samueldsingh/streamlit-app/blob/master/data/states_india.geojson).

## Installing and creating the skeleton on the web map

Install the requirements for creating the webmap:

```
pandas==1.2.4
folium==0.12.1.post1
streamlit==1.10.0
streamlit_folium==0.6.13
```

Import the streamlit library to create the basic skeleton:
```
import streamlit as st

APP_TITLE = 'Agriculture Crop Production in India'
APP_SUB_TITLE = 'Source: Ministry of Agriculture and Farmers Welfare of India'

def main():
    st.set_page_config(APP_TITLE)   #set page config for APP_TITLE
    st.title(APP_TITLE)             
    st.caption(APP_SUB_TITLE)

if __name__ == "__main__":
    main()
```
    
    
## Loading the yield facts
Load the data using pandas below the main function and explore the data:

```
#Load data
df = pd.read_csv('India Agriculture Crop Production.csv')

st.write(df.shape)
st.write(df.head())
st.write(df.columns)
```

We want to display the 'Yield' data. First we'll create the filters for state, crop, year, season, field_name and metric_title.
```
# create filters
state = 'Uttar Pradesh'
crop = 'Rice'
year = '2017-18'        
season = 'Kharif'
field_name = 'Yield'
metric_title = 'Total Yield'

# add condition that if state name is available filter it otherwise display every other thing  
df = df[(df['Year'] == year) & (df['Crop'] == crop) & (df['Season'] == season)]
if state:
    df = df[df['State'] == state]
df.drop_duplicates(inplace=True)      #drop duplicates
sum = df[field_name].sum()            #calculate the total 'Yield'
st.metric(metric_title, '{:.2f}'.format(sum))    #format the number to two decimal places

st.write(df.shape)
st.write(df.head())
st.write(df.columns)
```

Create a function total_yield to refactor the code for better visual appeal.
```
def total_yield(df, state, crop, year, season, field_name, metric_title):
    df = df[(df['Year'] == year) & (df['Crop'] == crop) & (df['Season'] == season)]
    if state:
        df = df[df['State'] == state]
    df.drop_duplicates(inplace=True)
    total = df[field_name].sum()
    st.metric(metric_title, '{:,}'.format(round(total)))
```

Use the same total_yield function, to display the total production area in hectares by accessing the Area column in the csv data.
```
total_yield(df, state, crop, year, season, field_name, 'Total Yield')
total_yield(df_area, state, crop, year, season, 'Area', 'Total Area in Hectares')
```

Display the total area, total production and total yield as columns instead of rows:
```
# Display metrics
    st.subheader(f'{state} Facts')
    col1, col2, col3 = st.columns(3)
    with col1:
        total_yield(df_area, state, crop, year, season, 'Area', 'Total Area in Hectares')
    with col2:
        total_yield(df_prod, state, crop, year, season, 'Production', 'Production in Tonnes')
    with col3:
        total_yield(df, state, crop, year, season, field_name, 'Total Yield')
```

## Display folium map
Install the necessary libraries

```
pip install folium==0.12.1.post1
pip install streamlit_folium==0.6.13
```

Display the folium map with the CartoDB positron tiles.
```
def display_map(df, year, crop, season):
    df = df[(df['Year'] == year) & (df['Crop'] == crop) & (df['Season'] == season)]

    map = folium.Map(location=[20,80], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
    st_map = st_folium(map, width=700, height=500)
```

## Plot overlay on the map
We'll create a choropleth map to show the total yield in different states. We can tie the state name in geojson file to the state name in the csv file.

The geojson file contains the state name under "st_nm" properties section:

```
choropleth = folium.Choropleth(
        geo_data = 'data/states_india.geojson',
        data = df,
        columns=('State', 'Yield'),
        key_on= 'feature.properties.st_nm',
        line_opacity=0.8,
        highlight=True   
    )
    choropleth.geojson.add_to(map)
```

## Display tooltip
Create a child element for the choropleth geojson object to display the state name while hovering over the map.

```
choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['st_nm'], labels=False)
    )
```

## Filter data on clicking the map
Filter the metadata on clicking the map:
```
state = ''
if st_map['last_active_drawing']:
    state = st_map['last_active_drawing']['properties']['st_nm']

    return state

state = display_state_filter(df_country, state) #grab the state from the function
```

## Create time filters
Create filters on the sidebars to select the year, season, crop and state

```
def display_time_filters(df):
    year_list = [''] + list(df['Year'].unique())    #use [''] to create an empty selection
    year_list.sort(reverse=True)
    year = st.sidebar.selectbox('Year', year_list)
    season_list = [''] + list(df['Season'].unique())
    season = st.sidebar.selectbox('Season', season_list)
    st.header(f'{year} {season}')
    return year, season

def crop_filter(df):
    crop_list = [''] + list(df['Crop'].unique())
    crop_list.sort()
    return st.sidebar.selectbox('Crop', crop_list)

def display_state_filter(df, state):
    state_list = [''] + list(df['State'].unique())
    state_list.sort()
    state_index = state_list.index(state) if state and state in state_list else 0   #display state only it is in state_list else select the first index
    return st.sidebar.selectbox('State', state_list, state_index)
```

The [entire code](https://github.com/samueldsingh/streamlit-app/blob/master/streamlit_app.py) tied together to produce the [interactive webmap](https://samueldsingh-streamlit-app-streamlit-app-ha3455.streamlit.app/) is given here.

### References:
Create Dashboard with Folium Map, Streamlit and Python - Full Course (Zackaria Chowdary)
