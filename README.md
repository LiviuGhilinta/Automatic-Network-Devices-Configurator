**EasyConfig** este o aplicatie web conceputa pentru automatizarea si configurarea statica mult mai rapida a interfetelor dispozitivelor dintr-o topologie de retea(routere, PC-uri si switch-uri)



!!! **Important** !!! Aceasta aplicatia a fost dezvolatata si optimizata exclusiv pentru simulatorul GNS3.



**Scop**: Simplifica procesul de alocare statica a adreselor IP prin interfata web, scutind utilizatorul de folosirea Command Line.

Permite configurarea simultana a mai multor dispozitive in acelasi timp.



**Tehnlogii utilizate**:

Python 3: Pentru logica din backend a aplicatiei web(Django), dar si pentru conectarea si prelucrarea datelor de la API-ul GNS3(modul: netmiko)

PostgreSQL: Pentru stocarea informatiilor preluate de la API: proiecte, dispozitive prezente in proiect si interfetele acestora, disponibile pentru configurare.

Docker & Docker Compose: Containerizarea completa a microserviciilor.



Containere:

1. **Container pentru baza de date** : Ruleaza o instanta oficiala PostgreSQL unde sunt salvate starile retelei si datele aplicatiei.

2. **Container web** : Ruleaza intreaga aplicatie web cu tot cu sistemele de automatizare.





Ghid de utilizare(in Terminal):

1. Porneste containerele:

**docker-compose up**

2. Deschide migrarile pentru baza de date:

**docker-compose exec web python manage.py migrate**

3. Creazati un cont de utilizator:

**docker-compose exec web python manage.py createsuperuser**
