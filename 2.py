import pyAesCrypt

password = input('Пароль для шифрования файла: ')

#Зашифровать
# pyAesCrypt.encryptFile('file.txt', 'file.txt.aes', password)

#Расшифровать
pyAesCrypt.decryptFile('file.txt.aes', 'fileout.txt', password)