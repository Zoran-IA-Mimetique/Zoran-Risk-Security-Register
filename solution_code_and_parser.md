# Solution — Code & Parser Sécurisés

## Problème (R1, R4, R5)
- **Injection glyphique** via flux `.zgs`/HyperGlottal mal validés (R1).
- **Exécution non sandboxée** dans l’interpréteur (R4 indirect).
- **DoS par complexité** si entrées récursives non bornées (R5).

## Solution
1. **Validation stricte des entrées** (schémas JSON/YAML + tailles/forme).
2. **Parser “safe”** (éviter `eval`, interdire fonctions dangereuses).
3. **Sandbox** (process isolé/contenerisé, quotas CPU/RAM/temps).
4. **Timeouts & quotas** (défense anti-DoS).

## Implémentation
- Exemple opérationnel dans `main.py` : `safe_parser()` + `RollbackGuard` (ΔM11.3).
- Gabarit de validation JSON (exemple minimal) :

```json
{
  "type": "object",
  "required": ["hdr","payload"],
  "properties": {
    "hdr": { "type": "object" },
    "payload": { "type": "object" }
  },
  "additionalProperties": false
}
```

> Astuce : faire la **validation structurelle** (types/champs) même sans moteur JSON Schema → en Python, vérifier explicitement `dict`, présence de clés, tailles max, etc.

## Pourquoi ça fonctionne
- **Réduction de surface d’attaque** (pas d’exécution implicite).
- **Défense en profondeur** (validation + sandbox + quotas).
- **Prévention de paralysie ΔM11.3** (guard + backoff).