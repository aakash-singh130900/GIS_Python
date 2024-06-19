def input_file():
    with open('C:/pythia/Simulation_Data/eGHR/AU.SOL', 'r') as file:
        content = file.read()
    print("File read successfully")

    sections = content.split('*')
    print(f"Number of sections: {len(sections)}")

    with open('C:/pythia/Simulation_Data/eGHR/Processed_AU.SOL', 'w') as outfile:
        for section in sections:
            if 'SLB' in section.strip():
                processed_section, non_numeric_rows, final_output = process_data_point_section(section)
                outfile.write('\n' + '*' + section.split('\n', 1)[0] + '\n')  # Write section identifier
                for row in non_numeric_rows:
                    outfile.write(row + '\n')  # Write non-numeric rows
                for row in final_output:
                    formatted_row = '     F A    ' + ' '.join([f"{value:.1f}" if value == -99 else f"{value:.3f}" for value in row])
                    outfile.write(formatted_row + '\n')
            else:
                outfile.write(section.split('\n', 1)[0] + '\n')  # Write unprocessed sections as is

def process_data_point_section(section):
    lines = section.strip().split('\n')[1:]
    all_values = []
    non_numeric_rows = []

    for row in lines:
        try:
            numeric_values = [float(value) for value in row.split()[2:]]
            all_values.append(numeric_values)
        except ValueError:
            non_numeric_rows.append(row)

    if len(all_values) < 5:
        return section, non_numeric_rows, []  # Return original section and non-numeric rows if not enough data

    mean_first_three = [round(sum(values) / 3, 3) for values in zip(*all_values[:3])]
    fourth_list = [round(value, 3) for value in all_values[3]]
    mean_last_two = [round(sum(values) / 2, 3) for values in zip(*all_values[-2:])]

    final_output = [mean_first_three, fourth_list, mean_last_two]

    return section, non_numeric_rows, final_output

input_file()