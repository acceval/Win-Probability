[![Win Probability](https://github.com/acceval/Win-Probability/actions/workflows/main.yml/badge.svg)](https://github.com/acceval/Win-Probability/actions/workflows/main.yml)

# Win-Probability

## Price Model

### Resource URL

```
https://win-probability.herokuapp.com/price_model
```

### Parameters

```
{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units"}
```

Input:
1. File 
2. msrp
3. unitcost
4. unitprice
5. win
6. units

### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 185' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units"}' https://win-probability.herokuapp.com/price_model
```

### Sample Output

```
{"status": 1, "error": null, "data": [{"parameters": {"intercept": -7.756274057361606, "price": 9.164204466877205}, "suggestion": {"optimal_price_ratio": 0.8300000000000003, "actual_price": 20750.000000000007, "probability": 0.5374259547306021, "margin": 3090.199239700966}}]}
```

## Segmented Model

### Resource URL

```
https://win-probability.herokuapp.com/segmented_model
```

### Parameters

### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 216' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "government":"Government"}' https://win-probability.herokuapp.com/segmented_model
````

### Sample Output

```
{"status": 1, "error": null, "data": [{"government": {"parameters": {"intercept": -14.218724594791366, "price": 20.001700874328492}, "suggestion": {"optimal_price_ratio": 0.7100000000000002, "actual_price": 17750.000000000004, "probability": 0.5043791315291146, "margin": 1387.042611705067}}, "corporate": {"parameters": {"intercept": -25.97034068132109, "price": 26.640062449882997}, "suggestion": {"optimal_price_ratio": 0.9000000000000004, "actual_price": 22500.000000000007, "probability": 0.8801956773814624, "margin": 6601.467580360974}}}]}
```

## Size Model

### Resource URL

```
https://win-probability.herokuapp.com/size_model
```

### Parameters

### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 211' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "government":"Government"}' https://win-probability.herokuapp.com/size_model
```

### Sample Output

```
{"status": 1, "error": null, "data": [{"government": {"parameters": {"intercept": -15.072509234946159, "price": 20.27781282625948, "size": 0.033369155500851864}, "suggestion": {"optimal_price_ratio": 0.7200000000000002, "actual_price": 18000.000000000004, "probability": 0.6159715171247364, "margin": 1847.9145513742114}}, "corporate": {"parameters": {"intercept": -25.903769192432303, "price": 26.612452435024107, "size": -0.002289412025967165}, "suggestion": {"optimal_price_ratio": 0.9000000000000004, "actual_price": 22500.000000000007, "probability": 0.875725733319258, "margin": 6567.942999894441}}}]}
```

