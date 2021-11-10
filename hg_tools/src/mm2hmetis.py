import sys, re


if len(sys.argv) <= 1:
  print("Please pass the Matrix Market file as argument.");
  
else:
  file_name = re.split('[\. /]',sys.argv[1])[-2]
  print(file_name)
  output_file = file_name + ".hmetis"
  with open(sys.argv[1], 'r') as mm_file:
    line = mm_file.readline()
    while line[0] == '%':
      line = mm_file.readline()
    [num_hyperedges, num_vertices, num_lines] = map(int, line.split(' '))
    print(num_hyperedges, num_vertices)
    l = []
    for i in range(1, num_hyperedges+1):
      l.append([])

    for i in range(1, num_lines+1):
      line = mm_file.readline()
      [hyperedge, vertex] = map(int, line.split(' '))
      l[hyperedge-1].append(vertex)


    with open(output_file, 'w') as hmetis_file:
      for inner_list in l:
        if inner_list:
          for element in inner_list:
            hmetis_file.write(' ' + str(element))

        hmetis_file.write('\n')






