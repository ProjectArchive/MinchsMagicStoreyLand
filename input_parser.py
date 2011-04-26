def input_parser():
    
    # initialize a bunch of storage arrays
    time = []
    v1 = []
    v2 = []
    v3 = []
    v24 = []
    v5 = []
    v37 = []
    i_long = []
    i_v3 = []
    i_v2 = []
    i_v1 = []

    # initialize the final integer storage arrays
    time_int = []
    v1_int = []
    v2_int = []
    v3_int = []
    v24_int = []
    v5_int = []
    v37_int = []
    i_long_int = []
    i_v3_int = []
    i_v2_int = []
    i_v1_int = []

    # our reference list of lists for sorting the "other data"
    other_data_order = [v1, v2, v3, v24, v5, v37, i_long, i_v3, i_v2, i_v1]

    # full list of all the lists we're outputting
    output_list = [time, v1, v2, v3, v24, v5, v37, i_long, i_v3, i_v2, i_v1]

    # full FINAL list of all the lists (with integers, not strings)
    output_list_int = [time_int, v1_int, v2_int, v3_int, v24_int, v5_int, v37_int, i_long_int, i_v3_int, i_v2_int, i_v1_int]

    # helper array initialization
    other_data = []

    # open the file
    fout = open('sampleCircuitData.txt')
    content_string = ""
    for line in fout:
        content_string += line

    # tokenize
    content_string = content_string.splitlines()

    # populate the time array
    for entry in content_string:
        if not(entry[0:1] == '\t'):
            entry = entry.splitlines()
            entry_string = entry[0]
            indx = entry_string.find('\t\t')
            parsed_time = entry_string[indx + 2: len(entry_string)]
            time.append(parsed_time)
        else:
            # populate all of the other data by iterating through the entire array
            entry = entry.splitlines()
            entry_string = entry[0]
            indx = entry_string.find('\t')
            parsed_data = entry_string[indx + 1: len(entry_string)]
            other_data.append(parsed_data)

    # put things into the right array
    counter = 0
    for entry in other_data:
        counter_mod = counter%10
        list_to_append = other_data_order[counter_mod -1]
        list_to_append.append(entry)
        counter += 1

    # get rid of the junk in the beginning
    for entry in output_list:
        for sub_entry in entry:
            for i in range(5):
                entry.pop(i)
    
    for j in range(len(output_list)):
        entry = output_list[j]
        for i in range(len(entry)):
            output_list[j][i] = float(entry[i])
            
            
    print output_list[0]

        
        
        
            
    
input_parser()
