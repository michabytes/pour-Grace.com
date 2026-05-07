"""
ClinicController - Couche métier de l'application
Orchestre les opérations CRUD via le DatabaseManager
"""

from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, date
from database_manager import DatabaseManager


class ClinicController:
    """Contrôleur métier pour la gestion clinique."""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialise le contrôleur.
        
        Args:
            db_manager: Instance du gestionnaire de base de données
        """
        self.db = db_manager
    
    # ==================== PATIENTS ====================
    
    def get_patients(self) -> Tuple[bool, List[Dict], str]:
        """Récupère tous les patients."""
        return self.db.execute_procedure('spGetPatients')
    
    def add_patient(self, nom: str, sexe: str, date_naissance: date, lieu: str) -> Tuple[bool, Optional[int], str]:
        """Ajoute un nouveau patient."""
        params = (nom, sexe, date_naissance, lieu)
        return self.db.execute_procedure_with_output('spAddPatient', params, 1)
    
    def update_patient(self, id_patient: int, nom: str, sexe: str, date_naissance: date, lieu: str) -> Tuple[bool, None, str]:
        """Modifie un patient existant."""
        params = (id_patient, nom, sexe, date_naissance, lieu)
        success, _, error = self.db.execute_procedure('spUpdatePatient', params)
        return success, None, error
    
    def delete_patient(self, id_patient: int) -> Tuple[bool, None, str]:
        """Supprime un patient."""
        params = (id_patient,)
        success, _, error = self.db.execute_procedure('spDeletePatient', params)
        return success, None, error
    
    # ==================== PERSONNEL ====================
    
    def get_personnel(self) -> Tuple[bool, List[Dict], str]:
        """Récupère tout le personnel."""
        return self.db.execute_procedure('spGetPersonnel')
    
    def add_personnel(self, nom: str, statut: str, actif: bool) -> Tuple[bool, Optional[int], str]:
        """Ajoute un nouveau membre du personnel."""
        params = (nom, statut, 1 if actif else 0)
        return self.db.execute_procedure_with_output('spAddPersonnel', params, 1)
    
    def update_personnel(self, id_personnel: int, nom: str, statut: str, actif: bool) -> Tuple[bool, None, str]:
        """Modifie un membre du personnel."""
        params = (id_personnel, nom, statut, 1 if actif else 0)
        success, _, error = self.db.execute_procedure('spUpdatePersonnel', params)
        return success, None, error
    
    def delete_personnel(self, id_personnel: int) -> Tuple[bool, None, str]:
        """Supprime un membre du personnel."""
        params = (id_personnel,)
        success, _, error = self.db.execute_procedure('spDeletePersonnel', params)
        return success, None, error
    
    # ==================== CHAMBRES ====================
    
    def get_chambres(self) -> Tuple[bool, List[Dict], str]:
        """Récupère toutes les chambres."""
        return self.db.execute_procedure('spGetChambres')
    
    def add_chambre(self, numero: str, nb_lits: int, statut: str) -> Tuple[bool, Optional[int], str]:
        """Ajoute une nouvelle chambre."""
        params = (numero, nb_lits, statut)
        return self.db.execute_procedure_with_output('spAddChambre', params, 1)
    
    def update_chambre(self, numero: str, nb_lits: int, statut: str) -> Tuple[bool, None, str]:
        """Modifie une chambre existante."""
        params = (numero, nb_lits, statut)
        success, _, error = self.db.execute_procedure('spUpdateChambre', params)
        return success, None, error
    
    def delete_chambre(self, numero: str) -> Tuple[bool, None, str]:
        """Supprime une chambre."""
        params = (numero,)
        success, _, error = self.db.execute_procedure('spDeleteChambre', params)
        return success, None, error
    
    # ==================== ACTES ====================
    
    def get_actes(self) -> Tuple[bool, List[Dict], str]:
        """Récupère tous les actes avec informations liées."""
        return self.db.execute_procedure('spGetActes')
    
    def add_acte(self, date_acte: datetime, description: str, conclusion: str, 
                 id_patient: int, id_personnel: int) -> Tuple[bool, Optional[int], str]:
        """Ajoute un nouvel acte."""
        params = (date_acte, description, conclusion, id_patient, id_personnel)
        return self.db.execute_procedure_with_output('spAddActe', params, 1)
    
    def update_acte(self, id_acte: int, date_acte: datetime, description: str, 
                    conclusion: str, id_patient: int, id_personnel: int) -> Tuple[bool, None, str]:
        """Modifie un acte existant."""
        params = (id_acte, date_acte, description, conclusion, id_patient, id_personnel)
        success, _, error = self.db.execute_procedure('spUpdateActe', params)
        return success, None, error
    
    def delete_acte(self, id_acte: int) -> Tuple[bool, None, str]:
        """Supprime un acte."""
        params = (id_acte,)
        success, _, error = self.db.execute_procedure('spDeleteActe', params)
        return success, None, error
    
    # ==================== MEDICAMENTS ====================
    
    def get_medicaments(self) -> Tuple[bool, List[Dict], str]:
        """Récupère tous les médicaments."""
        return self.db.execute_procedure('spGetMedicaments')
    
    def add_medicament(self, nom: str, dosage: str, prix: float) -> Tuple[bool, Optional[int], str]:
        """Ajoute un nouveau médicament."""
        params = (nom, dosage, prix)
        return self.db.execute_procedure_with_output('spAddMedicament', params, 1)
    
    def update_medicament(self, id_med: int, nom: str, dosage: str, prix: float) -> Tuple[bool, None, str]:
        """Modifie un médicament existant."""
        params = (id_med, nom, dosage, prix)
        success, _, error = self.db.execute_procedure('spUpdateMedicament', params)
        return success, None, error
    
    def delete_medicament(self, id_med: int) -> Tuple[bool, None, str]:
        """Supprime un médicament."""
        params = (id_med,)
        success, _, error = self.db.execute_procedure('spDeleteMedicament', params)
        return success, None, error
    
    # ==================== ORDONNANCES ====================
    
    def get_ordonnances(self) -> Tuple[bool, List[Dict], str]:
        """Récupère toutes les ordonnances avec informations liées."""
        return self.db.execute_procedure('spGetOrdonnances')
    
    def add_oronnance(self, date_ord: datetime, medicaments: str, posologie: str,
                      duree: int, id_acte: int, id_patient: int, id_personnel: int) -> Tuple[bool, Optional[int], str]:
        """Ajoute une nouvelle ordonnance."""
        params = (date_ord, medicaments, posologie, duree, id_acte, id_patient, id_personnel)
        return self.db.execute_procedure_with_output('spAddOrdonnance', params, 1)
    
    def update_oronnance(self, id_ord: int, date_ord: datetime, medicaments: str, posologie: str,
                         duree: int, id_acte: int, id_patient: int, id_personnel: int) -> Tuple[bool, None, str]:
        """Modifie une ordonnance existante."""
        params = (id_ord, date_ord, medicaments, posologie, duree, id_acte, id_patient, id_personnel)
        success, _, error = self.db.execute_procedure('spUpdateOrdonnance', params)
        return success, None, error
    
    def delete_oronnance(self, id_ord: int) -> Tuple[bool, None, str]:
        """Supprime une ordonnance."""
        params = (id_ord,)
        success, _, error = self.db.execute_procedure('spDeleteOrdonnance', params)
        return success, None, error
    
    # ==================== CONSULTATIONS ====================
    
    def get_consultations(self) -> Tuple[bool, List[Dict], str]:
        """Récupère toutes les consultations avec informations liées."""
        return self.db.execute_procedure('spGetConsultations')
    
    def add_consultation(self, date_cons: datetime, motif: str, diagnostic: str,
                         id_patient: int, id_personnel: int) -> Tuple[bool, Optional[int], str]:
        """Ajoute une nouvelle consultation."""
        params = (date_cons, motif, diagnostic, id_patient, id_personnel)
        return self.db.execute_procedure_with_output('spAddConsultation', params, 1)
    
    def update_consultation(self, id_cons: int, date_cons: datetime, motif: str, diagnostic: str,
                            id_patient: int, id_personnel: int) -> Tuple[bool, None, str]:
        """Modifie une consultation existante."""
        params = (id_cons, date_cons, motif, diagnostic, id_patient, id_personnel)
        success, _, error = self.db.execute_procedure('spUpdateConsultation', params)
        return success, None, error
    
    def delete_consultation(self, id_cons: int) -> Tuple[bool, None, str]:
        """Supprime une consultation."""
        params = (id_cons,)
        success, _, error = self.db.execute_procedure('spDeleteConsultation', params)
        return success, None, error
