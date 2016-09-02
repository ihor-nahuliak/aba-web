#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir, getpid
from os.path import isfile, join, splitext
import logging
from aba.aba_parser import ABA_Parser
from aba.aba_perf_logger import ABA_Perf_Logger

## Safety measure so that the process won't overshoot my RAM limit
import sys
if sys.platform == "win32":
    import perf_memory_limiter
    five_gb = 5 * 1024 * 1024 * 1024
    perf_memory_limiter.set_limit(getpid(), five_gb)

logging.basicConfig(filename='logs/PerfTest.log',level=logging.INFO,format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Start performance test")
global_perf_logger = ABA_Perf_Logger("Overall performance test")
global_perf_logger.start()

path = "perf_test_data"
test_files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == ".txt"]

for file in test_files:
    with open(join(path, file), 'r') as f:
        source_code = f.read()
        logging.info("Start running %s", file)
        perf_logger = ABA_Perf_Logger("%s" % file)
        perf_logger.start()

        parser = ABA_Parser(source_code)
        parse_errors = parser.parse()

        if len(parse_errors) > 0:
            logging.info("Parse error: %s", ', '.join(parse_errors))
        else:
            try:
                parser.construct_aba()
            except MemoryError:
                logging.error("Out of memory!")
            except Exception as exp:
                logging.error("Runtime error: %s", str(exp))

        perf_logger.end()

global_perf_logger.end()