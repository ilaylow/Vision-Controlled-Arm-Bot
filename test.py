import Adeept
import time

global thread_flag
thread_flag = 1

Adeept.com_init('COM13',115200,1)
Adeept.wiat_connect()

############cut-off rule#################

Adeept.three_function("'pinmode'",8,1)
while thread_flag:
  Adeept.three_function("'digitalWrite'",8,1)
  time.sleep(1)
  Adeept.three_function("'digitalWrite'",8,0)
  time.sleep(1)