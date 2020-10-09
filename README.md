toy python implementation of the streaming machine learning model serving pattern described in Serving Machine Learning Models by Boris Lublinsky*

![diagram](https://downloads.lightbend.com/website/blog/how-to-serve-machine-learning-models-with-dynamically-controlled-streams/image-2.png)

uses faust kafka streams implementation from robinhood

to run locally you need kafka installed and running then:  

* start faust worker  
```
faust -A model_serving worker -l info
```
* send events to data stream   
```
faust -A model_serving send events '{"some": "data"}'
```
* send model updates to control stream
```
faust -A model_serving send model_updates '{"model_location" : "$MODEL_PATH"}'
```


*[book](https://www.oreilly.com/library/view/serving-machine-learning/9781492024095/), [paper](https://www.lightbend.com/blog/serve-machine-learning-models-dynamically-controlled-streams)

