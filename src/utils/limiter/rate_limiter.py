import time
from datetime import datetime, timedelta
from math import ceil
from typing import List

from requests import Response

from utils.limiter.limiter import Limiter


class RateLimiter(Limiter):
    _self = None

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.requests_logs_very_short: List[datetime] = []
        self.requests_logs_short: List[datetime] = []
        self.requests_logs_long: List[datetime] = []

    def __calculate_wait_time(self, time_window: int, log: List[datetime]) -> float:
        now = datetime.now()
        oldest_call = log[0]
        time_difference_in_seconds = (now - oldest_call).total_seconds()
        wait_time = ceil(time_window - time_difference_in_seconds)
        print(f"\n Waiting for {abs(wait_time)} seconds")
        return wait_time

    def __log_cleaner(self, log: List[datetime], time_window: int):
        now = datetime.now()

        for call in log:
            time_difference = now - call
            if time_difference > timedelta(seconds=time_window):
                log.remove(call)
            else:
                break

    def rate_limiter(self, response: Response) -> None:
        now = datetime.now()
        self.requests_logs_very_short.append(now)
        self.requests_logs_short.append(now)
        self.requests_logs_long.append(now)

        (
            very_short_state_limit,
            short_state_limit,
            long_state_limit,
        ) = response.headers["X-Rate-Limit-Ip"].split(",")

        very_short_info, short_info, long_info = response.headers[
            "X-Rate-Limit-Ip-State"
        ].split(",")

        very_short_state_limit = int(very_short_state_limit.split(":")[0])
        short_state_limit = int(short_state_limit.split(":")[0])
        long_state_limit = int(long_state_limit.split(":")[0])

        current_very_short_state = int(very_short_info.split(":")[0])
        current_short_state = int(short_info.split(":")[0])
        current_long_state = int(long_info.split(":")[0])

        time_window_very_short = int(very_short_info.split(":")[1])
        time_window_short = int(short_info.split(":")[1])
        time_window_long = int(long_info.split(":")[1])

        # print(
        #     f"API requests status: "
        #     f"{current_very_short_state}:{very_short_state_limit}, "
        #     f"{current_short_state}:{short_state_limit}, "
        #     f"{current_long_state}:{long_state_limit}"
        # )

        self.__log_cleaner(self.requests_logs_very_short, time_window_very_short)
        self.__log_cleaner(self.requests_logs_short, time_window_short)
        self.__log_cleaner(self.requests_logs_long, time_window_long)

        if current_very_short_state == very_short_state_limit - 1:
            wait_time = self.__calculate_wait_time(
                time_window_very_short, self.requests_logs_very_short
            )
            time.sleep(abs(wait_time))

        if current_short_state == short_state_limit - 1:
            wait_time = self.__calculate_wait_time(
                time_window_short, self.requests_logs_short
            )
            time.sleep(abs(wait_time))

        if current_long_state == long_state_limit - 1:
            wait_time = self.__calculate_wait_time(
                time_window_long, self.requests_logs_long
            )
            time.sleep(abs(wait_time))
