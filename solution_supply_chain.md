# Solution — Supply Chain Sécurisée

## Problème (R7)
Dépendances et services tiers vulnérables (CVE, licences, intégrité).

## Solution
1. **SBoM** par release (CycloneDX ou équivalent).
2. **Scan CVE** en CI (osv-scanner, pip-audit, trivy).
3. **Signature d’artefacts** (Sigstore/Cosign) et vérification en déploiement.
4. **Politiques licences** (allow/deny) + builds reproductibles (lockfiles).

## Implémentation
- Politique : `supply_chain_policy.yaml`.
- Exemple de workflow : `.github/workflows/security-ci.yml` (scan deps + seuil de blocage).
- Documentation : `why/why_supply_chain.md` pour pédagogie.

## Pourquoi ça fonctionne
- **Visibilité** : SBoM donne l’inventaire réel.
- **Réactivité** : scans CVE automatisés → corrections rapides.
- **Intégrité** : signature empêche la chaîne d’être empoisonnée.