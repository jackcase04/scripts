import sys
import struct
import numpy as np
import matplotlib.pyplot as plt

PROFILED_FUNCTION_COUNT = 6
PROFILED_SAMPLES = 1024
TIMER_FREQ = 84.0

FUNCTION_NAMES = [
    "SCH_LOOP",
    "LED_HIGH",
    "LED_LOW",
    "BUTTON",
    "UART",
    "ADC",
]

def parse_file(filepath, should_return_dict=True):
    with open(filepath, 'rb') as file:
        data = file.read()

    index_size = PROFILED_FUNCTION_COUNT * 4
    temp_index = struct.unpack(f"<{PROFILED_FUNCTION_COUNT * 2}H", data[:index_size])
    profile_index = np.array(temp_index).reshape(PROFILED_FUNCTION_COUNT, 2)

    temp_time = struct.unpack(f"{PROFILED_FUNCTION_COUNT * PROFILED_SAMPLES * 2}I", data[index_size:])
    profile_time = np.array(temp_time).reshape(PROFILED_FUNCTION_COUNT, 2, PROFILED_SAMPLES)

    # At this point in the code we have profile_index and profile_time
    # just like they are in the C code. From here on out it's converted
    # to a hash map to be easier to work with.
    # If you need access to the specific start and end times, you can 
    # come back to here to get them from profile_index and profile_time.

    if should_return_dict:
        dict = {}

        for i in range(len(FUNCTION_NAMES)):
            durations_us = []

            samples = profile_index[i][0]

            if samples == 0:
                dict[FUNCTION_NAMES[i]] = durations_us
                continue

            start_times = profile_time[i][0][:samples]
            end_times = profile_time[i][1][:samples]

            durations_us = (end_times - start_times) / TIMER_FREQ

            dict[FUNCTION_NAMES[i]] = durations_us

        return dict
    else:
        return profile_index, profile_time

def print_summary(results):
    print("\nFunction      Samples   Avg (µs)   Min (µs)   Max (µs)  Jitter (µs)")
    print("-----------------------------------------------------------------")

    for function, durations_us in results.items(): 
        samples = len(durations_us)
        if samples == 0:
            print(f"{function:<12} {0:>8}")
            continue
        
        print(f"{function:<12} {samples:>8} {np.mean(durations_us):>10.3f} {np.min(durations_us):>10.3f} "
              f"{np.max(durations_us):>10.3f} {np.max(durations_us)-np.min(durations_us):>12.3f}")

def func_exec_time(results, functions_to_plot):
    fig, axes = plt.subplots(len(functions_to_plot),1, figsize=(10,8))

    for i in range(len(functions_to_plot)):
        axes[i].plot(results[functions_to_plot[i]])
        axes[i].set_title(functions_to_plot[i])
        axes[i].set_xlabel("Sample number")
        axes[i].set_ylabel("Duration (µs)")

    plt.tight_layout()
    plt.show()
    # plt.savefig("execution_times.png", dpi=150)  

def sch_loop_period(profile_index, profile_time):
    samples = profile_index[0][0]

    start_times = profile_time[0][0][:samples]

    distance_us = []

    for i in range(len(start_times) - 1):
        distance_us.append((start_times[i+1] - start_times[i]) / TIMER_FREQ) 
    
    plt.plot(distance_us)
    plt.title("SCH_LOOP period (time between succesive starts)") 
    plt.xlabel("Iteration number")
    plt.ylabel("Period (µs)")
    plt.show()
    # plt.savefig("sch_loop_period.png", dpi=150)

def led_error(profile_index, profile_time):
    functions_to_plot = [1,2]

    fig, axes = plt.subplots(2,1, figsize=(10,8))
    index = 0

    for i in functions_to_plot:
        samples = profile_index[i][0]
        start_times = profile_time[i][0][:samples] / (TIMER_FREQ * 1000.0)

        error = []
        intended_start = 0.0 if i == 1 else 5000.0 

        for exec in start_times:
            error.append(exec - intended_start)
            
            intended_start += 6000.0

        axes[index].plot(error, marker='o')
        axes[index].set_title(f"{FUNCTION_NAMES[i]} error (past intended start time)")
        axes[index].set_xlabel("Call number")
        axes[index].set_ylabel("Error (ms)")

        index += 1

    plt.tight_layout()
    plt.show()

    # plt.savefig("scheduler_accuracy.png", dpi=150)

def led_error_compare(profile_index_old, profile_time_old, profile_index_new, profile_time_new):
    functions_to_plot = [1,2]

    fig, axes = plt.subplots(2,1, figsize=(10,8))
    index = 0

    for i in functions_to_plot:
        samples_old = profile_index_old[i][0]
        samples_new = profile_index_new[i][0]

        start_times_old = profile_time_old[i][0][:samples_old] / (TIMER_FREQ * 1000.0)
        start_time_new = profile_time_new[i][0][:samples_new] / (TIMER_FREQ * 1000.0)

        error_old = []
        intended_start = 0.0 if i == 1 else 5000.0 

        for exec in start_times_old:
            error_old.append(exec - intended_start)
            
            intended_start += 6000.0

        error_new = []
        intended_start = 0.0 if i == 1 else 5000.0 

        for exec in start_time_new:
            error_new.append(exec - intended_start)
            
            intended_start += 6000.0

        axes[index].plot(error_old, marker='o', label="old")
        axes[index].plot(error_new, marker='o', label="new")
        axes[index].set_title(f"{FUNCTION_NAMES[i]} error (past intended start time)")
        axes[index].set_xlabel("Call number")
        axes[index].set_ylabel("Error (ms)")

        index += 1

    plt.tight_layout()
    plt.show()

    # plt.savefig("scheduler_comparison.png", dpi=150)

results = parse_file(sys.argv[1])
results2 = parse_file(sys.argv[2])

results["BUTTON"] = results2["BUTTON"]

functions_to_plot = ["UART", "ADC", "BUTTON"]
func_exec_time(results, functions_to_plot)