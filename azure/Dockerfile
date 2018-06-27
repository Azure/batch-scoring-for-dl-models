FROM python:3.6-jessie

WORKDIR /job
ADD scripts/create_job.py /job
ADD scripts/util /job/util
ADD requirements.txt /job

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "create_job.py"]


