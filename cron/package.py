
import os, subprocess, argparse, zipfile, shutil, io
import boto3

def files_to_zip(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            archive_name = full_path[len(path) + len(os.sep):]
            yield full_path, archive_name

def makeZipFileBytes():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as z:
        path = os.path.dirname(os.path.realpath(__file__))
        for full_path, archive_name in files_to_zip(path=path):
            z.write(full_path, archive_name)
    return buf.getvalue()

def updateLambda():
    aws_lambda = boto3.client('lambda')
    aws_lambda.update_function_code(
        FunctionName="luath-checker",
        ZipFile=makeZipFileBytes(),
        Publish=True
    )

if __name__ == "__main__":
    try:
        print "Updating Lambda function..."
        updateLambda()
    finally:
        print "Done"
