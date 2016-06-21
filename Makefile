all: managehosting README.md

clean:
	rm -rf managehosting managehosting.tar.gz
	find . -name "*.pyc" -delete

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
MANDIR ?= $(PREFIX)/man
SHAREDIR ?= $(PREFIX)/share
PYTHON ?= /usr/bin/env python

# set SYSCONFDIR to /etc if PREFIX=/usr or PREFIX=/usr/local
SYSCONFDIR != if [ $(PREFIX) = /usr -o $(PREFIX) = /usr/local ]; then echo /etc; else echo $(PREFIX)/etc; fi

install: managehosting
	install -d $(DESTDIR)$(BINDIR)
	install -m 755 managehosting $(DESTDIR)$(BINDIR)

tar: managehosting.tar.gz

managehosting: *.py
	zip --quiet managehosting *.py
	echo '#!$(PYTHON)' > managehosting
	cat managehosting.zip >> managehosting
	rm managehosting.zip
	chmod a+x managehosting

managehosting.tar.gz: managehosting
	@tar -czf managehosting.tar.gz --owner 0 --group 0 \
		--exclude '*.pyc' \
		-- \
		*.py \
		README.md \
		Makefile \
		managehosting
