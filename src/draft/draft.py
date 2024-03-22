import multiprocessing
import time


# Define a function to perform a computation-intensive task
def compute_task(task_id, iterations):
    print(f"Process {task_id} started.")
    start_time = time.time()
    result = 0
    for i in range(iterations):
        result += i
    end_time = time.time()
    print(f"Process {task_id} completed. Time taken: {end_time - start_time:.2f} seconds")
    return result


if __name__ == "__main__":
    # Number of processes to create
    num_processes = 4

    # Number of iterations for each process
    iterations_per_process = 10000000

    # Create a pool of worker processes
    pool = multiprocessing.Pool(processes=num_processes)

    # Start the computation tasks in parallel
    results = [ pool.apply_async(compute_task, (i, iterations_per_process)) for i in range(num_processes)]

    # Wait for all processes to complete and collect results
    pool.close()
    pool.join()

    # Extract results from async results objects
    final_results = [result.get() for result in results]

    # Print the results
    print("Final Results:", final_results)
