"""
Database Manager - Couche d'accès aux données
Gère la connexion SQL Server via pyodbc avec procédures stockées uniquement
"""

import pyodbc
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gestionnaire de connexion et d'exécution de procédures stockées SQL Server."""
    
    _instance: Optional['DatabaseManager'] = None
    
    def __new__(cls, connection_string: str = "") -> 'DatabaseManager':
        """Singleton pattern pour réutiliser la connexion."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, connection_string: str = ""):
        """Initialise le gestionnaire de base de données."""
        if self._initialized:
            return
        
        self._connection_string = connection_string
        self._connection: Optional[pyodbc.Connection] = None
        self._initialized = True
    
    def connect(self, connection_string: Optional[str] = None) -> bool:
        """
        Établit la connexion à la base de données.
        
        Args:
            connection_string: Chaîne de connexion SQL Server
            
        Returns:
            bool: True si la connexion réussit
        """
        try:
            conn_str = connection_string or self._connection_string
            if not conn_str:
                logger.error("Aucune chaîne de connexion fournie")
                return False
            
            self._connection = pyodbc.connect(conn_str, autocommit=False)
            logger.info("Connexion SQL Server établie avec succès")
            return True
        except pyodbc.Error as e:
            logger.error(f"Erreur de connexion SQL Server: {e}")
            return False
    
    def disconnect(self) -> None:
        """Ferme la connexion à la base de données."""
        if self._connection:
            try:
                self._connection.close()
                logger.info("Connexion SQL Server fermée")
            except pyodbc.Error as e:
                logger.error(f"Erreur lors de la fermeture: {e}")
            finally:
                self._connection = None
    
    def is_connected(self) -> bool:
        """Vérifie si la connexion est active."""
        if self._connection is None:
            return False
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except pyodbc.Error:
            return False
    
    def execute_procedure(self, procedure_name: str, 
                         params: Optional[Tuple] = None,
                         output_params: Optional[List[str]] = None) -> Tuple[bool, Any, str]:
        """
        Exécute une procédure stockée avec gestion des erreurs et transactions.
        
        Args:
            procedure_name: Nom de la procédure stockée (ex: 'spGetPatients')
            params: Tuple de paramètres pour la procédure
            output_params: Liste des noms de paramètres OUTPUT
            
        Returns:
            Tuple[bool, Any, str]: (succès, résultat/data, message d'erreur)
        """
        if not self.is_connected():
            return False, None, "Pas de connexion à la base de données"
        
        try:
            cursor = self._connection.cursor()
            
            # Construction de l'appel de procédure
            if params:
                param_placeholders = ", ".join(["?" for _ in params])
                if output_params:
                    # Ajouter les paramètres OUTPUT
                    for out_param in output_params:
                        param_placeholders += f", ? OUTPUT"
                sql = f"{{CALL {procedure_name}({param_placeholders})}}"
            else:
                sql = f"{{CALL {procedure_name}}}"
            
            # Exécution
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            
            # Récupération des résultats pour les procédures SELECT
            if procedure_name.startswith('spGet'):
                columns = [column[0] for column in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                cursor.close()
                return True, results, ""
            
            # Commit pour les opérations INSERT/UPDATE/DELETE
            self._connection.commit()
            
            # Récupération des paramètres OUTPUT
            output_values = {}
            if output_params and cursor.nextset():
                for i, param_name in enumerate(output_params):
                    output_values[param_name] = cursor.getvalue(i)
            
            cursor.close()
            
            # Retourne l'ID généré s'il existe
            if output_values:
                return True, output_values, ""
            return True, None, ""
            
        except pyodbc.Error as e:
            error_msg = str(e)
            logger.error(f"Erreur procédure {procedure_name}: {error_msg}")
            try:
                self._connection.rollback()
            except pyodbc.Error:
                pass
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            logger.error(error_msg)
            try:
                self._connection.rollback()
            except pyodbc.Error:
                pass
            return False, None, error_msg
    
    def execute_procedure_with_output(self, procedure_name: str,
                                      params: Tuple,
                                      output_param_count: int = 1) -> Tuple[bool, Optional[int], str]:
        """
        Exécute une procédure stockée avec paramètre OUTPUT (pour les IDs).
        
        Args:
            procedure_name: Nom de la procédure
            params: Paramètres d'entrée
            output_param_count: Nombre de paramètres OUTPUT attendus
            
        Returns:
            Tuple[bool, Optional[int], str]: (succès, ID généré, message)
        """
        if not self.is_connected():
            return False, None, "Pas de connexion à la base de données"
        
        try:
            cursor = self._connection.cursor()
            
            # Construire la chaîne d'appel avec paramètres OUTPUT
            input_placeholders = ", ".join(["?" for _ in params])
            output_placeholders = ", ".join(["? OUTPUT" for _ in range(output_param_count)])
            sql = f"{{CALL {procedure_name}({input_placeholders}, {output_placeholders})}}"
            
            # Créer la liste complet des paramètres
            all_params = list(params) + [0] * output_param_count
            
            cursor.execute(sql, all_params)
            self._connection.commit()
            
            # Récupérer la valeur OUTPUT
            cursor.nextset()
            new_id = cursor.getvalue(0) if output_param_count > 0 else None
            
            cursor.close()
            return True, int(new_id) if new_id else None, ""
            
        except pyodbc.Error as e:
            error_msg = str(e)
            logger.error(f"Erreur procédure {procedure_name}: {error_msg}")
            try:
                self._connection.rollback()
            except pyodbc.Error:
                pass
            return False, None, error_msg
        except Exception as e:
            error_msg = f"Erreur inattendue: {str(e)}"
            logger.error(error_msg)
            try:
                self._connection.rollback()
            except pyodbc.Error:
                pass
            return False, None, error_msg
