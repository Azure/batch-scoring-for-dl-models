import logging
import azure.functions as func

import azure.mgmt.batchai.models as models
import azure.mgmt.batchai as batchai


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
