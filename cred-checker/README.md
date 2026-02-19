# cred-checker

Composant autonome — détecte le credential SSH valide pour chaque host d'un CSV et produit un inventaire Ansible segmenté.

## Entrée / Sortie

| | Fichier | Format |
|---|---|---|
| Entrée | `hosts.csv` | CSV, colonne unique `hostname` |
| Sortie | `output/inventory.ini` | Inventaire Ansible `[legacy]` / `[new]` |

## Comportement

- Le DNS interne résout les hostnames — aucune IP dans le CSV ni dans l'inventaire.
- Credential legacy testé en premier, new en second.
- Host sans credential valide : loggué, commenté dans l'inventaire, job en **UNSTABLE** (pas FAILURE).
- Aucun credential (user/password) dans l'inventaire produit.

## Placeholders à remplacer

| Fichier | Placeholder | Description |
|---|---|---|
| `Jenkinsfile` | `YOUR_REGISTRY/ansible-agent:latest` | Image Docker de l'agent |
| `Jenkinsfile` | `REPO_URL` | URL du repo git |
| `Jenkinsfile` | `LEGACY_CREDS_ID` | ID credentials Jenkins legacy |
| `Jenkinsfile` | `NEW_CREDS_ID` | ID credentials Jenkins new |
