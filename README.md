# scriptie
Bachelor scriptie Informatiekunde

Scoren op Twitter

Tijdens dit onderzoek is gekeken naar de mogelijkheden van het detecteren van deelgebeurtenissen tijdens sportwedstrijden. Deze deelgebeurtenissen zijn kaarten of doelpunten.

De data voor het onderzoek komen uit het Twitter corpus op de karora server van de Rijksuniversiteit Groningen. Deze zijn verzameld per wedstrijd met behulp van de tweet2tab tool, die tevens op de karora server te vinden is. De data per wedstrijd zijn opgeslagen als tekstbestanden met de datum als bestandsnaam.

prefilter.py
In dit programma moeten in de lijst met conditions de elementen aangepast worden per wedstrijd. Als voorbeeld voor de wedstrijd Nederland - Spanje zijn de elementen in de lijst ‘spanje’ ‘nederland’ en ‘#spaned’. Het resultaat hiervan wordt geschreven naar een tekstbestand dat alleen nog wedstrijd-gelateerde tweets bevat.

Annotatie

Nadat de tweets gefilterd zijn er alleen nog wedstrijd-gerelateerde tweets over gebleven zijn, moeten de tweets geannoteerd worden in de klassen ‘relevant’ of ‘irrelevant’. Dit is gedaan door een 0 of een 1 achter de tweet te plaatsen, waar de 0 voor irrelevant staat en de 1 voor relevant. Tevens is het laatste uur van tweets uit het tekstbestand gehaald zodat er alleen tweets overblijven die tijdens de wedstrijd of maximaal een half uur na de wedstrijd geplaatst zijn. Er zijn twee wedstrijden geannoteerd, Spanje - Nederland en Australië - Nederland. Deze geannoteerde data zijn opgeslagen als gameonlyspanedannotated.txt en gameonlyausnedannotated.txt.

Classificatie

De geannoteerde data worden vervolgens als traindata gebruikt in Weka, maar vanwege tijdgebrek en te laag uit vallende scores wordt er verder niet met geclassificeerde tweets gewerkt.

tweetAnalyser.py

Afhankelijk van de wedstrijd moet in het programma het pad naar de de juiste spelerslijst aangepast worden zodat de juiste spelersnamen ingeladen worden.
De annoteerde of (in ideale situatie) geclassificeerde tweets worden vervolgens met een command line argument ingelezen in het programma. Het programma doet vervolgens de rest en geeft als output een overzicht van de wedstrijd.
