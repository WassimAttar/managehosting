clean:
	rm -rf managehosting managehosting.tar.gz
	find . -name "*.pyc" -delete

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
PYTHON ?= /usr/bin/env python

install: managehosting
	install -d $(BINDIR)
	install -m 755 managehosting $(BINDIR)

managehosting.tar.gz:
	@tar -czf managehosting.tar.gz --owner 0 --group 0 \
		--exclude '*.pyc' \
		-- \
		*.py \
		README.md \
		Makefile \

managehosting:
	zip --quiet managehosting *.py
	echo '#!$(PYTHON)' > managehosting
	cat managehosting.zip >> managehosting
	rm managehosting.zip
	chmod a+x managehosting