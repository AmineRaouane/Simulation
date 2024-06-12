import heapq
import numpy as np

def alea(IX,IY,IZ):
  # Opérations modulo pour maintenir IX, IY et IZ dans l'intervalle [0, 176]
  IX = 171*(IX % 177) - 2 * (IX // 177) #type:ignore
  IY = 172*(IY % 176) - 35 * (IY // 176) #type:ignore
  IZ = 170*(IZ % 178) - 63 * (IZ // 178) #type:ignore

  if IX < 0:
    IX += 30269
  if IY < 0:
    IY += 30307
  if IZ < 0:
    IZ += 30323
  # Calculer la valeur intermédiaire
  inter = (IX / 30269) + (IY / 30307) + (IZ / 30323)
  return [inter - int(inter),IX,IY,IZ]

def draw_from_distribution(IX,IY,IZ,values, probabilities):
    # return random.choices(values, probabilities)[0]
    x,IX,IY,IZ = alea(IX,IY,IZ)#type:ignore
    cum_probs = np.cumsum(probabilities)
    idx = np.searchsorted(cum_probs, x)
    return (values[idx], IX, IY, IZ)
    

def is_peak_period(time,close_time):
        return (12 * 60 <= time < 15 * 60) or (18 * 60 <= time < close_time)

def Single_simulation(current_time, last_queue_length_update_time, events, queue, schedule_event, customer_times, IX, IY, IZ, Caisses, open_time, close_time, prob_no_payment):
    # Event handling variables
    counter_busy = [False] * Caisses
    counter_utilization_time = [0] * Caisses
    total_customers, lost_customers = 0, 0
    normal_period_customers, peak_period_customers = 0, 0
    same_time_arrivals, not_payed_customers = 0, 0
    total_waiting_time, total_queue_length = 0, 0
    time_with_max_one_customer = 0

    ARRIVAL, SHOPPING_DONE = "arrival", "shopping_done"
    PAYMENT_DONE = [f"payment_done_c{i+1}" for i in range(Caisses)]
    normal_arrival_intervals = [1, 2, 3, 4, 5, 6]
    normal_arrival_probabilities = [0.30, 0.50, 0.10, 0.05, 0.03, 0.02]
    peak_arrival_intervals = [0, 1, 2, 3]
    peak_arrival_probabilities = [0.15, 0.30, 0.40, 0.15]
    shopping_times = [2, 4, 6, 8, 10]
    shopping_probabilities = [0.10, 0.20, 0.40, 0.20, 0.10]
    payment_times = [1, 2, 3, 4]
    payment_probabilities = [0.20, 0.40, 0.25, 0.15]

    while current_time < close_time or events:
        if events:
            current_time, event_type, customer_id = heapq.heappop(events)
        else:
            break
        
        if event_type == ARRIVAL:
            if current_time >= close_time:
                break

            total_customers += 1
            next_customer_id = total_customers

            if is_peak_period(current_time,close_time):
                inter_arrival_time, IX, IY, IZ = draw_from_distribution(IX, IY, IZ, peak_arrival_intervals, peak_arrival_probabilities)
                peak_period_customers += 1
            else:
                inter_arrival_time, IX, IY, IZ = draw_from_distribution(IX, IY, IZ, normal_arrival_intervals, normal_arrival_probabilities)
                normal_period_customers += 1

            next_arrival_time = current_time + inter_arrival_time
            schedule_event(events, next_arrival_time, ARRIVAL, next_customer_id)

            if inter_arrival_time == 0:
                same_time_arrivals += 1

            if len(queue) < 2:
                shopping_time, IX, IY, IZ = draw_from_distribution(IX, IY, IZ, shopping_times, shopping_probabilities)
                shopping_done_time = current_time + shopping_time
                schedule_event(events, shopping_done_time, SHOPPING_DONE, customer_id)
            else:
                lost_customers += 1

        elif event_type == SHOPPING_DONE:
            x, IX, IY, IZ = alea(IX,IY,IZ)
            if x < prob_no_payment:
                not_payed_customers += 1
            else:
                queue.append((customer_id, current_time))
                for i in range(Caisses):
                    if not counter_busy[i]:
                        counter_busy[i] = True
                        queue_customer_id, queue_entry_time = queue.pop(0)
                        payment_time, IX, IY, IZ = draw_from_distribution(IX, IY, IZ, payment_times, payment_probabilities)
                        counter_utilization_time[i] += payment_time
                        payment_done_time = current_time + payment_time
                        total_waiting_time += current_time - queue_entry_time
                        schedule_event(events, payment_done_time, PAYMENT_DONE[i], queue_customer_id)
                        break

        else:
            counter_index = int(event_type[-1]) - 1
            counter_busy[counter_index] = False
            if queue:
                counter_busy[counter_index] = True
                queue_customer_id, queue_entry_time = queue.pop(0)
                payment_time, IX, IY, IZ = draw_from_distribution(IX, IY, IZ, payment_times, payment_probabilities)
                counter_utilization_time[counter_index] += payment_time
                payment_done_time = current_time + payment_time
                total_waiting_time += current_time - queue_entry_time
                schedule_event(events, payment_done_time, PAYMENT_DONE[counter_index], queue_customer_id)

        if len(queue) <= 1:
            time_with_max_one_customer += (current_time - last_queue_length_update_time)

        total_queue_length += len(queue) * (current_time - last_queue_length_update_time)
        last_queue_length_update_time = current_time

    total_simulation_time = close_time - open_time
    average_waiting_time = total_waiting_time / (total_customers - not_payed_customers) if total_customers else 0
    average_queue_length = total_queue_length / total_simulation_time
    time_with_max_one_customer_ratio = time_with_max_one_customer / total_simulation_time
    average_system_time = sum([max(end - start, 0) for start, end in customer_times]) / total_customers if total_customers else 0
    utilization_ratios = [utilization / total_simulation_time for utilization in counter_utilization_time]

    return [
        normal_period_customers/1, peak_period_customers/1, total_customers/1, lost_customers/1,
        same_time_arrivals/1, not_payed_customers/1, average_waiting_time, average_queue_length,
        time_with_max_one_customer_ratio, average_system_time, *utilization_ratios
    ]

#cols=['PN', 'PP', 'NCE','NCP','NCAMT','NCNPC','TATmoy','LMQ','TMaxQ1','TSmoy','TauxC1','TauxC2']
