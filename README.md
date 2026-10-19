# Art Commission

Odoo 19.0 — gestion des demandes de commission d'un dessinateur (portail, négociation de prix, facturation).

## Install

Run from the projects directory (`~/workspace/niboo`):

```bash
install_project.sh git@github.com:NIBOO-AKI/ART.git addons-art develop ART
```

## Update

```bash
cd ~/workspace/niboo/ART/addons-art
update_project.sh develop
```

## Run

```bash
cd ~/workspace/niboo/ART
bin/python odoo/odoo-bin -c etc/odoo.cfg -d art -i art_commission -u art_commission --dev=xml
```

