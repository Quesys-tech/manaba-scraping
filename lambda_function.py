import json
import scraping

def lambda_handler(event, context):
    # TODO implement
    scraping.main()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
