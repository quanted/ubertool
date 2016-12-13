FROM python:2

# Install Python Dependencies
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

COPY . /src/
WORKDIR /src

CMD ["nose2", "--with-cov"]