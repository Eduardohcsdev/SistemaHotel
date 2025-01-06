import json
from datetime import datetime

# Classe base para Quarto
class Quarto:
    def __init__(self, numero_quarto, tarifa_base):
        self.numero_quarto = numero_quarto
        self.tarifa_base = tarifa_base
        self.reservado = False

    def calcular_tarifa_diaria(self, dias):
        return self.tarifa_base * dias

# Subclasse para Quarto Simples
class QuartoSimples(Quarto):
    def __init__(self, numero_quarto):
        super().__init__(numero_quarto, tarifa_base=100)

# Subclasse para Quarto Luxo
class QuartoLuxo(Quarto):
    def __init__(self, numero_quarto):
        super().__init__(numero_quarto, tarifa_base=250)

    def calcular_tarifa_diaria(self, dias):
        return (self.tarifa_base * dias) * 0.9  # 10% de desconto para estadias longas

# Sistema de Reservas
class SistemaReservas:
    def __init__(self):
        self.quartos = []
        self.reservas = []
        self.carregar_dados()

    def adicionar_quarto(self, quarto):
        self.quartos.append(quarto)

    def criar_quarto(self):
        tipo = input("Tipo de quarto (simples/luxo): ").strip().lower()
        numero_quarto = int(input("Número do quarto: "))

        if tipo == "simples":
            novo_quarto = QuartoSimples(numero_quarto)
        elif tipo == "luxo":
            novo_quarto = QuartoLuxo(numero_quarto)
        else:
            print("Tipo de quarto inválido.")
            return

        self.adicionar_quarto(novo_quarto)
        print(f"Quarto {numero_quarto} do tipo {tipo} adicionado com sucesso!")

    def editar_quarto(self):
        numero_quarto = int(input("Número do quarto a ser editado: "))
        quarto = next((q for q in self.quartos if q.numero_quarto == numero_quarto), None)

        if not quarto:
            print("Quarto não encontrado.")
            return

        novo_tipo = input("Novo tipo de quarto (simples/luxo): ").strip().lower()
        if novo_tipo == "simples":
            quarto.__class__ = QuartoSimples
            quarto.tarifa_base = 100
        elif novo_tipo == "luxo":
            quarto.__class__ = QuartoLuxo
            quarto.tarifa_base = 250
        else:
            print("Tipo inválido. Edição cancelada.")
            return

        print(f"Quarto {numero_quarto} atualizado para tipo {novo_tipo}.")

    def excluir_quarto(self):
        numero_quarto = int(input("Número do quarto a ser excluído: "))
        quarto = next((q for q in self.quartos if q.numero_quarto == numero_quarto), None)

        if not quarto:
            print("Quarto não encontrado.")
            return

        self.quartos.remove(quarto)
        print(f"Quarto {numero_quarto} removido com sucesso!")

    def fazer_reserva(self, nome_hospede, numero_quarto, check_in, check_out):
        quarto = next((q for q in self.quartos if q.numero_quarto == numero_quarto and not q.reservado), None)
        if not quarto:
            print(f"Quarto {numero_quarto} não está disponível.")
            return

        dias = (check_out - check_in).days
        custo_total = quarto.calcular_tarifa_diaria(dias)

        reserva = {
            "nome_hospede": nome_hospede,
            "numero_quarto": numero_quarto,
            "check_in": check_in.strftime('%Y-%m-%d'),
            "check_out": check_out.strftime('%Y-%m-%d'),
            "custo_total": custo_total
        }

        quarto.reservado = True
        self.reservas.append(reserva)
        print(f"Reserva para {nome_hospede} confirmada: Quarto {numero_quarto}, Custo Total: R${custo_total:.2f}")

    def cancelar_reserva(self, nome_hospede):
        reserva = next((r for r in self.reservas if r["nome_hospede"] == nome_hospede), None)
        if not reserva:
            print(f"Nenhuma reserva encontrada para {nome_hospede}.")
            return

        quarto = next(q for q in self.quartos if q.numero_quarto == reserva["numero_quarto"])
        quarto.reservado = False
        self.reservas.remove(reserva)
        print(f"Reserva para {nome_hospede} foi cancelada.")

    def salvar_dados(self):
        dados = {
            "quartos": [{"numero_quarto": q.numero_quarto, "tarifa_base": q.tarifa_base, "reservado": q.reservado} for q in self.quartos],
            "reservas": self.reservas
        }
        with open("dados_hotel.json", "w") as arquivo:
            json.dump(dados, arquivo)

    def carregar_dados(self):
        try:
            with open("dados_hotel.json", "r") as arquivo:
                dados = json.load(arquivo)
                for dados_quarto in dados["quartos"]:
                    classe_quarto = QuartoSimples if dados_quarto["tarifa_base"] == 100 else QuartoLuxo
                    quarto = classe_quarto(dados_quarto["numero_quarto"])
                    quarto.reservado = dados_quarto["reservado"]
                    self.quartos.append(quarto)
                self.reservas = dados["reservas"]
        except FileNotFoundError:
            pass

    def solicitar_data(self, mensagem):
        while True:
            try:
                data = input(mensagem)
                return datetime.strptime(data, "%Y-%m-%d")
            except ValueError:
                print("Data inválida! Por favor, insira no formato AAAA-MM-DD.")

    def exibir_menu(self):
        while True:
            print("\nMenu do Sistema de Reservas:")
            print("1. Fazer Reserva")
            print("2. Cancelar Reserva")
            print("3. Listar Quartos")
            print("4. Listar Reservas")
            print("5. Criar Quarto")
            print("6. Editar Quarto")
            print("7. Excluir Quarto")
            print("8. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                nome_hospede = input("Nome do hóspede: ")
                numero_quarto = int(input("Número do quarto: "))
                check_in = self.solicitar_data("Data de check-in (AAAA-MM-DD): ")
                check_out = self.solicitar_data("Data de check-out (AAAA-MM-DD): ")
                self.fazer_reserva(nome_hospede, numero_quarto, check_in, check_out)

            elif opcao == "2":
                nome_hospede = input("Nome do hóspede para cancelar a reserva: ")
                self.cancelar_reserva(nome_hospede)

            elif opcao == "3":
                print("\nQuartos Disponíveis:")
                for quarto in self.quartos:
                    status = "Reservado" if quarto.reservado else "Disponível"
                    print(f"Quarto {quarto.numero_quarto} - {status}")

            elif opcao == "4":
                print("\nReservas Atuais:")
                for reserva in self.reservas:
                    print(f"Hóspede: {reserva['nome_hospede']}, Quarto: {reserva['numero_quarto']}, Check-in: {reserva['check_in']}, Check-out: {reserva['check_out']}, Custo: R${reserva['custo_total']:.2f}")

            elif opcao == "5":
                self.criar_quarto()

            elif opcao == "6":
                self.editar_quarto()

            elif opcao == "7":
                self.excluir_quarto()

            elif opcao == "8":
                self.salvar_dados()
                print("Saindo do sistema. Até logo!")
                break

            else:
                print("Opção inválida. Tente novamente.")

# Exemplo de Uso
if __name__ == "__main__":
    sistema = SistemaReservas()

    # Adicionando quartos
    # sistema.adicionar_quarto(QuartoSimples(101))
    # sistema.adicionar_quarto(QuartoSimples(102))
    # sistema.adicionar_quarto(QuartoLuxo(201))
    # sistema.adicionar_quarto(QuartoLuxo(202))

    # Iniciando menu do sistema
    sistema.exibir_menu()
