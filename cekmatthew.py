

#0 kalo ada di posisi awal, 1 kalo ada di posisi tujuan
#kambing, serigala, sayur, petani
aturan1 = [0,0,0,0] #semua di awal
aturan2 = [1,0,0,1] #kambing go atau ditinggal sendiri atau sayur back
aturan3 = [0,0,1,0] #sayur go atau ditinggal sendiri
aturan4 = [0,1,0,0] #serigala go atau ditinggal sendiri
aturan5 = [0,1,1,0] #kambing back
aturan6 = [1,0,0,1] #serigala back
aturan7 = [1,1,1,1] #semua di seberang

rules = [aturan1,aturan2, aturan3, aturan4, aturan5, aturan6, aturan7]
print("List Aturan: ")
print(rules)


node = {1: aturan1,
        2: aturan2,
        3: aturan3,
        4: aturan4,
        5: aturan5,
        6: aturan6,
        7: aturan7}

relasi = {1: [2,3,4],
          2: [1,5,6],
          3:[1,4,5],
          4:[1,3,6],
          5: [2,3,4],
          6: [2,4,5],
          7: [1,2,3,4,5,6]}


user_input = input("Input: ")
user_output = input("Output: ")

start = [user_input ]
end = [user_output]

#ukuran matrix sama dengan banyak rule

matrix = []
for i in range(len(node)):
  row = [0]*len(node)
  matrix.append(row)

#setiap rules di node yg terhubung bernilai 1
for i, connected_rules in relasi.items():
  for j in connected_rules:
    matrix [i-1][j-1] = matrix [j-1][i-1] = 1
    
for i in range(len(node)):
    for j in range(len(node)):
        print(matrix[i][j], end=' ')
    print()

#DFS
def dfs(node, visited, relasi, end):
    visited.append(node)
    print(node+1, end=' ')
    if node+1 == end:
        return True
    for i in relasi[node+1]:
        if i-1 not in visited:
            if dfs(i-1, visited, relasi, end):
                return True
    return False

visited = []
start_node = int(user_input)
end_node = int(user_output)
dfs(start_node-1, visited, relasi, end_node)
