import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

APP_TITLE = 'Agriculture Crop Production in India'
APP_SUB_TITLE = 'Source: Ministry of Agriculture and Farmers Welfare of India'

def total_yield(df, year, season, state, field_name, crop, metric_title):
    df = df[(df['Year'] == year) & (df['Season'] == season) & (df['Crop'] == crop)]
    if state:
        df = df[df['State'] == state]
    df.drop_duplicates(inplace=True)
    total = df[field_name].sum()
    st.metric(metric_title, '{:,}'.format(round(total)))

def display_map(df, year, crop, season):
    df = df[(df['Year'] == year) & (df['Season'] == season) & (df['Crop'] == crop)]

    map = folium.Map(location=[20,80], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')

    choropleth = folium.Choropleth(
        geo_data = 'data/states_india.geojson',
        data = df,
        columns=('State', 'Yield'),
        key_on= 'feature.properties.st_nm',
        line_opacity=0.8,
        highlight=True   
    )
    choropleth.geojson.add_to(map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['st_nm'], labels=False)
    )

    st_map = st_folium(map, width=700, height=500)

    state = ''
    if st_map['last_active_drawing']:
        state = st_map['last_active_drawing']['properties']['st_nm']

    return state

def display_time_filters(df):
    year_list = [''] + list(df['Year'].unique())
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
    state_index = state_list.index(state) if state and state in state_list else 0
    return st.sidebar.selectbox('State', state_list, state_index)

def main():
    st.set_page_config(APP_TITLE)
    st.title(APP_TITLE)
    st.caption(APP_SUB_TITLE)

    #LOAD DATA
    df_country = pd.read_csv('data/India Agriculture Crop Production.csv')   
    df_area = pd.read_csv('data/India Agriculture Crop Production.csv')
    df_prod = pd.read_csv('data/India Agriculture Crop Production.csv')
    df = pd.read_csv('data/India Agriculture Crop Production.csv')

    field_name = 'Yield'
    crop = 'Rice'
 
    #DISPLAY FILTERS AND MAP
    year, season = display_time_filters(df_country)
    state = display_map(df_country, year, crop, season)
    crop = crop_filter(df_country)
    state = display_state_filter(df_country, state)



    #DISPLAY METRICS
    st.subheader(f'{state} Facts')
    col1, col2, col3 = st.columns(3)
    with col1:
        total_yield(df_area, year, season, state, 'Area', crop, 'Total Area (Hectares)')
    with col2:
        total_yield(df_prod, year, season, state, 'Production', crop, 'Total Production (Tonnes)')
    with col3:
        total_yield(df, year, season, state, field_name, crop, f'Total {field_name}')


if __name__ == "__main__":
    main()
