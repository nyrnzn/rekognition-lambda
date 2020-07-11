import json
import boto3

def lambda_handler(event, context):
    
    BUCKET = "image-dump-for-rekognition"
    KEY = "test.jpg"
    REGION = "us-east-1"
    FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
    
    for face in detect_faces(BUCKET, KEY, REGION):
		print "Face ({Confidence}%)".format(**face)
		
		# emotions
		for emotion in face['Emotions']:
			print "  {Type} : {Confidence}%".format(**emotion)
			
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def detect_faces(bucket, key, region, attributes=['ALL']):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.detect_faces(
	    Image={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
	    Attributes=attributes,
	)
	return response['FaceDetails']