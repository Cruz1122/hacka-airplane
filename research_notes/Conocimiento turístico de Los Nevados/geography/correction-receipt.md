# Geography correction receipt

Date: 2026-11-21. Section file: `data/knowledge/sections/geography.json`. Quotations: `geography/evidence/quotations-2026-11-21.md`.

## Review findings

1. Artificial examples across the section, including the sampled statements about the valley, the park versus the volcano, and geological heritage.
   Resolution: all 50 entries were rewritten. Examples are short queries, full questions, Colombian spelling, missing accents or typos, and one or two English questions. Authorial lines such as “no es una laguna, es un valle alto”, “un volcán no agota el área protegida”, “reconocimiento del lugar, no un permiso” and “patrimonio de la aplicación” are gone.

2. `geography.geoheritage` mixed source comparison and app-endorsement into the visitor reply.
   Resolution: the short answer is the IUGS recognition since 2022, one of 100 sites, from the September 2024 SGC fact sheet. The 2025 national heritage sentence was re-read on the park page and names Nevado del Ruiz; it stays in `detail`. No app endorsement.

3. `geography.watersheds` listed too many rivers and described the research merge in the default reply.
   Resolution: the short answer names the Cauca and Magdalena basins and a few rivers. The longer membership and the source of each river are in `steps` and `detail`.

4. `geography.park_area` and `geography.santa_isabel_height` asked visitors to hold competing figures.
   Resolution: park area leads with the fact-sheet header, 61,388.24 ha. The history paragraph’s 61,410 ha and CARDER’s 61,410.53 ha on 2026-07-14 are in `detail`, without an average. Santa Isabel leads with the IDEAM summits and their method (South 4,935 m, Central 4,923 m, North/Hongo 4,903 m, SRTM 12.5 and GPS). The SGC single height of 4,965 m from 2024-08-09 stays in the same reply because it is a different kind of measurement, not a second number to memorize without that distinction.

5. Canned contrastive reflections, including the cloudy valley and the line about who owns the water.
   Resolution: reflections were removed from every entry.

6. Scope overlap for geological age, IUGS recognition, glacier summits and Conejeras.
   Resolution: `geography.ruiz_age` keeps the physical ages from the SGC sheet and bulletin and does not answer eruption history. IUGS stays in `geography.geoheritage`. Glacier answers name the three summits the park and IDEAM still associate with ice. Conejeras’ extinction between December 2023 and February 2024 was read on the IDEAM page and was not copied; retreat figures belong to flora. Glacier areas in square kilometres, the 1.82% cover and the 2028 sentence were not copied.

7. SGC fact sheet should be treated as an opened official source.
   Resolution: the September 2024 PDF was downloaded and read. Short quotations are in the evidence file. URLs that were not opened in this pass, including the March 2026 POE, are not cited as retrieved. The fifth proposed sector was removed from the visitor text.

## Sampled entries

| Id | What changed |
|---|---|
| `geography.watersheds` | Two basins in the short answer; full list moved out of the default reply. |
| `geography.park_versus_volcano` | Visitor questions replace thesis-like examples. The short answer says what the park is. |
| `geography.valle_tumbas` | Place, alternate name and the Brisas road. The cloudy-valley reflection is gone. Open stretches are confirmed with the park. |
| `geography.santa_isabel` | Dome complex and three named summits. Heights stay in `geography.santa_isabel_height`. |
| `geography.geoheritage` | IUGS only in the short answer. 2025 national heritage, with Ruiz as the subject, is in `detail`. |

## Counts

- Entries: 50. Target was 70. The gap was not filled.
- Examples: 600, 12 each.
- Schema validation against `inputs/knowledge-section.schema.json`: 0 errors.
- Local contract checks for this section: 0 errors.
- Seeds 11, 13, 14, 19, 22, 23, 34, 36, 39 and 43 still map to the same entry ids.

## Unresolved, and stated as such

- No single official hectare, no named eleventh municipality, no single Santa Isabel or Cisne height, no current Arenas outline, no heights for La Olleta, La Piraña or Nereidas.
- Otún open-water area and a post-2006 source elevation are unpublished in the pages read.
- Laguna Verde’s water altitude, and whether the trail and the ice remnant are the same point, are not settled by the two pages.
- The Gobernación page does not say whether Laguna del Encanto is inside the polygon, and it has no visible publication date. The IDEAM glacier pages also have no visible publication date.
- Department shares other than Risaralda’s 35.6% for Pereira and Santa Rosa de Cabal were not found.
- No current volcanic alert was established. Answers point to the SGC bulletin.

No blocking false number remains in the served answers. The open items are missing or conflicting official figures, not invented ones.
