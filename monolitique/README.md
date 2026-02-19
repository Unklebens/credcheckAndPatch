# vm credchecker

Composant réutilisable Jenkins/Ansible pour identifier automatiquement le credential d'un parc de VM et déclencher le bon playbook de patch.

## Architecture — deux jobs indépendants

```
┌─────────────────────────────────────────────────────────┐
│  JOB 1 : cred-checker                                   │
│                                                         │
│  agent docker                                           │
│      │                                                  │
│      ├─ git clone <REPO_URL>                            │
│      ├─ csv-to-inventory.py  →  output/all-hosts.ini   │
│      ├─ cred-checker.yml                               │
│      │       ├─ test credential legacy                  │
│      │       ├─ test credential new                     │
│      │       ├─ forge output/inventory.ini              │
│      │       └─ forge output/stack-patch.yml            │
│      └─ archiveArtifacts ──────────────────────────┐   │
└────────────────────────────────────────────────────│───┘
                                                     │ Copy Artifact plugin
┌────────────────────────────────────────────────────│───┐
│  JOB 2 : stack-patcher                             │   │
│                                                     ▼   │
│  agent docker                                           │
│      │                                                  │
│      ├─ git clone <REPO_URL>                            │
│      ├─ copyArtifacts(cred-checker)                     │
│      │       output/inventory.ini                       │
│      │       output/stack-patch.yml                     │
│      └─ ansible-playbook output/stack-patch.yml         │
│              -i output/inventory.ini                    │
└─────────────────────────────────────────────────────────┘
```

## Fichiers

```
vm credchecker/
├── Jenkinsfile.cred-checker      # Job 1
├── Jenkinsfile.stack-patcher     # Job 2
├── hosts.csv                     # Source VM (hostname, ip)
├── csv-to-inventory.py           # CSV → inventaire [all]
├── cred-checker.yml              # Playbook de détection
├── templates/
│   ├── inventory.ini.j2          # Template inventaire segmenté
│   └── stack-patch.yml.j2        # Template playbook forgé
├── playbooks/
│   ├── patch-legacy.yml          # À compléter selon gouvernance legacy
│   └── patch-new.yml             # À compléter selon gouvernance new
└── output/                       # Généré à l'exécution (gitignore)
```

## Placeholders à remplacer

| Fichier                        | Placeholder                  | Description                        |
|-------------------------------|------------------------------|------------------------------------|
| Jenkinsfile.cred-checker       | `REPO_URL`                   | URL du repo git credchecker        |
| Jenkinsfile.cred-checker       | `your-registry/ansible-agent`| Image Docker de l'agent Jenkins    |
| Jenkinsfile.cred-checker       | `LEGACY_CREDS_ID`            | ID credentials Jenkins legacy      |
| Jenkinsfile.cred-checker       | `NEW_CREDS_ID`               | ID credentials Jenkins new         |
| Jenkinsfile.stack-patcher      | `REPO_URL`                   | Même repo                          |
| Jenkinsfile.stack-patcher      | `your-registry/ansible-agent`| Même image agent                   |
| Jenkinsfile.stack-patcher      | `LEGACY_CREDS_ID`            | Même ID credentials legacy         |
| Jenkinsfile.stack-patcher      | `NEW_CREDS_ID`               | Même ID credentials new            |
| Jenkinsfile.stack-patcher      | `CRED_CHECKER_JOB`           | Nom exact du job cred-checker      |

## Prérequis Jenkins

- Plugin **Copy Artifact** installé (pour la récupération des artefacts entre jobs)
- Plugin **Docker Pipeline** pour les agents conteneurisés
- Credentials de type **Username with Password** créés dans Jenkins

## CSV source

```csv
hostname,ip
srv-legacy-01,10.0.1.11
srv-new-01,10.0.2.21
```

## Sécurité

- Les credentials sont injectés via `credentials()` Jenkins — jamais en clair.
- `output/` est dans `.gitignore`.
