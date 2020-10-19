import numpy as np
# from scipy.optimize import curve_fit

def main(region, no_periods):


    xdata = []
    ydata = []

    with open('data/' + region + '/ydata.txt') as f:
        for line in f:
            # if float(line) > threshold:
            #     ydata.append(threshold)
            # el
            # if float(line) < 0:
            #     ydata.append(0)
            # else:
            #     ydata.append(float(line))
            ydata.append(float(line))

    with open('data/' + region + '/xdata.txt') as f:
        for line in f:
            xdata.append(float(line))


    # xdata = [float(i)/float(len(ydata)) for i in xrange(len(ydata))]

    # plt.plot(xdata, ydata, 'b-', label='data')


    def func(x, a, b, c):
        return a * np.exp(-b * x) + c


    # popt, pcov = curve_fit(func, xdata, ydata)

    order = 2
    coeffs = np.polyfit(xdata, ydata, order)
    poly_curve = np.poly1d(coeffs)
    # print z

    levels = 20
    demands = np.linspace(min(xdata), 1, levels)
    prices = poly_curve(demands)
    # print prices

    # plt.plot(xdata, ydata, '.', label="data")
    # plt.plot(xp, p(xp), 'r-', label="poly fit")
    # # plt.plot(xp, func(xp, *popt), 'w-', label='exp fit')
    #
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.show()

    lookup = []
    lookup.append([round(p, 2) for p in prices])
    for i in xrange(no_periods):
        lookup.append([round(d, 2) for d in demands])

    lookup = np.transpose(lookup).tolist()
    return lookup
