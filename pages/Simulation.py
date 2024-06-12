import heapq
import pandas as pd
import numpy as np
from Single_simulation import Single_simulation
import streamlit as st
from scipy import stats
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns
import time

import sys
import os



# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



st.header("Parameteres de la simulation")

c1, c2 ,c3= st.columns(3)

IX = c1.number_input("IX :",value=10, min_value=1, max_value=30000)
IY = c2.number_input("IY :",value=20, min_value=1, max_value=30000)
IZ = c3.number_input("IZ :",value=30, min_value=1, max_value=30000)

dIX = c1.number_input("dIX :",value=5, min_value=1, max_value=20)
dIY = c2.number_input("dIY :",value=7, min_value=1, max_value=20)
dIZ = c3.number_input("dIZ :",value=11, min_value=1, max_value=20)

a1, a2,a3,a4= st.columns(4)
opening = a1.number_input("open_time :",value=9,min_value=7, max_value=11)
closing = a2.number_input("close_time :",value=21,min_value=19, max_value=23)
num_simulations = a3.number_input("num_simulations :",value=40,min_value=1, max_value=100)
prob_no_payment = a4.number_input("prob_no_payment :",value=0.15,min_value=0.1, max_value=0.3)

open_time = opening*60
close_time = closing*60
ARRIVAL = "arrival"
cols=['PN', 'PP', 'NCE','NCP','NCAMT','NCNPC','TATmoy','LMQ','TMaxQ1','TSmoy','TauxC1','TauxC2']
Plots = ["Box Plot","Line Plot","Heatmap","Histogram","Violin Plot"]
df2 = pd.DataFrame(columns=cols)
df3 = pd.DataFrame(columns=cols+['TauxC3'])

def initialize():
    return ([],[],[[0,0] for _ in range(2000)],0,open_time,open_time)

def schedule_event(events,time, event_type, customer_id):
        heapq.heappush(events, (time, event_type, customer_id))
        if event_type == ARRIVAL :
            customer_times[customer_id][0] = time
        else :
            customer_times[customer_id][1] = time

for i in range(int(num_simulations)):
    events,queue,customer_times,total_customers,current_time,last_queue_length_update_time = initialize()
    # Initial event: first customer arrival
    schedule_event(events,current_time, ARRIVAL, total_customers)
    # Simulation loop
    Result2 = Single_simulation(current_time,
    last_queue_length_update_time,
    events,
    queue,
    schedule_event,
    customer_times,
    IX,
    IY,
    IZ,
    2,
    open_time,
    close_time,
    prob_no_payment)
    
    df2 = pd.concat([df2, pd.DataFrame([Result2], columns=cols)], ignore_index=True)
    events,queue,customer_times,total_customers,current_time,last_queue_length_update_time = initialize()
    # Initial event: first customer arrival
    schedule_event(events,current_time, ARRIVAL, total_customers)

    Result3 = Single_simulation(current_time,
    last_queue_length_update_time,
    events,
    queue,
    schedule_event,
    customer_times,
    IX,
    IY,
    IZ,
    3,
    open_time,
    close_time,
    prob_no_payment)
    
    df3 = pd.concat([df3, pd.DataFrame([Result3], columns=cols+['TauxC3'])], ignore_index=True)

    IX,IY,IZ = IX+dIX,IY+dIY,IZ+dIZ

Data = {2:df2,3:df3}

def Plot(df, option, column):
    fig, ax = plt.subplots(figsize=(16, 9))

    if option == "Box Plot":
        sns.boxplot(data=df, y=column, ax=ax)
        ax.set_title(f'Box Plot of {column}', fontsize=16)
        ax.set_xlabel('Values', fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)

    elif option == "Line Plot":
        sns.lineplot(data=df, x=df.index, y=column, ax=ax, marker='o')
        ax.set_title(f'Line Plot of {column} Across Simulation Runs', fontsize=16)
        ax.set_xlabel('Simulation Run', fontsize=14)
        ax.set_ylabel(column, fontsize=14)

    elif option == "Histogram":
        sns.histplot(df[column], bins=20, kde=True, ax=ax)
        ax.set_title(f'Histogram of {column}', fontsize=16)
        ax.set_xlabel('Values', fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)

    elif option == "Heatmap":
        corr = df.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Heatmap', fontsize=16)
        ax.set_xlabel('Metrics', fontsize=14)
        ax.set_ylabel('Metrics', fontsize=14)

    else:
        sns.violinplot(data=df, x=column, ax=ax)
        ax.set_title(f'Violin Plot of {column}', fontsize=16)
        ax.set_xlabel('Values', fontsize=14)
        ax.set_ylabel('Density', fontsize=14)

    return fig

@st.experimental_fragment
def Stats(df,option):
    st.subheader("Statistiques")
    confidence_level = st.slider("Confidence level", 0.8, 1.0, 0.95, 0.01)
    sample_mean = df[option].mean()
    sample_std = df[option].std()
    n = len(df[option])
    standard_error = sample_std / np.sqrt(n)
    t_score = stats.t.ppf((1 + confidence_level) / 2, n - 1)
    margin_of_error = t_score * standard_error
    confidence_interval = (sample_mean - margin_of_error, sample_mean + margin_of_error)
    st.metric(label=f"Confidence interval de {option}", value=f"{confidence_interval}", delta=f"±{margin_of_error:.2f}",delta_color="off")
    st.subheader(f"Histogram and Confidence Interval for {option}")
    fig, ax = plt.subplots(figsize=(16, 9))
    sns.histplot(df[option], bins=20, kde=True, ax=ax) # type: ignore
    ax.axvline(sample_mean, color='r', linestyle='--', label='Mean')
    ax.axvline(confidence_interval[0], color='g', linestyle='--', label=f'Lower Bound ({confidence_interval[0]:.2f})')
    ax.axvline(confidence_interval[1], color='b', linestyle='--', label=f'Upper Bound ({confidence_interval[1]:.2f})')
    ax.fill_betweenx([0, ax.get_ylim()[1]], confidence_interval[0], confidence_interval[1], color='yellow', alpha=0.3)
    ax.set_title(f"Histogram of {option} with {int(confidence_level*100)}% Confidence Interval")
    ax.set_xlabel('Values')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)

def perform_Ttest(df2, df3, column):
    data1 = df2[column]
    data2 = df3[column]

    Ttest_result = f_oneway(data1, data2)

    return Ttest_result.statistic, Ttest_result.pvalue

@st.experimental_fragment
def Simulation(i):
    st.header(f"Résultat de simulation de {i} Caisses")
    st.subheader(f"{i} Caisses simulation")
    st.dataframe(Data[i],use_container_width=True)
    st.dataframe(Data[i].describe(),use_container_width=True)

    st.subheader("Visualisation des données")
    col1,col2 = st.columns(2)
    option = col1.selectbox("Selectionner l'indicateur à analyser",list(Data[i]),key="option")
    plot_type = col2.selectbox("Selectionner le type de plot",Plots,key="plot_type1")
    fig = Plot(Data[i],plot_type,option)
    st.pyplot(fig)
    Stats(Data[i],option)

@st.experimental_fragment
def Comparaison():
    st.header("Comparison des simulations")
    col1,col2 = st.columns(2)
    option = col1.selectbox("Select the indicator to visualize?",cols,key="option2" )
    plot_type = col2.selectbox("Selectionner le type de plot",["Box Plot","Line Plot"],key="comparison_option")
    df2_renamed = df2.rename(columns={option: f'{option} (2 caisses)'})
    df3_renamed = df3.rename(columns={option: f'{option} (3 caisses)'})
    combined_df = pd.concat([df2_renamed[f'{option} (2 caisses)'], df3_renamed[f'{option} (3 caisses)']], axis=1)
    fig, ax = plt.subplots(figsize=(16, 9))
    if plot_type == "Box Plot":
        sns.boxplot(data=combined_df, ax=ax)
        ax.set_title(f'Box Plot of {option} for 2 and 3 Caisses Simulations', fontsize=16)
        ax.set_xlabel('Values', fontsize=14)
        ax.set_ylabel('Frequency', fontsize=14)
        ax.legend()
        st.pyplot(fig)
    else :
        sns.lineplot(data=combined_df, ax=ax, marker='o')
        ax.set_title(f'Line Plot of {option} for 2 and 3 Caisses Simulations', fontsize=16)
        ax.set_xlabel('Simulation Run', fontsize=14)
        ax.set_ylabel(option, fontsize=14)
        ax.legend()
        st.pyplot(fig)

    F_statistic, p_value = perform_Ttest(df2, df3, option)
    treshold = st.slider("F-statistic threshold", 0.0, 0.2, 0.05, 0.01)
    P1,P2,P3  = st.columns([1.5,3.5,0.5])
    P2.write(f"**T_test Results for column {option}:**")
    P2.write(f"F-statistic: {F_statistic:.2f}")
    P2.write(f"p-value: {p_value:.4f}")
    
    if p_value <= treshold:
        P2.write("**Conclusion:** There is a statistically significant difference between the means.")
    else:
        P2.write("**Conclusion:** There is no statistically significant difference between the means.")


with st.sidebar:
    page = st.radio(
    "Navigation",
    ('2 Caisses Simulation', '3 Caisses Simulation', 'Comparaison')
)


if page == '2 Caisses Simulation':
        Simulation(2)
elif page == '3 Caisses Simulation':
        Simulation(3)
elif page == 'Comparaison':
        Comparaison()
