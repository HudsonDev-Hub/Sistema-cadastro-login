import datetime

class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        try:
            self.file = open(self.filename, "r")
            self.users = {}
            for line in self.file:
                email, password, name, created = line.strip().split(";")
                self.users[email] = (password, name, created)
            self.file.close()
        except FileNotFoundError:
            # Se o arquivo não existir, criar um dicionário vazio
            self.users = {}

    def get_user(self, email):
        return self.users.get(email, -1)

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email.strip()] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email já existe!")
            return -1

    def validate(self, email, password):
        user = self.get_user(email)
        if user != -1:
            return user[0] == password
        else:
            return False

    def save(self):
        with open(self.filename, "w") as f:
            for user in self.users:
                f.write(
                    user + ";" +
                    self.users[user][0] + ";" +
                    self.users[user][1] + ";" +
                    self.users[user][2] + "\n"
                )

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]


# -------------------------------
# Programa principal com menu
# -------------------------------
def main():
    db = DataBase("users.txt")

    while True:
        print("\n=== MENU ===")
        print("1 - Cadastrar usuário")
        print("2 - Fazer login")
        print("3 - Listar usuários")
        print("4 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            email = input("Digite o email: ")
            senha = input("Digite a senha: ")
            nome = input("Digite o nome: ")
            db.add_user(email, senha, nome)
        elif escolha == "2":
            email = input("Digite o email: ")
            senha = input("Digite a senha: ")
            if db.validate(email, senha):
                print(f"Login realizado com sucesso! Bem-vindo, {db.users[email][1]}!")
            else:
                print("Email ou senha inválidos!")
        elif escolha == "3":
            print("=== Usuários cadastrados ===")
            for email, data in db.users.items():
                print(f"{email} - {data[1]} - Criado em: {data[2]}")
        elif escolha == "4":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
