# chained-jobs

Master job qui orchestre `cred-checker` puis `stack-patcher` en séquence.

## Flux

```
vm-patch-chain
    │
    ├─ build(cred-checker, CSV_FILE)
    │       └─ produit repo/output/inventory.ini (artefact)
    │
    ├─ copyArtifacts(cred-checker) → lit inventory.ini en mémoire
    │
    └─ build(stack-patcher, INVENTORY_CONTENT=<contenu inventory.ini>)
```

## Paramètre d'entrée

| Paramètre | Type   | Description                          |
|-----------|--------|--------------------------------------|
| CSV_FILE  | string | Chemin du CSV dans le repo cred-checker (colonne: hostname) |

## Gestion des statuts

| Statut fils  | Comportement master                          |
|--------------|----------------------------------------------|
| SUCCESS      | Continue normalement                         |
| UNSTABLE     | Master passe UNSTABLE, continue              |
| FAILURE      | Master passe FAILURE, chaîne interrompue     |

## Placeholders à remplacer

| Fichier      | Placeholder         | Description                    |
|--------------|---------------------|--------------------------------|
| `Jenkinsfile` | `cred-checker`     | Nom exact du job Jenkins       |
| `Jenkinsfile` | `stack-patcher`    | Nom exact du job Jenkins       |

## Prérequis Jenkins

- Plugin **Copy Artifact** installé
- Les jobs `cred-checker` et `stack-patcher` doivent exister et être accessibles
