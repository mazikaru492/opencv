import numpy as np
def main():
    a = np.array([[1,2,3,4,5,],
                  [6,7,8,9,10],
                  [11,12,13,14,15]])

    b = np.where(a < 8, a, 255)
    c = np.where(a > 8, a,0)
    print(b)
    print(c)

if __name__ == "__main__":
    main()