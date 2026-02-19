# stack-patcher

Composant autonome — exécute un playbook Ansible segmenté legacy/new sur un inventaire fourni en entrée.

## Entrée / Sortie

| | Description |
|---|---|
| Entrée | Contenu brut de `inventory.ini` (paramètre Jenkins multi-line) |
| Exécution | `main.yml` → `legacy.yml` sur `[legacy]`, `new.yml` sur `[new]` |

## Structure du repo

```
stack-patcher/
├── Jenkinsfile    # Job Jenkins
├── main.yml       # Point d'entrée — import legacy.yml + new.yml
├── legacy.yml     # Playbook pour le groupe [legacy]
└── new.yml        # Playbook pour le groupe [new]
```

## Placeholders à remplacer

| Fichier | Placeholder | Description |
|---|---|---|
| `Jenkinsfile` | `YOUR_REGISTRY/ansible-agent:latest` | Image Docker de l'agent |
| `Jenkinsfile` | `REPO_URL` | URL du repo git |
| `Jenkinsfile` | `LEGACY_CREDS_ID` | ID credentials Jenkins legacy |
| `Jenkinsfile` | `NEW_CREDS_ID` | ID credentials Jenkins new |
| `legacy.yml` | tasks | Tâches selon gouvernance legacy |
| `new.yml` | tasks | Tâches selon gouvernance new |
