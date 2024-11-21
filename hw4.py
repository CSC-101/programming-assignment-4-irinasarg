#Task 1
import sys


def open_data():
    data = []
    try:
        with open('percent_field.ops', 'r') as file:
            lines = file.readlines()

        headers = []
        for char in lines[0]:
            if char == ',':
                headers.append(' ')
            else:
                headers.append(char)
        headers = ''.join(headers).replace(' ', '').replace('\n', '').split(',')

        for line in lines[1:]:
            county = {}
            field_name = ''
            data_collector = ''
            i = 0
            in_quotes = False

            while i < len(line):
                char = line[i]

                if char == ',' and not in_quotes:
                    county[field_name] = data_collector
                    field_name = headers[len(county) - 1]
                    data_collector = ''
                elif char == '\n' and not in_quotes:
                    county[field_name] = data_collector
                    break
                elif char == '"' and data_collector == '':
                    in_quotes = not in_quotes
                else:
                    data_collector += char

                i += 1

            data.append(county)

        return data
    except FileNotFoundError:
        print("Error: File 'county_demographics.txt' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
def display_data(data):
    print(f"{len(data)} records loaded")
    for county in data:
        print(f"{county['County']}, {county['State']}")
        print(f"    Population: {county['Population']}")
        print(f"    Education")
        print(f"        >= High School: {county['Education High School or Higher']}%")
        print(f"        >= Bachelor's: {county['Education Bachelor\'s Degree or Higher']}%")
        print(f"    Ethnicity Percentages")
        print(f"        White: {county['Ethnicity White']}%")
        print(f"        Black: {county['Ethnicity Black']}%")
        print(f"        Asian: {county['Ethnicity Asian']}%")
        print(f"        Other: {county['Ethnicity Other']}%")
        print(f"    Income")
        print(f"        Median Household: {county['Income Median Household']}")
        print(f"        Per Capita: {county['Income Per Capita']}")
        print(f"        Below Poverty Level: {county['Income Persons Below Poverty Level']}%")

def filter_state(data, state):
    filtered = [county for county in data if county['State'] == state]
    print(f"Filter: state == {state} ({len(filtered)} entries)")
    return filtered

def filter_gt(data, field, value):
    filtered = [county for county in data if float(county[field]) > value]
    print(f"Filter: {field} gt {value} ({len(filtered)} entries)")
    return filtered

def filter_lt(data, field, value):
    filtered = [county for county in data if float(county[field]) < value]
    print(f"Filter: {field} lt {value} ({len(filtered)} entries)")
    return filtered


def population_total(data):
    total_population = sum(int(county['Population']) for county in data)
    print(f"2014 population: {total_population}")

def population_field(data, field):
    total_population = sum(float(county[field]) / 100 * int(county['Population']) for county in data)
    print(f"2014 {field} population: {total_population}")

def percent_field(data, field):
    total_population = sum(int(county['Population']) for county in data)
    sub_population = sum(float(county[field]) / 100 * int(county['Population']) for county in data)
    percentage = (sub_population / total_population) * 100
    print(f"2014 {field} percentage: {percentage}")


def process_operations(operations_file, data):
    try:
        with open(operations_file, 'r') as file:
            operations = file.readlines()
    except FileNotFoundError:
        print(f"Error: Operations file '{operations_file}' not found.")
        sys.exit(1)

    filtered_data = data
    for line_num, line in enumerate(operations, 1):
        line = line.rstrip()
        if len(line) == 0:
            continue

        colon_index = line.find(":")
        if colon_index == -1:
            print(f"Error: Malformed line {line_num}: {line}")
            continue

        operation = line[:colon_index]
        remaining = line[colon_index + 1:]

        try:
            if operation == "display":
                display_data(filtered_data)
            elif operation == "filter-state":
                state = remaining
                filtered_data = filter_state(filtered_data, state)
            elif operation == "filter-gt":
                field_value = remaining
                field, value_str = field_value.split(":")
                value = float(value_str)
                filtered_data = filter_gt(filtered_data, field, value)
            elif operation == "filter-lt":
                field_value = remaining
                field, value_str = field_value.split(":")
                value = float(value_str)
                filtered_data = filter_lt(filtered_data, field, value)
            elif operation == "population-total":
                population_total(filtered_data)
            elif operation == "population":
                field = remaining
                population_field(filtered_data, field)
            elif operation == "percent":
                field = remaining
                percent_field(filtered_data, field)
            else:
                print(f"Error: Unknown operation '{operation}' on line {line_num}")
        except ValueError:
            print(f"Error: Malformed data on line {line_num}. Skipping line.")


if __name__ == "__main__":
    data = open_data()

    if len(sys.argv) != 2:
        print("Error: Please provide the operations file.")
        sys.exit(1)

    operations_file = sys.argv[1]

    process_operations(operations_file, data)


