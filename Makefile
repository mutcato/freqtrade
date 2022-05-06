scrap:
	# Defaults: 
	# --days 30. 
	# --timeframe: 1m, 5m.
	docker-compose run --rm freqtrade download-data --exchange binance --pairs-file user_data/data/binance/pairs.json

download-data:
	docker-compose run --rm freqtrade download-data \
	--exchange binance \
	--pairs-file user_data/data/binance/pairs.json \
	-t 4h \
	--days 360

backtest:
	docker-compose run --rm freqtrade backtesting --datadir user_data/data/binance --export trades --stake-amount 100 -s BBRSINaiveStrategy -i 4h

bot-logs:
	docker logs -f freqtrade

trade:
	docker-compose run --rm freqtrade trade -c user_data/config-volume-pairlist.json -s BBRSINaiveStrategy

plotly:
	docker-compose run --rm freqtrade plot-dataframe --strategy BBRSINaiveStrategy -i 15m
