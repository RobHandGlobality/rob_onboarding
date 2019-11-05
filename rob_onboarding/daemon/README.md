Notes on steps to running daemon locally to test handler

Setup some needed data in local service
```
http POST http://localhost:5000/api/v1/order customerId=73daf342-572b-4ade-99df-77ed5d0fa16e 
http POST http://localhost:5000/api/v1/order_event orderId=dfbaeeb1-2d06-441e-90e5-be63d0b51cae eventType=PizzaCreated
http POST http://localhost:5000/api/v1/order_event orderId=dfbaeeb1-2d06-441e-90e5-be63d0b51cae eventType=PizzaToppingAdded
http POST http://localhost:5000/api/v1/order_event orderId=dfbaeeb1-2d06-441e-90e5-be63d0b51cae eventType=PizzaCustomizationFinished
http POST http://localhost:5000/api/v1/order_event orderId=dfbaeeb1-2d06-441e-90e5-be63d0b51cae eventType=OrderDeliveryDetailsAdded
http POST http://localhost:5000/api/v1/order_event orderId=dfbaeeb1-2d06-441e-90e5-be63d0b51cae eventType=OrderSubmitted
http GET http://localhost:5000/api/v1/order_event order_id=dfbaeeb1-2d06-441e-90e5-be63d0b51cae
http GET http://localhost:5000/api/v1/order_event/7536a474-eacf-45a5-8a2e-fb2579e8ce01
```

Take order_event.id from last response to craft the message.json which will be supplied to handler

Create a fake sqs message for given resource:
```
$ publish-naive --action created --resource=DeliveryEvent.PizzaDelivered --uri "http://localhost:5000/api/v1/order_event/906e7799-3d99-41f0-9174-155f98be4547" > message.json
```
Attempt to run daemon with above message:
```
$ cd daemon
$ chmod +x main.py
$ python main.py --debug --sqs-queue-url ./message.json --envelope NaiveSQSEnvelope 
```