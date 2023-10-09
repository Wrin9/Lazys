config.yaml里面设置quake的key

>python app.py -h
usage: app.py [-h] [--mode MODE] [--search SEARCH] [--start START] [--end END]

options:
  -h, --help       show this help message and exit
  --mode MODE      Search mode
  --search SEARCH  Search query
  --start START    Start, default 0
  --end END        End, default 10

例子：python app.py --mode="Quake" --search=app:"用友-UFIDA-NC财务系统" --start=0 --end=100

数据将会存储在当前目录下的Nscan.db中
