"""
Module Patients - Interface de gestion des patients
CRUD complet avec CustomTkinter uniquement
"""

import customtkinter as ctk
from typing import Optional, Dict, Any, List
from datetime import datetime, date
from ui_components import StyledTreeview, NotificationDialog, ConfirmationDialog
from clinic_controller import ClinicController


class PatientModule(ctk.CTkFrame):
    """Module de gestion des patients."""
    
    def __init__(self, parent, controller: ClinicController):
        """
        Initialise le module patients.
        
        Args:
            parent: Widget parent
            controller: Contrôleur métier
        """
        super().__init__(parent)
        self.controller = controller
        
        # Variables d'état
        self.current_patient_id: Optional[int] = None
        self.editing_mode: bool = False
        
        # Configuration layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Création des composants
        self._create_main_layout()
        self._create_toolbar()
        self._create_table()
        self._create_form_panel()
        
        # Chargement initial des données
        self.load_patients()
    
    def _create_main_layout(self):
        """Crée la disposition principale."""
        # Frame principal contenant tableau et formulaire
        self.main_container = ctk.CTkFrame(self, fg_color='transparent')
        self.main_container.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.rowconfigure(1, weight=1)
    
    def _create_toolbar(self):
        """Crée la barre d'outils."""
        toolbar = ctk.CTkFrame(self.main_container, height=60, fg_color='#1a1a1a')
        toolbar.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        toolbar.grid_propagate(False)
        
        # Titre
        title_label = ctk.CTkLabel(
            toolbar,
            text="👥 Gestion des Patients",
            font=ctk.CTkFont(size=20, weight='bold')
        )
        title_label.pack(side='left', padx=20, pady=15)
        
        # Boutons d'action
        button_frame = ctk.CTkFrame(toolbar, fg_color='transparent')
        button_frame.pack(side='right', padx=20, pady=10)
        
        self.btn_add = ctk.CTkButton(
            button_frame,
            text="➕ Ajouter",
            width=120,
            height=40,
            corner_radius=8,
            command=self._on_add_click
        )
        self.btn_add.pack(side='left', padx=5)
        
        self.btn_edit = ctk.CTkButton(
            button_frame,
            text="✏️ Modifier",
            width=120,
            height=40,
            corner_radius=8,
            fg_color='#f39c12',
            hover_color='#d68910',
            command=self._on_edit_click,
            state='disabled'
        )
        self.btn_edit.pack(side='left', padx=5)
        
        self.btn_delete = ctk.CTkButton(
            button_frame,
            text="🗑️ Supprimer",
            width=120,
            height=40,
            corner_radius=8,
            fg_color='#e74c3c',
            hover_color='#c0392b',
            command=self._on_delete_click,
            state='disabled'
        )
        self.btn_delete.pack(side='left', padx=5)
        
        self.btn_refresh = ctk.CTkButton(
            button_frame,
            text="🔄 Actualiser",
            width=120,
            height=40,
            corner_radius=8,
            fg_color='#34495e',
            hover_color='#2c3e50',
            command=self.load_patients
        )
        self.btn_refresh.pack(side='left', padx=5)
    
    def _create_table(self):
        """Crée le tableau de données."""
        table_frame = ctk.CTkFrame(self.main_container, fg_color='#1a1a1a')
        table_frame.grid(row=1, column=0, sticky='nsew')
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.rowconfigure(1, weight=1)
        
        # Champ de recherche
        search_frame = ctk.CTkFrame(table_frame, fg_color='transparent')
        search_frame.grid(row=0, column=0, sticky='ew', padx=15, pady=10)
        
        search_label = ctk.CTkLabel(search_frame, text="🔍 Recherche:")
        search_label.pack(side='left', padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nom, sexe, lieu...",
            width=300,
            height=35,
            corner_radius=8
        )
        self.search_entry.pack(side='left', fill='x', expand=True)
        self.search_entry.bind('<KeyRelease>', self._on_search)
        
        # Tableau
        columns = ['ID', 'Nom', 'Sexe', 'Date Naissance', 'Lieu']
        self.table = StyledTreeview(table_frame, columns=columns)
        self.table.tree.column('ID', width=60, anchor='center')
        self.table.tree.column('Nom', width=200, anchor='w')
        self.table.tree.column('Sexe', width=80, anchor='center')
        self.table.tree.column('Date Naissance', width=130, anchor='center')
        self.table.tree.column('Lieu', width=250, anchor='w')
        
        self.table.grid(row=1, column=0, sticky='nsew', padx=15, pady=(0, 15))
        
        # Bind sélection
        self.table.tree.bind('<<TreeviewSelect>>', self._on_selection_change)
        self.table.tree.bind('<Double-1>', self._on_double_click)
    
    def _create_form_panel(self):
        """Crée le panneau de formulaire latéral."""
        self.form_panel = ctk.CTkScrollableFrame(
            self,
            width=350,
            fg_color='#1a1a1a',
            label_text="📝 Formulaire Patient"
        )
        self.form_panel.grid(row=0, column=1, sticky='ns', padx=(10, 20), pady=20)
        
        # Champs du formulaire
        self._create_form_fields()
        
        # Boutons du formulaire
        self._create_form_buttons()
        
        # Masquer initialement
        self.form_panel.grid_remove()
    
    def _create_form_fields(self):
        """Crée les champs du formulaire."""
        padding_opts = {'padx': 20, 'pady': (15, 5)}
        
        # ID (lecture seule, pour modification)
        ctk.CTkLabel(self.form_panel, text="ID:", font=ctk.CTkFont(weight='bold')).pack(**padding_opts)
        self.form_id = ctk.CTkEntry(self.form_panel, state='disabled', width=280)
        self.form_id.pack(padx=20, pady=(0, 10))
        
        # Nom complet
        ctk.CTkLabel(self.form_panel, text="Nom Complet:", font=ctk.CTkFont(weight='bold')).pack(**padding_opts)
        self.form_nom = ctk.CTkEntry(self.form_panel, width=280, placeholder_text="Ex: Jean Dupont")
        self.form_nom.pack(padx=20, pady=(0, 10))
        
        # Sexe
        ctk.CTkLabel(self.form_panel, text="Sexe:", font=ctk.CTkFont(weight='bold')).pack(**padding_opts)
        self.form_sexe = ctk.CTkComboBox(self.form_panel, values=['M', 'F'], width=280)
        self.form_sexe.set('M')
        self.form_sexe.pack(padx=20, pady=(0, 10))
        
        # Date de naissance
        ctk.CTkLabel(self.form_panel, text="Date de Naissance:", font=ctk.CTkFont(weight='bold')).pack(**padding_opts)
        self.form_date = ctk.CTkEntry(self.form_panel, width=280, placeholder_text="YYYY-MM-DD")
        self.form_date.pack(padx=20, pady=(0, 10))
        
        # Lieu de naissance
        ctk.CTkLabel(self.form_panel, text="Lieu de Naissance:", font=ctk.CTkFont(weight='bold')).pack(**padding_opts)
        self.form_lieu = ctk.CTkEntry(self.form_panel, width=280, placeholder_text="Ville, Pays")
        self.form_lieu.pack(padx=20, pady=(0, 20))
    
    def _create_form_buttons(self):
        """Crée les boutons du formulaire."""
        button_frame = ctk.CTkFrame(self.form_panel, fg_color='transparent')
        button_frame.pack(fill='x', padx=20, pady=20)
        
        self.btn_save = ctk.CTkButton(
            button_frame,
            text="💾 Enregistrer",
            width=130,
            height=40,
            corner_radius=8,
            command=self._save_patient
        )
        self.btn_save.pack(side='left', padx=5)
        
        self.btn_cancel = ctk.CTkButton(
            button_frame,
            text="❌ Annuler",
            width=130,
            height=40,
            corner_radius=8,
            fg_color='#95a5a6',
            hover_color='#7f8c8d',
            command=self._close_form
        )
        self.btn_cancel.pack(side='left', padx=5)
    
    def load_patients(self):
        """Charge la liste des patients depuis la base de données."""
        self.table.delete_all()
        
        success, data, error = self.controller.get_patients()
        
        if success:
            for patient in data:
                date_str = str(patient.get('PADN', ''))[:10] if patient.get('PADN') else ''
                self.table.insert((
                    patient.get('IDPA', ''),
                    patient.get('PANP', ''),
                    patient.get('PASX', ''),
                    date_str,
                    patient.get('PALN', '')
                ))
        else:
            NotificationDialog(self, "Erreur", f"Échec du chargement: {error}", "error")
    
    def _on_add_click(self):
        """Gère le clic sur Ajouter."""
        self._open_form()
    
    def _on_edit_click(self):
        """Gère le clic sur Modifier."""
        selected_values = self.table.get_selected_values()
        if not selected_values:
            NotificationDialog(self, "Attention", "Veuillez sélectionner un patient à modifier.", "warning")
            return
        
        self._open_form(edit_mode=True, patient_data={
            'id': selected_values[0],
            'nom': selected_values[1],
            'sexe': selected_values[2],
            'date': selected_values[3],
            'lieu': selected_values[4]
        })
    
    def _on_delete_click(self):
        """Gère le clic sur Supprimer."""
        selected_values = self.table.get_selected_values()
        if not selected_values:
            NotificationDialog(self, "Attention", "Veuillez sélectionner un patient à supprimer.", "warning")
            return
        
        patient_id = selected_values[0]
        patient_nom = selected_values[1]
        
        def on_confirm():
            success, _, error = self.controller.delete_patient(int(patient_id))
            if success:
                NotificationDialog(self, "Succès", f"Patient '{patient_nom}' supprimé avec succès.", "success")
                self.load_patients()
                self._update_button_state()
            else:
                NotificationDialog(self, "Erreur", f"Échec de la suppression: {error}", "error")
        
        ConfirmationDialog(
            self,
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer le patient '{patient_nom}' ?\n\nCette action est irréversible.",
            on_confirm
        )
    
    def _on_selection_change(self, event=None):
        """Gère le changement de sélection dans le tableau."""
        self._update_button_state()
    
    def _on_double_click(self, event=None):
        """Gère le double-clic sur une ligne."""
        self._on_edit_click()
    
    def _on_search(self, event=None):
        """Filtre les résultats de recherche."""
        search_term = self.search_entry.get().lower()
        
        for item in self.table.tree.get_children():
            values = self.table.tree.item(item)['values']
            row_text = ' '.join(str(v).lower() for v in values)
            
            if search_term in row_text:
                self.table.tree.reattach(item, '', 'end')
            else:
                self.table.tree.detach(item)
    
    def _update_button_state(self):
        """Met à jour l'état des boutons selon la sélection."""
        has_selection = self.table.get_selected() is not None
        self.btn_edit.configure(state='normal' if has_selection else 'disabled')
        self.btn_delete.configure(state='normal' if has_selection else 'disabled')
    
    def _open_form(self, edit_mode: bool = False, patient_data: Optional[Dict] = None):
        """Ouvre le panneau de formulaire."""
        self.editing_mode = edit_mode
        self.form_panel.grid()
        
        if edit_mode and patient_data:
            self.current_patient_id = int(patient_data['id'])
            self.form_id.insert(0, str(patient_data['id']))
            self.form_nom.insert(0, patient_data['nom'])
            self.form_sexe.set(patient_data['sexe'])
            self.form_date.insert(0, patient_data['date'])
            self.form_lieu.insert(0, patient_data['lieu'])
        else:
            self._clear_form()
    
    def _close_form(self):
        """Ferme le panneau de formulaire."""
        self._clear_form()
        self.form_panel.grid_remove()
    
    def _clear_form(self):
        """Réinitialise le formulaire."""
        self.current_patient_id = None
        self.editing_mode = False
        
        self.form_id.delete(0, 'end')
        self.form_nom.delete(0, 'end')
        self.form_sexe.set('M')
        self.form_date.delete(0, 'end')
        self.form_lieu.delete(0, 'end')
    
    def _validate_form(self) -> tuple:
        """Valide les données du formulaire."""
        nom = self.form_nom.get().strip()
        sexe = self.form_sexe.get()
        date_str = self.form_date.get().strip()
        lieu = self.form_lieu.get().strip()
        
        if not nom:
            return False, None, "Le nom est obligatoire."
        
        if not date_str:
            return False, None, "La date de naissance est obligatoire."
        
        try:
            date_naissance = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return False, None, "Format de date invalide. Utilisez YYYY-MM-DD."
        
        if not lieu:
            return False, None, "Le lieu de naissance est obligatoire."
        
        return True, {
            'nom': nom,
            'sexe': sexe,
            'date': date_naissance,
            'lieu': lieu
        }, ""
    
    def _save_patient(self):
        """Enregistre le patient (ajout ou modification)."""
        valid, data, error = self._validate_form()
        
        if not valid:
            NotificationDialog(self, "Validation", error, "warning")
            return
        
        if self.editing_mode and self.current_patient_id:
            # Modification
            success, _, error = self.controller.update_patient(
                self.current_patient_id,
                data['nom'],
                data['sexe'],
                data['date'],
                data['lieu']
            )
            
            if success:
                NotificationDialog(self, "Succès", "Patient modifié avec succès.", "success")
                self._close_form()
                self.load_patients()
            else:
                NotificationDialog(self, "Erreur", f"Échec de la modification: {error}", "error")
        else:
            # Ajout
            success, new_id, error = self.controller.add_patient(
                data['nom'],
                data['sexe'],
                data['date'],
                data['lieu']
            )
            
            if success:
                NotificationDialog(self, "Succès", f"Patient ajouté avec succès (ID: {new_id}).", "success")
                self._close_form()
                self.load_patients()
            else:
                NotificationDialog(self, "Erreur", f"Échec de l'ajout: {error}", "error")
