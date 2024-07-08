import boto3

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

response = s3_client.list_buckets()

for bucket in response['Buckets']:
    print(bucket['Name'])

my_bucket = s3_resource.Bucket('homework5-s3bucket-kadri')

for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object)

s3_client.delete_object(Bucket='homework5-s3bucket-kadri', Key='Boto3 1.34.104 documentation.pdf')

for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object)

with open('Boto3 1.34.104 documentation.pdf', 'rb') as data:
    s3_resource.Bucket('homework5-s3bucket-kadri').put_object(Key='Boto3 1.34.104 documentation.pdf', Body=data)

for my_bucket_object in my_bucket.objects.all():
    print(my_bucket_object)