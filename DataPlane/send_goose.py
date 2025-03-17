import pyiec61850

server = pyiec61850.Server("10.0.0.84") 
goose = pyiec61850.GooseMessage("GOOSE_Publisher")

goose.set_data({
    "GooseID": "TestGOOSE",
    "DatSet": "SampleDataSet",
    "StNum": 1,
    "SqNum": 1,
    "GoCBRef": "IEDName/LLN0$GO$TestGOOSE"
})

server.send_goose(goose)
print("GOOSE message sent.")
