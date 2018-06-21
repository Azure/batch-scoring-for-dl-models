FROM python:3.6-jessie

WORKDIR /job
ADD /job /job

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "job_setup.py"]


