import faust
import dill as pickle
import random

# initialize kafka running locally
app = faust.App(
    'model-serving',
    broker='kafka://localhost:9092',
)

# create 2 kafka topics
events_topic = app.topic('events', partitions=1)
models_topic = app.topic('model_updates', partitions=1)


# create a table, allows for shared state between stream processors 
model_table = app.Table('model_table',
                        help='Model Serving Info',
                        default=int,
                        partitions=1)

# base model, takes an event, return a very accurate prediction
def model(event):
    return random.random()

# version of the model that the predict stream processor is using
model_version = 0


@app.agent(events_topic)
async def predict(events):
    """
    stream processor that consumes the events topic from kafka and runs predictions
    right now just prints back to stream, but could be hooked up as a component of a longer pipeline

    Args:
        events (iter): generator of event dictionaries 
    """
    global model, model_version

    async for event in events:
        live_version = model_table['live_version']

        # check stream processors model version against live version in shared table
        if model_version != live_version:
            # load in new model if out of sync
            print(f"Loading new model {live_version}")
            model_location = model_table['model_location']
            model = pickle.load(open(model_location, "rb"))
            model_version = live_version

        result = model(event)
        print(f"\nEvent: {event}\nPrediction: {result}")



@app.agent(models_topic)
async def update_model(model_updates):
    """
    stream processor that consumes the model_updates topic from kafka and saves to model_table

    Args:
        model_updates (iter): generator of model_update dictionaries
    """
    async for model_update in model_updates:
        model_location = model_update['model_location']
        print(f"Updating model to: {model_location}")

        model_table['live_version'] += 1
        model_table['model_location'] = model_location

