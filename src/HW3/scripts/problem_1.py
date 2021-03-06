import numpy as np
import sympy

def get_T_symbolic():
    s1,s2,s3,s4,s5,s6,s7 = sympy.symbols('s1 s2 s3 s4 s5 s6 s7')
    c1,c2,c3,c4,c5,c6,c7 = sympy.symbols('c1 c2 c3 c4 c5 c6 c7')

    d1,d3,d5,d7 = sympy.symbols('d1 d3 d5 d7')

    T1 = np.array([[c1,0,-s1,0],
                   [s1,0,c1,0],
                   [0,-1,0,d1],
                   [0,0,0,1]])
    T2 = np.array([[c2,0,s2,0],
                   [s2,0,-c2,0],
                   [0,1,0,0],
                   [0,0,0,1]])
    T3 = np.array([[c3,0,s3,0],
                   [s3,0,-c3,0],
                   [0,1,0,d3],
                   [0,0,0,1]])
    T4 = np.array([[c4,0,-s4,0],
                   [s4,0,c4,0],
                   [0,-1,0,0],
                   [0,0,0,1]])
    T5 = np.array([[c5,0,-s5,0],
                   [s5,0,c5,0],
                   [0,-1,0,d5],
                   [0,0,0,1]])
    T6 = np.array([[c6,0,s6,0],
                   [s6,0,-c6,0],
                   [0,1,0,0],
                   [0,0,0,1]])
    T7 = np.array([[c7,-s7,0,0],
                   [s7,c7,0,0],
                   [0,0,1,d7],
                   [0,0,0,1]])
    T = T1 @ T2 @ T3 @ T4 @ T5 @ T6 @ T7
    T = sympy.Matrix(T.tolist())
    T = sympy.nsimplify(T,tolerance=1e-10,rational=True)
    T = np.array(T.tolist())
    print("\nThe final Transformation matrix :\n")
    print(T)
    print("-----------------------------------")

def get_T(q):
    s1,s2,s3,s4,s5,s6,s7 = np.sin(q).tolist()
    c1,c2,c3,c4,c5,c6,c7 = np.cos(q).tolist()    

    d1,d3,d5,d7 = sympy.symbols('d1 d3 d5 d7')

    T1 = np.array([[c1,0,-s1,0],
                   [s1,0,c1,0],
                   [0,-1,0,d1],
                   [0,0,0,1]])
    T2 = np.array([[c2,0,s2,0],
                   [s2,0,-c2,0],
                   [0,1,0,0],
                   [0,0,0,1]])
    T3 = np.array([[c3,0,s3,0],
                   [s3,0,-c3,0],
                   [0,1,0,d3],
                   [0,0,0,1]])
    T4 = np.array([[c4,0,-s4,0],
                   [s4,0,c4,0],
                   [0,-1,0,0],
                   [0,0,0,1]])
    T5 = np.array([[c5,0,-s5,0],
                   [s5,0,c5,0],
                   [0,-1,0,d5],
                   [0,0,0,1]])
    T6 = np.array([[c6,0,s6,0],
                   [s6,0,-c6,0],
                   [0,1,0,0],
                   [0,0,0,1]])
    T7 = np.array([[c7,-s7,0,0],
                   [s7,c7,0,0],
                   [0,0,1,d7],
                   [0,0,0,1]])
    T = T1 @ T2 @ T3 @ T4 @ T5 @ T6 @ T7
    T = sympy.Matrix(T.tolist())
    T = sympy.nsimplify(T,tolerance=1e-10,rational=True)
    T = np.array(T.tolist())
    return T

def main():
    get_T_symbolic()
    q = np.array([90,0,0,0,0,0,0])
    q = (np.pi/180)*q
    T = get_T(q)
    print("\nFor Joint 1 with 90 degrees :")
    print("-------------------------------")
    print(T)
    q = np.array([0,90,0,0,0,0,0])
    q = (np.pi/180)*q
    T = get_T(q)
    print("\nFor Joint 2 with 90 degrees :")
    print(T)
    print("-------------------------------")
    q = np.array([0,0,90,0,0,0,0])
    q = (np.pi/180)*q
    T = get_T(q)
    print("\nFor Joint 3 with 90 degrees :")
    print(T)
    print("-------------------------------")
    q = np.array([0,0,0,90,0,0,0])
    q = (np.pi/180)*q
    T = get_T(q)
    print("\nFor Joint 4 with 90 degrees :")
    print(T)
    print("-------------------------------")
    q = np.array([0,0,0,0,90,0,0])
    q = (np.pi/180)*q
    T = get_T(q)
    print("\nFor Joint 5 with 90 degrees :")
    print(T)
    print("-------------------------------")

if __name__ == '__main__':
    main()