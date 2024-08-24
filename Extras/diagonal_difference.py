def diagonal_difference(matrix):
    n = len(matrix)
    
    diagonal1 = sum(
        matrix[i][i] 
        for i in range(n)
    )

    diagonal2 = sum(
        matrix[i][n-i-1] 
        for i in range(n)
    )
    
    return diagonal1 - diagonal2

Matrix = [
    [1, 2, 0], 
    [4, 5, 6], 
    [7, 8, 9]
]

print(diagonal_difference(Matrix))
