TARGET = aprofile.ko

MDIR = arch/arm/aprofile

DRIVER_OBJS =   aprof.o

CURRENT = $(shell uname -r)
KDIR = /usr/src/kernel/
PWD = $(shell pwd)
DEST = /lib/modules/$(CURRENT)/kernel/$(MDIR)

obj-m := aprofile.o
aprofile-objs := $(DRIVER_OBJS)

default:
	$(MAKE) -C $(KDIR) M=$$PWD

install:
	@if test -f $(DEST)/$(TARGET).orig; then\
		echo  "Backup of aprofile.ko already exists."; \
	else \
		echo  "Creating a backup of aprofile.ko."; \
		mv -v $(DEST)/$(TARGET) $(DEST)/$(TARGET).orig; \
	fi	
	su -c "cp $(TARGET) $(DEST) && /sbin/depmod -a"

revert:
	@echo  "Reverting to the original aprofile.ko."
	@mv -v $(DEST)/$(TARGET).orig $(DEST)/$(TARGET) 

clean:
	rm -f *.o aprofile.ko .*.cmd .*.flags *.mod.c

-include $(KDIR)/Rules.make
