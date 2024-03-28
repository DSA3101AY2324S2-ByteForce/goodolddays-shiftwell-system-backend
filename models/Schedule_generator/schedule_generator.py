from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
def schedule_employees(file_path):
    ##### input Data ------------------------------------####
    df = pd.read_csv(file_path)
    hourly_demand = df['num_customers'] / 100

    ##### variables ------------------------------------####
    total_num_staff = 10
    num_parttimers = 5
    num_fulltimers = 5
    num_shifts = 6
    num_days = 7
    all_employee = range(total_num_staff)
    all_shifts = range(num_shifts)
    all_days = range(num_days)

    fulltimers = [0,1,2,3,4] ## ids of full-time employees
    parttimers = [5,6,7,8,9] ## ids of part-time employees
    chef = [0,1] ## ids of chefs
    other = [2,3,4,5,6,7,8,9] ## ids of other staff

    cost_chef = 15
    cost_chef_weekend = 16
    cost_chef_ph = 17

    cost_fulltimer = 13
    cost_fulltimer_weekend = 14
    cost_fulltimer_ph = 15 

    cost_parttimer = 11
    cost_parttimer_weekend = 12
    cost_parttimer_ph = 13
    ##### initialize model------------------------------------####
    model = cp_model.CpModel()

    shifts = {}
    for e in all_employee:
        for d in all_days:
            for s in all_shifts:
                shifts[(e, d, s)] = model.new_bool_var(f"shift_n{e}_d{d}_s{s}")

    ####------------------------------------####
    ##### Constraints           
    ## contraint: minimum 44 hrs (22 shifts) per week for full-timers
    for x in fulltimers:
        model.add(model.sum([shifts[x][d][s] for d in range(num_days) for s in range(num_shifts)]) >= 22)
            
    ## constraint: maximum 48 hrs (24 shifts) per week for full-timers
    for x in fulltimers:
        model.add(model.sum([shifts[x][d][s] for d in range(num_days) for s in range(num_shifts)]) <= 24)
        
    ## constraint: minimum 33 hrs (16 shifts) per week for part-timers
    for x in parttimers:
        model.add(model.sum([shifts[x][d][s] for d in range(num_days) for s in range(num_shifts)]) >= 16)
        
    ## constraint: maximum 36 hrs (18 shifts) per week for part-timers
    for x in parttimers:
        model.add(model.sum([shifts[x][d][s] for d in range(num_days) for s in range(num_shifts)]) <= 18)

    ## constraint: each shift has exactly 1 chef
    for d in all_days:
        for s in all_shifts:
            model.add(model.sum([shifts[c][d][s] for c in chef]) == 1)

    ## constraint: each shift has exactly x staff based on the demand
    for d in all_days:
        for s in all_shifts:
            model.add(model.sum([shifts[x][d][s] for x in all_employee]) == hourly_demand[d][s])
            
    ## constraint: each staff can only work no more than 4 shifts per day
    for x in all_employee:
        for d in all_days:
            model.add(model.sum([shifts[x][d][s] for s in all_shifts]) <= 4)
            
    ## constraint: each staff can only work 1 shift at a time
    for x in all_employee:
        for d in all_days:
            model.add(model.sum([shifts[x][d][s] for s in all_shifts]) <= 1)

    ## constraint: each staff can only work 1 shift at a time
    for x in all_employee:
        for s in all_shifts:
            model.add(model.sum([shifts[x][d][s] for d in all_days]) <= 1)
            
    ##### Objective Function ----------------------------------#######
    cost = 0
    for x in chef:
        for d in all_days:
            is_ph = df[d][is_ph]
            for s in all_shifts:
                if d < 5:
                    if is_ph:
                        cost += shifts[x][d][s] * cost_chef_ph
                    else:
                        cost += shifts[x][d][s] * cost_chef
                elif d >= 5:
                    if is_ph:
                        cost += shifts[x][d][s] * cost_chef_ph
                    else:
                        cost += shifts[x][d][s] * cost_chef_weekend
                
    for x in fulltimers:
        for d in all_days:
            is_ph = df[d][is_ph]
            for s in all_shifts:
                if d < 5:
                    if is_ph:
                        cost += shifts[x][d][s] * cost_fulltimer_ph
                    else:
                        cost += shifts[x][d][s] * cost_fulltimer
                elif d >= 5:
                    if is_ph:
                        cost += shifts[x][d][s] * cost_fulltimer_ph
                    else:
                        cost += shifts[x][d][s] * cost_fulltimer_weekend
                
    for x in parttimers:
        for d in all_days:
            is_ph = df[d][is_ph]
            for s in all_shifts:
                if d < 5:
                    if is_ph:
                        cost += shifts[x][d][s] * cost_parttimer_ph
                    else:
                        cost += shifts[x][d][s] * cost_parttimer
                elif d >= 5:
                    if is_ph:
                        cost += shifts[x][d][s] * cost_parttimer_ph
                    else:
                        cost += shifts[x][d][s] * cost_parttimer_weekend

    ###------------------------------------####

    model.minimize(cost)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(f"Total cost: {solver.ObjectiveValue()}")
        
        # Create a list to hold the data
        schedule_data = []
        
        for d in all_days:
            for s in all_shifts:
                for x in all_employee:
                    if solver.Value(shifts[(x, d, s)]) == 1:
                        # Append a dictionary for each assigned shift
                        schedule_data.append({
                            'Day': d,
                            'Shift': s,
                            'Employee': x
                        })
        
        # Convert the list of dictionaries to a pandas DataFrame
        schedule_df = pd.DataFrame(schedule_data)
        
        # Save the DataFrame to a CSV file
        schedule_df.to_csv('schedule.csv', index=False)
        print("Schedule saved to schedule.csv")
    else:
        print("No solution found.")
        schedule_df = pd.DataFrame()  # Empty DataFrame if no solution

    return schedule_df
    


