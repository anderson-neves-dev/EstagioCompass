import boto3

s3 = boto3.client('s3')

with open('app/queries-sql/quereS3Select.sql', 'r') as query:
    queryS3Select = query.read()

response = s3.select_object_content(
    Bucket='basededadossprint5',
    Key='demostrativo_acidentes_riosp_formatado.csv',
    ExpressionType='SQL',
    Expression=queryS3Select,
    InputSerialization = {
        'CSV': {
            'FileHeaderInfo': 'USE', 
            'RecordDelimiter': '\n',
            'FieldDelimiter': ',',
            'QuoteCharacter': '"',        
        }
    },
    OutputSerialization = {'CSV': {}},
)
print('Total de acidentes, total de vítimas ilesas, levemente feridas, moderamente feridas, gravemente feridas, fatalidades, soma total de envolvidos, frase de arredodamento de total envolvídos')
for event in response['Payload']:
    if 'Records' in event:
        records = event['Records']['Payload'].decode('utf-8')
        print(records)
    elif 'Stats' in event:
        statsDetails = event['Stats']['Details']
        print("Stats details bytesScanned: ")
        print(statsDetails['BytesScanned'])
        print("Stats details bytesProcessed: ")
        print(statsDetails['BytesProcessed'])
        print("Stats details bytesReturned: ")
        print(statsDetails['BytesReturned'])
