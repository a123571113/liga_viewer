import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

from src.utils_sorting import sort_results, create_pairing_list
from src.utils_data import get_data_current_event, get_data_steady_event 

# Load confing
from config import *


def initialize_states() -> None:
   
    try:
        df = get_data_steady_event(event="event_01")
        st.session_state["data_event_01"] = sort_results(result_df=df)
    except Exception as e:
        print(e)

    try:
        df = get_data_steady_event(event="event_02")
        st.session_state["data_event_02"] = sort_results(result_df=df)
    except Exception as e:
        print(e)

    try:
        df = get_data_steady_event(event="event_03")
        st.session_state["data_event_03"] = sort_results(result_df=df)
    except Exception as e:
        print(e)

    try:
        df = get_data_steady_event(event="event_04")
        st.session_state["data_event_04"] = sort_results(result_df=df)
    except Exception as e:
        print(e)
    
    try:
        df = get_data_current_event(event="event_05")
        st.session_state["data_event_05"] = sort_results(result_df=df)
    except Exception as e:
        print(e)

    try:
        df = get_data_steady_event(event="event_06")
        st.session_state["data_event_06"] = sort_results(result_df=df)
    except Exception as e:
        print(e)


def calculate_place_flow(result_df: pd.DataFrame) -> pd.DataFrame:
    df_sorted_index = pd.DataFrame()

    for i, name in enumerate(race_columns):
        
        df_buffer = result_df.copy()
        df_buffer.iloc[:, (i+3):] = 0 #np.nan

        indices = sort_results(df_buffer)["Teams"].values

        df_sorted_index[name] = indices

    result_df_ = pd.DataFrame(index=range(len(TEAMS)), columns=race_columns)
    result_df_.index = TEAMS

    for club in TEAMS:
        res = []
        for col in df_sorted_index.columns:
                        
            s = (df_sorted_index[col] == club)

            place = s[s].index.values[0] + 1

            res.append(place)
        
        result_df_.loc[club] = res
        
    return result_df_


def create_flow_plot(result_df_: pd.DataFrame):
    # Create a figure
    fig = go.Figure()

    # Plot each row of result_df_ as a separate trace
    for index, row in result_df_.iterrows():
        fig.add_trace(go.Scatter(
            x=row.index,
            y=row.values,
            mode='lines',
            name=f'{index}',
            # hovertemplate=f'Index: {row.index}<br>Value: %{y:.2f}<extra></extra>'
        ))

    # Update the layout of the figure
    fig.update_layout(
        height=800,
        width=1200,
        yaxis_title='Platz',
        yaxis=dict(autorange='reversed'),  # Reverse y-axis
        #xaxis_tickangle=-90,  # Rotate x-axis labels
        xaxis_title_font=dict(size=14),
        yaxis_title_font=dict(size=14),
    )

    # Show the plot
    return fig


def highlight_medals(val):
    if val == 1:
        color = 'rgba(255, 215, 0, 0.7)'  # Gold with transparency
    elif val == 2:
        color = 'rgba(192, 192, 192, 0.7)'  # Silver with transparency
    elif val == 3:
        color = 'rgba(205, 127, 50, 0.7)'  # Bronze with transparency
    else:
        color = ''
    return f'background-color: {color}'


def highlight_medals(val):
    if val == 1:
        color = 'rgba(255, 215, 0, 0.8)'  # Gold with transparency
    elif val == 2:
        color = 'rgba(192, 192, 192, 0.8)'  # Silver with transparency
    elif val == 3:
        color = 'rgba(205, 127, 50, 0.8)'  # Bronze with transparency
    else:
        color = ''
    return f'background-color: {color}'


def grey_last_rows(df):
    df_copy = pd.DataFrame('', index=df.index, columns=df.columns)
    df_copy.iloc[-4:, :] = 'background-color: rgba(224, 224, 224, 0.5)'
    return df_copy


def compute_overall():
    overall_results = pd.DataFrame({'Teams': TEAMS})

    for event in range(1, EVENTS+1):
        result_df = st.session_state["data_event_0" + str(event)]

        if result_df["Total"].sum() == 0:
            overall_results['Event {}'.format(event)] = 0
        
        else:

            result_df.insert(0, 'Rank', range(1, result_df.shape[0] + 1))
            result_df.sort_values(by='Teams', inplace=True)
            overall_results['Event {}'.format(event)] = result_df['Rank'].values
    
    sum_columns = ['Event {}'.format(event) for event in range(1, EVENTS + 1)]
    overall_results['Total'] = overall_results[sum_columns].sum(axis=1)
    overall_results.sort_values(by=['Total','Event {}'.format(EVENTS)], inplace=True)
    try:
        overall_results.drop(columns=['Rank'], inplace=True)
    except KeyError:
        pass
    
    overall_results.insert(0, 'Rank', range(1, overall_results.shape[0] + 1))

    overall_results = overall_results.style.map(
        highlight_medals,
        subset=sum_columns
    )

    overall_results = overall_results.apply(
        grey_last_rows, axis=None
    )


    st.write("### Saison 2024 Ergebnis")
    st.dataframe(
        overall_results,
        height=665,
        use_container_width=True,
        hide_index=True,
    )


def highlight_fleet(_, team_in_fleet: list[bool], color: str):
    return ["color:" + color if team else "" for team in team_in_fleet]
    # return ["background-color:" + color if team else "" for team in team_in_fleet]


def add_pairinglist_font(df: pd.DataFrame, event: int) -> pd.DataFrame:
    if event == 6:
        return df
    
    else:
        pairing_list, _ = create_pairing_list(event=event - 1)
        pairing_list = pairing_list.drop(["flight", "Race"], axis=1)

        pairing_list = pairing_list.replace("BYC(BA)", "BYC (BA)")
        pairing_list = pairing_list.replace("BYC(BE)", "BYC (BE)")

        pairing_list = pairing_list.replace("KYC(SH)", "KYC (SH)")
        pairing_list = pairing_list.replace("KYC(BW)", "KYC (BW)")
        
        teams = df["Teams"].values

        flight = 1
        style_df = df.style

        colors = ["red", "blue", "green"]
        # colors = ["#dca0b6", "#ADD8E6", "#90EE90"]

        for i in range(pairing_list.shape[0]):
            team_in_fleet = np.isin(teams, pairing_list.iloc[i, :].values)
            
            column_name = 'Flight ' + str(flight)
            
            color = colors[i % len(colors)]
            
            style_df = style_df.apply(highlight_fleet, subset=[column_name], team_in_fleet=team_in_fleet, color=color)#.map(lambda x: 'font-weight: bold')
                               #.set_properties(**{"font-weight": "bold"})

            if (i + 1) % 3 == 0:
                flight += 1
        
        return style_df


def display_event(title: str, data_event: str) -> None:
    st.write("### Ergebnisse " + title)

    data = st.session_state[data_event].astype(str)

    # print(data)

    data = data.replace("nan","0")

    # Replace 0 with "" in columns that only contain 0
    data_to_show = data.copy()
    
    for column in race_columns:
        try:
            if data_to_show[column].astype(float).sum() == 0:
               data_to_show[column] = data_to_show[column].str.replace("0", "")  
        except:
            pass

    data_to_show.insert(0, 'Rank', range(1, data_to_show.shape[0] + 1))

    if DISPLAY_COLORCODING:
        st.dataframe(
            add_pairinglist_font(df=data_to_show,event=int(data_event[-1])),
            height=665,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.dataframe(
            data_to_show,
            height=665,
            use_container_width=True,
            hide_index=True
        )

    df_ = calculate_place_flow(data)

    plot_flow = create_flow_plot(df_)

    st.write("### Flow")
    st.plotly_chart(plot_flow)