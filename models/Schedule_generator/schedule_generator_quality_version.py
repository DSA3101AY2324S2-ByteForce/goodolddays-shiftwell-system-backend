from ortools.sat.python import cp_model
import numpy as np
import pandas as pd
def schedule_employees(file_path):
    
    print("Scheduling employees start")
    
    ##### input Data ------------------------------------####
    df = pd.read_csv(file_path)

    ##### variables ------------------------------------####
    total_num_staff = 10
    num_parttimers = 5
    num_fulltimers = 5
    num_shifts = 6
    num_days = 7
    all_employee = [1,2,3,4,5,6,7,8,9,10]
    all_shifts = [1, 2, 3, 4, 5, 6]
    all_days = df['day_of_week'].unique()
    #increment demand by 1 for each shift
    df['demand'] = df['demand']

    fulltimers = [1,2,3,4,5] ## ids of full-time employees
    parttimers = [6,7,8,9,10] ## ids of part-time employees
    chef = [1,2] ## ids of chefs; assume chefs are all full timer
    other_fulltimers = [2,3,4] ## ids of other full-timers

    cost_chef = 15 * 2
    cost_chef_weekend = 16 * 2
    cost_chef_ph = 17 * 2

    cost_fulltimer = 13 *2 
    cost_fulltimer_weekend = 14 *2
    cost_fulltimer_ph = 15 * 2

    cost_parttimer = 11 * 2
    cost_parttimer_weekend = 12 * 2
    cost_parttimer_ph = 13 * 2
    ##### initialize model------------------------------------####
    model = cp_model.CpModel()

    shifts = {}
    for x in all_employee:
        for d in all_days:
            for s in all_shifts:
                shifts[(x, d, s)] = model.NewBoolVar(f'shift_{x}_{d}_{s}')
                
    print("Variables and model initialized")
    
    ##### constraints ----------------------------------#######+
        
    ## constraint: maximum 48 hrs (24 shifts) per week for full-timers
    for x in fulltimers:
        model.add(sum([shifts[(x, d, s)] for d in all_days for s in all_shifts]) <= 24)
        
    
    ## constraint: each shift has at leats 1 chef
    for d in all_days:
        for s in all_shifts:
            model.add(sum([shifts[(c,d,s)] for c in chef]) >= 1)
        
     ## constraint: each shift has exactly x staff based on the demand
    for d in all_days:
        for s in all_shifts:
            demand = df[(df['day_of_week'] == d) & (df['shift'] == s)]['demand'].iloc[0]
            model.add(sum([shifts[(x, d, s)] for x in all_employee]) == (demand + 1))

   ## constraint at least 2 full-timers per shift
    for d in all_days:
        for s in all_shifts:
            model.add(sum([shifts[(x, d, s)] for x in fulltimers]) >= 2)
            
    ## constraint: each staff can only work no more than 4 shifts per day
    for x in all_employee:
        for d in all_days:
            model.add(sum([shifts[(x, d, s)] for s in all_shifts]) <= 4)
        
    ## constraint: minimum 44 hrs (22 shifts) per week for full-timers
    for x in fulltimers:
        model.add(sum([shifts[(x, d, s)] for d in all_days for s in all_shifts]) >= 22)
    
            
    


###------------------------------------####



    cost = 0
    for x in chef:
        for d in all_days:
            flg_is_ph = df.loc[(df['day_of_week'] == d) & (df['shift'] == s), 'flg_is_ph'].iloc[0]
            for s in all_shifts:
                if d < 5:
                    if flg_is_ph == 1:
                        cost += shifts[(x, d, s)] * cost_chef_ph
                    else:
                        cost += shifts[(x, d, s)] * cost_chef
                elif d >= 5:
                    if flg_is_ph:
                        cost += shifts[(x, d, s)] * cost_chef_ph
                    else:
                        cost += shifts[(x, d, s)] * cost_chef_weekend
                
    for x in other_fulltimers:
        for d in all_days:
            flg_is_ph = df.loc[(df['day_of_week'] == d) & (df['shift'] == s), 'flg_is_ph'].iloc[0]
            for s in all_shifts:
                if d < 5:
                    if flg_is_ph == 1:
                        cost += shifts[(x, d, s)] * cost_fulltimer_ph
                    else:
                        cost += shifts[(x, d, s)] * cost_fulltimer
                elif d >= 5:
                    if flg_is_ph:
                        cost += shifts[(x, d, s)] * cost_fulltimer_ph
                    else:
                        cost += shifts[(x, d, s)] * cost_fulltimer_weekend
                
    for x in parttimers:
        for d in all_days:
            flg_is_ph = df.loc[(df['day_of_week'] == d) & (df['shift'] == s), 'flg_is_ph'].iloc[0]
            for s in all_shifts:
                if d < 5:
                    if flg_is_ph==1:
                        cost += shifts[(x, d, s)] * cost_parttimer_ph
                    else:
                        cost += shifts[(x, d, s)] * cost_parttimer
                elif d >= 5:
                    if flg_is_ph:
                        cost += shifts[(x, d, s)] * cost_parttimer_ph
                    else:
                        cost += shifts[(x, d, s)] * cost_parttimer_weekend
    model.minimize(cost)
    print("Objective function added")
        
    print("Model solving...")
        

    solver = cp_model.CpSolver()
    solver.parameters.linearization_level = 0
    status = solver.solve(model)
    
    
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



if __name__ == "__main__":
    file_path = 'test2.csv'  # Update this path
    schedule_employees(file_path)

    
    
   