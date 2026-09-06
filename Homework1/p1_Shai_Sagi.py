import math
import matplotlib.pyplot as plt


def main():
    while True:
        a_input=input("Enter a: ")
        if a_input=="":
            break

        a=float(a_input)
        b=float(input("Enter b: "))
        c=float(input("Enter c: "))

        discriminant=b ** 2 - 4 * a * c

        if discriminant < 0:
            print("no real solutions")
            center=-b / (2 * a)
            xmin=center - 5
            xmax=center + 5
        elif discriminant == 0:
            x1=-b / (2 * a)
            print("one solution: {:.5f}".format(x1))
            xmin=x1 - 5
            xmax=x1 + 5
        else:
            x1=(-b - math.sqrt(discriminant)) / (2 * a)
            x2=(-b + math.sqrt(discriminant)) / (2 * a)
            print("two solutions: x1={:.5f} x2={:.5f}".format(x1, x2))
            xmin=min(x1, x2) - 2
            xmax=max(x1, x2) + 2

        xs=[xmin + i * (xmax - xmin) / 149 for i in range(150)]
        ys=[a * x ** 2 + b * x + c for x in xs]

        plt.figure()
        plt.plot(xs, ys)
        plt.axhline(0, color="black")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Quadratic Function")
        plt.grid(True)
        plt.show()


if __name__=="__main__":
    main()
