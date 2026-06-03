.PHONY: clean all release

all: build/reportGenerator

release: all
	goreleaser release --snapshot --clean

clean:
	rm -rf build
	rm -rf dist

build/reportGenerator: ./reportGenerator/* ./shared/*
	cd ./reportGenerator; go mod tidy; go build -ldflags '-w -s' -o ../build/reportGenerator .; cp -r weathercodes template.html ../build/
	cp ./reportGenerator/.env.example build/.env.example