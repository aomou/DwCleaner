import streamlit as st
import pandas as pd
import math
import re                # 檢查座標格式
from geopy import Point  # 轉換座標
import pydeck as pdk     # 畫地圖

st.title('Map')

df = pd.read_csv("/Users/josephine/Python/ccClub2410/project/data/1_jellyfish_originalData.csv")

st.dataframe(df)

#### check column
if 'verbatimLatitude' not in df.columns and 'decimalLatitude' not in df.columns:  # no decimal, no verbatim
    st.write('No coordinates available!')
else:
    if 'verbatimLatitude' in df.columns and 'decimalLatitude' not in df.columns:    # verbatim only
        df['verbatimLatitude'] = df['decimalLatitude']
        df['verbatimLongitude'] = df['decimalLongitude']
                                                                                 
    #### check coords format (decimal) ----
    st.subheader('Check coordinates format')
    col1, col2 = st.columns(2)
    # valid format
    pattern = re.compile(r'^-?\d+(\.\d+)?$')
    def is_decimal_by_regex(value):
        
        # 若為 None 或 NaN 先視為不符合
        if pd.isna(value):
            return False
        
        # 字串化後，比對 regex
        value_str = str(value).strip()
        return bool(pattern.match(value_str))

    # subset invalid format
    not_decimal = []
    for lat, lon in zip(df['decimalLatitude'], df['decimalLongitude']):
        not_decimal.append(not is_decimal_by_regex(lat) or not is_decimal_by_regex(lon))  # select not matched row (if False append True)

    # generate new df with decimal format
    new_df = df.copy()

    if sum(not_decimal) != 0:   
        # print invalid coords
        col1.write('Invalid coords:', df[['decimalLatitude', 'decimalLongitude']][not_decimal]) 

        # subset invalid coords (copy) & generate edited version: `new_df`
        df_not_decimal = df[['decimalLatitude', 'decimalLongitude']][not_decimal].copy()

        for i, row in df_not_decimal.iterrows():
            coords = row['decimalLatitude'] + ' ' + row['decimalLongitude']
            p_coords = Point(coords)
            new_df.loc[i, ['decimalLatitude', 'decimalLongitude']] = p_coords.latitude, p_coords.longitude

        col2.write('Corrected coords:', new_df[['decimalLatitude', 'decimalLongitude']][not_decimal])

    else:
        st.write('All coordinates are decimal!')

    #### Map ----

    # Streamlit base map ----
    st.subheader('Simple map')

    # make sure coords is numeric
    new_df = new_df.astype({'decimalLatitude': 'float', 'decimalLongitude': 'float', 'individualCount': 'int'})
    # replace NaN
    new_df['vernacularName'] = new_df['vernacularName'].fillna("")

    st.map(new_df, latitude='decimalLatitude', longitude='decimalLongitude') 

    # PyDeck map ----
    st.subheader('PyDeck map')

    # calculate best zoom
    # 1. 從 new_df 找出經緯度的 min / max
    min_lat = new_df["decimalLatitude"].min()
    max_lat = new_df["decimalLatitude"].max()
    min_lon = new_df["decimalLongitude"].min()
    max_lon = new_df["decimalLongitude"].max()

    # 2. 計算地圖中心點（經度、緯度）
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2

    # 3. 根據資料範圍，簡單估算出 Zoom
    #    這裡提供一個簡單的經驗公式，可再依需求調整
    def get_zoom_for_bounds(min_lat, max_lat, min_lon, max_lon):
        # 計算範圍 (range) — 先拿 lat_range, lon_range 的較大者
        lat_range = max_lat - min_lat
        lon_range = max_lon - min_lon
        max_range = max(lat_range, lon_range)
        
        # 若資料點只有一個(或全部相同)，避免除以 0
        if max_range <= 0:
            return 10  # 給個預設比較近的 zoom
        
        # 常見的參考公式 zoom = 360° / max_range
        zoom = math.log2(360 / max_range)
        
        # 適度限制 zoom 的上下限，避免 zoom 過大或過小
        zoom = max(0, zoom)       # 不要小於 0
        zoom = min(20, zoom)      # 不要超過 20 (一般地圖約 20~22 已極近)
        return round(zoom, 2)     # 保留兩位小數

    auto_zoom = get_zoom_for_bounds(min_lat, max_lat, min_lon, max_lon)


    ## Define layer
    layer = pdk.Layer(
        'ScatterplotLayer',
        new_df,
        get_position = '[decimalLongitude, decimalLatitude]',
        get_radius = 'individualCount * 10 + 500',
        radius_min_pixels = 3,
        radius_max_pixels = 50,
        get_fill_color = '[255, 255, 0, 160]',
        pickable = True
    )

    ## Define view
    view_state = pdk.ViewState(
        latitude = center_lat,
        longitude = center_lon,
        zoom = auto_zoom,
        pitch = 0  # 傾斜角度
    )

    ## Display map through Streamlit ----
    st.write('Size: individualCount 點的大小代表個體數')
    st.pydeck_chart(pdk.Deck(
        layers = [layer],
        initial_view_state = view_state,
        tooltip = {'html': 'ID: <span style="font-family: monospace;">{occurrenceID}</span>, {vernacularName} <i>{scientificName}</i>'}
    ))