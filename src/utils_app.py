import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

from src.utils_sorting import sort_results, create_pairing_list
from src.utils_data import get_data_current_event, get_data_steady_event

# Load confing
from config import *

def setup_page() -> None:
    st.set_page_config(layout="wide")

    hide_streamlit_style = """
                    <style>
                    div[data-testid="stToolbar"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stDecoration"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stStatusWidget"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    #MainMenu {
                    visibility: hidden;
                    height: 0%;
                    }
                    header {
                    visibility: hidden;
                    height: 0%;
                    }
                    footer {
                    visibility: hidden;
                    height: 0%;
                    }
                    .custom-footer {
                    position: fixed;
                    bottom: 0.0;
                    width: 100%;
                    text-align: center;
                    font-size: 12px;
                    color: gray;
                    }
                    </style>
                    <div class="custom-footer">
                    Developed with ❤️ by Hans & Hans. Copyright 2024 Anton Sattler, Julius Neszvecsko.
                    </div>
                    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def initialize_states() -> None:
   
    for event, func_name in EVENTS_L1:
        try:
            # Dynamically call the appropriate function
            if func_name == "get_data_steady_event":
                df = get_data_steady_event(event=event, database="dsbl")
            else:
                df = get_data_current_event(event=event, database="dsbl")
            
            st.session_state[f"data_L1_{event}"] = sort_results(result_df=df)
        except Exception as e:
            print(e)

    for event, func_name in EVENTS_L2:
        try:
            # Dynamically call the appropriate function
            if func_name == "get_data_steady_event":
                df = get_data_steady_event(event=event, database="dsbl2")
            else:
                df = get_data_current_event(event=event, database="dsbl2")
            
            st.session_state[f"data_L2_{event}"] = sort_results(result_df=df)
        except Exception as e:
            print(e)


def calculate_place_flow(result_df: pd.DataFrame, liga:int) -> pd.DataFrame:
    if liga == 1:
        teams = TEAMS_L1

    elif liga == 2:
        teams = TEAMS_L2

    df_sorted_index = pd.DataFrame()

    for i, name in enumerate(race_columns):
        
        df_buffer = result_df.copy()
        df_buffer.iloc[:, (i+3):] = 0 #np.nan

        indices = sort_results(df_buffer)["Teams"].values

        df_sorted_index[name] = indices

    result_df_ = pd.DataFrame(index=range(len(teams)), columns=race_columns)
    result_df_.index = teams

    for club in teams:
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


def highlight_fleet(_, team_in_fleet: list[bool], color: str):
    return ["color:" + color if team else "" for team in team_in_fleet]
    # return ["background-color:" + color if team else "" for team in team_in_fleet]


def add_pairinglist_font(df: pd.DataFrame, event: int, liga: int) -> pd.DataFrame:
    pairing_list, _ = create_pairing_list(event=event - 1, liga=liga)
    pairing_list = pairing_list.drop(["flight", "Race"], axis=1)

    pairing_list = pairing_list.replace("BYC(BA)", "BYC (BA)")
    pairing_list = pairing_list.replace("BYC(BE)", "BYC (BE)")

    pairing_list = pairing_list.replace("KYC(SH)", "KYC (SH)")
    pairing_list = pairing_list.replace("KYC(BW)", "KYC (BW)")
    
    teams = df["Teams"].values

    flight = 1

    df.replace("", "___", inplace=True)
    style_df = df.style

    colors = ["red", "blue", "#109010"]
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


def display_event(title: str, data_event: str, liga: int) -> None:
    st.write("### Ergebnisse " + title)

    data = st.session_state[data_event].astype(str)

    # print(data)

    data = data.replace("nan","0")

    # Replace 0 with "" in columns that only contain 0
    data_to_show = data.copy()

    # data_to_show["SCP"] = data_to_show["SCP"].astype(float).astype(int).astype(str)
    
    for column in race_columns:
        try:
            if data_to_show[column].astype(float).sum() == 0:
               data_to_show[column] = data_to_show[column].str.replace("0", "")  
        except:
            pass

    for column in race_columns:
        data_to_show[column] = data_to_show[column].str.replace(".0", "")

    data_to_show.insert(0, 'Rank', range(1, data_to_show.shape[0] + 1))

    if DISPLAY_COLORCODING:
        st.dataframe(
            add_pairinglist_font(
                df=data_to_show,event=int(data_event[-1]),
                liga=liga
            ),
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

    # df_ = calculate_place_flow(result_df=data, liga=liga)

    # plot_flow = create_flow_plot(df_)

    # st.write("### Flow")
    # st.plotly_chart(plot_flow)


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


def compute_overall(events: int, liga: int) -> None:
    if liga == 1:
        teams = TEAMS_L1
        session_name = "data_L1_event_0"

    elif liga == 2:
        teams = TEAMS_L2
        session_name = "data_L2_event_0"
        # events = 4

    overall_results = pd.DataFrame({'Teams': teams})
    valid_events = []
    for event in range(1, events+1):
        result_df = st.session_state[session_name + str(event)]

        # get only valid events with enough flights completed
        # TODO: maybe fix, such that this is only applied after event is finished,
        #  e.g. eventw with 3 flights is included on a friday but not on sunday afternoon
        if result_df.dropna(inplace=False, axis=1, how='any',).shape[1] > 7:
            valid_events.append(event)
        else:
            # ignore event
            continue

        if result_df["Total"].min() == 0:
            overall_results['Event {}'.format(event)] = 0
        else:
            result_df.insert(0, 'Rank', range(1, result_df.shape[0] + 1))
            result_df.sort_values(by='Teams', inplace=True)
            overall_results['Event {}'.format(event)] = result_df['Rank'].values

    # if no event is valid, just return the teams
    if len(valid_events) == 0:
        return overall_results

    sum_columns = ['Event {}'.format(event) for event in valid_events]
    overall_results['Total'] = overall_results[sum_columns].sum(axis=1)
    overall_results.sort_values(by=['Total','Event {}'.format(max(valid_events))], inplace=True)
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

    return overall_results


def display_overall() -> None:
    L1_saison = compute_overall(events=len(EVENTS_L1), liga=1) 

    L2_saison = compute_overall(events=len(EVENTS_L2), liga=2)

    print("[INFO] Overall results computed.") 

    _, col_L1, _, col_L2, _ = st.columns([1, 4, 1, 4, 1])

    with col_L1:
        st.write("### 1. Liga")
        st.dataframe(
            L1_saison,
            height=665,
            use_container_width=True,
            hide_index=True
        )

    with col_L2:
        st.write("### 2. Liga")
        st.dataframe(
            L2_saison,
            height=665,
            use_container_width=True,
            hide_index=True,
            
        )
