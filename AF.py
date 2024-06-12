import os
import re

class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = ListNode(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def __str__(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return '\n'.join(result)

class Node:
    def __init__(self, key, details):
        self.key = key
        self.left = None
        self.right = None
        self.details = details

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key, details):
        if self.root is None:
            self.root = Node(key, details)
        else:
            self._insert(self.root, key, details)

    def _insert(self, root, key, details):
        if key < root.key:
            if root.left is None:
                root.left = Node(key, details)
            else:
                self._insert(root.left, key, details)
        elif key > root.key:
            if root.right is None:
                root.right = Node(key, details)
            else:
                self._insert(root.right, key, details)
        else:
            root.details = details  # Substituir detalhes se o contato já existir

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, root, key):
        if root is None or root.key == key:
            return root
        if key < root.key:
            return self._search(root.left, key)
        return self._search(root.right, key)

    def inorder_traversal(self, root):
        if root:
            yield from self.inorder_traversal(root.left)
            yield root
            yield from self.inorder_traversal(root.right)

    def remove(self, key):
        self.root, _ = self._remove(self.root, key)

    def _remove(self, root, key):
        if root is None:
            return root, None
        if key < root.key:
            root.left, removed = self._remove(root.left, key)
        elif key > root.key:
            root.right, removed = self._remove(root.right, key)
        else:
            if root.left is None:
                return root.right, root
            if root.right is None:
                return root.left, root
            min_larger_node = self._get_min(root.right)
            root.key, root.details = min_larger_node.key, min_larger_node.details
            root.right, _ = self._remove(root.right, min_larger_node.key)
            removed = root
        return root, removed

    def _get_min(self, root):
        while root.left is not None:
            root = root.left
        return root

class GerenciadorDeContatos:
    def __init__(self):
        self.contacts = BinaryTree()

    def validar_email(self, email):
        # Regex simples para validação de email
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.match(regex, email) is not None

    def validar_telefone(self, telefone):
        # Regex simples para validação de telefone (10-15 dígitos)
        regex = r'^\d{10,15}$'
        return re.match(regex, telefone) is not None

    def adicionar_contato(self, nome, telefone, email):
        if not self.validar_telefone(telefone):
            print("Número de telefone inválido. Deve conter entre 10 a 15 dígitos.")
            return
        if not self.validar_email(email):
            print("Endereço de email inválido.")
            return
        details = LinkedList()
        details.append(f"Telefone: {telefone}")
        details.append(f"Email: {email}")
        existing_contact = self.contacts.search(nome)
        if existing_contact:
            update = input(f"Já existe um contato com o nome '{nome}'. Deseja atualizá-lo? (s/n): ").strip().lower()
            if update == 's':
                self.atualizar_contato(nome, telefone, email)
                print("Contato atualizado com sucesso.")
            else:
                print("Contato não foi adicionado.")
        else:
            self.contacts.insert(nome, details)
            print("Contato adicionado com sucesso.")

    def remover_contato(self, nome):
        self.contacts.remove(nome)

    def buscar_contato(self, nome):
        node = self.contacts.search(nome)
        if node:
            return f"Nome: {node.key}\n{node.details}"
        else:
            return "Contato não encontrado."

    def atualizar_contato(self, nome, novo_telefone=None, novo_email=None):
        if novo_telefone and not self.validar_telefone(novo_telefone):
            print("Número de telefone inválido. Deve conter entre 10 a 15 dígitos.")
            return
        if novo_email and not self.validar_email(novo_email):
            print("Endereço de email inválido.")
            return
        node = self.contacts.search(nome)
        if node:
            self.remover_contato(nome)
            new_details = LinkedList()
            if novo_telefone:
                new_details.append(f"Telefone: {novo_telefone}")
            else:
                current = node.details.head
                while current:
                    if "Telefone:" in current.data:
                        new_details.append(current.data)
                    current = current.next
            if novo_email:
                new_details.append(f"Email: {novo_email}")
            else:
                current = node.details.head
                while current:
                    if "Email:" in current.data:
                        new_details.append(current.data)
                    current = current.next
            self.contacts.insert(nome, new_details)
        else:
            print("Contato não encontrado.")

    def listar_contatos(self):
        contacts = list(self.contacts.inorder_traversal(self.contacts.root))
        if not contacts:
            return "Nenhum contato cadastrado."
        else:
            return '\n\n'.join(f"Nome: {node.key}\n{node.details}" for node in contacts)

    def limpar_tela(self):
        # Limpar a tela do terminal
        os.system('cls' if os.name == 'nt' else 'clear')

    def executar(self):
        while True:
            self.limpar_tela()
            print("\nGerenciador de Contatos")
            print("1. Adicionar Contato")
            print("2. Remover Contato")
            print("3. Buscar Contato")
            print("4. Listar Contatos")
            print("5. Atualizar Contato")
            print("6. Sair")
            escolha = input("Digite sua escolha: ")

            self.limpar_tela()
            if escolha == '1':
                nome = input("Digite o nome: ")
                telefone = input("Digite o telefone: ")
                email = input("Digite o email: ")
                self.adicionar_contato(nome, telefone, email)
            elif escolha == '2':
                nome = input("Digite o nome do contato a ser removido: ")
                self.remover_contato(nome)
                print("Contato removido com sucesso.")
            elif escolha == '3':
                nome = input("Digite o nome para buscar: ")
                print(self.buscar_contato(nome))
            elif escolha == '4':
                print("Listando contatos:")
                print(self.listar_contatos())
            elif escolha == '5':
                nome = input("Digite o nome do contato a ser atualizado: ")
                novo_telefone = input("Digite o novo telefone (deixe em branco se não houver mudança): ")
                novo_email = input("Digite o novo email (deixe em branco se não houver mudança): ")
                self.atualizar_contato(nome, novo_telefone, novo_email)
                print("Contato atualizado com sucesso.")
            elif escolha == '6':
                print("Saindo do programa.")
                break
            else:
                print("Escolha inválida. Por favor, tente novamente.")
            input("Pressione Enter para continuar...")

if __name__ == "__main__":
    manager = GerenciadorDeContatos()
    manager.executar()
