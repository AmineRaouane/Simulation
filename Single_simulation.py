import heapq
import random
import numpy as np


def Single_simulation(current_time,
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
    IZ,
    Caisses):

    while current_time < close_time or events:
        # Get next event
        if events:
            current_time, event_type, customer_id = heapq.heappop(events)
        else:
            break
        
        if event_type == ARRIVAL:


            if current_time >= close_time:
                break

            total_customers += 1
            next_customer_id = total_customers

            # Determine inter-arrival time based on period
            if is_peak_period(current_time):
                inter_arrival_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,peak_arrival_intervals, peak_arrival_probabilities)
                peak_period_customers += 1
            else:
                inter_arrival_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,normal_arrival_intervals, normal_arrival_probabilities)
                normal_period_customers += 1

            next_arrival_time = current_time + inter_arrival_time
            schedule_event(next_arrival_time, ARRIVAL, next_customer_id)

            # Check for customers arriving at the same time
            if inter_arrival_time == 0:
                same_time_arrivals += 1

            if len(queue) < 2:
                # Customer goes shopping
                shopping_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,shopping_times, shopping_probabilities)
                shopping_done_time = current_time + shopping_time
                schedule_event(shopping_done_time, SHOPPING_DONE, customer_id)
            else:
                # Customer leaves
                lost_customers += 1

        elif event_type == SHOPPING_DONE:
            # 15% chance customer does not proceed to payment
            x,IX,IY,IZ=alea(IX,IY,IZ)
            if x < prob_no_payment:
                not_payed_customers += 1
            else:
                # Customer finished shopping and joins queue
                queue.append((customer_id, current_time))  # Append with current time for waiting calculation

                # Try to send customer to a counter
                if not counter_1_busy:
                    # Send to counter 1
                    counter_1_busy = True
                    queue_customer_id, queue_entry_time = queue.pop(0)
                    payment_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,payment_times, payment_probabilities)
                    counter_1_utilization_time += payment_time # type: ignore
                    payment_done_time = current_time + payment_time
                    total_waiting_time += current_time - queue_entry_time
                    schedule_event(payment_done_time, PAYMENT_DONE_C1, queue_customer_id)
                elif not counter_2_busy:
                    # Send to counter 2
                    counter_2_busy = True
                    queue_customer_id, queue_entry_time = queue.pop(0)
                    payment_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,payment_times, payment_probabilities)
                    counter_2_utilization_time += payment_time # type: ignore
                    payment_done_time = current_time + payment_time
                    total_waiting_time += current_time - queue_entry_time
                    schedule_event(payment_done_time, PAYMENT_DONE_C2, queue_customer_id)
                #!
                elif Caisses==3 and not counter_3_busy:
                    # Send to counter 3
                    counter_3_busy = True
                    queue_customer_id, queue_entry_time = queue.pop(0)
                    payment_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,payment_times, payment_probabilities)
                    counter_3_utilization_time += payment_time # type: ignore
                    payment_done_time = current_time + payment_time
                    total_waiting_time += current_time - queue_entry_time
                    schedule_event(payment_done_time, PAYMENT_DONE_C3, queue_customer_id)


        elif event_type == PAYMENT_DONE_C1:
            # Customer finished paying at counter 1
            counter_1_busy = False

            # Check queue for next customer
            if queue:
                counter_1_busy = True
                queue_customer_id, queue_entry_time = queue.pop(0)
                payment_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,payment_times, payment_probabilities)
                counter_1_utilization_time += payment_time # type: ignore
                payment_done_time = current_time + payment_time
                total_waiting_time += current_time - queue_entry_time
                schedule_event(payment_done_time, PAYMENT_DONE_C1, queue_customer_id)

        elif event_type == PAYMENT_DONE_C2:
            # Customer finished paying at counter 2
            counter_2_busy = False

            # Check queue for next customer
            if queue:
                counter_2_busy = True
                queue_customer_id, queue_entry_time = queue.pop(0)
                payment_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,payment_times, payment_probabilities)
                counter_2_utilization_time += payment_time # type: ignore
                payment_done_time = current_time + payment_time
                total_waiting_time += current_time - queue_entry_time
                schedule_event(payment_done_time, PAYMENT_DONE_C2, queue_customer_id)
        #!
        elif Caisses==3 and event_type == PAYMENT_DONE_C3:

            counter_3_busy = False
            # Check queue for next customer
            if queue:
                counter_3_busy = True
                queue_customer_id, queue_entry_time = queue.pop(0)
                payment_time,IX,IY,IZ = draw_from_distribution(IX,IY,IZ,payment_times, payment_probabilities)
                counter_3_utilization_time += payment_time # type: ignore
                payment_done_time = current_time + payment_time
                total_waiting_time += current_time - queue_entry_time
                schedule_event(payment_done_time, PAYMENT_DONE_C3, queue_customer_id)

        if len(queue) <= 1:
            time_with_max_one_customer += (current_time - last_queue_length_update_time)

        # Update total queue length
        total_queue_length += len(queue) * (current_time - last_queue_length_update_time)
        last_queue_length_update_time = current_time
        # Track times with at most one customer in queue

    # Calculate metrics
    total_simulation_time = close_time - open_time
    average_waiting_time = total_waiting_time / (total_customers - not_payed_customers) if total_customers else 0
    average_queue_length = total_queue_length / total_simulation_time
    time_with_max_one_customer_ratio = time_with_max_one_customer / total_simulation_time
    counter_1_utilization_ratio = counter_1_utilization_time / total_simulation_time
    counter_2_utilization_ratio = counter_2_utilization_time / total_simulation_time
    counter_3_utilization_ratio = counter_3_utilization_time / total_simulation_time
    total_system_time = sum([max(end-start,0) for (start,end) in customer_times])
    average_system_time = total_system_time / total_customers if total_customers else 0
    L = [counter_3_utilization_ratio] if Caisses==3 else []
    return [normal_period_customers,peak_period_customers,total_customers,lost_customers,
            same_time_arrivals,not_payed_customers,average_waiting_time,average_queue_length,
            time_with_max_one_customer_ratio,average_system_time,counter_1_utilization_ratio,
            counter_2_utilization_ratio] + L