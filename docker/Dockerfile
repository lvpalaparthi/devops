#Javascript
FROM node:8.16.1-alpine
WORKDIR /app
COPY package.json /app
RUN npm install
EXPOSE 5000
COPY . /app
CMD node index.js


#ENTRYPOINT ["node", "index.js"]
#COPY package.json /app


#Python
FROM python:alpine3.10
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
#moving copy folder improves layer caching 
COPY . /app
CMD python ./launch.py

#COPY requirements.txt /app/requirements.txt
#ENTRYPOINT ["python", "./launch.py"]


#Java 
FROM maven:3.6.3-jdk-8-slim AS stage1
WORKDIR /home/app
COPY . /home/app
RUN mvn -f /home/app/pom.xml clean package

#create an inage 
FROM openjdk:8-jdk-alpine 
EXPOSE 5000
COPY --from=stage1 /home/app/target/hello-world-java.jar hello-world-java.jar
#launches java application 
ENTRYPOINT ["sh", "-c", "java -jar /hello-world-jar.jar"]