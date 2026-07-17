import time

def execution_time(function):

    start = time.perf_counter()

    result = function()

    end = time.perf_counter()

    return (
        result,
        end - start
    )