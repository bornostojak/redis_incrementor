# Docker Swarm redis incrementor project
___
Cilj projekta:
- Zadatak (1) => stvoriti docker image u proizvoljnom jeziku koji inkrementira kljuc u redisu
- Zadatak (2) => deploy-ati navedeni image u swarm i scale-ati ga na 10 instanci
- Zadatak (3) => usporediti performanse na zadatke (1) i (2)

## Zadatak 1
Zadatak 1 pisan je u python-u koristeci flask i flask_restful framework. Napravio sam jednostavni web servis koji posjetom stranicu inkrementira brojač i vrati vrijednost.
Ako pak želimo resetirati brojac, to mozemo uciniti posjetom na adresu `/reset`, što resetira brojač i vari njegovo trenutno (resetirano) stanje.
Želimo li vidjeti stanje brojaca bez da ga inkrementiramo ili resetiramo, to možemo učiniti posjetom na `/counter`.

## Zadatak 2
Projek je testiran kreiranje docker swarma na 1 i na 2 odvojena računala na istoj lokalnoj mrezi.
Obzirom da sam imao neke probleme u pocetku pokusavajuci stovriti docker swarm između vm-a i laptopa, deployao sam docker swarm koristeci iduci naredbu:
`docker stack deploy -c docker-compose-deploy-stack.yml incr`

Alternativno bih kreirao zajednicku backend mrezu
`docker network create --driver overlay backend`

Te unutar iste dodado dvije odvojene instance, prvo *redis* a zatim *incrementor*
`docker service create --name redis --network backend -p 6379:6379 redis:6.2.6-alpine`
`docker service create --name incrementor --network backend -p 80:8080 -e REDIS_SERVER=redis bornostojak/incrementor:0.1.2`

Kako bih skalirao broj *incrementor* instanci na 10
`docker service scale incrementor=10`

*PITANJE: Da li 10 instanci znaci 10x vece performanse?*
ODGOVOR: NE. Ovisno o alikaciji skaliranje aplikacije može utjecati na njezine performanse. *Ovjde to nije sličuaj*, barem ne pod okolnostima pod kojima sam ja vodio testiranja, ali nam skaliranje u swarmu omogućava redundanciju i **load balancing** kako bi mogli istovremeno usluživati veći broj korisnika brže i nesmetano.

## Zadatak 3

