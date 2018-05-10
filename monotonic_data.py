import random


mono_data = []
number_data_points = 10
max_number = 
while len(mono_data) < number_data_points:
    if not mono_data:
        random_number = random.randint(0,1)
        mono_data.append(random_number)
    else:
        random_number = random.randint(0,2*mono_data[-1]+1)
        if random_number >mono_data[-1]:
            mono_data.append(random_number)
    
print(mono_data)