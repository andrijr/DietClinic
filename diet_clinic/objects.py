

class User:

    def __init__(self, loginUser, passwordUser, firstNameUser, lastNameUser, permissionUser='role_doctor'):
        self.loginUser = loginUser
        self.passwordUser = passwordUser
        self.firstNameUser = firstNameUser
        self.lastNameUser = lastNameUser
        self.permissionUser = permissionUser

    def __str__(self):
        return "Login: " + self.loginUser + " | Imię: " + self.firstNameUser + " | Nazwisko: " + self.lastNameUser + ' | Permission: ' + self.permissionUser


class Patient:

    def __init__(self, loginPatient, firstNamePatient, lastNamePatient,  genderPatient, dateBirthPatient,  phonePatient='', emailPatient=''):
        self.loginPatient = loginPatient
        self.firstNamePatient = firstNamePatient
        self.lastNamePatient = lastNamePatient
        self.genderPatient = genderPatient
        self.dateBirthPatient = dateBirthPatient
        self.phonePatient = phonePatient
        self.emailPatient = emailPatient


class Comment:

    def __init__(self, comment):
        self.comment = comment


class Diet:

    def __init__(self, nameDiet, height, weight, weightTarget=None, activity=None, waist=None, hips=None, water=None, fatTissue=None, muscleTissue=None):
        self.nameDiet = nameDiet
        self.height = height
        self.weight = weight
        self.weightTarget = weightTarget
        self.activity = activity
        self.waist = waist
        self.hips = hips
        self.water = water
        self.fatTissue = fatTissue
        self.muscleTissue = muscleTissue


class DietProduct:

    def __init__(self, timeOfDate, productQuantity):
        self.timeOfDate = timeOfDate
        self.productQuantity = productQuantity


class Product:
    def __init__(self, nazwaPolska, bialkoOgolemG, bialkoZwierzeceG, bialkoRoslinneG, tluszczG, weglowodanyOgolemG, weglowodanyPrzyswajalneG, energiaKcal, odpadkiProc=None):
        self.nazwaPolska = nazwaPolska
        self.bialkoOgolemG = bialkoOgolemG
        self.bialkoZwierzeceG = bialkoZwierzeceG
        self.bialkoRoslinneG = bialkoRoslinneG
        self.tluszczG = tluszczG
        self.weglowodanyOgolemG = weglowodanyOgolemG
        self.weglowodanyPrzyswajalneG = weglowodanyPrzyswajalneG
        self.energiaKcal = energiaKcal
        self.odpadkiProc = odpadkiProc

    def productRepr(self):
        return self.nazwaPolska, self.bialkoOgolemG, self.bialkoZwierzeceG, self.bialkoRoslinneG, self.tluszczG, self.weglowodanyOgolemG, self.weglowodanyPrzyswajalneG, \
               self.energiaKcal, self.odpadkiProc


