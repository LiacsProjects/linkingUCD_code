# Linking University, City and Diversity.

Het project linking University, Diversity en City heeft tot doel het ontwikkelen van een website te gebruiken door geschiedkundigen 
geinteresseerd naar het verleden van de Leidse universiteit en haar hoogleraren en studenten.

# Website en haar bronnen

De huidige website haalt haar informatie van diverse bronnen. Bericht van de maker van de eerste versie van deze website, Liam van Dreumel:

### Rector magnifici bestanden:

De rector magnifici is niet geverifieerd met het hoogleraren Excel bestand. Ik had wel tijdens het werken aan de lijsten opgemerkt dat er een overlap in zit. 
Meerdere hoogleraren in het Excel bestand zijn doorgestroomd naar de functie van rector. De twee lijsten kunnen daarom ook prima samengevoegd worden tot één. 
Waarbij dan het rectorschap een extra eigenschap kan zijn. Volgens mij was natuurlijk ook al de bedoeling om uiteindelijk hoogleraar, student en rector samen 
te voegen in één visualisatie.

Over de kwaliteit van de bestanden, de Excel bestanden zijn als volgt op te delen:

###	Hoogleraren bestanden: 
Bevat het hoogleraren Excel bestand van LUCD. Deze heb ik zelf verder opgeschoond zodat het beter op de visualisatie paste (denk hierbij aan zaken als het 
standaardiseren van datums en niet verwerkbare datums eruit halen). Vervolgens zijn dataframes per eigenschap gemaakt die in de visualisatie getoond worden. 
De dataframes zijn vervolgens als aparte Excel bestanden geëxporteerd. De reden hiervoor was om per eigenschap het aantal verschijningen per jaar weer te geven 
en ook de daarbij horende eeuw toe te voegen. De data in deze bestanden is dus hetzelfde als die van de hoogleraren en is van dezelfde kwaliteit. Echter: 
enkele datums zijn eruit gehaald of aangepast wanneer deze niet te gebruiken waren. Bijvoorbeeld: waarden als ‘rond 1700’ zijn weggelaten, er is in die gevallen 
dus geen datum beschikbaar. In gevallen waar twee datapunten stonden, bijv: 20-8-1750 / 21-8-1750’, heb ik arbitrair zelf een van de datums gekozen om mee 
verder te gaan. Dit heb ik handmatig gedaan. De kwaliteit van deze sub Excel files is dus iets lager omdat enkele data weggelaten of veranderd is in geval van 
onzekerheid om toch een correcte visualisatie te kunnen doen.

### Studenten bestanden: 
Voor de studenten bestanden is hetzelfde gedaan als bij de hoogleraren.

### Rector bestanden: 
Opnieuw hetzelfde behandeld als de hoogleraren. Het verschil is dat de data van Wikipedia komt. Daarbij moet wel gezegd worden dat de informatie van Wikipedia 
van de website van de Universiteit Leiden lijkt te zijn gehaald. Dit zou nog even gecheckt moeten worden voor de zekerheid maar ik ben dus vrij zeker dat dit 
van hoge kwaliteit is.

### Steden bestanden: 
De steden bestanden bestaan uit 3 uitgebreide Excel-bestanden met geografische informatie. Deze bestanden zijn in de laatste versie die ik heb aangeleverd nog 
niet in gebruikt maar kunnen in de toekomstig als georeference worden gebruikt om de geografische data van de historische personen mee te linken. Elke stad 
bevat latitude en longitude informatie, een korte land code en de bevolkingsgrootte. Het bestand komt van origine van een andere git-repository. Ik kan hierbij 
verder weinig zeggen over de kwaliteit van de informatie.

### JSON .json bestanden: 
Deze zijn te vinden in de /assets/ map. Ze bevatten geografische informatie van landen en zijn gebruikt om als georeference voor de geografische kaarten op de 
website. Ook deze zijn van andere git-repositories gehaald en ik kan verder niets over de kwaliteit zeggen. Dat gezegd hebbende, kijkend naar de geografische 
kaarten lijkt de informatie van alle landen te kloppen. De data van de Excel bestanden wordt goed gelinkt met de wereld kaart, dus lijkt alles te kloppen.

###	Test family bestand: 
Een probeersel dat ik heb gemaakt door wat willekeurige namen te verzinnen. Dit was bedoeld als testbestand om de familiestambomen te testen. 

### BAT en TXT .bat en .txt bestanden: 
Deze bestanden zijn gebruikt om bepaalde csv bestanden op te delen wanneer deze te groot waren. Deze bestanden kunnen verwijderd worden.

### Kleinere studenten bestanden: 
Dit is het student bestand opgedeeld in kleinere bestanden zodat het naar NodeGoat geupload kon worden. Deze zijn verder niet relevant voor de website en kunnen 
verwijderd worden. Een overzicht van alle opschoning activiteiten staat in het ‘data_cleaning.py’ bestand. Dit bestand gebruikt de drie hoofd-Excel bestanden 
(hoogleraren, studenten, rectors), schoont deze op en maakt de extra Excel bestanden aan.
