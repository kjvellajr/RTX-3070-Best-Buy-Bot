SHELL := /bin/bash

.PHONY = help
.DEFAULT_GOAL := help

setup: ## setup dependencies
	pip install selenium aiohttp slack_sdk
	curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_91 > release_version
	wget -q -O chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$$(cat release_version)/chromedriver_linux64.zip
	unzip -o chromedriver_linux64.zip -d opt/
	rm chromedriver_linux64.zip

run: ## run bot
	python bot.py

help: 
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
