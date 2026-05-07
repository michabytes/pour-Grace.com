-- ============================================================
-- SCRIPT SQL - PROCÉDURES STOCKÉES POUR GESTION CLINIQUE
-- SQL Server / pyodbc
-- ============================================================

-- ============================================================
-- TABLE: PATIENTS (IDPA, PANP, PASX, PADN, PALN)
-- ============================================================

-- spGetPatients: Récupérer tous les patients
CREATE OR ALTER PROCEDURE spGetPatients
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT IDPA, PANP, PASX, PADN, PALN 
        FROM PATIENTS 
        ORDER BY PANP;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddPatient: Ajouter un patient
CREATE OR ALTER PROCEDURE spAddPatient
    @PANP NVARCHAR(100),
    @PASX NVARCHAR(10),
    @PADN DATE,
    @PALN NVARCHAR(200),
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO PATIENTS (PANP, PASX, PADN, PALN)
        VALUES (@PANP, @PASX, @PADN, @PALN);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdatePatient: Modifier un patient
CREATE OR ALTER PROCEDURE spUpdatePatient
    @IDPA INT,
    @PANP NVARCHAR(100),
    @PASX NVARCHAR(10),
    @PADN DATE,
    @PALN NVARCHAR(200)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE PATIENTS 
        SET PANP = @PANP, 
            PASX = @PASX, 
            PADN = @PADN, 
            PALN = @PALN
        WHERE IDPA = @IDPA;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Patient non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeletePatient: Supprimer un patient
CREATE OR ALTER PROCEDURE spDeletePatient
    @IDPA INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM PATIENTS WHERE IDPA = @IDPA;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Patient non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ============================================================
-- TABLE: PERSONNEL (PEID, PENP, STATI, STATM)
-- ============================================================

-- spGetPersonnel: Récupérer tout le personnel
CREATE OR ALTER PROCEDURE spGetPersonnel
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT PEID, PENP, STATI, STATM 
        FROM PERSONNEL 
        ORDER BY PENP;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddPersonnel: Ajouter un membre du personnel
CREATE OR ALTER PROCEDURE spAddPersonnel
    @PENP NVARCHAR(100),
    @STATI NVARCHAR(50),
    @STATM BIT,
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO PERSONNEL (PENP, STATI, STATM)
        VALUES (@PENP, @STATI, @STATM);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdatePersonnel: Modifier un membre du personnel
CREATE OR ALTER PROCEDURE spUpdatePersonnel
    @PEID INT,
    @PENP NVARCHAR(100),
    @STATI NVARCHAR(50),
    @STATM BIT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE PERSONNEL 
        SET PENP = @PENP, 
            STATI = @STATI, 
            STATM = @STATM
        WHERE PEID = @PEID;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Personnel non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeletePersonnel: Supprimer un membre du personnel
CREATE OR ALTER PROCEDURE spDeletePersonnel
    @PEID INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM PERSONNEL WHERE PEID = @PEID;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Personnel non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ============================================================
-- TABLE: CHAMBRES (NUMCH, NOLIT, STACH)
-- ============================================================

-- spGetChambres: Récupérer toutes les chambres
CREATE OR ALTER PROCEDURE spGetChambres
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT NUMCH, NOLIT, STACH 
        FROM CHAMBRES 
        ORDER BY NUMCH;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddChambre: Ajouter une chambre
CREATE OR ALTER PROCEDURE spAddChambre
    @NUMCH NVARCHAR(20),
    @NOLIT INT,
    @STACH NVARCHAR(50),
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO CHAMBRES (NUMCH, NOLIT, STACH)
        VALUES (@NUMCH, @NOLIT, @STACH);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdateChambre: Modifier une chambre
CREATE OR ALTER PROCEDURE spUpdateChambre
    @NUMCH NVARCHAR(20),
    @NOLIT INT,
    @STACH NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE CHAMBRES 
        SET NOLIT = @NOLIT, 
            STACH = @STACH
        WHERE NUMCH = @NUMCH;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Chambre non trouvée', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeleteChambre: Supprimer une chambre
CREATE OR ALTER PROCEDURE spDeleteChambre
    @NUMCH NVARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM CHAMBRES WHERE NUMCH = @NUMCH;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Chambre non trouvée', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ============================================================
-- TABLE: ACTES (ACID, ACDA, ACHR, ACCON, IDPA, PEID)
-- ============================================================

-- spGetActes: Récupérer tous les actes avec informations liées
CREATE OR ALTER PROCEDURE spGetActes
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT 
            a.ACID, 
            a.ACDA, 
            a.ACHR, 
            a.ACCON, 
            a.IDPA, 
            p.PANP AS PatientNom,
            a.PEID, 
            pe.PENP AS PersonnelNom
        FROM ACTES a
        LEFT JOIN PATIENTS p ON a.IDPA = p.IDPA
        LEFT JOIN PERSONNEL pe ON a.PEID = pe.PEID
        ORDER BY a.ACDA DESC;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddActe: Ajouter un acte
CREATE OR ALTER PROCEDURE spAddActe
    @ACDA DATETIME,
    @ACHR NVARCHAR(200),
    @ACCON NVARCHAR(MAX),
    @IDPA INT,
    @PEID INT,
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO ACTES (ACDA, ACHR, ACCON, IDPA, PEID)
        VALUES (@ACDA, @ACHR, @ACCON, @IDPA, @PEID);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdateActe: Modifier un acte
CREATE OR ALTER PROCEDURE spUpdateActe
    @ACID INT,
    @ACDA DATETIME,
    @ACHR NVARCHAR(200),
    @ACCON NVARCHAR(MAX),
    @IDPA INT,
    @PEID INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE ACTES 
        SET ACDA = @ACDA, 
            ACHR = @ACHR, 
            ACCON = @ACCON, 
            IDPA = @IDPA, 
            PEID = @PEID
        WHERE ACID = @ACID;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Acte non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeleteActe: Supprimer un acte
CREATE OR ALTER PROCEDURE spDeleteActe
    @ACID INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM ACTES WHERE ACID = @ACID;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Acte non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ============================================================
-- TABLE: MEDICAMENTS (à créer si n'existe pas)
-- ============================================================

-- spGetMedicaments: Récupérer tous les médicaments
CREATE OR ALTER PROCEDURE spGetMedicaments
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT IDMED, NOMMED, DOSAGE, PRIX 
        FROM MEDICAMENTS 
        ORDER BY NOMMED;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddMedicament: Ajouter un médicament
CREATE OR ALTER PROCEDURE spAddMedicament
    @NOMMED NVARCHAR(100),
    @DOSAGE NVARCHAR(50),
    @PRIX DECIMAL(10,2),
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO MEDICAMENTS (NOMMED, DOSAGE, PRIX)
        VALUES (@NOMMED, @DOSAGE, @PRIX);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdateMedicament: Modifier un médicament
CREATE OR ALTER PROCEDURE spUpdateMedicament
    @IDMED INT,
    @NOMMED NVARCHAR(100),
    @DOSAGE NVARCHAR(50),
    @PRIX DECIMAL(10,2)
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE MEDICAMENTS 
        SET NOMMED = @NOMMED, 
            DOSAGE = @DOSAGE, 
            PRIX = @PRIX
        WHERE IDMED = @IDMED;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Médicament non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeleteMedicament: Supprimer un médicament
CREATE OR ALTER PROCEDURE spDeleteMedicament
    @IDMED INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM MEDICAMENTS WHERE IDMED = @IDMED;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Médicament non trouvé', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ============================================================
-- TABLE: ORDONNANCE (IDOR, ORDA, ORMED, ORPO, ORDU, ACID, IDPA, PEID)
-- ============================================================

-- spGetOrdonnances: Récupérer toutes les ordonnances avec informations liées
CREATE OR ALTER PROCEDURE spGetOrdonnances
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT 
            o.IDOR, 
            o.ORDA, 
            o.ORMED, 
            o.ORPO, 
            o.ORDU, 
            o.ACID, 
            o.IDPA,
            p.PANP AS PatientNom,
            o.PEID,
            pe.PENP AS PersonnelNom
        FROM ORDONNANCE o
        LEFT JOIN PATIENTS p ON o.IDPA = p.IDPA
        LEFT JOIN PERSONNEL pe ON o.PEID = pe.PEID
        ORDER BY o.ORDA DESC;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddOrdonnance: Ajouter une ordonnance
CREATE OR ALTER PROCEDURE spAddOrdonnance
    @ORDA DATETIME,
    @ORMED NVARCHAR(MAX),
    @ORPO NVARCHAR(MAX),
    @ORDU INT,
    @ACID INT,
    @IDPA INT,
    @PEID INT,
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO ORDONNANCE (ORDA, ORMED, ORPO, ORDU, ACID, IDPA, PEID)
        VALUES (@ORDA, @ORMED, @ORPO, @ORDU, @ACID, @IDPA, @PEID);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdateOrdonnance: Modifier une ordonnance
CREATE OR ALTER PROCEDURE spUpdateOrdonnance
    @IDOR INT,
    @ORDA DATETIME,
    @ORMED NVARCHAR(MAX),
    @ORPO NVARCHAR(MAX),
    @ORDU INT,
    @ACID INT,
    @IDPA INT,
    @PEID INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE ORDONNANCE 
        SET ORDA = @ORDA, 
            ORMED = @ORMED, 
            ORPO = @ORPO, 
            ORDU = @ORDU, 
            ACID = @ACID, 
            IDPA = @IDPA, 
            PEID = @PEID
        WHERE IDOR = @IDOR;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Ordonnance non trouvée', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeleteOrdonnance: Supprimer une ordonnance
CREATE OR ALTER PROCEDURE spDeleteOrdonnance
    @IDOR INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM ORDONNANCE WHERE IDOR = @IDOR;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Ordonnance non trouvée', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- ============================================================
-- TABLE: CONSULTATIONS (module supplémentaire)
-- ============================================================

-- spGetConsultations: Récupérer toutes les consultations
CREATE OR ALTER PROCEDURE spGetConsultations
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        SELECT 
            c.IDCONS,
            c.DATECONS,
            c.MOTIF,
            c.DIAGNOSTIC,
            c.IDPA,
            p.PANP AS PatientNom,
            c.PEID,
            pe.PENP AS PersonnelNom
        FROM CONSULTATIONS c
        LEFT JOIN PATIENTS p ON c.IDPA = p.IDPA
        LEFT JOIN PERSONNEL pe ON c.PEID = pe.PEID
        ORDER BY c.DATECONS DESC;
    END TRY
    BEGIN CATCH
        THROW;
    END CATCH
END
GO

-- spAddConsultation: Ajouter une consultation
CREATE OR ALTER PROCEDURE spAddConsultation
    @DATECONS DATETIME,
    @MOTIF NVARCHAR(200),
    @DIAGNOSTIC NVARCHAR(MAX),
    @IDPA INT,
    @PEID INT,
    @NewID INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        INSERT INTO CONSULTATIONS (DATECONS, MOTIF, DIAGNOSTIC, IDPA, PEID)
        VALUES (@DATECONS, @MOTIF, @DIAGNOSTIC, @IDPA, @PEID);
        
        SET @NewID = SCOPE_IDENTITY();
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spUpdateConsultation: Modifier une consultation
CREATE OR ALTER PROCEDURE spUpdateConsultation
    @IDCONS INT,
    @DATECONS DATETIME,
    @MOTIF NVARCHAR(200),
    @DIAGNOSTIC NVARCHAR(MAX),
    @IDPA INT,
    @PEID INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        UPDATE CONSULTATIONS 
        SET DATECONS = @DATECONS, 
            MOTIF = @MOTIF, 
            DIAGNOSTIC = @DIAGNOSTIC, 
            IDPA = @IDPA, 
            PEID = @PEID
        WHERE IDCONS = @IDCONS;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Consultation non trouvée', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

-- spDeleteConsultation: Supprimer une consultation
CREATE OR ALTER PROCEDURE spDeleteConsultation
    @IDCONS INT
AS
BEGIN
    SET NOCOUNT ON;
    BEGIN TRY
        BEGIN TRANSACTION;
        
        DELETE FROM CONSULTATIONS WHERE IDCONS = @IDCONS;
        
        IF @@ROWCOUNT = 0
            RAISERROR('Consultation non trouvée', 16, 1);
        
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;
        THROW;
    END CATCH
END
GO

PRINT 'Toutes les procédures stockées ont été créées avec succès.'
