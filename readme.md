***to create mapping between docker and current wroking direcotry we neeeed to create a volume and ten the volume maps***
***current direcotry with the container andy changes made to crrent direcotry gets updated to the container as well***
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" smorest-api 
to build docker file
docker build -t smorest-api .

to run the docker file u can do is 
docker run -dp 5000:5000 image name this wont keep track of it remember 
 <!-- or  -->
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" smorest-api  #to run the docker container such that it keeps track of it 


pushing any thing to github use these commands 

…or create a new repository on the command line
echo "# python-flask" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Param3504/python-flask.git  //if this shows error fatal: The current branch main has no upstream branch.
To push the current branch and set the remote as upstream, use

    git push --set-upstream origin main
    
that means u have to  execute above line 
git push -u origin main
…or push an existing repository from the command line
git remote add origin https://github.com/Param3504/python-flask.git
git branch -M main
git push -u origin main


<!-- running  dockefile locally  -->

docker run -dp 5000:5000 -w /app -v "$(pwd):/app" imagename  sh -c "flask run --host 0.0.0.0"
