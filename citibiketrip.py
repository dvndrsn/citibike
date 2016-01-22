import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
from location import location
import multiprocessing as mp
import time
import sys
import os.path
import os
import gc
# from memory_profiler import profile

def process_frame(data):
    data['starttime']=pd.to_datetime(data['starttime'],errors='raise')
    data['stoptime']=pd.to_datetime(data['stoptime'],errors='raise')

    # Define date parameters
    data['date']=data['starttime'].apply(lambda x: x.date())
    data['year']=data['starttime'].apply(lambda x: x.year)
    data['month']=data['starttime'].apply(lambda x: x.month)
    data['day']=data['starttime'].apply(lambda x: x.day)
    data['weekday']=data['starttime'].apply(lambda x: x.isoweekday())
    data['hour']=data['starttime'].apply(lambda x: x.hour)

    # Define distance and location parameters
    data['start_loc']=data.apply(
        lambda x:
        location(x['start station longitude'],
                 x['start station latitude']),
        axis=1)

    data['end_loc']=data.apply(
        lambda x:
        location(x['end station longitude'],
                 x['end station latitude']),
        axis=1)

    data['harversine_dist']=data.apply(
        lambda x:
        x['start_loc'].harversine(x['end_loc']),
        axis=1)

    return data



def process_file_async(file, pools, chunk_size):
    reader = pd.read_csv(file, header=0, chunksize=chunk_size)
    pool = mp.Pool(pools) # should not be more than # of cores

    funclist = []
    num_chunks = 0
    for df in reader:
        num_chunks += 1
        print("Processing async chunk # {}".format(num_chunks))
        f = pool.apply_async(process_frame,[df])
        funclist.append(f)
        # debugging, so break
        # break

    data = pd.DataFrame()
    curr_chunk = 0
    for f in funclist:
        curr_chunk += 1
        print("Waiting for chunk # {} of {}".format(curr_chunk, num_chunks))
        data = data.append(f.get())
        print("Processed data: {}".format(data.shape))

    pool.close()

    return data


def pickle_data(df, file):
    print("Pickling results in {}".format(file))

    df.to_pickle(file + ".p")


def process_file(file):
    data = pd.read_csv(file, header=0)

    data = process_frame(data)

    return data


def auto_chunksize(file, pools):
    line_count = sum(1 for line in open(file))
    auto_chunksize = line_count // pools # use integer division
    return auto_chunksize


def main():
    path = 'data/raw' # sys.argv[1]
    chunks = 'auto' # sys.argv[2]
    pools = 4 # int(sys.argv[3])

    print("Garbabgeee timee!")
    #print(gc.get_objects())
    print(gc.collect())
    print(gc.garbage)
    #print(gc.get_objects())
    if os.path.isdir(path):
        files = [os.path.join(path,f) for f in os.listdir(path) \
                 if os.path.isfile(os.path.join(path, f))]
    else:
        files = [path]

    for file in files:
        chunksize = auto_chunksize(file, pools) \
                    if chunks == 'auto' else int(chunks)

        # open this file by default..
        print("Running process for {} with {} pools and chunksize {}".format(
            file,pools, chunksize))

        async_start_time = time.time()
        if chunksize == 0:
            data = process_file(file)
        else:
            data = process_file_async(file, pools, chunksize)

        print("Garbabgeee timee!")
        #print(gc.get_objects())
        print(gc.collect())
        print(gc.garbage)
        #print(gc.get_objects())

        target_file = "data/processed/" + os.path.basename(file) + ".p"
        pickle_data(data, target_file)
        async_runtime = time.time() - async_start_time

        #Async Execution took 653.6547598838806 seconds w/ chunksize 1000
        #Async Execution took 400.7142684459686 seconds w/ chunksize 10000
        print("Execution took {} seconds w/ {} pools and chunksize {}".format(
            async_runtime, pools, chunksize))
        # input()
        #Sync Execution took 760.2624118328094 seconds
        # print("Sync Execution took {} seconds".format(sync_runtime))


if __name__ == '__main__':
    main()