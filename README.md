# IOE574_TermProject_SnowPlow
IOE574_TermProject_SnowPlow

# Report link:
https://docs.google.com/document/d/1SGIqCPkZYdZ7TkQLKl9wCcb04u9XeCXol07NJOc08gw/edit?usp=sharing

# Example usage
num_plows = 3
start_nodes = [133, 420, 221]  # Example start nodes
plow_speed = 15  # 30 operating, half considering 

plow_results = run_snowplow_simulation(num_plows, start_nodes, plow_speed, M, 720)

# Node id for potential start point of plowing
Hospitals:
University Hospital: 69, 285, 67, 62, 153
VA Hospital: 8, 9, 272

Schools:
UMich Central Campus: 310
UMich North Campus 281 
Community High: 14, 288, 123, 186
Pioneer High: 381, 95, 352, 141
Huron High: 35, 131

# Number of households who go to the grocery store on a given day:
26820 total households
The average household goes to the grocery 1.6 times per week
Total number of households that go to the grocery every day: 6130

# Cases, every case has N replications
Case 1: No Snow
Case 2: 4-inch Snow, No Plow
Case 3: 4-inch Snow, 1 Plow start from Center of Downtown
Case 4: 4-inch Snow, 2 Plows start from Center of Downtown
Case 5: 4-inch Snow, 2 Plows starting from UMich Northcampus and Poineer High

# Changes need to the simulation model
Run less number of reps - Major 
Add uncertainty aruond plow speed - Kate
Add 0 plow situation - Graham and Kate
Add uncertinaty around travel speed - Riley
Add a time for each intersection (use difference mean time for with or without snow and a small variation) - Riley
Add travel time from house to nearest local node (stright distance, 10mph with reduction factor) - Chris
    -Changing this slightly to be a random triangular distribution with mean 3 and limits 1 and 7 and multiplying it by 2 to reflect the way there and the way back
    -Trying to reflect the randomness of the road layout and how living close to a main road doesn't necessarily mean it's fast to get there (e.g. I live <100ft from a main road but it takes ~5 min for me to drive to the main road from my house)

# Report
Outline
https://docs.google.com/document/d/1SGIqCPkZYdZ7TkQLKl9wCcb04u9XeCXol07NJOc08gw/edit
Report https://docs.google.com/document/d/12sxgXbl0XrnprUHyvgI_8ti5Fjwy0BlCFtqMYyOVJHk/edit#heading=h.c81j1v3jh51x
Project requirements 
https://umich.instructure.com/courses/625120/pages/term-project

# New Excutable Files
The 5 central cases are run with the following comment under current directory
Python3 Run_Simulation_Central_Cases.py version_name number_reps