# This needs to be cleaned up

import sys
import pandas as pd

import boto3
s3 = boto3.client("s3")


def app(environ, start_response):
    # Make sure the file was correctly retrieved from AWS bucket, and catch any errors 
    try:
        # The "Body" key in the response is a StreamingBody object
        body = s3.get_object(Bucket = "reddibot", Key = "sub_data.csv")["Body"]
        # Using the read method on the StreamingBody returns a bytestring, which can be converted back 
        # to unicode
        sub_data = body.read()
        sub_data = sub_data.decode("utf-8")

    except Exception as err:
        
        status = "500"
        
        t = type(err)
        err_msg = f"An Exception of type {t} occurred. Please try again later."
        err_msg = err_msg.encode("utf-8")

        headers = [("Content-Type", "text/plain")]
        start_response(status, headers)
        # Send the error message in the response
        return [err_msg]

    path = environ["PATH_INFO"].strip('/')
    # Give client the option to view the data in 'pretty' form (this is the default)
    if ((path == "pretty") or (path == '')):

        status = "200"

        df = pd.read_csv(sub_data)
        data = str(df).encode("utf-8")
    
        headers = [("Content-Type", "text/plain")]
        start_response(status, headers)

        return [data]
    # Give client the option to view the data in CSV format
    elif (path == "csv"):

        status = "200"
        
        data = sub_data.encode("utf-8")

        headers = [("Content-Type", "text/csv")]
        start_response(status, headers)

        return [data]
    # If the client provided some weird path, they get an error (maybe change this?)
    else:

        status = "400"

        err_msg = "400 BAD REQUEST"
        err_msg = err_msg.encode("utf-8")

        headers = [("Content-Type", "text/plain")]
        start_response(status, headers)

        return [err_msg]
        





