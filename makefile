Port = 48763
all: server.py request.py toolbox.py cookie.py
	python server.py $(Port)
clean:
	rm -rf Account_list.npy Cookie.npy message.txt nohup.out __pycache__