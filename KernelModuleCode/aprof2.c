#define CPU_COUNT 4
#include <stdio.h>
#include "linux/kthread.h"

int per_cpu_thread_fn(void* data);

/* Thread util function for binding the thread to CPU*/
struct task_struct* thread_init(void* data, int cpu)
{
    struct task_struct *ts;

    ts=kthread_create(per_cpu_thread_fn, data, "per_cpu_thread");
    kthread_bind(ts, cpu);
    if (!IS_ERR(ts)) {
        wake_up_process(ts);
    }
    else {
        printk("Failed to bind thread to CPU %d\n", cpu);
    }
    return ts;
}


void do_something()
{
}

/* Child thread */
int per_cpu_thread_fn(void* data)
{
    int* d = (int*)data;
    printf("%d\n",*d);
}

/* Main thread */
int main_thread()
{
    int i;
    for(i=0;i<CPU_COUNT;i++){       
        thread_init(&i, i);
    }
}