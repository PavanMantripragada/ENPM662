import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

#d1,d3,d5,d7 = sp.symbols('d1 d3 d5 d7')

d1,d3,d5,d7 = 360.0,420.0,399.5,205.5

class Kuka:
    def __init__(self,q):
        self.q = q.reshape(7,1)*(np.pi/180)
        self.d = np.array([d1,0,d3,0,d5,0,d7])
        self.alpha = np.array([-90,90,90,-90,-90,90,0])*(np.pi/180)
        self.a = np.zeros(7)

    def get_joints(self):
        return self.q

    def set_joints(self,q):
        self.q = q.reshape(7,1)
    
    def A(self,i):
        a = self.a
        alpha = self.alpha
        d = self.d
        q = self.q.reshape(7,)
        A = np.array([[np.cos(q[i]), -np.sin(q[i])*np.cos(alpha[i]),
                       np.sin(q[i])*np.sin(alpha[i]), a[i]*np.cos(q[i])],
                      [np.sin(q[i]), np.cos(q[i])*np.cos(alpha[i]),
                       -np.cos(q[i])*np.sin(alpha[i]), a[i]*np.sin(q[i])],
                      [0, np.sin(alpha[i]), np.cos(alpha[i]), d[i]],
                      [0, 0, 0, 1]])
        return A   

    def o(self,n):
        T = np.identity(4)
        for i in range(n):
            T = T @ self.A(i)
        o = T[0:3,3]
        return o
    
    def z(self,n):
        T = np.identity(4)
        for i in range(n):
            T = T @ self.A(i)
        z = T[0:3,2]
        return z
    
    def J(self):
        j = np.zeros((6,1))
        for i in range(1,3):
            p = np.cross(self.z(i-1),self.o(7)-self.o(i-1)).reshape(3,1)
            p = np.vstack((p,self.z(i-1).reshape(3,1)))
            j = np.hstack((j,p))
        for i in range(4,8):
            p = np.cross(self.z(i-1),self.o(7)-self.o(i-1)).reshape(3,1)
            p = np.vstack((p,self.z(i-1).reshape(3,1)))
            j = np.hstack((j,p))
        jacobian = j[:,1:]
        if abs(np.linalg.det(jacobian)) <= 1e-1:
            print("singular warning!", abs(np.linalg.det(jacobian)))

        return jacobian

    def FVK(self,qdot):
        if len(qdot) >= 7:
            print("Please make sure you enter only 6 joint velocities, ignore joint 3!")
        Xdot = self.J() @ qdot.reshape(6,1)
        return Xdot

    def IVK_circle(self,t):
        omega = 2*np.pi/5
        radius = 100 # mm
        #xdot = 1
        ydot = -radius*omega*np.sin(omega*t + np.pi/2)
        xdot = 0
        #zdot = 1 
        zdot = radius*omega*np.cos(omega*t + + np.pi/2)
        # Assuming that the tool frame doesn't rotate
        Xdot = np.array([xdot,ydot,zdot,0,0,0]).reshape(6,1)
        qdot = np.linalg.inv(self.J()) @ Xdot
        error = Xdot - self.FVK(qdot)
        qdot = np.insert(qdot, 2, 0).reshape(7,1)
        return qdot, error

    def show(self,fig,ax):
        ax.clear()
        # Link 1
        j1 = self.o(0)
        j2 = self.o(1)
        j4 = self.o(3)
        j6 = self.o(5)
        ee = self.o(7)

        x = [j1[0],j2[0]]
        y = [j1[1],j2[1]]
        z = [j1[2],j2[2]]
        ax.plot(x,y,z,color='k',linewidth=5)
        x = [j2[0],j4[0]]
        y = [j2[1],j4[1]]
        z = [j2[2],j4[2]]
        ax.plot(x,y,z,color='k',linewidth=5)
        x = [j4[0],j6[0]]
        y = [j4[1],j6[1]]
        z = [j4[2],j6[2]]
        ax.plot(x,y,z,color='k',linewidth=5)
        x = [j6[0],ee[0]]
        y = [j6[1],ee[1]]
        z = [j6[2],ee[2]]
        ax.plot(x,y,z,color='k',linewidth=5)
        A = self.A(0) @ self.A(1) @ self.A(2) @ self.A(3) @ self.A(4) @ self.A(5) @ self.A(6)
        o =  A @ np.array([0,0,0,1]).T
        vx = A[0:3,0:3] @ np.array([100,0,0])
        vy = A[0:3,0:3] @ np.array([0,100,0])
        vz = A[0:3,0:3] @ np.array([0,0,100])
        ax.quiver(o[0],o[1],o[2],vx[0],vx[1],vx[2],color='r')
        ax.quiver(o[0],o[1],o[2],vy[0],vy[1],vy[2],color='g')
        ax.quiver(o[0],o[1],o[2],vz[0],vz[1],vz[2],color='b')
        ax.set_xlim3d(-800,800)
        ax.set_ylim3d(-600,1000)
        ax.set_zlim3d(0,1000)
        fig.canvas.draw()
        fig.canvas.flush_events()

def main():
    q = np.array([0,-30,0,-45,0,75,0])
    robot = Kuka(q)
    print(robot.o(7))
    #print(robot.J()[:3,:])
    end_time = 5
    time_steps = 2000
    dt = end_time/time_steps
    T = np.linspace(0,end_time,time_steps)
    #qdot,error = robot.IVK_circle(1)
    #print(error)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    #ax2 = fig.add_subplot()
    plt.ion()
    plt.axis('auto')
    for t in T:
        #robot.show(fig,ax)
        qdot,error = robot.IVK_circle(t)
        q = robot.get_joints()
        #print(error)
        #ax2.plot(error)
        #print(q)
        #print(qdot)
        q += qdot*dt
        #print(q)
        robot.set_joints(q)
        x,y,z = robot.o(7).tolist()
        #print([x,y,z])
        ax.plot(x,y,z,c='k',marker='.')
        #plt.pause(0.01)
    #ax.set_xlim(-30,30)
    #ax.set_ylim(550,610)
    #ax.set_zlim(750,850)
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_zlabel("Z axis")
    plt.pause(340)


if __name__ == '__main__':
    main()