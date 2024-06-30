# Dokumentation von bekannten Problemen



## Problem 1: Leerzeichen in Nachrichten



### Beschreibung:

Beim Schreiben einer Nachricht, die Leerzeichen enthält, wird der Nachricht ein zusätzliches " hinzugefügt:


json: {"message":""asfd adsf""}

Dieses Problem entsteht durch die Art und Weise, wie Leerzeichen und andere Sonderzeichen in Nachrichten verarbeitet werden.



## Problem 2: ASCII-Erzwingung

### Beschreibung:

Unicode-Zeichen führen zu unerwarteten Ausgaben. Das System verarbeitet Unicode-Zeichen nicht korrekt, was zu fehlerhaften Darstellungen und möglicherweise zu Abstürzen führt. Es wird daher empfohlen, die Verwendung von ASCII-Zeichen zu erzwingen, um diese Probleme zu vermeiden.
