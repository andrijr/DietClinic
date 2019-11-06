from diet_clinic.objects import User, Patient, Comment, Diet, DietProduct, Product
from diet_clinic.database_manager import DatabaseManager



dbManager = DatabaseManager()
dbManager.selectVDietByIdPatient(1)
print()
dbManager.selectVDietProductAndProductByIdDiet(1)

