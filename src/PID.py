import time

class PID:
    def __init__(self, kp, ki, kd):
        """
        Set up the PID control.

        :param kp: the value for Kp
        :param ki: the value for Ki
        :param kd: the value for Kd
        """

        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.err_sum = 0
        self.prev_err = 0
        self.prev_time = 0

    def generate(self, err):
        """
        Generate the output of PID.

        :param err: new err
        :return: the result of PID
        """

        if self.prev_time == 0:
            self.prev_time = time.time()
            self.err_sum += err
            self.prev_err = err
            return self.kp * err 

        cur_time = time.time()
        elapsed_time = (cur_time - self.prev_time)
        self.prev_time = cur_time

        self.err_sum += err
        res = self.kp * err + self.ki * self.err_sum * elapsed_time + self.kd * (err - self.prev_err) / elapsed_time
        self.prev_err = err

        return res