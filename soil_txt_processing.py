import os
import glob

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
        return section, non_numeric_rows, []  

    mean_first_three = [round(sum(values) / 3, 3) for values in zip(*all_values[:3])]
    fourth_list = [round(value, 3) for value in all_values[3]]
    mean_last_two = [round(sum(values) / 2, 3) for values in zip(*all_values[-2:])]

    final_output = [mean_first_three, fourth_list, mean_last_two]

    return section, non_numeric_rows, final_output

def process_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file_path in glob.glob(os.path.join(input_dir, '*.SOL')):
        with open(file_path, 'r') as file:
            content = file.read()
        print(f"Processing file: {os.path.basename(file_path)}")

        sections = content.split('*')

        output_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_path, 'w') as outfile:
            for section in sections:
                if 'SLB' in section.strip():
                    processed_section, non_numeric_rows, final_output = process_data_point_section(section)
                    outfile.write('\n' + '*' + section.split('\n', 1)[0] + '\n')  
                    for row in non_numeric_rows:
                        outfile.write(row + '\n') 
                    for row in final_output:
                        formatted_row = '     F A    ' + ' '.join([f"{value:.1f}" if value == -99 else f"{value:.3f}" for value in row])
                        outfile.write(formatted_row + '\n')
                else:
                    outfile.write('*' + section if section else '')

input_dir = 'C:/pythia/Simulation_Data/eGHR'
output_dir = 'C:/pythia/Simulation_Data_India/eGHR'
process_files(input_dir, output_dir)
