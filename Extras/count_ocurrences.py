def count_occurrences(input_list, query_list):
    return [
        input_list.count(query) 
        for query in query_list
    ]

INPUT = ['xc', 'dz', 'bbb', 'dz']
QUERY = ['bbb', 'ac', 'dz']

print(count_occurrences(INPUT, QUERY))
