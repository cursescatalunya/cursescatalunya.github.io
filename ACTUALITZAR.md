# Com s'actualitza Curses de Catalunya

La web és estàtica (GitHub Pages). Tot el contingut del calendari és a **`dades.js`**: una cursa per línia dins de `const RACES=[ ... ]`, i la data de l'última revisió a `const UPDATED='AAAA-MM-DD'`. `index.html` només conté el disseny i la lògica; no cal tocar-lo per afegir o canviar curses.

## Format d'una cursa

```json
{"id":"hostrailric","nom":"Hostrailric","esport":"trail","data":"2027-02-21","poble":"Hostalric","comarca":"Selva",
 "web":"https://hostrailric.com/","font":{"nom":"Ultres Catalunya","url":"https://ultrescatalunya.com/calendari-trail-catalunya-2027"},
 "desc":"Cursa de muntanya amb sortida a Hostalric (Selva), amb 2 distàncies de 14 a 24 km.",
 "lat":41.74483,"lng":2.63113,"lloc":"Hostalric, Catalunya","exact":false,
 "mods":[{"nom":"24K","km":24,"dplus":1300,"wikiloc":"https://www.wikiloc.com/trail-running-trails/...-249754757","wl":{"n":"Hostrailric llarga 2026","km":24.6,"up":1194}},
         {"nom":"14K","km":14,"dplus":600}]}
```

- `id`: únic, en minúscules i guions. No canviar el d'una cursa existent (s'usa a l'adreça `#cursa-<id>`).
- `esport`: `trail`, `asfalt`, `btt`, `carretera`, `backyard` o `canicross`.
- `data`: dia de la cursa (`AAAA-MM-DD`). Si una distància es corre un altre dia, posa `"data"` dins d'aquella modalitat.
- `mods`: una entrada per distància. `km` (número o `null` si no se sap), `dplus` (metres o `null`), `hora` (`"HH:MM"`, només si és oficial), `horaPrev:1` si l'hora és d'una edició anterior.
- `wikiloc` + `wl`: track aproximat d'una edició anterior; la web el mostra amb el visor de Wikiloc i un avís de recorregut aproximat. `wl.n` és el títol del track (l'any que contingui es mostra com a edició).
- `provisional:1` quan la data encara no és definitiva. `webTipus:"fitxa"` quan l'enllaç no és la web oficial sinó una fitxa d'informació.
- `lat`/`lng`: punt de sortida aproximat (inici dels tracks o centre del poble). `exact:true` només si és el punt oficial de sortida.

## Regles de qualitat

1. Només curses a Catalunya amb **data confirmada per una font** (web oficial, Ultres Catalunya, federacions, calendaris públics). Res de dates inventades.
2. Si dues fonts no coincideixen, cal una tercera font o la web oficial; si no es pot resoldre, `provisional:1`.
3. No s'inclouen caminades, curses infantils, cros escolars ni curses suspeses.
4. Els tracks de Wikiloc han de ser de la mateixa cursa (nom), sortir a menys de 15 km del poble i tenir una distància i desnivell semblants (±15 % aprox.). Millor els oficials o els més recents.
5. Les curses passades no cal esborrar-les: la web ja amaga les passades del llistat. Es poden treure les que tinguin més de 2 mesos.

## Després de canviar dades.js

Executa `python3 eines/pagines.py`: regenera les pàgines de cada cursa (`cursa/<id>/`), `sitemap.xml` i `robots.txt`, que són les que indexa Google. Fes commit de tot.
