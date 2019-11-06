import pymysql
import matplotlib.pyplot as plt
import pandas as pd
from diet_clinic.config import host_db, login_db, password_db, name_db
from datetime import datetime
from diet_clinic.objects import User, Patient, Comment, Diet, DietProduct, Product


class DatabaseManager:

    def __init__(self):
        self.loginDatabase(host_db, login_db, password_db, name_db)
        self.activeIdUser = None
        self.activeIdPatient = None
        self.activeIdDiet = None
        self.activeIdProduct = None
        self.activeIdDietProduct = None

    def __str__(self):
        return "Połączono z bazą danych" if self.loginDatabaseOk else "Rozłączono z bazą danych"

    def loginDatabase(self, host_db, login_db, password_db, name_db):
        try:
            self.connect = pymysql.connect(host_db, login_db, password_db, name_db)
            self.cursor = self.connect.cursor()
            self.loginDatabaseOk = True
        except:
            self.loginDatabaseOk = False

    def loginUser(self, loginUser, passwordUser):
        self.cursor.execute("SELECT id_user, login, password, first_name, last_name, permission, account_blocking, active FROM users;")
        for row in self.cursor.fetchall():
            if row[1] == loginUser and row[2] == passwordUser and row[7] == True:
                self.cursor.execute("UPDATE users SET account_blocking = %s where id_user = %s ",  (0, row[0]))
                self.connect.commit()
                self.activeIdUser = row[0]
                return row[5]
            elif row[1] == loginUser and row[2] != passwordUser and row[7] == True:
                account_blocking = row[6] + 1
                self._updateUserAccountBlockingByLogin(row[1], account_blocking)
                if row[6] >= 4:
                    self._updateUserActiveByLogin(row[1], 0)
                self.activeIdUser = None
                return 'bledne_haslo'
            elif row[1] == loginUser and row[7] == False:
                self.activeIdUser = None
                return 'konto_zablokowane'

    def _updateUserAccountBlockingByLogin(self, loginUser, accountBlocking=0):
        self.cursor.execute("UPDATE users SET account_blocking = %s where login = '%s' " % (accountBlocking, loginUser))
        self.connect.commit()

    def _updateUserActiveByLogin(self, loginUser, activeUser=1):
        self.cursor.execute("UPDATE users SET active = %s where login = '%s' " % (activeUser, loginUser))
        self.connect.commit()

    def _commitDecision(self, commitPrint="Wprowadzono zmiany", rollbackPrint=""):
        decision = input("Czy zatwierdzić operacje T/N ")
        if decision.upper() == 'T':
            self.connect.commit()
            print(commitPrint)
        else:
            self.connect.rollback()
            print(rollbackPrint)
###

    def selectUser(self):
        self.cursor.execute("SELECT id_user, login, first_name, last_name, permission, account_blocking, active FROM users ORDER BY permission, login;")
        print("| %4s | %10s | %15s | %15s | %12s | %10s | %10s " % ("ID", "Login", "Imię", "Nazwisko", "Permission", "Blocking", "Active"))
        for row in self.cursor.fetchall():
            print("| %4d | %10s | %15s | %15s | %12s | %10s | %10s |" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6] ))

    def addUserByObject(self, user):
        try:
            self.cursor.execute("INSERT INTO users (login, password, first_name, last_name, permission) VALUES ('%s', '%s' ,'%s', '%s', '%s');" %
                                (user.loginUser, user.passwordUser, user.firstNameUser, user.lastNameUser, user.permissionUser))
            self._commitDecision('Dodano urzytkownika')
        except:
            print("Błąd wprowadzania lub taki login zajęty ")

    def updateUserByObjectLogin(self, user):
        try:
            self.cursor.execute("UPDATE users SET password ='%s', first_name = '%s', last_name = '%s', permission = '%s' WHERE login = '%s' ;" %
                                (user.passwordUser, user.firstNameUser, user.lastNameUser, user.permissionUser, user.loginUser))
            self._commitDecision("Zaktualizowano urzytkownika")
        except:
            print("Błąd wprowadzania")

    def deleteUserByLogin(self, loginUser):
        try:
            self.cursor.execute("DELETE FROM users  WHERE login = '%s';" % (loginUser))
            self._commitDecision("Usunięto urzytkownika")
        except:
            print("Brak takiego loginu")
###

    def selectPatient(self):
        self.cursor.execute("SELECT id_patient, login, first_name, last_name, gender, timestampdiff(year, date_birth, now()), date_birth, phone, email, active, date_creation FROM patients ORDER BY first_name, last_name;")
        print("| %4s | %15s | %15s | %15s | %10s | %7s | %15s | %12s | %15s | %7s | %15s |" % ("ID", "Login", "Imię", "Nazwisko", "Pleć", "Wiek", "Data urodzenia", "Telefon", "Email",  "Active", "Data utworzenia"))
        for row in self.cursor.fetchall():
            print("| %4d | %15s | %15s | %15s | %10s | %7s | %15s | %12s | %15s | %7s | %15s |" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], datetime.date(row[10])))

    def selectPatientByFirstNameLastName(self, firstNamePatient, lastNamePatient):
        self.cursor.execute("SELECT id_patient, login, first_name, last_name, gender, timestampdiff(year, date_birth, now()), date_birth, phone, email, active, date_creation FROM patients "
                            "where lower(first_name) like '%s' or lower(last_name) like '%s';"
                            % ('%' +firstNamePatient.lower() + '%', '%' + lastNamePatient.lower() + '%'))
        print("| %4s | %15s | %15s | %15s | %10s | %7s | %15s | %12s | %15s | %7s | %15s |" % ("ID", "Login", "Imię", "Nazwisko",  "Pleć", "Wiek", "Data urodzenia", "Telefon", "Email",  "Active", "Data utworzenia"))
        for row in self.cursor.fetchall():
            print("| %4s | %15s | %15s | %15s | %10s | %7s | %15s | %12s | %15s | %7s | %15s |" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],  row[9],datetime.date(row[10])))

    def selectPatientByIdGetId(self, idPatient):
        self.cursor.execute("SELECT id_patient, login, first_name, last_name, gender, timestampdiff(year, date_birth, now()), date_birth, phone, email, active, date_creation FROM patients where id_patient = %s ;"
                            % (idPatient))
        print("| %4s | %15s | %15s | %15s | %10s | %7s | %15s | %12s | %15s | %7s | %15s |" % ("ID", "Login", "Imię", "Nazwisko", "Pleć", "Wiek", "Data urodzenia", "Telefon", "Email",  "Active", "Data utworzenia"))
        for row in self.cursor.fetchall():
            print("| %4d | %15s | %15s | %15s | %10s | %7s | %15s | %12s | %15s | %7s | %15s |" % (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], datetime.date(row[10])))
            self.activeIdPatient = row[0]

    def addPatientByObjectGetId(self, patient):
        try:
            self.cursor.execute("INSERT INTO patients (login, first_name, last_name, gender, date_birth,  phone, email) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" %
                                (patient.loginPatient, patient.firstNamePatient, patient.lastNamePatient, patient.genderPatient,  patient.dateBirthPatient,  patient.phonePatient, patient.emailPatient))
            self._commitDecision('Dodano pacjenta')
            return self._getIdPatientByObjectLogin(patient)
        except:
            print("Błąd wprowadzania.")

    def _getIdPatientByObjectLogin(self, patient):
        try:
            self.cursor.execute("SELECT id_patient FROM patients where login = '%s' " % (patient.loginPatient))
            self.activeIdPatient = self.cursor.fetchall()[0][0]
            return self.activeIdPatient
        except IndexError:
            self.activeIdPatient = None
            return self.activeIdPatient

    def _getIdPatientByLogin(self, loginPatient):
        try:
            self.cursor.execute("SELECT id_patient FROM patients where login = '%s' " % (loginPatient))
            self.activeIdPatient = self.cursor.fetchall()[0][0]
            return self.activeIdPatient
        except IndexError:
            self.activeIdPatient = None
            return self.activeIdPatient

    def updatePatientByObjectLoginGetId(self, patient):
        try:
            self.cursor.execute("UPDATE patients SET first_name = '%s', last_name = '%s', gender = '%s', date_birth = '%s', phone = '%s', email = '%s' WHERE login = '%s' ;" %
                                (patient.firstNamePatient, patient.lastNamePatient, patient.genderPatient, patient.dateBirthPatient, patient.phonePatient, patient.emailPatient, patient.loginPatient))
            self._commitDecision("Zaktualizowano pacjenta")
            return self._getIdPatientByObjectLogin(patient)
        except:
            print("Błąd wprowadzania")

    ### Zrobić aby nie wszyscy mogłi usuwać pacjentów

    def deletePatientByLogin(self, loginPatient):
        try:
            self.cursor.execute("DELETE FROM patients  WHERE login = '%s';" % (loginPatient))
            self._commitDecision("Usunięto pacjenta")
        except:
            print("Brak takiego loginu")
###

    def selectVPatientCommentByIdPatient(self, idPatient):
        try:
            self.cursor.execute("SELECT  number_patient_comment, date_creation, comment FROM v_patients_comments  WHERE id_patient = %s ORDER BY date_creation;" % (idPatient))
            print("| %4s | %15s | %-50s |" % ("N PK",  "Data utworzenia", "Komentarzy"))
            for row in self.cursor.fetchall():
                print("| %4s | %15s | %-50s " % (row[0], datetime.date(row[1]), row[2]))
        except:
            return "Brak Komentarzy"

    def addPatientCommentByObjectAndIdPatient(self, idPatient, comment):
        try:
            self.cursor.execute("INSERT INTO patients_comments (id_patient, comment) VALUES (%s, '%s');" % (idPatient, comment.comment))
            self._commitDecision('Dodano Komentarz do Pacjenta')
        except:
            print("Błąd wprowadzania")

    def _getIdPatientCommentByIdPatientAndNumber(self, idPatient, numberPatientComment):
        try:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT id_patient_comment FROM v_patients_comments where  id_patient = %s and number_patient_comment = %s " % (idPatient, numberPatientComment))
            idPatientComment = self.cursor.fetchall()[0][0]
            return idPatientComment
        except IndexError:
            idPatientComment = None
            return idPatientComment

    def updatePatientCommentByObjectAndIdPatientAndNumber(self, idPatient, numberPatientComment, comment):
        try:
            self.cursor.execute("UPDATE patients_comments SET comment = '%s' WHERE id_patient = %s and id_patient_comment = %s ;" %
                                (comment.comment, idPatient, self._getIdPatientCommentByIdPatientAndNumber(idPatient, numberPatientComment)))
            self._commitDecision("Zaktualizowano komentarz")
        except:
            print("Błąd wprowadzania")

    def deletePatientCommentByIdPatientAndNumber(self, idPatient, numberPatientComment):
        try:
            self.cursor.execute("DELETE FROM patients_comments  WHERE id_patient = %s and id_patient_comment = %s ;" % (idPatient,
                                self._getIdPatientCommentByIdPatientAndNumber(idPatient, numberPatientComment)))
            self._commitDecision("Usunięto komentarz")
        except:
            print("Brak takiego komentarza")
###

    # def selectVDietByIdPatient(self, idPatient):
    #     self.cursor.execute("SELECT number_diet, name_diet, height, weight, weight_target, activity, waist, hips, water, fat_tissue, muscle_tissue, date_diet, active "
    #                         "FROM v_diets WHERE id_patient = %s ORDER BY date_diet;" % (idPatient))
    #     print("| %4s |  %11s | %30s | %6s | %6s | %8s | %10s | %7s | %7s | %7s | %13s | %13s | %8s | %8s | %7s |" %
    #           ("N D",  "Data Diety", "Nazwa Diety", "Wzrost", "Waga", "Waga cel", "Aktywność",  "Talia", "Biodra", "Woda", "Tkanka tłusz.", "Tkanka mięśn.", "BMI", "WHR", "Aktywna"))
    #     patient_diets = self.cursor.fetchall()
    #     for row in patient_diets:
    #         print("| %4s |  %11s | %30s | %6s | %6s | %8s | %10s | %7s | %7s | %7s | %13s | %13s | %8s | %8s | %7s |" %
    #               (row[0], datetime.date(row[11]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], round(row[3]/(row[2]/100)**2,2),
    #                (0 if row[9] == None else round(row[6]/row[7],2)), row[12]))

    def selectVDietByIdPatient(self, idPatient):
        self.cursor.execute("SELECT number_diet, name_diet, height, weight, weight_target, activity, waist, hips, water, fat_tissue, muscle_tissue, date_diet, active "
                            "FROM v_diets WHERE id_patient = %s ORDER BY date_diet;" % (idPatient))
        print("| %4s |  %11s | %30s | %6s | %6s | %8s | %10s | %7s | %7s | %7s | %13s | %13s | %8s | %8s | %7s |" %
              ("N D",  "Data Diety", "Nazwa Diety", "Wzrost", "Waga", "Waga cel", "Aktywność",  "Talia", "Biodra", "Woda", "Tkanka tłusz.", "Tkanka mięśn.", "BMI", "WHR", "Aktywna"))
        patient_diets = self.cursor.fetchall()
        patient_diets_n = []
        for row in patient_diets:
            row_n = [row[0], datetime.date(row[11]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], round(row[3]/(row[2]/100)**2,2),
                   (0 if row[9] == None else round(row[6]/row[7],2)), row[12]]
            patient_diets_n.append(row_n)
            print("| %4s |  %11s | %30s | %6s | %6s | %8s | %10s | %7s | %7s | %7s | %13s | %13s | %8s | %8s | %7s |" %
                  (row_n[0], row_n[1], row_n[2], row_n[3], row_n[4], row_n[5], row_n[6], row_n[7], row_n[8], row_n[9], row_n[10], row_n[11], row_n[12],
                   row_n[13], row_n[14]))
        # repr graficzne
        # x_label = ["N D", "Data Diety", "Nazwa Diety", "Wzrost", "Waga", "Waga cel", "Aktywność",  "Talia", "Biodra", "Woda", "Tkanka tłusz.", "Tkanka mięśn.", "BMI",
        #            "WHR", "Aktywna"]
        df_diets = pd.DataFrame(patient_diets_n)

        plt.figure(1, figsize=[14,6])
        plt.subplot(2,2,1)
        plt.barh(df_diets[2], df_diets[4])
        plt.title('Waga pacjenta po dietach')
        plt.subplot(2,2,2)
        plt.plot(df_diets[2], df_diets[4], "r--", label='waga')
        plt.plot(df_diets[2], df_diets[5], "g--", label='waga docelowa')
        plt.plot(df_diets[2], df_diets[12], "b--", label='BMI')
        plt.legend()
        plt.title('Waga pacjenta po dietach vs BMI')
        plt.subplot(2,2,3)
        plt.plot(df_diets[2], df_diets[9], "g--", label='woda')
        plt.plot(df_diets[2], df_diets[10], "b--", label='tkanka tłuszczowa')
        plt.plot(df_diets[2], df_diets[11], "r--", label='tkanka mięśniowa')
        plt.legend()
        plt.title('Woda vs Tkanka tłusz. vs Tkanka mięśn.')
        plt.subplot(2,2,4)
        plt.plot(df_diets[2], df_diets[13], "g--", label='WHR')
        plt.plot(df_diets[2], df_diets[7], "b--", label='Talia')
        plt.plot(df_diets[2], df_diets[8], "r--", label='Biodra')
        plt.legend()
        plt.title('WHR vs Talia vs Biodra')

        plt.savefig('patient_diets')
        plt.tight_layout()
        plt.show()

    def selectVDietByIdAndIdPatientGetId(self, idPatient, idDiet):
        self.cursor.execute("SELECT number_diet, name_diet, height, weight, weight_target, activity, waist, hips, water, fat_tissue, muscle_tissue, date_diet, active "
                            "FROM v_diets WHERE id_patient = %s and id_diet = %s ORDER BY date_diet;" % (idPatient, idDiet))
        print("| %4s |  %11s | %30s | %6s | %6s | %8s | %10s | %7s | %7s | %7s | %13s | %13s | %8s | %8s | %7s |" %
              ("N D",  "Data Diety", "Nazwa Diety", "Wzrost", "Waga", "Waga cel", "Aktywność",  "Talia", "Biodra", "Woda", "Tkanka tłusz.", "Tkanka mięśn.", "BMI",  "WHR", "Aktywna"))
        for row in self.cursor.fetchall():
            print("| %4s |  %11s | %30s | %6s | %6s | %8s | %10s | %7s | %7s | %7s | %13s | %13s | %8s | %8s | %7s |" %
                  (row[0], datetime.date(row[11]), row[1], row[2], row[3], row[4], row[5], row[6], row[7], (row[8]), row[9], row[10], round(row[3]/(row[2]/100)**2,2),
                   (0 if row[9] == None else round(row[6]/row[7],2)), row[12]))
            self.activeIdDiet = row[0]

    def addDietByObjectAndIdUserAndIdPatientGetId(self, idUser, idPatient, diet):
        try:
            self.cursor.execute("INSERT INTO diets (id_user, id_patient, name_diet, height, weight, weight_target, activity, waist, hips , water, fat_tissue, muscle_tissue) "
                                "VALUES (%s, %s, '%s', %s, %s, %s, '%s', %s,  %s, %s, %s, %s); " %
            (idUser, idPatient, diet.nameDiet, diet.height, diet.weight, diet.weightTarget, diet.activity, diet.waist, diet.hips, diet.water, diet.fatTissue, diet.muscleTissue))
            self._commitDecision('Dodano dietę')
            self.activeIdDiet = self.cursor.lastrowid
        except:
            print("Błąd wprowadzania")

    def _getIdDietByNumber(self, numberDiet):
        try:
            self.cursor.execute("SELECT id_diet FROM v_diets where number_diet = %s " % (numberDiet))
            self.activeIdDiet = self.cursor.fetchall()[0][0]
            return self.activeIdDiet
        except IndexError:
            self.activeIdDiet = None
            return self.activeIdDiet

    def updateDietByObjectAndNumberAndIdPatientGetId(self, idPatient, numberDiet, diet):
        try:
            self.cursor.execute("UPDATE diets SET name_diet = '%s', height = %s, weight = %s, weight_target = %s, activity = '%s', waist = %s, hips = %s, water = %s, fat_tissue = %s, muscle_tissue = %s "
                                "WHERE id_diet = %s and id_patient = %s;" %
                                (diet.nameDiet, diet.height, diet.weight, diet.weightTarget, diet.activity, diet.waist, diet.hips, diet.water, diet.fatTissue, diet.muscleTissue,
                                 self._getIdDietByNumber(numberDiet), idPatient))
            self._commitDecision("Zaktualizowano dietę")
            self.activeIdDiet = self._getIdDietByNumber(numberDiet)
        except:
            print("Błąd wprowadzania")

    def deleteDietByNumber(self, idPatient, numberDiet):
        try:
            self.cursor.execute("DELETE FROM diets  WHERE id_diet = %s and id_patient = %s;" % (self._getIdDietByNumber(numberDiet), idPatient))
            self._commitDecision("Usunięto dietę")
        except:
            print("Brak takiego ID ")
###

    def selectVDietCommentByIdDiet(self, idDiet):
        try:
            self.cursor.execute("SELECT  number_diet_comment, date_creation, comment FROM v_diets_comments  WHERE id_diet = %s ORDER BY date_creation;" % (idDiet))
            print("| %4s | %15s | %-50s |" % ("N DK",  "Data utworzenia", "Komentarzy"))
            for row in self.cursor.fetchall():
                print("| %4s | %15s | %-50s " % (row[0], datetime.date(row[1]), row[2]))
        except:
            return "Brak Komentarzy"

    def addDietCommentByObjectAndIdDiet(self, idDiet, comment):
        try:
            self.cursor.execute("INSERT INTO diets_comments (id_diet, comment) VALUES (%s, '%s');" % (idDiet, comment.comment))
            self._commitDecision('Dodano Komentarz do Diety')
        except:
            print("Błąd wprowadzania")

    def _getIdDietCommentByIdDietAndNumber(self, idDiet, numberDietComment):
        try:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT id_diet_comment FROM v_diets_comments where  id_diet = %s and number_diet_comment = %s " % (idDiet, numberDietComment))
            idDietComment = self.cursor.fetchall()[0][0]
            return idDietComment
        except IndexError:
            idDietComment = None
            return idDietComment

    def updateDietCommentByObjectAndIdDietAndNumber(self, idDiet, numberDietComment, comment):
        try:
            self.cursor.execute("UPDATE diets_comments SET comment = '%s' WHERE id_diet = %s and id_diet_comment = %s ;" %
                                (comment.comment, idDiet, self._getIdDietCommentByIdDietAndNumber(idDiet, numberDietComment)))
            self._commitDecision("Zaktualizowano komentarz")
        except:
            print("Błąd wprowadzania")

    def deleteDietCommentByIdDietAndNumber(self, idDiet, numberDietComment):
        try:
            self.cursor.execute("DELETE FROM diets_comments  WHERE id_diet = %s and id_diet_comment = %s ;" % (idDiet, self._getIdDietCommentByIdDietAndNumber(idDiet, numberDietComment)))
            self._commitDecision("Usunięto komentarz")
        except:
            print("Brak takiego komentarza")
###

    def selectProductByName(self, nazwaPolska):
        print("Lista Produktów")
        self.cursor.execute("SELECT id_product, name_db, nazwa_polska, bialko_ogolem_g, bialko_zwierzece_g, bialko_roslinne_g, tluszcz_g, weglowodany_ogolem_g, weglowodany_przyswajalne_g, "
                            "energia_kcal, odpadki_proc FROM products WHERE nazwa_polska like '%s' ORDER BY id_product ;" % ('%' + nazwaPolska + '%'))
        print("| %8s | %9s | %9s | %8s | %8s | %14s | %10s | %10s | %5s | %5s | %-40s"
              % ("Biał_g", "Biał_zw_g", "Biał_ro_g", "Tłu_g", "Węgło_g",  "Węgłow_prz_g",  "Energ_kcal",  "Odpadki_pr", "ID", "DB", "Nazwa"))
        for row in self.cursor.fetchall():
            print("| %8s | %9s | %9s | %8s | %8s | %14s | %10s | %10s | %5s | %5s | %-40s" % (row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[0], row[1], row[2]))

    def addProductByObjectGetId(self, product):
        try:
            # cursor = self.connect.cursor()
            self.cursor.execute("INSERT INTO products (nazwa_polska, bialko_ogolem_g, bialko_zwierzece_g, bialko_roslinne_g, tluszcz_g, weglowodany_ogolem_g, "
                                "weglowodany_przyswajalne_g, energia_kcal, odpadki_proc) VALUES ('%s', %s, %s, %s, %s, %s, %s, %s, %s);" %
                                (product.nazwaPolska, product.bialkoOgolemG, product.bialkoZwierzeceG, product.bialkoRoslinneG, product.tluszczG, product.weglowodanyOgolemG,
                                 product.weglowodanyPrzyswajalneG, product.energiaKcal, product.odpadkiProc))
            self._commitDecision('Dodano produkt')
            # self.activeIdProduct = self.cursor.lastrowid
        except:
            print("Błąd wprowadzania ")

    def updateProductByObjectAndIdGetId(self, idProduct, product):
        try:
            self.cursor.execute("UPDATE products SET nazwa_polska = '%s', bialko_ogolem_g = %s, bialko_zwierzece_g = %s, bialko_roslinne_g = %s, tluszcz_g = %s, weglowodany_ogolem_g = %s,"
                                "weglowodany_przyswajalne_g = %s, energia_kcal = %s, odpadki_proc = %s WHERE idProduct = %s ;" %
                                (product.nazwaPolska, product.bialkoOgolemG, product.bialkoZwierzeceG, product.bialkoRoslinneG, product.tluszczG, product.weglowodanyOgolemG,
                                 product.weglowodanyPrzyswajalneG, product.energiaKcal, product.odpadkiProc, idProduct))
            self._commitDecision("Zaktualizowano produkt")
            # self.activeIdProduct = self.cursor.lastrowid
        except:
            print("Błąd wprowadzania")

    def deleteProductById(self, idProduct):
        try:
            self.cursor.execute("DELETE FROM products  WHERE name_db = 'new' and id_product = '%s';" % (idProduct))
            self._commitDecision("Usunięto produkt")
        except:
            print("Brak takiego produktu lub nie możesz usunąć tego produktu")
###

    # def selectVDietProductAndProductByIdDiet(self, idDiet):
    #     try:
    #         self.cursor.execute("select number_diet_product, time_of_date, id_product, nazwa_polska, "
    #                             "product_quantity, bialko_ogolem_g, bialko_zwierzece_g, bialko_roslinne_g, tluszcz_g, weglowodany_ogolem_g, weglowodany_przyswajalne_g, energia_kcal "
    #                             "from v_diets_products Where id_diet = %s ORDER BY id_diet, number_diet_product; " % (idDiet))
    #         print("| %4s | %14s | %6s | %-50s | %6s | %6s | %9s | %9s | %8s | %8s | %10s | %9s | %-6s " %
    #               ("N DP",  "Pora Dnia", "ID PRO", "Nazwa Polska", "ILość", "Biał_g","Biał_zw_g","Biał_ro_g","Tłusz_g","Wegł_g","Wegł_prz_g","Ener_kcal", "BTW"))
    #         row_5, row_6, row_7, row_8, row_9, row_10, row_11 = 0, 0, 0, 0, 0, 0, 0
    #         for row in patient_diet:
    #             print("| %4s | %-14s | %6s | %-50s | %6s | %6s | %9s | %9s | %8s | %8s | %10s | %9s | 1:%s:%s " %
    #                   (row[0], row[1], row[2], row[3], row[4], round(row[5]/100*row[4],2), round(row[6]/100*row[4],2), round(row[7]/100*row[4],2), round(row[8]/100*row[4],2),
    #                   round(row[9]/100*row[4],2), round(row[10]/100*row[4],2), round(row[11]/100*row[4],2), round((row[8]*9)/(row[5]*4)), round((row[9]*4)/(row[5]*4)) ))
    #             row_5 += row[5] / 100*row[4]
    #             row_6 += row[6] / 100*row[4]
    #             row_7 += row[7] / 100*row[4]
    #             row_8 += row[8] / 100*row[4]
    #             row_9 += row[9] / 100*row[4]
    #             row_10 += row[10] / 100*row[4]
    #             row_11 += row[11] / 100*row[4]
    #         print("| %4s | %-14s | %6s | %-50s | %6s | %6s | %9s | %9s | %8s | %8s | %10s | %9s | 1:%s:%s " %
    #               ('', '', '', 'Podsumowanie', '', round(row_5,2), round(row_6,2), round(row_7,2), round(row_8,2), round(row_9,2), round(row_10,2), round(row_11,2),
    #                round((row_8*9)/(row_5*4)), round((row_9*4)/(row_5*4)) ))
    #     except:
    #         return "Brak Diety"

    def selectVDietProductAndProductByIdDiet(self, idDiet):
        try:
            self.cursor.execute("select number_diet_product, time_of_date, id_product, nazwa_polska, "
                                "product_quantity, bialko_ogolem_g, bialko_zwierzece_g, bialko_roslinne_g, tluszcz_g, weglowodany_ogolem_g, weglowodany_przyswajalne_g, energia_kcal "
                                "from v_diets_products Where id_diet = %s ORDER BY id_diet, number_diet_product; " % (idDiet))
            print("| %4s | %14s | %6s | %-50s | %6s | %6s | %9s | %9s | %8s | %8s | %10s | %9s | %7s |" %
                  ("N DP",  "Pora Dnia", "ID PRO", "Nazwa Polska", "ILość", "Biał_g","Biał_zw_g","Biał_ro_g","Tłusz_g","Wegł_g","Wegł_prz_g","Ener_kcal", "BTW"))
            row_5, row_6, row_7, row_8, row_9, row_10, row_11 = 0, 0, 0, 0, 0, 0, 0
            patient_diet = self.cursor.fetchall()
            patient_diet_n = []
            for row in patient_diet:
                row_n = [row[0], row[1], row[2], row[3], row[4], round(row[5]/100*row[4],2), round(row[6]/100*row[4],2), round(row[7]/100*row[4],2), round(row[8]/100*row[4],2),
                      round(row[9]/100*row[4],2), round(row[10]/100*row[4],2), round(row[11]/100*row[4],2), round((row[8]*9)/(row[5]*4)), round((row[9]*4)/(row[5]*4)) ]
                patient_diet_n.append(row_n)
                print("| %4s | %-14s | %6s | %-50s | %6s | %6s | %9s | %9s | %8s | %8s | %10s | %9s | 1:%2s:%2s |" %
                      (row_n[0], row_n[1], row_n[2], row_n[3], row_n[4], row_n[5], row_n[6], row_n[7], row_n[8],
                      row_n[9], row_n[10], row_n[11], row_n[12], row_n[13]))
                row_5 += row[5] / 100*row[4]
                row_6 += row[6] / 100*row[4]
                row_7 += row[7] / 100*row[4]
                row_8 += row[8] / 100*row[4]
                row_9 += row[9] / 100*row[4]
                row_10 += row[10] / 100*row[4]
                row_11 += row[11] / 100*row[4]
            print("| %4s | %-14s | %6s | %-50s | %6s | %6s | %9s | %9s | %8s | %8s | %10s | %9s | 1:%2s:%2s |" %
                  ('', '', '', 'Podsumowanie', '', round(row_5,2), round(row_6,2), round(row_7,2), round(row_8,2), round(row_9,2), round(row_10,2), round(row_11,2),
                   round((row_8*9)/(row_5*4)), round((row_9*4)/(row_5*4)) ))
            # repr graficzne
            df_diet = pd.DataFrame(patient_diet_n)

            plt.figure(1, figsize=[10, 6])
            plt.subplot(1, 1, 1)
            plt.pie(df_diet[11], labels=df_diet[1], startangle=90)
            plt.title('Energia w ciągu dnia')

            plt.savefig('diet')
            plt.tight_layout()
            plt.show()
        except:
            return "Brak Diety"

    def addDietProductByObjectAndIdDietAndIdProduct(self, idDiet, idProduct, dietProduct):
        try:
            self.cursor.execute("INSERT INTO diets_products (id_diet, id_product, time_of_date, product_quantity) VALUES (%s, %s, '%s', %s);" %
                                (idDiet, idProduct, dietProduct.timeOfDate, dietProduct.productQuantity))
            self._commitDecision('Dodano Produkt do diety')
        except:
            print("Błąd wprowadzania")

    def _getIdDietProductByIdDietAndNumber(self, idDiet, numberDietProduct):
        try:
            self.cursor = self.connect.cursor()
            self.cursor.execute("SELECT id_diet_product FROM v_diets_products where  id_diet = %s and number_diet_product = %s  " % (idDiet, numberDietProduct))
            self.activeIdDietProduct = self.cursor.fetchall()[0][0]
            return self.activeIdDietProduct
        except IndexError:
            self.activeIdDietProduct = None
            return self.activeIdDietProduct

    def updateDietProductByObjectAndIdDietAndNumber(self, idDiet, numberDietProduct, dietProduct):

        try:
            self.cursor.execute("UPDATE diets_products SET time_of_date = '%s', product_quantity = %s WHERE id_diet_product = %s and id_diet = %s ;" %
                                (dietProduct.timeOfDate, dietProduct.productQuantity, self._getIdDietProductByIdDietAndNumber(idDiet, numberDietProduct), idDiet))
            self._commitDecision("Zaktualizowano produkt w diecie")
        except:
            print("Błąd wprowadzania")

    def deleteDietProductByNumberAndIdDiet(self, idDiet, numberDietProduct):
        try:
            self.cursor.execute("DELETE FROM diets_products  WHERE id_diet_product = %s and id_diet = %s ;" %
                                (self._getIdDietProductByIdDietAndNumber(idDiet, numberDietProduct), idDiet))
            self._commitDecision("Usunięto produkt z diety")
        except:
            print("Brak takiego produktu w diecie")





# dbManager = DatabaseManager()
# dbManager.selectVDietByIdPatient(1)
# print()
# dbManager.selectVDietProductAndProductByIdDiet(1)

