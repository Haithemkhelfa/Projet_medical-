#! /bin/bash
mkdir tempdir
# Copy files to tempdir
cp Projet_Data_Engineering.py tempdir/.
cp clinical_trials.csv tempdir/.
cp drugs.csv tempdir/.
cp pubmed.csv tempdir/.
cp pubmed.json tempdir/.


#Création du fichier Dockerfile 

echo "FROM python" > tempdir/Dockerfile
echo "RUN pip3 install pandas" >> tempdir/Dockerfile
echo "RUN pip3 install json" >> tempdir/Dockerfile
echo "RUN pip3 install re" >> tempdir/Dockerfile
echo "COPY  ./static /home/myapp/static/" >> tempdir/Dockerfile
echo "COPY  ./my_data /home/myapp/my_data/" >> tempdir/Dockerfile
echo "COPY Projet_Data_Engineering.py /home/myapp/" >> tempdir/Dockerfile
echo "EXPOSE 5050" >> tempdir/Dockerfile
echo "CMD python3 /home/myapp/Projet_Data_Engineering.py" >> tempdir/Dockerfile

#Lancement du build de l'image testmedical à partir de Dockerfile sous /tempdir
cd tempdir
docker image build -t testmedical .

#lancement du container  testrunning avec l'image testapp
docker run -t -d -p 5050:5050 --name testproject testmedical

#Tester si le container a bien démarré

docker ps -a
