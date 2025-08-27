# Solution — Protection des Données (RGPD)

## Problème (R3, R8, R11)
- **Fuite de fragments mémoire** (ZDM) et non-respect des droits (R3).
- **Maintenance hasardeuse** (R8) et **mauvaises configs** (R11).

## Solution
1. **Pseudonymisation** systématique des identifiants (`email`, `tel`, `id`).
2. **TTL** (durées de conservation) appliqué par politique.
3. **Journalisation immuable** des accès/modifications (Merkle).
4. **API Droit à l’oubli** (`/delete_fragment`) — suppression sélective.

## Implémentation (stdlib)
- Voir `rgpd_tools.py` : `pseudonymize()`, `mask()`, `enforce_ttl()`.
- Journal Merkle : `merkle_demo.py` (chaînage et vérification).

## Pourquoi ça fonctionne
- **Minimisation** → on réduit l’exposition réelle.
- **Traçabilité** → on prouve les actions (audit).
- **Conformité** → mécanismes concrets RGPD (TTL, oubli).