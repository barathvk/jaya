.PHONY: all scrape
all: scrape
download-texts:
	rm -rf ./data/texts
	rm -rf ./temp
	mkdir -p ./data/texts
	wget 'http://www.sacred-texts.com/hin/maha/mahatxt.zip' -P ./temp
	unzip ./temp/mahatxt.zip -d ./data/texts
	rm -rf ./temp
download-elastic:
	rm -rf ./bin
	rm -rf ./temp
	mkdir ./bin
	wget 'https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/zip/elasticsearch/2.1.1/elasticsearch-2.1.1.zip' -P ./temp
	unzip ./temp/elasticsearch-2.1.1.zip -d ./bin
	mv ./bin/elasticsearch-2.1.1 ./bin/elasticsearch
	rm -rf ./temp
start-elastic:
	@cd bin/elasticsearch/bin; ./elasticsearch
scrape:
	@cd scrape; ./run.sh
