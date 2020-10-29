import numpy as np
import cv2 as cv
import math

class MeanShift:

    def __init__(self, distribution, trace_window, n_iter_limit=10):
        self.distribution = distribution
        self.centroid = (trace_window[0] + int(trace_window[2] / 2), trace_window[1] + int(trace_window[3] / 2))
        self.n_iter_limit = n_iter_limit
        self.trace_window = trace_window
        self.optimized = False
        self.dx = self.trace_window[2] / 2
        self.dy = self.trace_window[3] / 2
        self.fit()

    def check_xy(self, mx, my):
        if mx-self.dx < 0:
            mx = 0
            print('Change')
        elif mx - self.trace_window[2] > self.distribution.shape[0]:
            mx = self.distribution.shape[0] - self.trace_window[2]
            print('Change')
        else:
            mx = mx-self.dx

        if my-self.dy < 0:
            my = 0
            print('Change')
        elif my - self.trace_window[3] > self.distribution.shape[1]:
            my = self.distribution.shape[1] - self.trace_window[3]
            print('Change')
        else:
            my = my-self.dy

        return mx, my

    def _m(self, ):
        x, y, w, h = [int(v) for v in self.trace_window]
        kernel = self.distribution[y:y + h, x:x + w].T

        x_tmp = np.ones(kernel.shape) * np.arange(x, x + w)[:, np.newaxis]
        y_tmp = np.ones(kernel.shape) * np.arange(y, y + h)
        if np.sum(kernel)==0:
            return

        m_x = np.average(x_tmp, weights=kernel)
        m_y = np.average(y_tmp, weights=kernel)

        m_x, m_y = self.check_xy(m_x, m_y)

        new_trace_window = (m_x, m_y, self.trace_window[2], self.trace_window[3])
        if new_trace_window == self.trace_window:
            self.optimized = True
        self.trace_window = new_trace_window

    def fit(self, ):
        while not self.optimized and self.n_iter_limit > 0:
            self.n_iter_limit -= 1
            try:
                self._m()
            except:
                pass

    def get_trace_window(self, ):
        return self.trace_window


class CamShift(MeanShift):

    def __init__(self, distribution, trace_window, n_iter_limit=10):
        super().__init__(distribution, trace_window, n_iter_limit)

    def camshift(self, ):
        iter_count = 0

        while True:
            iter_count += 1
            x, y, w, h = [int(v) for v in self.trace_window]
            kernel = self.distribution[y:y + h, x:x + w].T
            x_tmp = np.ones(kernel.shape) * np.arange(x, x + w)[:, np.newaxis]
            y_tmp = np.ones(kernel.shape) * np.arange(y, y + h)

            m00 = kernel.sum()
            if (m00 == 0):
                break

            m_x = np.average(x_tmp, weights=kernel)
            m_y = np.average(y_tmp, weights=kernel)
            m_x, m_y = self.check_xy(m_x, m_y)

            new_trace_window = (m_x, m_y, self.trace_window[2], self.trace_window[3])
            x, y, w, h = [int(v) for v in new_trace_window]

            #####
            x_tmp2 = np.average(np.ones(kernel.shape) * np.power(np.arange(x, x + w)[:, np.newaxis], 2), weights=kernel)
            y_tmp2 = np.average(np.ones(kernel.shape) * np.power(np.arange(y, y + h), 2), weights=kernel)
            xy_tmp = np.average(np.ones(kernel.shape) * np.arange(x, x + w)[:, np.newaxis] * np.arange(y, y + h), weights=kernel)

            a = x_tmp2 - m_x**2
            c = y_tmp2 - m_y**2
            b = (xy_tmp - m_x*m_y)

            l = np.sqrt(((a+c)+np.sqrt(b**2+(a-c)**2)))
            w = np.sqrt(((a + c) - np.sqrt(b ** 2 + (a - c) ** 2)))

            print(l,w)


            new_trace_window = (m_x, m_y, l, l)
            #####
            iter_count+=1
            if new_trace_window == self.trace_window or iter_count>10:
                break
            self.trace_window = new_trace_window

    def get_trace_window(self, ):
        self.camshift()
        print(self.trace_window)
        return self.trace_window

#
#
