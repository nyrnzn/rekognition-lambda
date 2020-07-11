import json
import boto3

def lambda_handler(event, context):
    
    BUCKET = "image-dump-for-rekognition"
    KEY_SOURCE = "rajeshhamal1.jpg"
    KEY_TARGET = "downey.jpg"
    REGION = "us-east-1"
    FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
    
    source_face, matches = compare_faces(BUCKET, KEY_SOURCE, BUCKET, KEY_TARGET, REGION)

    # the main source face
    print "Source Face ({Confidence}%)".format(**source_face)
    
    # one match for each target face
    for match in matches:
    	print "Target Face ({Confidence}%)".format(**match['Face'])
    	print "  Similarity : {}%".format(match['Similarity'])
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def compare_faces(bucket, key, bucket_target, key_target, region, threshold=0):
	rekognition = boto3.client("rekognition", region)
	response = rekognition.compare_faces(
	    SourceImage={
			"S3Object": {
				"Bucket": bucket,
				"Name": key,
			}
		},
		TargetImage={
			"S3Object": {
				"Bucket": bucket_target,
				"Name": key_target,
			}
		},
	    SimilarityThreshold=threshold,
	)
	return response['SourceImageFace'], response['FaceMatches']