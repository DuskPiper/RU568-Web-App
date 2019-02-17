import numpy as np
import load_data
import math

def baysian_regression_predict(time, price, test_val):
    M = 4
    beta = 12
    alpha = 0.1
    # Now Calc 𝜑T(x)
    a = [[math.pow(test_val, i) for i in range(M + 1)]]
    matrix_a = np.matrix(a)
    # Now Calc alpha * I
    I = [[0 for _ in range(M + 1)] for _ in range(M + 1)]
    for i in range(M + 1):
        I[i][i] = alpha
    matrix_I = np.matrix(I)
    # Now Calc sum-𝜑(xn)
    b = [[0] for _ in range(M + 1)]
    for j in range(len(time) - 1):
        for i in range(M + 1):
            b[i][0] += math.pow(time[j], i)
    matrix_b = np.matrix(b)
    # Now Calc Matrix S
    matrix_S_ = matrix_b * matrix_a * beta + matrix_I
    matrix_S = np.linalg.inv(matrix_S_)
    # Now Calc sum-[𝜑(xn)*tn]
    c = [[0] for _ in range(M + 1)]
    for i in range(len(time) - 1):
        for j in range(M + 1):
            c[j][0] += (math.pow(time[i], j) * price[i])
    matrix_c = np.matrix(c)
    # Now Calc mean
    mean_matrix = matrix_a * matrix_S * matrix_c * beta
    mean = mean_matrix.item(0)
    # Now Calc 𝜑(x)
    d = [[0] for _ in range(M + 1)]
    for i in range(M + 1):
        d[i][0] = math.pow(test_val, i)
    matrix_d = np.matrix(d)
    # Now Calc variance
    variance = math.sqrt((matrix_a * matrix_S * matrix_d)[0][0] + (1 / beta))
    # Now show results
    print("Predicted Val   : {:.4f}".format(mean))
    print("Actual Val      : {:.4f}".format(price[-1]))
    print("Range Predction : [{:.4f}, {:.4f}]".format(mean - 3 * variance, mean + 3 * variance))
    print("Absolute Error  : {:.4f}".format(abs(price[-1] - mean)))
    print("Relative Error  : {:.4f}%".format(abs(price[-1] - mean) / price[-1] * 100))


if __name__ == "__main__":
    csv_path = "./data/"
    files = load_data.find_csv(csv_path)
    for f in files:
        print(("-" * 5 + f.split(".")[0] + " Summary" + "-" * 20)[:40])
        time, price = load_data.read_csv(csv_path, f)
        baysian_regression_predict(time, price, time[-1])
        print("-" * 40, end = "\n\n\n")
