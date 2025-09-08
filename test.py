import numpy as np

def calculate_angles(A, B):
    norm_A = np.linalg.norm(A, axis=1)
    norm_B = np.linalg.norm(B, axis=1)
    indices = np.logical_and(norm_A > 0, norm_B > 0)
    cosines = np.sum(A * B, axis=1)[indices] / (norm_A[indices] * norm_B[indices])
    angles = np.arccos(np.clip(cosines, -1.0, 1.0))
    return {k: v for k, v in zip(np.where(indices)[0], angles)}

A = np.array([[1, 0, 0], [0, 0, 0], [1, 1, 1]])
B = np.array([[0, 1, 0], [0, 0, 0], [1, 0, 0]])

print(calculate_angles(B, A))
