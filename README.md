[![Win Probability](https://github.com/acceval/Win-Probability/actions/workflows/main.yml/badge.svg)](https://github.com/acceval/Win-Probability/actions/workflows/main.yml)

# Win-Probability

## Price Model

### Resource URL

```
https://win-probability.herokuapp.com/price_model
```

### Parameters

```
{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "cons":"prob > 0.8", "margin_threshold":"50"}
```

Input:
1. File : Path to input file. Sample file can be found at: https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv.   
2. msrp : MSRP column name in the file. The name can't contain space.
3. unitcost : unitcost column name in the file. The name can't contain space.
4. unitprice : unitprice column name in the file. The name can't contain space.
5. win : win column name in the file. The name can't contain space.
6. units : units column name in the file. The name can't contain space.
7. cons : [optional] constraint of the output. The format is like this: "prob [<,<=,>,>=] [number]". At this time, the only accepted variable is "prob".
8. margin_threshold : [optional] the tolerable deducted margin threshold to be used along with the constraint. 

### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 231' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/fleet_sales.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "cons":"prob > 0.8", "margin_threshold":"50"}' https://win-probability.herokuapp.com/price_model
```

### Sample Output

```
{"status": 1, "error": null, "data": [{"parameters": {"intercept": -7.756270649447668, "price": 9.164200156150054}, "constraint": "prob > 0.8", "margin_threshold": 50.0, "suggestion": {"optimal_price_ratio": 0.6900000000000002, "actual_price": 17250.000000000004, "probability": 0.8073640497111536, "margin": 1816.5691118500986}}]}
```

## Segmented Model

### Resource URL

```
https://win-probability.herokuapp.com/segmented_model
```

### Parameters

```
{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "government":"Government", "cons":"prob > 0.8", "margin_threshold":"50"}
```

Input:
1. File : Path to input file. Sample file can be found at: https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv.   
2. msrp : MSRP column name in the file. The name can't contain space.
3. unitcost : unitcost column name in the file. The name can't contain space.
4. unitprice : unitprice column name in the file. The name can't contain space.
5. win : win column name in the file. The name can't contain space.
6. units : units column name in the file. The name can't contain space.
7. government : government column name in the file. The name can't contain space. A flag indicatin that the transaction row belong to government. 1 for government transaction, 0 for corporate transaction.
8. cons : [optional] constraint of the output. The format is like this: "prob [<,<=,>,>=] [number]". At this time, the only accepted variable is "prob".
9. margin_threshold : [optional] the tolerable deducted margin threshold to be used along with the constraint. 


### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 262' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/segmented_model.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "government":"Government", "cons":"prob > 0.8", "margin_threshold":"50"}' https://win-probability.herokuapp.com/segmented_model
````

### Sample Output

```
{"status": 1, "error": null, "data": [{"government": {"parameters": {"intercept": -14.218728794802145, "price": 20.001706624867932}, "constraint": "prob > 0.8", "margin_threshold": 50.0, "suggestion": {"optimal_price_ratio": 0.6400000000000001, "actual_price": 16000.000000000004, "probability": 0.8049676353761264, "margin": 804.9676353761294}}, "corporate": {"parameters": {"intercept": -25.97032640274357, "price": 26.640045506707242}, "constraint": "prob > 0.8", "margin_threshold": 50.0, "suggestion": {"optimal_price_ratio": 0.8900000000000003, "actual_price": 22250.000000000007, "probability": 0.9055683018147103, "margin": 6565.370188156656}}}]}
```

## Size Model

### Resource URL

```
https://win-probability.herokuapp.com/size_model
```

### Parameters

```
{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "government":"Government", "cons":"prob > 0.8", "margin_threshold":"50"}
```

Input:
1. File : Path to input file. Sample file can be found at: https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv.   
2. msrp : MSRP column name in the file. The name can't contain space.
3. unitcost : unitcost column name in the file. The name can't contain space.
4. unitprice : unitprice column name in the file. The name can't contain space.
5. win : win column name in the file. The name can't contain space.
6. units : units column name in the file. The name can't contain space.
7. government : government column name in the file. The name can't contain space. A flag indicatin that the transaction row belong to government. 1 for government transaction, 0 for corporate transaction.
8. cons : [optional] constraint of the output. The format is like this: "prob [<,<=,>,>=] [number]". At this time, the only accepted variable is "prob".
9. margin_threshold : [optional] the tolerable deducted margin threshold to be used along with the constraint. 

### How To Call

```
curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 257' -H 'Content-type: application/json' -H 'User-Agent: python-requests/2.26.0' -d '{"file" :"https://raw.githubusercontent.com/acceval/Win-Probability/main/size_model.csv", "msrp":"MSRP", "unitcost":"Unit_Cost", "unitprice":"Unit_Price", "win":"Win", "units":"Units", "government":"Government", "cons":"prob > 0.8", "margin_threshold":"50"}' https://win-probability.herokuapp.com/size_model
```

### Sample Output

```
{"status": 1, "error": null, "data": [{"government": {"parameters": {"intercept": -15.072509222936542, "price": 20.277812849157183, "size": 0.03336915656538306}, "constraint": "prob > 0.8", "margin_threshold": 50.0, "suggestion": {"optimal_price_ratio": 0.6600000000000001, "actual_price": 16500.000000000004, "probability": 0.8441127047733161, "margin": 1266.1690571599772}}, "corporate": {"parameters": {"intercept": -25.903732236930107, "price": 26.612409769478223, "size": -0.002289422824377025}, "constraint": "prob > 0.8", "margin_threshold": 50.0, "suggestion": {"optimal_price_ratio": 0.8900000000000003, "actual_price": 22250.000000000007, "probability": 0.9019151513789001, "margin": 6538.884847497033}}}]}
```

