"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    temp_list = []
    new_list = []
    counter = 0
    for item in line:
        if item is not 0:
            temp_list.append(item)
    
    while counter < len(temp_list):
        if counter + 1 < len(temp_list):
            if temp_list[counter] == temp_list[counter+1]:
                new_list.append(temp_list[counter] * 2)
                counter += 2
            else:
                new_list.append(temp_list[counter])
                counter += 1
        else:
            new_list.append(temp_list[counter])
            counter += 1
    
    while len(new_list) < len(line):
        new_list.append(0)
        
    return new_list
