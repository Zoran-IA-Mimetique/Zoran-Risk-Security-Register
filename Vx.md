# V(x) — Fonction de potentiel de risque Zoran

**Objet** : définir une fonction continue et bornée qui transforme un vecteur de facteurs de risque **x** en un **score 0–100**, utilisable pour la priorisation (runbooks, SLA, CI/CD sécurité).

---

## 1. Définition

On note **x = {p, I, E, X, v, R, H, D, K, C}**, où :

- **p** ∈ [0,1] : probabilité d’occurrence (likelihood).  
- **I** ∈ [0,10] : impact brut (technique + métier + conformité).  
- **E** ∈ [0,10] : exploitabilité (simplicité technique, outils publics).  
- **X** ∈ [0,10] : exposition (surface, périmètre, dépendances).  
- **v** ∈ [0,10] : vélocité d’exploitation (rapidité/automatisation d’attaque).  
- **R** ∈ [0,10] : sensibilité **ΔM11.3** (risque de rollbacks en boucle / paralysie).  
- **H** ∈ [0,10] : sévérité **éthique** (biais, manipulation, atteinte aux droits).  
- **D** ∈ [0,10] : **détectabilité** (plus c’est détectable, plus le risque réel baisse).  
- **K** ∈ [0,10] : **efficacité des contrôles** (préventifs/détectifs/correctifs).  
- **C** ∈ [0,1] : **confiance** dans l’estimation (incertitude).

---

## 2. Formule (par défaut, multiplicative normalisée)

On combine multiplicativement les facteurs aggravants et divisivement les facteurs atténuants, puis on normalise avec une constante d’échelle **s** (par défaut 50) :

```
Raw = ( (p * I) * (1 + E/10) * (1 + X/10) * (1 + v/10) * (1 + R/10) * (1 + H/10) )
      / ( (1 + D/10) * (1 + K/10) )

V(x) = 100 * Raw / (Raw + s)           # score borné 0–100
V_conf(x) = V(x) * (0.5 + 0.5*C)       # pénalise l’incertitude (C∈[0,1])
```

- **Intuition** : si **D** (détectabilité) et **K** (contrôles) montent, le risque baisse.  
- **Bornage** : plus **Raw** croît, plus **V(x)** tend vers 100, sans explosion.  
- **Confiance** : si C=0.6 → V_conf = 0.8·V (pénalité douce).

> Paramètre `s` ajustable par domaine (santé/justice → `s=30` ; interne R&D → `s=70`).

---

## 3. Cartographie R1→R12 (risk_register.yaml → x)

| ID | Risque | Param par défaut (exemple) |
|----|--------|----------------------------|
| R1 | Injection glyphique | E=9, X=8, v=8, D=4, K=5 |
| R2 | Rollback forcé ΔM11.3 | R=9, I=8, v=7, K=4 |
| R3 | Fuite mémoire ZDM | I=9, X=7, D=3, K=5, H=6 |
| R4 | Adversarial modèles | p=0.5, I=7, E=8, K=5 |
| R5 | DoS complexité | p=0.6, I=6, X=7, D=6, K=6 |
| R6 | Empoisonnement parasitique | p=0.4, I=7, X=8, D=5 |
| R7 | Supply chain | p=0.5, I=8, X=9, K=5 |
| R8 | Maintenance/patch | p=0.6, I=6, v=6, K=6 |
| R9 | Accès physique | I=8, X=6, D=5, K=7 |
| R10| Ingénierie sociale | p=0.7, I=7, v=8, D=4, K=5 |
| R11| Mauvaise configuration | p=0.6, I=7, X=7, K=5 |
| R12| Documentation obsolète | p=0.5, I=5, K=6 |

Ces valeurs sont **seulement des seeds** : elles doivent être ajustées par contexte et retour d’expérience.

---

## 4. Exemple chiffré (R1 — Injection glyphique)
Hypothèses : `p=0.65, I=8, E=9, X=8, v=8, R=6, H=4, D=4, K=5, C=0.7, s=50`

```
Raw ≈ ((0.65*8)*(1+0.9)*(1+0.8)*(1+0.8)*(1+0.6)*(1+0.4)) / ((1+0.4)*(1+0.5))
    ≈ (5.2 * 1.9 * 1.8 * 1.8 * 1.6 * 1.4) / (1.4 * 1.5)
    ≈ (5.2 * 13.2576) / 2.1 ≈ 32.269 / 2.1 ≈ 15.37

V(x) = 100 * 15.37 / (15.37 + 50) ≈ 23.5
V_conf(x) = 23.5 * (0.5 + 0.5*0.7) = 23.5 * 0.85 ≈ 20.0 / 100
```

Interprétation : **Risque moyen-élevé** justifiant une mitigation prioritaire (parser strict + sandbox + WAF).

---

## 5. Seuils & décisions (runbooks)
- **V < 20** : Surveiller (log only)  
- **20 ≤ V < 40** : Corriger en sprint (< 30 j)  
- **40 ≤ V < 60** : Correction prioritaire (< 7 j)  
- **V ≥ 60** : **Bloquant CI/CD** (déploiement refusé) + correctif immédiat

---

## 6. Implémentation (voir `vx.py`)
- Entrée : JSON avec clés `{p,I,E,X,v,R,H,D,K,C,s}`.  
- Sortie : score `V`, score ajusté `V_conf`, et décomposition `Raw`.  
- Intégration : job CI qui lit `risk_register.yaml`, mappe R1→R12 vers **x**, calcule V(x), et échoue si seuil dépassé.

---

## 7. Notes éthiques
Le composant **H** (sévérité éthique) n’est **pas un gadget** : toute atteinte aux droits fondamentaux **majorera** V(x).  
Il est recommandé de documenter dans `EthicChain` la justification de **H** et les mesures de réduction (transparence, audit biais).

---

## 8. Licence
MIT — libre usage. Mention requise : Zoran aSiM.