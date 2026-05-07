"""
UI Components - Composants d'interface personnalisés CustomTkinter
Composants réutilisables pour l'application clinique
"""

import customtkinter as ctk
from typing import Callable, Optional
import tkinter as tk


class NotificationDialog(ctk.CTkToplevel):
    """Fenêtre de notification élégante pour succès/erreur/avertissement."""
    
    def __init__(self, parent, title: str, message: str, 
                 notification_type: str = "info",
                 on_close: Optional[Callable] = None):
        """
        Crée une notification modale.
        
        Args:
            parent: Fenêtre parente
            title: Titre de la notification
            message: Message à afficher
            notification_type: 'success', 'error', 'warning', ou 'info'
            on_close: Callback appelé à la fermeture
        """
        super().__init__(parent)
        
        self.on_close = on_close
        
        # Configuration de la fenêtre
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Couleurs selon le type
        colors = {
            'success': ('#2ecc71', '#27ae60'),
            'error': ('#e74c3c', '#c0392b'),
            'warning': ('#f39c12', '#d68910'),
            'info': ('#3498db', '#2980b9')
        }
        color_primary, color_secondary = colors.get(notification_type, colors['info'])
        
        # Centre la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (150 // 2)
        self.geometry(f"400x150+{x}+{y}")
        
        # Icône selon le type
        icons = {
            'success': '✓',
            'error': '✗',
            'warning': '⚠',
            'info': 'ℹ'
        }
        icon = icons.get(notification_type, 'ℹ')
        
        # Frame principale
        main_frame = ctk.CTkFrame(self, fg_color=color_primary)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Contenu
        content_frame = ctk.CTkFrame(main_frame, fg_color=color_primary)
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Icône et titre
        title_label = ctk.CTkLabel(
            content_frame,
            text=f"{icon}  {title}",
            font=ctk.CTkFont(size=18, weight='bold'),
            text_color='white'
        )
        title_label.pack(pady=(0, 10))
        
        # Message
        message_label = ctk.CTkLabel(
            content_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            text_color='white',
            wraplength=350,
            justify='center'
        )
        message_label.pack(pady=(0, 20))
        
        # Bouton OK
        ok_button = ctk.CTkButton(
            content_frame,
            text="OK",
            width=100,
            height=35,
            corner_radius=8,
            fg_color='white',
            text_color=color_secondary,
            hover_color='#ecf0f1',
            command=self._on_close
        )
        ok_button.pack()
        
        # Bind touche Echap
        self.bind('<Escape>', lambda e: self._on_close())
    
    def _on_close(self):
        """Gère la fermeture de la notification."""
        if self.on_close:
            self.on_close()
        self.destroy()


class ConfirmationDialog(ctk.CTkToplevel):
    """Fenêtre de confirmation modale pour les suppressions."""
    
    def __init__(self, parent, title: str, message: str,
                 on_confirm: Callable, on_cancel: Optional[Callable] = None):
        """
        Crée un dialog de confirmation.
        
        Args:
            parent: Fenêtre parente
            title: Titre du dialog
            message: Message de confirmation
            on_confirm: Callback appelé si confirmé
            on_cancel: Callback appelé si annulé
        """
        super().__init__(parent)
        
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        # Configuration
        self.title(title)
        self.geometry("450x180")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centre la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (180 // 2)
        self.geometry(f"450x180+{x}+{y}")
        
        # Frame principale
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Titre avec icône
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"⚠️  {title}",
            font=ctk.CTkFont(size=18, weight='bold'),
            text_color='#e74c3c'
        )
        title_label.pack(pady=(0, 15))
        
        # Message
        message_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=14),
            wraplength=400,
            justify='center'
        )
        message_label.pack(pady=(0, 25))
        
        # Boutons
        button_frame = ctk.CTkFrame(main_frame, fg_color='transparent')
        button_frame.pack()
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Annuler",
            width=120,
            height=40,
            corner_radius=8,
            fg_color='#95a5a6',
            hover_color='#7f8c8d',
            command=self._on_cancel
        )
        cancel_button.pack(side='left', padx=10)
        
        confirm_button = ctk.CTkButton(
            button_frame,
            text="Confirmer",
            width=120,
            height=40,
            corner_radius=8,
            fg_color='#e74c3c',
            hover_color='#c0392b',
            command=self._on_confirm
        )
        confirm_button.pack(side='left', padx=10)
        
        # Bind touches
        self.bind('<Return>', lambda e: self._on_confirm())
        self.bind('<Escape>', lambda e: self._on_cancel())
    
    def _on_confirm(self):
        """Gère la confirmation."""
        self.on_confirm()
        self.destroy()
    
    def _on_cancel(self):
        """Gère l'annulation."""
        if self.on_cancel:
            self.on_cancel()
        self.destroy()


class LoadingScreen(ctk.CTkToplevel):
    """Écran de chargement avec barre de progression animée."""
    
    def __init__(self, parent, title: str = "Chargement..."):
        """
        Crée l'écran de chargement.
        
        Args:
            parent: Fenêtre parente
            title: Titre à afficher
        """
        super().__init__(parent)
        
        self.title(title)
        self.geometry("400x200")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Centre la fenêtre
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.winfo_screenheight() // 2) - (200 // 2)
        self.geometry(f"400x200+{x}+{y}")
        
        # Frame principale
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame,
            text=title,
            font=ctk.CTkFont(size=18, weight='bold')
        )
        title_label.pack(pady=(20, 20))
        
        # Barre de progression (mode indéterminé)
        self.progress = ctk.CTkProgressBar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', padx=20, pady=10)
        self.progress.set(0)
        self.progress.start()
        
        # Label de statut
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Veuillez patienter...",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(10, 0))
    
    def update_status(self, message: str):
        """Met à jour le message de statut."""
        self.status_label.configure(text=message)
    
    def close(self):
        """Ferme l'écran de chargement."""
        self.progress.stop()
        self.destroy()


class StyledTreeview(ctk.CTkFrame):
    """Wrapper pour ttk.Treeview avec style sombre personnalisé."""
    
    def __init__(self, parent, columns: list, show_headers: bool = True, **kwargs):
        """
        Crée un tableau stylisé.
        
        Args:
            parent: Widget parent
            columns: Liste des colonnes
            show_headers: Afficher les en-têtes
            **kwargs: Arguments supplémentaires pour CTkFrame
        """
        super().__init__(parent, **kwargs)
        
        from tkinter import ttk
        
        # Configuration du style Treeview
        style = ttk.Style()
        
        # Thème sombre
        style.theme_use('clam')
        
        # Style général
        style.configure("Custom.Treeview",
                       background='#2b2b2b',
                       fieldbackground='#2b2b2b',
                       foreground='white',
                       rowheight=35,
                       borderwidth=0,
                       font=('Segoe UI', 11))
        
        # En-têtes
        style.configure("Custom.Treeview.Heading",
                       background='#1a1a1a',
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'))
        
        # Hover effect (nécessite bind manuel)
        style.map("Custom.Treeview",
                 background=[('selected', '#3498db')],
                 foreground=[('selected', 'white')])
        
        # Création du Treeview
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show='headings' if show_headers else '',
            style="Custom.Treeview"
        )
        
        # Configuration des colonnes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', minwidth=100, width=150)
        
        # Scrollbars
        self.v_scrollbar = ctk.CTkScrollbar(self, orientation='vertical', command=self.tree.yview)
        self.h_scrollbar = ctk.CTkScrollbar(self, orientation='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Layout
        self.tree.pack(side='left', fill='both', expand=True)
        self.v_scrollbar.pack(side='right', fill='y')
        self.h_scrollbar.pack(side='bottom', fill='x')
        
        # Hover effect manuel
        self._hover_item = None
        self.tree.bind('<Motion>', self._on_motion)
        self.tree.bind('<Leave>', self._on_leave)
    
    def _on_motion(self, event):
        """Gère l'effet hover sur les lignes."""
        region = self.tree.identify("region", event.x, event.y)
        item = self.tree.identify_row(event.y)
        
        if region == "cell" and item:
            if self._hover_item != item:
                self._hover_item = item
        else:
            self._hover_item = None
    
    def _on_leave(self, event):
        """Gère la sortie du widget."""
        self._hover_item = None
    
    def insert(self, values: tuple, iid: Optional[str] = None) -> str:
        """Insère une ligne."""
        return self.tree.insert('', 'end', iid=iid, values=values)
    
    def delete_all(self):
        """Supprime toutes les lignes."""
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_selected(self) -> Optional[str]:
        """Retourne l'ID de l'élément sélectionné."""
        selection = self.tree.selection()
        return selection[0] if selection else None
    
    def get_selected_values(self) -> Optional[tuple]:
        """Retourne les valeurs de l'élément sélectionné."""
        selected = self.get_selected()
        if selected:
            return self.tree.item(selected)['values']
        return None
