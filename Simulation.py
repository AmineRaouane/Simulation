import heapq
import pandas as pd
import numpy as np
from Single_simulation import Single_simulation
import sys
import os
import streamlit as st

st.title("Simulation supermarché")

c1, c2 ,c3= st.columns(3)

IX = c1.number_input("IX :",value=10, min_value=1, max_value=30000)
IY = c2.number_input("IY :",value=20, min_value=1, max_value=30000)
IZ = c3.number_input("IZ :",value=30, min_value=1, max_value=30000)

dIX = c1.number_input("dIX :",value=7, min_value=1, max_value=20)
dIY = c2.number_input("dIY :",value=13, min_value=1, max_value=20)
dIZ = c3.number_input("dIZ :",value=17, min_value=1, max_value=20)

num_simulations = st.number_input("num_simulations :",value=4,min_value=4, max_value=100)




def alea(IX,IY,IZ):
  # Opérations modulo pour maintenir IX, IY et IZ dans l'intervalle [0, 176]
  IX = 171*(IX % 177) - 2 * (IX // 177) #type:ignore
  IY = 172*(IY % 176) - 35 * (IY // 176) #type:ignore
  IZ = 170*(IZ % 178) - 63 * (IZ // 178) #type:ignore

  # Ajouter 30269, 30307 et 30323 si IX, IY ou IZ est négatif
  if IX < 0:
    IX += 30269
  if IY < 0:
    IY += 30307
  if IZ < 0:
    IZ += 30323
  # Calculer la valeur intermédiaire
  inter = (IX / 30269) + (IY / 30307) + (IZ / 30323)
  # Retourner la partie fractionnaire de la valeur intermédiaire et les nouvelles valeurs de IX, IY et IZ
  return [inter - int(inter),IX,IY,IZ]

def draw_from_distribution(IX,IY,IZ,values, probabilities):
    # return random.choices(values, probabilities)[0]
    x,IX,IY,IZ = alea(IX,IY,IZ)#type:ignore
    for idx, cum_prob in enumerate(np.cumsum(probabilities)):
        if x <= cum_prob:
            return (values[idx],IX,IY,IZ)
    return (x,IX,IY,IZ)

# Simulation parameters
open_time = 9 * 60  # in minutes (9 AM)
close_time = 21 * 60  # in minutes (9 PM)
# Event types
ARRIVAL = "arrival"
SHOPPING_DONE = "shopping_done"
PAYMENT_DONE_C1 = "payment_done_c1"
PAYMENT_DONE_C2 = "payment_done_c2"
PAYMENT_DONE_C3 = "payment_done_c3"
# Inter-arrival time distribution for normal periods
normal_arrival_intervals = [1, 2, 3, 4, 5, 6]
normal_arrival_probabilities = [0.30, 0.50, 0.10, 0.05, 0.03, 0.02]
# Inter-arrival time distribution for peak periods
peak_arrival_intervals = [0, 1, 2, 3]
peak_arrival_probabilities = [0.15, 0.30, 0.40, 0.15]
# Shopping time distribution
shopping_times = [2, 4, 6, 8, 10]
shopping_probabilities = [0.10, 0.20, 0.40, 0.20, 0.10]
# Payment time distribution
payment_times = [1, 2, 3, 4]
payment_probabilities = [0.20, 0.40, 0.25, 0.15]
# Probability that a customer will not proceed to payment after shopping
prob_no_payment = 0.15


# IX= int(input("IX "))
# IY = int(input("IY "))
# IZ = int(input("IZ "))

cols=['PN', 'PP', 'NCE','NCP','NCAMT','NCNPC','TATmoy','LMQ','TMaxQ1','TSmoy','TauxC1','TauxC2']
df2 = pd.DataFrame(columns=cols)
df3 = pd.DataFrame(columns=cols+['TauxC3'])

for i in range(int(num_simulations)):
    current_time = open_time
    total_customers = 0
    lost_customers = 0
    normal_period_customers = 0
    peak_period_customers = 0
    same_time_arrivals = 0
    not_payed_customers = 0
    total_waiting_time = 0
    total_queue_length = 0
    time_with_max_one_customer = 0
    total_system_time = 0
    customer_times = [[0,0] for _ in range(2000)]

    events = []  # Priority queue for events
    queue = []

# Payment counters
    counter_1_busy = False
    counter_2_busy = False
    counter_1_utilization_time = 0
    counter_2_utilization_time = 0
    counter_3_busy = False
    counter_3_utilization_time = 0

    last_queue_length_update_time = current_time
# Function to schedule an event
    def schedule_event(time, event_type, customer_id):
        heapq.heappush(events, (time, event_type, customer_id))
        if event_type == ARRIVAL :
            customer_times[customer_id][0] = time
        else :
            customer_times[customer_id][1] = time

    # Determine if the current time is in a peak period
    def is_peak_period(time):
        return (12 * 60 <= time < 15 * 60) or (18 * 60 <= time < 21 * 60)

    # Initial event: first customer arrival
    schedule_event(current_time, ARRIVAL, total_customers)

    # Simulation loop
    Result2 = Single_simulation(current_time,
    last_queue_length_update_time,
    total_customers ,
    lost_customers ,
    normal_period_customers ,
    peak_period_customers ,
    same_time_arrivals ,
    not_payed_customers ,
    total_waiting_time ,
    total_queue_length ,
    time_with_max_one_customer ,
    total_system_time ,
    customer_times,
    ARRIVAL ,
    SHOPPING_DONE ,
    PAYMENT_DONE_C1 ,
    PAYMENT_DONE_C2 ,
    PAYMENT_DONE_C3,
    open_time,
    close_time,
    events,
    queue,
    normal_arrival_intervals,
    normal_arrival_probabilities ,
    peak_arrival_intervals,
    peak_arrival_probabilities,
    shopping_times,
    shopping_probabilities,
    payment_times,
    payment_probabilities,
    prob_no_payment,
    counter_1_busy,
    counter_2_busy,
    counter_1_utilization_time,
    counter_2_utilization_time,
    counter_3_busy,
    counter_3_utilization_time,
    alea,
    draw_from_distribution,
    is_peak_period,
    schedule_event,
    IX,
    IY,
    IZ,2)
    
    df2 = pd.concat([df2, pd.DataFrame([Result2], columns=cols)], ignore_index=True)
    IX,IY,IZ = IX+dIX,IY+dIY,IZ+dIZ

st.header("2 Caisses simulation")
st.dataframe(df2)


for i in range(int(num_simulations)):
    current_time = open_time
    total_customers = 0
    lost_customers = 0
    normal_period_customers = 0
    peak_period_customers = 0
    same_time_arrivals = 0
    not_payed_customers = 0
    total_waiting_time = 0
    total_queue_length = 0
    time_with_max_one_customer = 0
    total_system_time = 0
    customer_times = [[0,0] for _ in range(2000)]

    events = []  # Priority queue for events
    queue = []

# Payment counters
    counter_1_busy = False
    counter_2_busy = False
    counter_1_utilization_time = 0
    counter_2_utilization_time = 0
    counter_3_busy = False
    counter_3_utilization_time = 0

    last_queue_length_update_time = current_time
# Function to schedule an event
    def schedule_event(time, event_type, customer_id):
        heapq.heappush(events, (time, event_type, customer_id))
        if event_type == ARRIVAL :
            customer_times[customer_id][0] = time
        else :
            customer_times[customer_id][1] = time

    # Determine if the current time is in a peak period
    def is_peak_period(time):
        return (12 * 60 <= time < 15 * 60) or (18 * 60 <= time < 21 * 60)

    # Initial event: first customer arrival
    schedule_event(current_time, ARRIVAL, total_customers)

    # Simulation loop
    Result3 = Single_simulation(current_time,
    last_queue_length_update_time,
    total_customers ,
    lost_customers ,
    normal_period_customers ,
    peak_period_customers ,
    same_time_arrivals ,
    not_payed_customers ,
    total_waiting_time ,
    total_queue_length ,
    time_with_max_one_customer ,
    total_system_time ,
    customer_times,
    ARRIVAL ,
    SHOPPING_DONE ,
    PAYMENT_DONE_C1 ,
    PAYMENT_DONE_C2 ,
    PAYMENT_DONE_C3,
    open_time,
    close_time,
    events,
    queue,
    normal_arrival_intervals,
    normal_arrival_probabilities ,
    peak_arrival_intervals,
    peak_arrival_probabilities,
    shopping_times,
    shopping_probabilities,
    payment_times,
    payment_probabilities,
    prob_no_payment,
    counter_1_busy,
    counter_2_busy,
    counter_1_utilization_time,
    counter_2_utilization_time,
    counter_3_busy,
    counter_3_utilization_time,
    alea,
    draw_from_distribution,
    is_peak_period,
    schedule_event,
    IX,
    IY,
    IZ,3)
    
    df3 = pd.concat([df3, pd.DataFrame([Result3], columns=cols+['TauxC3'])], ignore_index=True)
    IX,IY,IZ = IX+dIX,IY+dIY,IZ+dIZ

st.header("3 Caisses simulation")
st.dataframe(df3)