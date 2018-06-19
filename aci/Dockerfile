FROM python:3.6-jessie

WORKDIR /script
ADD . /script

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["python", "script/job_setup.py"]


