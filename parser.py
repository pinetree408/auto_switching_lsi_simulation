import csv
from random import shuffle

def get_searched_list(input_string, target_list):
    searched_list = []
    for target in target_list:
        if target.startswith(input_string):
            searched_list.append(target)
    return sorted(searched_list, reverse=True)

def key_input_model(input_length):
    return 1.019 * input_length - 0.095

def list_navigation_model(target_index):
    return 0.257 * target_index + 0.546

with open('simul_result_la.csv', 'w') as csvfile, open('name.txt', 'r') as f_r:
    result_writer = csv.writer(csvfile, delimiter=' ')
    result_writer.writerow([
        'poolSize',
        '3-completion',
        '3-keyInput',
        '3-listNavigation',
        '3-suggestionRatio',
        '6-completion',
        '6-keyInput',
        '6-listNavigation',
        '6-suggestionRatio',
        '12-completion',
        '12-keyInput',
        '12-listNavigation',
        '12-suggestionRatio',
        '24-completion',
        '24-keyInput',
        '24-listNavigation',
        '24-suggestionRatio',
    ])
    lines = f_r.read().splitlines()
    name_list = []
    for line in lines:
        items = line.split('\t')
        name = items[1].strip().lower()
        if not name in name_list:
            name_list.append(name)
    for target_size in range(60, 1901):
        shuffle(name_list)
        target_list = name_list[:target_size]
        result_list = [target_size]
        for limit in [3, 6, 12, 24]:
            avr_completion_time = 0
            avr_key_input_time = 0
            avr_list_navigation_time = 0
            auto_switch_count = 0
            select_suggestion_count = 0
            for target in target_list:
                key_input_time = 0
                list_navigation_time = 0
                for index in range(len(target)):
                    input_length = index + 1
                    input_string = target[:input_length]
                    searched_list = get_searched_list(input_string, target_list)
                    if len(searched_list) <= limit:
                        key_input_time = key_input_model(input_length)
                        list_navigation_time = list_navigation_model(searched_list.index(target))
                        avr_key_input_time = avr_key_input_time + key_input_time
                        avr_list_navigation_time = avr_list_navigation_time + list_navigation_time
                        auto_switch_count = auto_switch_count + 1
                        break
                    else:
                        if target == searched_list[0]:
                            key_input_time = key_input_model(input_length + 1)
                            list_navigation_time = 0
                            select_suggestion_count = select_suggestion_count + 1
                            break
                completion_time = key_input_time + list_navigation_time
                avr_completion_time = avr_completion_time + completion_time
            avr_completion_time = avr_completion_time / len(target_list)
            avr_key_input_time = avr_key_input_time / auto_switch_count
            avr_list_navigation_time = avr_list_navigation_time / auto_switch_count
            select_suggestion_ratio = select_suggestion_count * 1.0 / len(target_list)
            result_list.append(round(avr_completion_time, 3))
            result_list.append(round(avr_key_input_time, 3))
            result_list.append(round(avr_list_navigation_time, 3))
            result_list.append(round(select_suggestion_ratio, 3))
        result_writer.writerow(result_list)
        print target_size, " done"
