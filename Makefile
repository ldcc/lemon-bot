app=lemon
cqhttp=go-cqhttp

$(app): abort-$(app)
	docker run -dp 0.0.0.0:6000:6000 -v $(PWD)/src/data/store:/app/src/data/store --name $(app) $(app):latest
cqhttp: abort-cqhttp
	cd cqhttp && \
	chmod +x $(cqhttp) && \
	./$(cqhttp) > /dev/null 2>&1 &
start:
	make cqhttp
	make $(app)
commit:
	git add src/data/store
	if [ -z git status | grep 'nothing to commit' ]; then \
  		git commit -m 'save stored' &&\
		git stash &&\
		if [ -n "`git stash list`" ]; then git stash drop; fi \
	fi
	git pull origin master
	git push origin master
upgrade:
	make commit
	git pull origin master
	if [ -z "`docker images | grep python | grep 3.8`" ]; then docker pull python:3.8; fi
	docker build -t $(app):latest .
	make $(app)

abort: abort-cqhttp abort-$(app)
abort-$(app):
	if [ -n "`docker ps -a | grep $(app)`" ]; then docker rm `docker stop $(app)`; fi
abort-cqhttp:
	if [ -n "`pgrep $(cqhttp)`" ]; then sudo pkill $(cqhttp); fi

.PHONY: cqhttp upgrade start abort abort-$(app) abort-cqhttp
