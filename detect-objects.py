import json
import boto3

def lambda_handler(event, context):
    
    BUCKET = "image-dump-for-rekognition"
    KEY = "cat-and-dog.jpg"
    
    #response = detect_labels(BUCKET, KEY)
    
    for label in detect_labels(BUCKET, KEY):
	    print "{Name} - {Confidence}%".format(**label)
	
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


def detect_labels(bucket, key, max_labels=10, min_confidence=90, region="us-east-1"):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_labels(
		Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		MaxLabels=max_labels,
		MinConfidence=min_confidence,
	)
	return response['Labels']
