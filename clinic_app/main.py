"""
Application principale - Clinic Management System
Point d'entrée de l'application avec navigation et gestion des modules
"""

import customtkinter as ctk
import sys
import os

# Ajout du chemin pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_manager import DatabaseManager
from clinic_controller import ClinicController
from ui_components import LoadingScreen, NotificationDialog
from module_patients import PatientModule


class ClinicApp(ctk.CTk):
    """Application principale de gestion clinique."""
    
    def __init__(self):
        """Initialise l'application."""
        super().__init__()
        
        # Configuration de la fenêtre principale
        self.title("🏥 Clinic Management System")
        self.geometry("1400x900")
        self.minsize(1200, 800)
        
        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables d'état
        self.db_manager: DatabaseManager = None
        self.controller: ClinicController = None
        self.current_module = None
        
        # Configuration grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Affichage de l'écran de chargement
        self._show_loading_screen()
    
    def _show_loading_screen(self):
        """Affiche l'écran de chargement initial."""
        self.loading = LoadingScreen(self, "Démarrage de l'application...")
        self.loading.update_status("Initialisation de l'interface...")
        
        # Centre la fenêtre principale après le loading
        self.after(1500, self._initialize_app)
    
    def _initialize_app(self):
        """Initialise l'application après le chargement."""
        self.loading.update_status("Configuration de la base de données...")
        
        # Création des composants UI
        self._create_sidebar()
        self._create_main_area()
        self._create_status_bar()
        
        # Fermeture du loading screen
        self.loading.close()
        
        # Tentative de connexion à la base de données
        self.after(500, self._connect_to_database)
    
    def _connect_to_database(self):
        """Tente de se connecter à la base de données."""
        # Chaîne de connexion - À modifier selon votre configuration
        # Format: DRIVERS={ODBC Driver 17 for SQL Server};SERVER=nom_serveur;DATABASE=nom_db;UID=user;PWD=password
        connection_string = os.getenv(
            'CLINIC_DB_CONNECTION',
            'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=ClinicDB;Trusted_Connection=yes;'
        )
        
        self.db_manager = DatabaseManager(connection_string)
        
        if self.db_manager.connect():
            self.controller = ClinicController(self.db_manager)
            self.status_label.configure(text="● Connecté à la base de données", text_color='#2ecc71')
            
            # Chargement du module par défaut (Patients)
            self._load_module('patients')
        else:
            self.status_label.configure(text="⚠ Non connecté à la base de données", text_color='#e74c3c')
            
            NotificationDialog(
                self,
                "Erreur de connexion",
                "Impossible de se connecter à la base de données.\n\n"
                "Vérifiez votre configuration SQL Server.\n\n"
                "L'application fonctionnera en mode démo.",
                "error"
            )
    
    def _create_sidebar(self):
        """Crée la barre de navigation latérale."""
        sidebar = ctk.CTkFrame(self, width=250, fg_color='#1a1a1a')
        sidebar.grid(row=0, column=0, sticky='ns')
        sidebar.grid_propagate(False)
        
        # Logo / Titre
        logo_frame = ctk.CTkFrame(sidebar, fg_color='transparent', height=100)
        logo_frame.pack(fill='x', padx=20, pady=20)
        logo_frame.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🏥\nClinic\nManager",
            font=ctk.CTkFont(size=24, weight='bold'),
            justify='center'
        )
        logo_label.pack(expand=True)
        
        # Séparateur
        separator = ctk.CTkFrame(sidebar, height=2, fg_color='#34495e')
        separator.pack(fill='x', padx=20, pady=10)
        
        # Menu de navigation
        nav_frame = ctk.CTkFrame(sidebar, fg_color='transparent')
        nav_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Boutons de navigation
        self.nav_buttons = {}
        
        menu_items = [
            ('patients', '👥', 'Patients'),
            ('personnel', '👨‍⚕️', 'Personnel'),
            ('chambres', '🛏️', 'Chambres'),
            ('actes', '📋', 'Actes'),
            ('medicaments', '💊', 'Médicaments'),
            ('ordonnances', '📝', 'Ordonnances'),
            ('consultations', '🩺', 'Consultations')
        ]
        
        for key, icon, label in menu_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=f"{icon}  {label}",
                anchor='w',
                height=50,
                corner_radius=8,
                fg_color='transparent',
                hover_color='#2c3e50',
                command=lambda k=key: self._on_nav_click(k)
            )
            btn.pack(fill='x', pady=5)
            self.nav_buttons[key] = btn
        
        # Pied de sidebar
        footer_frame = ctk.CTkFrame(sidebar, fg_color='transparent', height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        # Bouton déconnexion/quit
        quit_btn = ctk.CTkButton(
            footer_frame,
            text="🚪 Quitter",
            height=45,
            corner_radius=8,
            fg_color='#e74c3c',
            hover_color='#c0392b',
            command=self._on_quit
        )
        quit_btn.pack(padx=20, pady=10)
    
    def _create_main_area(self):
        """Crée la zone centrale de contenu."""
        self.main_area = ctk.CTkFrame(self, fg_color='#2b2b2b')
        self.main_area.grid(row=0, column=1, sticky='nsew')
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.rowconfigure(0, weight=1)
        
        # Label de bienvenue (affiché par défaut)
        welcome_frame = ctk.CTkFrame(self.main_area, fg_color='transparent')
        welcome_frame.grid(row=0, column=0, sticky='nsew')
        
        welcome_label = ctk.CTkLabel(
            welcome_frame,
            text="🏥\n\nBienvenue dans\nClinic Management System\n\nSélectionnez un module dans le menu latéral",
            font=ctk.CTkFont(size=24),
            justify='center'
        )
        welcome_label.place(relx=0.5, rely=0.5, anchor='center')
    
    def _create_status_bar(self):
        """Crée la barre de statut."""
        status_bar = ctk.CTkFrame(self, height=35, fg_color='#1a1a1a')
        status_bar.grid(row=1, column=0, columnspan=2, sticky='ew')
        status_bar.grid_propagate(False)
        
        # Label de statut (connexion DB)
        self.status_label = ctk.CTkLabel(
            status_bar,
            text="○ Non connecté",
            font=ctk.CTkFont(size=12),
            text_color='#95a5a6'
        )
        self.status_label.pack(side='left', padx=20, pady=5)
        
        # Version
        version_label = ctk.CTkLabel(
            status_bar,
            text="v1.0.0 | © 2024 Clinic Manager",
            font=ctk.CTkFont(size=11),
            text_color='#7f8c8d'
        )
        version_label.pack(side='right', padx=20, pady=5)
    
    def _on_nav_click(self, module_key: str):
        """Gère le clic sur un bouton de navigation."""
        # Mise à jour visuelle des boutons
        for key, btn in self.nav_buttons.items():
            if key == module_key:
                btn.configure(fg_color='#34495e')
            else:
                btn.configure(fg_color='transparent')
        
        # Chargement du module
        self._load_module(module_key)
    
    def _load_module(self, module_key: str):
        """Charge un module spécifique."""
        # Nettoyage du contenu actuel
        for widget in self.main_area.winfo_children():
            widget.destroy()
        
        # Modules disponibles (seul Patients est implémenté pour l'exemple)
        if module_key == 'patients':
            if self.controller:
                module = PatientModule(self.main_area, self.controller)
            else:
                # Mode démo sans DB
                demo_label = ctk.CTkLabel(
                    self.main_area,
                    text="👥 Module Patients\n\nMode démo - Connectez-vous à la DB pour activer",
                    font=ctk.CTkFont(size=18),
                    justify='center'
                )
                demo_label.place(relx=0.5, rely=0.5, anchor='center')
                return
        else:
            # Placeholder pour les autres modules
            placeholder = ctk.CTkLabel(
                self.main_area,
                text=f"🚧 Module {module_key.title()}\n\nEn cours de développement",
                font=ctk.CTkFont(size=20),
                justify='center'
            )
            placeholder.place(relx=0.5, rely=0.5, anchor='center')
            return
        
        module.grid(row=0, column=0, sticky='nsew')
        self.current_module = module
    
    def _on_quit(self):
        """Gère la fermeture de l'application."""
        if self.db_manager:
            self.db_manager.disconnect()
        self.quit()
        self.destroy()


def main():
    """Point d'entrée principal."""
    app = ClinicApp()
    app.mainloop()


if __name__ == "__main__":
    main()
