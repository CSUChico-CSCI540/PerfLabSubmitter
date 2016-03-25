/**
 * @file aprof.c
 *
 * @remark Copyright 2013 P.J. Drongowski
 * @remark Read the file COPYING
 * @remark Initial code written by Paul J. Drongowski and has been modified to use 
 *         per-core kthreads for multi-core ARM systems. 
 * 
 *
 * @author Bryan Dixon
 */
#define CPU_COUNT 4

#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/moduleparam.h>
#include <linux/workqueue.h>
#include <linux/time.h>
#include <linux/kthread.h>
#include <asm/mutex.h>
#include <asm/smp.h>


//
// Read the Secure Use and Non-secure Access Validation
// Control Register and return its value.
//
static inline unsigned long
armv6_sunsav_read(void)
{
	u32 val;
	asm volatile("mrc p15, 0, %0, c9, c14, 0" : "=r"(val));
	return val;
}

//
// Write the Secure Use and Non-secure Access Validation
// Control Register
//
static inline int
armv6_subsav_enable(void* val)
{
    int cpu;
    unsigned long value = 1 ;
    unsigned long sunsav;  
	asm volatile("mcr   p15, 0, %0, c9, c14, 0" : : "r"(value));
	asm volatile("mcr p15, 0, %0, c9, c12, 1" :: "r"(0x8000000f));
	asm volatile("MCR p15, 0, %0, C9, C14, 2\n\t" :: "r"(0x8000000f));
	sunsav = armv6_sunsav_read() ;
	cpu = smp_processor_id();

    printk ("per_cpu_thread entering (cpu:%d)...\n", cpu);

	printk ("SUNSAV: %lu\n", sunsav) ;
	return 0;
}

static inline int
armv6_subsav_disable(void* val)
{
    int cpu;
    unsigned long value = 0 ;
    unsigned long sunsav;  
	asm volatile("mcr   p15, 0, %0, c9, c14, 0" : : "r"(value));
	sunsav = armv6_sunsav_read() ;
	cpu = smp_processor_id();

    printk ("per_cpu_thread entering (cpu:%d)...\n", cpu);

	printk ("SUNSAV: %lu\n", sunsav) ;
	return 0;
}


struct task_struct* thread_init(void* data, int cpu)
{
    struct task_struct *ts;
    
    ts=kthread_create(&armv6_subsav_enable, data, "per_cpu_thread");
    kthread_bind(ts, cpu);
    if (!IS_ERR(ts)) {
        wake_up_process(ts);
    }
    else {
        printk ("Failed to bind thread to CPU %d\n", cpu);
    }
    return ts;
}

struct task_struct* thread_disable(void* data, int cpu)
{
    struct task_struct *ts;
    
    ts=kthread_create(&armv6_subsav_disable, data, "per_cpu_thread");
    kthread_bind(ts, cpu);
    if (!IS_ERR(ts)) {
        wake_up_process(ts);
    }
    else {
        printk ("Failed to bind thread to CPU %d\n", cpu);
    }
    return ts;
}


static int __init aprofile_init(void)
{
	int err = 0 ;
	int i=0;
	
	printk ("aprofile module loaded\n") ;	
    for(i=0;i<CPU_COUNT;i++){       
        thread_init(&i, i);
    }
	

	return( err ) ;
}

static void __exit aprofile_exit(void)
{
	unsigned long sunsav = 0 ;
	int i;

	// Disable user-space access to the Performance Monitor counters
	for(i=0;i<CPU_COUNT;i++){       
        thread_disable(&i, i);
    }
	// Read the Secure User and Non-secure Access Validation register
	//sunsav = armv6_sunsav_read() ;

	printk ("SUNSAV: %lu\n", sunsav) ;
	printk ("aprofile module unloading...\n") ;
}

module_init(aprofile_init);
module_exit(aprofile_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Bryan Dixon");
MODULE_DESCRIPTION("Simple ARMv6 profiler multi-core enabler");
