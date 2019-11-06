from diet_clinic.objects import User, Patient, Comment, Diet, DietProduct, Product
from diet_clinic.database_manager import DatabaseManager



dbManager = DatabaseManager()
welcomeDietClinic = True
while dbManager.loginDatabaseOk == True:
    while welcomeDietClinic==True:
        print("Witamy w DIET CLINIC")
        dbManager.selectUser()
        loginUser = input('Podaj login: ')
        passwordUser = input("Podaj hasło: ")
        decisionLoginUser = dbManager.loginUser(loginUser, passwordUser)
        if decisionLoginUser == 'konto_zablokowane':
            print('Konto Zablokowane')
            break
        elif decisionLoginUser == 'bledne_haslo':
            print('Błędne Hasło')
            break

        while decisionLoginUser == 'role_admin':
            print("Panel Administratora")
            main = input("L - lista użytkowników, D - dodaj użytkownika, Z - zaktualizuj użytkownika, O - odblokuj użytkownika, X - zablokuj użytkownika, "
                "U - usuń użytkownika, P - panel dietetyka, Q - wyloguj ")
            if main.upper() == 'L':
                print("Lista Użytkowników")
                dbManager.selectUser()
            elif main.upper() == 'D':
                user = User(input("Podaj login* "), input("Podaj Hasło* "), input("Podaj Imię* "), input("Podaj Nazwisko* "), input("Podaj role_admin / role_doctor "))
                dbManager.addUserByObject(user)
            elif main.upper() == 'Z':
                user = User(input("Podaj login* "), input("Podaj Hasło* "), input("Podaj Imię* "), input("Podaj Nazwisko* "), input("Podaj role_admin / role_doctor "))
                dbManager.updateUserByObjectLogin(user)
            elif main.upper() == 'U':
                loginUser = input("Podaj login* ")
                dbManager.deleteUserByLogin(loginUser)
            elif main.upper() == 'O':
                loginUser = input("Podaj login* ")
                dbManager._updateUserAccountBlockingByLogin(loginUser, 0)
                dbManager._updateUserActiveByLogin(loginUser, 1)
            elif main.upper() == 'X':
                loginUser = input("Podaj login* ")
                dbManager._updateUserActiveByLogin(loginUser, 0)
            elif main.upper() == 'P':
                decisionLoginUser = 'role_doctor'
            elif main.upper() == 'Q':
                print("Wylogowano z panelu Administratora")
                dbManager.connect.close()
                # welcomeDietClinic = False
                exit()


        while decisionLoginUser == 'role_doctor':
            print("Panel Lekarski")
            # print("User:", dbManager.activeIdUser, "Patient:", dbManager.activeIdPatient, "Dieta:", dbManager.activeIdDiet, "Product:", dbManager.activeIdProduct, "DietaProduct:", dbManager.activeIdDietProduct)
            main = input("P - wybierz pacjenta, L - lista pacjentów, W - wyszukaj pacjenta,  D - dodaj pacjenta, Z - zaktualizuj pacjenta, U - usuń pacjenta,  Q - wyloguj ")
            if main.upper() == 'L':
                print("Lista pacjentów:")
                dbManager.selectPatient()
            elif main.upper() == 'W':
                firstNamePatient = input("Podaj imię* ")
                lastNamePatient = input("Podaj Nazwisko* ")
                print("Lista pacjentów:")
                dbManager.selectPatientByFirstNameLastName(firstNamePatient, lastNamePatient)
            elif main.upper() == 'D':
                patient = Patient(input("Podaj login* "), input("Podaj Imię* "), input("Podaj Nazwisko* "),  input("Płeć* "), input("Data urodzenia "),  input("Telefon "), input("Email "))
                dbManager.addPatientByObjectGetId(patient)
            elif main.upper() == 'Z':
                patient = Patient(input("Podaj login* "), input("Podaj Imię* "), input("Podaj Nazwisko* "),  input("Płeć* "), input("Data urodzenia "),  input("Telefon "), input("Email "))
                dbManager.updatePatientByObjectLoginGetId(patient)
            elif main.upper() == 'U':
                loginPatient = input("Podaj login* ")
                dbManager.deletePatientByLogin(loginPatient)
            elif main.upper() == 'Q':
                print("Wylogowano z panelu Lekarskiego")
                dbManager.connect.close()
                # welcomeDietClinic = False
                exit()

            elif main.upper() == 'P':
                loginPatient = input("Podaj login pacjenta* ")
                dbManager._getIdPatientByLogin(loginPatient)
                while dbManager.activeIdPatient != None:
                    # print("User:", dbManager.activeIdUser, "Patient:", dbManager.activeIdPatient, "Dieta:", dbManager.activeIdDiet, "Product:", dbManager.activeIdProduct, "DietaProduct:", dbManager.activeIdDietProduct)
                    print("Pacjent")
                    dbManager.selectPatientByIdGetId(dbManager.activeIdPatient)
                    print("Komentarzy:")
                    dbManager.selectVPatientCommentByIdPatient(dbManager.activeIdPatient)
                    print("Diety:")
                    dbManager.selectVDietByIdPatient(dbManager.activeIdPatient)
                    main = input("P - wybierz dietę, D - dodaj dietę, Z - zaktualizuj dietę, U - usuń dietę, \n"
                                 "LK - lista Komentarzy, DK - dodaj komentarz, ZK - zaktualizuj komentarz, UK - usuń komentarz, Q - Wyjdź z panelu pacjenta ")
                    if main.upper() == 'LK':
                        print("Komentarzy:")
                        dbManager.selectVPatientCommentByIdPatient(dbManager.activeIdPatient)
                    elif main.upper() == 'DK':
                        comment = Comment(input('Dodaj komentarz do pacjenta: '))
                        dbManager.addPatientCommentByObjectAndIdPatient(dbManager.activeIdPatient, comment)
                    elif main.upper() == 'ZK':
                        numberPatientComment = input('Podaj Numer komentarza: ')
                        comment = Comment(input('Dodaj komentarz do pacjenta: '))
                        dbManager.updatePatientCommentByObjectAndIdPatientAndNumber(dbManager.activeIdPatient, numberPatientComment, comment)
                    elif main.upper() == 'UK':
                        numberPatientComment = input('Podaj Numer komentarza pacjenta: ')
                        dbManager.deletePatientCommentByIdPatientAndNumber(dbManager.activeIdPatient, numberPatientComment)
                    elif main.upper() == 'D':
                        diet = Diet(input("Nazwa diety* "), input("Wzrost* "), input("Waga* "),  input("Waga docelowa* "),
                                    input("Aktywność* Wyczynowy / Bardzo aktywny / Aktywny / Umiarkowany / Niska aktywność / Osoba leżąca  "),
                                    input("Talia* "), input("Biodra* "), input("Woda* "), input("Tkanka tłuszczowa* "), input("Tkanka mięśniowa* "))
                        dbManager.addDietByObjectAndIdUserAndIdPatientGetId(dbManager.activeIdUser, dbManager.activeIdPatient, diet)
                    elif main.upper() == 'Z':
                        numberDiet = input("Podaj Numer Diety* ")
                        diet = Diet(input("Nazwa diety* "), input("Wzrost* "), input("Waga* "),  input("Waga docelowa* "),
                                    input("Aktywność* Wyczynowy / Bardzo aktywny / Aktywny / Umiarkowany / Niska aktywność / Osoba leżąca  "),
                                    input("Talia* "), input("Biodra* "), input("Woda* "), input("Tkanka tłuszczowa* "), input("Tkanka mięśniowa* "))
                        dbManager.updateDietByObjectAndNumberAndIdPatientGetId(dbManager.activeIdPatient, numberDiet, diet)
                    elif main.upper() == 'U':
                        numberDiet = input("Podaj Numer Diety do usunięcia* ")
                        dbManager.deleteDietByNumber(dbManager.activeIdPatient, numberDiet)
                    elif main.upper() == 'Q':
                        dbManager.activeIdPatient = None
                    elif main.upper() == 'P':
                        numberDiet = input("Podaj Numer Diety* ")
                        print("Dieta")
                        dbManager._getIdDietByNumber(numberDiet)
                        while dbManager.activeIdDiet != None:
                            print("Pacjent:")
                            dbManager.selectPatientByIdGetId(dbManager.activeIdPatient)
                            print("Komentarzy:")
                            dbManager.selectVPatientCommentByIdPatient(dbManager.activeIdPatient)
                            print("Dieta:")
                            dbManager.selectVDietByIdAndIdPatientGetId(dbManager.activeIdPatient, dbManager.activeIdDiet)
                            print("Komentarzy do Diety:")
                            dbManager.selectVDietCommentByIdDiet(dbManager.activeIdDiet)
                            print("Produkty Diety")
                            dbManager.selectVDietProductAndProductByIdDiet(dbManager.activeIdDiet)
                            # print("User:", dbManager.activeIdUser, "Patient:", dbManager.activeIdPatient, "Dieta:", dbManager.activeIdDiet, "Product:", dbManager.activeIdProduct, "DietaProduct:", dbManager.activeIdDietProduct)
                            main = input("W - wyszukaj produkt, D - dodaj produkt do diety, Z - zaktualizuj produkt w diecie, U - usuń produkt w diecie, \n"
                                         "LK - lista komentarzy diety, DK - dodaj komentarz do diety, ZK - zaktualizuj komentarz do diety, UK - usuń komentarz z diety, \n"
                                         "DP - dodaj produkt, ZP - zaktualizuj produkt, UP - usuń produkt, Q - Wyjdź z diety ")
                            if main.upper() == 'LK':
                                print("Komentarzy do Diety:")
                                dbManager.selectVDietCommentByIdDiet(dbManager.activeIdDiet)
                            elif main.upper() == 'DK':
                                comment = Comment(input('Dodaj komentarz do diety: '))
                                dbManager.addDietCommentByObjectAndIdDiet(dbManager.activeIdDiet, comment)
                            elif main.upper() == 'ZK':
                                numberDietComment = input('Podaj Numer Komentarza* ')
                                comment = Comment(input('Dodaj komentarz do diety: '))
                                dbManager.updateDietCommentByObjectAndIdDietAndNumber(dbManager.activeIdDiet, numberDietComment, comment)
                            elif main.upper() == 'UK':
                                numberDietComment = input('Podaj Numer Komentarza* ')
                                dbManager.deleteDietCommentByIdDietAndNumber(dbManager.activeIdDiet, numberDietComment)
                            elif main.upper() == 'W':
                                print("Wybierz produkt z listy po ID: ")
                                dbManager.selectProductByName(input("Wyszukaj nazwę produktu: "))
                            elif main.upper() == 'D':
                                idProduct = input("Podaj ID produktu ")
                                dietProduct = DietProduct(input("Podaj porę dnia 1_Sniadanie 2_Sniadanie 3_Obiad 4_Podwieczorek 5_Kolacja "), input("Podaj ilość w gramach "))
                                dbManager.addDietProductByObjectAndIdDietAndIdProduct(dbManager.activeIdDiet, idProduct, dietProduct)
                            elif main.upper() == 'Z':
                                numberDietProduct = input("Podaj Numer produktu na liście ")
                                dietProduct = DietProduct(input("Podaj porę dnia 1_Sniadanie 2_Sniadanie 3_Obiad 4_Podwieczorek 5_Kolacja "), input("Podaj ilość w gramach "))
                                dbManager.updateDietProductByObjectAndIdDietAndNumber(dbManager.activeIdDiet, numberDietProduct, dietProduct)
                            elif main.upper() == 'U':
                                numberDietProduct = input("Podaj Numer produktu na liście ")
                                dbManager.deleteDietProductByNumberAndIdDiet(dbManager.activeIdDiet, numberDietProduct)
                            elif main.upper() == 'DP':
                                product = Product(input("Nazwa Polska* "), float(input("Białko Ogółem g* ")), float(input("Białko zwierzęce g* ")),  float(input("Białko roślinne g* ")),
                                                  float(input("Tłuszcz* ")), float(input("Węglowodany ogółem g* ")), float(input("Węglowodany przyswajalne g* ")),
                                                  float(input("Energia kcal* ")), float(input("Odpadki procent* ")))
                                dbManager.addProductByObjectGetId(product)
                            elif main.upper() == 'ZP':
                                idProduct = input("Podaj ID produktu ")
                                product = Product(input("Nazwa Polska* "), float(input("Białko Ogółem g* ")), float(input("Białko zwierzęce g* ")),  float(input("Białko roślinne g* ")),
                                                  float(input("Tłuszcz* ")), float(input("Węglowodany ogółem g* ")), float(input("Węglowodany przyswajalne g* ")),
                                                  float(input("Energia kcal* ")), float(input("Odpadki procent* ")))
                                dbManager.updateProductByObjectAndIdGetId(idProduct, product)
                            elif main.upper() == 'DP':
                                idProduct = input("Podaj ID produktu ")
                                dbManager.deleteProductById(idProduct)

                            elif main.upper() == 'Q':
                                dbManager.activeIdDiet = None


else:
    print(dbManager)