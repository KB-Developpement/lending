# Copyright (c) 2026, KB Dev and Contributors
# License: GNU General Public License v3. See license.txt
"""Harmonise la terminologie française de l'app lending.

Certaines chaînes (Applicant Name, Collection Offset Sequence…, Loan Demand) sont
traduites par les apps frappe/erpnext (qui priment sur le fr.po de lending). Pour
imposer un vocabulaire cohérent côté UI (Demandeur, Recouvrement/Imputation,
Échéance) sans modifier les fichiers de ces apps, ce patch crée des enregistrements
« Translation » personnalisés (priorité maximale dans Frappe).

Idempotent : ré-exécutable sans effet de bord (mise à jour si déjà présent).
"""

import frappe

FR_TRANSLATIONS = {
	"Applicant Name": "Nom du demandeur",
	"Collection Offset Sequence": "Séquence d'imputation des recouvrements",
	"Collection Offset Sequence for Settlement Collection": "Séquence d'imputation des recouvrements pour le recouvrement de règlement",
	"Collection Offset Sequence for Standard Asset": "Séquence d'imputation des recouvrements pour actif standard",
	"Collection Offset Sequence for Sub Standard Asset": "Séquence d'imputation des recouvrements pour actif sous-standard",
	"Collection Offset Sequence for Written Off Asset": "Séquence d'imputation des recouvrements pour actif passé en abandon de créance",
	"Loan Demand": "Échéance de prêt",
}


def execute():
	if not frappe.db.exists("DocType", "Translation"):
		return

	for source_text, translated_text in FR_TRANSLATIONS.items():
		name = frappe.db.exists(
			"Translation", {"language": "fr", "source_text": source_text}
		)
		if name:
			doc = frappe.get_doc("Translation", name)
			if doc.translated_text != translated_text:
				doc.translated_text = translated_text
				doc.save(ignore_permissions=True)
		else:
			frappe.get_doc(
				{
					"doctype": "Translation",
					"language": "fr",
					"source_text": source_text,
					"translated_text": translated_text,
				}
			).insert(ignore_permissions=True)

	frappe.clear_cache()
