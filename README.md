# UE4Scripts

Skrypty automatyzujce zadania do wykorzystania z Unrealowymi pluginami Python Editor Script Plugin i Editor.
4.19 i wyżej, testowane na 4.20.1, nie gwarantuję że będzie działać w 4.19.

## Cleanupassets

Służy do porządkowania zadanego folderu i sortowania assetów w nim zawartych według klasy.

### Jak tego użyć?

1. Otwierasz w notatniku/Notepad++ (jak cywilizowany człowiek) i zmieniasz 
 * string **folder** tak, żeby wskazywał na folder który chcesz mieć posortowany,
 * string **targetFolder** na folder do którego chcesz mieć wrzucone posortowane assety,
 * opcjonalnie dictionary foldernames, podając jako klucz silnikową nazwę klasy i jako wartość customową nazwę folderu do którego assety tej klasy zostaną wrzucone.
2. Odpalasz edytor, właczasz podane wyżej dwa pluginy, restartujesz edytor, wybierasz File->Execute Python Script i wybierasz cleanupassets.py
