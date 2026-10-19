# Cahier des charges — Gestion des commissions d'un dessinateur

**Client :** illustrateur indépendant
**Plateforme :** Odoo 19 Community
**Modules livrés :** `art_commission`, `art_commission_account`

---

## 1. Contexte

L'artiste reçoit aujourd'hui ses demandes de commission par DM et par mail. Il perd le fil des
négociations, oublie des deadlines et facture à la main. Il veut :

- que ses clients soumettent et suivent leurs demandes eux-mêmes depuis un **portail** ;
- **accepter**, **refuser** ou **proposer un prix plus élevé, avec une argumentation** ;
- une facture générée automatiquement à la livraison ;
- que le fichier final ne soit téléchargeable **qu'une fois la facture payée**.

## 2. Profils utilisateurs

| Profil | Type | Droits |
|---|---|---|
| **Artiste** | Utilisateur interne, groupe `Commissions / Artiste` | Accès complet : demandes, grille tarifaire, configuration |
| **Client** | Utilisateur portail (`base.group_portal`) | Ne voit **que ses propres** demandes. Crée une demande, répond aux propositions de prix, télécharge ses fichiers |

## 3. Données

### 3.1 Grille tarifaire
- **Type de commission** (`art.commission.type`) : nom (unique), prix de base (> 0), description, actif.
  Exemples : Sketch, Lineart, Couleur, Illustration complète.
- **Option / supplément** (`art.commission.option`) : nom (unique), prix supplémentaire (≥ 0).
  Exemples : Fond détaillé, Personnage supplémentaire, Usage commercial.

### 3.2 Demande de commission (`art.commission`)
- Référence auto (séquence, ex. `COM/2026/0001`)
- Client (`res.partner`), titre, description du besoin
- Type (obligatoire), options (plusieurs)
- **Prix calculé** = prix de base + somme des options (compute, non stocké manuellement)
- **Prix convenu** : initialisé au prix calculé, mis à jour quand une hausse est acceptée
- Date limite souhaitée
- Acceptation des conditions : case cochée + date/heure d'acceptation (lecture seule, preuve)
- Images de référence (pièces jointes)
- Fichier final (pièce jointe protégée)
- État, chatter (suivi des changements d'état et de prix)

### 3.3 Proposition de prix (`art.commission.price.proposal`)
- Commission liée, nouveau prix, argumentation (obligatoire), état (en attente / acceptée / refusée), date.

## 4. Cycle de vie

```
            ┌──────────── refuser ───────────► Refusée
            │
 Nouvelle ──┼── accepter ──► Acceptée ── démarrer ──► En cours ── livrer ──► Livrée
            │                    ▲
            └── proposer prix ──► En négociation
                                 │  client accepte → prix convenu mis à jour → Acceptée
                                 └  client refuse  → Annulée
```

- Le client peut annuler sa demande tant qu'elle est **Nouvelle** ou **En négociation**.
- Une demande **Livrée / Refusée / Annulée** n'est plus modifiable.

## 5. Règles métier

1. **File d'attente max** : paramètre configurable (Réglages, défaut 5). L'artiste ne peut pas
   accepter une demande si le nombre de demandes *Acceptées + En cours* atteint la limite.
2. **Prix** : prix de base > 0, supplément ≥ 0 ; une proposition doit être **strictement
   supérieure** au prix convenu actuel ; l'argumentation est obligatoire.
3. **Une seule proposition en attente** à la fois par commission.
4. **Conditions** : impossible de soumettre une demande sans accepter les conditions
   (pas de contenu interdit, droits d'usage, délais). La date d'acceptation est enregistrée.
5. Impossible de supprimer une demande qui n'est pas *Nouvelle* ou *Annulée*.

## 6. Portail client (module `portal`)

- Page « Mes commissions » : liste + détail de chaque demande (état, prix, historique).
- Formulaire de nouvelle demande : type, options, description, deadline, images de référence,
  case des conditions.
- Boutons **Accepter / Refuser** sur une proposition de prix en attente.
- Téléchargement du fichier final **si et seulement si** la facture liée est payée.

## 7. Communication (module `mail`)

- Chatter sur la demande, suivi des champs état et prix convenu.
- Email au client quand l'artiste fait une proposition (contient le nouveau prix et l'argumentation).
- Email au client en cas de refus et de livraison.

## 8. Facturation (module `art_commission_account`)

- Dépend de `art_commission` et `account`.
- Au passage en **Livrée**, création automatique d'une facture client :
  une ligne pour le type, une ligne par option (ou une ligne au prix convenu si une hausse a été acceptée).
- Lien facture ↔ commission, visible depuis la demande.

## 9. Exigences de sécurité

- **ACL** (`ir.model.access.csv`) pour chaque modèle et chaque groupe. Aucun modèle sans ACL.
- **Record rules** portail : un client ne lit que les demandes dont il est le partenaire
  (via son partenaire commercial).
- Le client portail **ne peut jamais** modifier le prix, l'état ou le partenaire directement :
  toutes les actions portail passent par des contrôleurs qui **vérifient la propriété** du
  document et **valident chaque champ** côté serveur.
- `sudo()` seulement après ces vérifications, et le plus localement possible.
- **Uploads** : images seulement (png, jpg, webp) détectées par le **contenu** du fichier et non
  par son extension ; 5 fichiers max, 5 Mo max chacun.
- Fichier final : servi par un contrôleur qui vérifie propriétaire **et** état de paiement.
- Protection CSRF active sur tous les formulaires.

## 10. Backend

- Menu **Commissions** : Demandes | Configuration (Types, Options, Réglages).
- Vue **kanban** des demandes groupée par état (vue par défaut), plus vues liste et formulaire.
- Boutons d'action dans le header du formulaire, visibles selon l'état.

## 11. Critères d'acceptation

- [ ] Un client portail crée une demande, la voit dans son portail, et ne voit **aucune** demande d'un autre client (même en modifiant l'ID dans l'URL).
- [ ] L'artiste propose une hausse ; le client reçoit un email, accepte ; le prix convenu est mis à jour.
- [ ] Accepter une 6ᵉ demande avec la limite à 5 affiche une erreur claire.
- [ ] La livraison crée une facture correcte ; le fichier n'est téléchargeable qu'après paiement.
- [ ] Un fichier `.exe` renommé en `.png` est refusé à l'upload.
- [ ] Les modules s'installent et se désinstallent proprement sur une base vierge.
