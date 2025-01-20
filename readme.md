***to create mapping between docker and current wroking direcotry we neeeed to create a volume and ten the volume maps***
***current direcotry with the container andy changes made to crrent direcotry gets updated to the container as well***
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" smorest-api 
to build docker file
docker build -t smorest-api .

to run the docker file u can do is 
docker run -dp 5000:5000 image name this wont keep track of it remember 
 <!-- or  -->
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" smorest-api  #to run the docker container such that it keeps track of it 
