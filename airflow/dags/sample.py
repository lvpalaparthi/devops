#import modules
from datetime import timedelta
import airflow
import time
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

#set default arguments 
default_args = {
    'owner' : 'airflow',
    'start_date' : days_ago(5),
    #'end_date' : datetime(2021, 12, 30),
    'depends_on_past' : False,
    'email' : ['lvpalaparthi@gmail.com'],
    'email_on_failure' : False,
    'email_on_retry' : False,
    'retries' : 1,
    'retry_delay' : timedelta(minutes=5),
    'queue': 'bash_queue',
    'pool': 'backfill',
    'priority_weight': 10,
    'end_date': datetime(2016, 1, 1),
    'wait_for_downstream': False,
    'dag': dag,
    'adhoc':False,
    'sla': timedelta(hours=2),
    'execution_timeout': timedelta(seconds=300),
    'on_failure_callback': some_function,
    'on_success_callback': some_other_function,
    'on_retry_callback': another_function,
    'trigger_rule': u'all_success'
}


#give dag a name, configure the schedule, and set dag settings 

dag = DAG(
    'first_dag',
    default_args = default_args,
    description = "this is my first DAG",
    schedule_interval = timedelta(days=1),

)

#tasks created by instantiating operators 
t1 = BashOperator(
    task_id = 'first_task',
    bash_command = 'echo 1',
    dag=dag,
)

t2 = BashOperator(
    task_id = 'second_task',
    bash_command = 'echo 2',
    dag = dag,
)

templated_command = """
{% for i in range(5) %}
echo "{{ds}}"
echo " {{macros.ds_add(ds, 7)}}"
echo "{{params.mu_param}}"
{% endfor %}
"""

t3 = BashOperator(
    task_id='templated_third_task',
    depends_on_past=False,
    bash_command=templated_command,
    params={'my_param' : 'Parameter that I passed in'},
    dag = dag,
)

def print_context(**context):
    print('Process is working!')

run_this_task = PythonOperator(
    task_id='print_the_context',
    provide_context = True,
    python_callable = print_context,
    dag=dag,
)

def my_sleeping_function(random_base):
    time.sleep(random_base)
    print(f"random base {random_base} Done!")

with dag:
    for i in range(3):
        run_this = PythonOperator(
            task_id = 'sleep_for_' + str(i),
            python_callable=my_sleeping_function,
            op_kwargs={'random_base' : float(i)/10},
        )
run_this_task >> t4
t4 = PythonOperator(
    task_id = 'sleep_for_1',
    python_callable=my_sleeping_function,
    op_kwargs={'random_base' : float(1)/10},
    dag=dag,
)

clean = BashOperator(
    task_id = 'clean_task',
    bash_command = 'echo 3',
    dag=dag,
)

# task_2.set_downstream(task_3)
#task_1.set_downstream(task_2)

# task_1 >> task_2
t2.set_upstream(t1)
t3.set_upstream(t2)
t3 >> [run_this_task, run_this]
# run_this_task >> t4
clean << [run_this_task, run_this]

#task_2.set_downstream(task_3)

#task1 >> [task_2, task_3]