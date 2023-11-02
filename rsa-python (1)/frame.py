import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from rsa import generate_key_pair, encrypt, decrypt, split_message, split_blocks, join_blocks

class RSAApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Add widgets and layouts here
        self.setGeometry(650, 300, 400, 400)
        self.setWindowTitle('RSA Encryptor / Decryptor')
        self.show()

        # Create input fields and buttons
        self.p_label = QLabel('Nhập số nguyên tố (17, 19, 23, etc):')
        self.p_edit = QLineEdit()
        self.q_label = QLabel('Nhập một số nguyên tố khác với số trên:')
        self.q_edit = QLineEdit()
        self.encrypt_button = QPushButton('Mã hóa')
        self.decrypt_button = QPushButton('Giải mã')
        self.message_label = QLabel('Nhập thông điệp để mã hóa:')
        self.message_edit = QLineEdit()
        self.encrypted_label = QLabel('Thông điệp đã được mã hóa:')
        self.encrypted_edit = QLineEdit()
        self.encrypted_edit.setReadOnly(True)
        self.decrypted_label = QLabel('Thông điệp đã được giải mã:')
        self.decrypted_edit = QLineEdit()
        self.decrypted_edit.setReadOnly(True)
        self.d_label = QLabel("Nhập private key 'd':")
        self.d_edit = QLineEdit()
        self.n_label = QLabel("Nhập private key 'n':")
        self.n_edit = QLineEdit()
        self.encrypted_message_label = QLabel('Nhập thông điệp đã mã hóa để giải mã:')
        self.encrypted_message_edit = QLineEdit()
        self.e_label = QLabel("Public key 'e':")
        self.e_edit = QLineEdit()
        self.e_edit.setReadOnly(True)
        self.n2_label = QLabel("Public key 'n':")
        self.n2_edit = QLineEdit()
        self.n2_edit.setReadOnly(True)
        self.dShow_label = QLabel("Private key 'd':")
        self.dShow_edit = QLineEdit()
        self.dShow_edit.setReadOnly(True)
        self.space_label = QLabel("____________________________________________________________________")

        # Create layouts
        self.p_layout = QHBoxLayout()
        self.p_layout.addWidget(self.p_label)
        self.p_layout.addWidget(self.p_edit)
        self.q_layout = QHBoxLayout()
        self.q_layout.addWidget(self.q_label)
        self.q_layout.addWidget(self.q_edit)
        self.encrypt_layout = QHBoxLayout()
        self.encrypt_layout.addWidget(self.encrypt_button)
        self.decrypt_layout = QHBoxLayout()
        self.decrypt_layout.addWidget(self.decrypt_button)
        self.message_layout = QHBoxLayout()
        self.message_layout.addWidget(self.message_label)
        self.message_layout.addWidget(self.message_edit)
        self.encrypted_layout = QHBoxLayout()
        self.encrypted_layout.addWidget(self.encrypted_label)
        self.encrypted_layout.addWidget(self.encrypted_edit)
        self.decrypted_layout = QHBoxLayout()
        self.decrypted_layout.addWidget(self.decrypted_label)
        self.decrypted_layout.addWidget(self.decrypted_edit)
        self.d_n_layout = QHBoxLayout()
        self.d_n_layout.addWidget(self.d_label)
        self.d_n_layout.addWidget(self.d_edit)
        self.d_n_layout.addWidget(self.n_label)
        self.d_n_layout.addWidget(self.n_edit)
        self.encrypted_message_layout = QHBoxLayout()
        self.encrypted_message_layout.addWidget(self.encrypted_message_label)
        self.encrypted_message_layout.addWidget(self.encrypted_message_edit)
        self.e_n2_d_layout = QHBoxLayout()
        self.e_n2_d_layout.addWidget(self.e_label)
        self.e_n2_d_layout.addWidget(self.e_edit)
        self.e_n2_d_layout.addWidget(self.n2_label)
        self.e_n2_d_layout.addWidget(self.n2_edit)
        self.e_n2_d_layout.addWidget(self.dShow_label)
        self.e_n2_d_layout.addWidget(self.dShow_edit)
        self.space_layout = QHBoxLayout()
        self.space_layout.addWidget(self.space_label)

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.p_layout)
        self.main_layout.addLayout(self.q_layout)
        # encrypt
        self.main_layout.addLayout(self.message_layout)
        self.main_layout.addLayout(self.e_n2_d_layout)
        self.main_layout.addLayout(self.encrypt_layout)
        self.main_layout.addLayout(self.encrypted_layout)
        self.main_layout.addLayout(self.space_layout)
        # decrypt
        self.main_layout.addLayout(self.encrypted_message_layout)
        self.main_layout.addLayout(self.d_n_layout)
        self.main_layout.addLayout(self.decrypt_layout)
        self.main_layout.addLayout(self.decrypted_layout)
        self.setLayout(self.main_layout)

        # Connect buttons to functions
        self.encrypt_button.clicked.connect(self.encrypt_message)
        self.decrypt_button.clicked.connect(self.decrypt_message)

    def encrypt_message(self):
        try:
            p = int(self.p_edit.text())
            q = int(self.q_edit.text())
            public, private = generate_key_pair(p, q)
            message = self.message_edit.text()
            block_size = len(str(public[1])) - 1
            blocks = split_message(message, block_size)
            encrypted_blocks = []
            for block in blocks:
                encrypted_block = encrypt(public, block)
                encrypted_blocks.append(encrypted_block)
            encrypted_message = join_blocks(encrypted_blocks)
            self.encrypted_edit.setText(encrypted_message)
            self.e_edit.setText(str(public[0]))
            self.dShow_edit.setText(str(private[0]))
            self.n2_edit.setText(str(public[1]))
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))

    def decrypt_message(self):
        try:
            d = int(self.d_edit.text())
            n = int(self.n_edit.text())
            private_key = (d, n)
            encrypted_message = self.encrypted_message_edit.text()
            encrypted_blocks = split_blocks(encrypted_message)
            decrypted_message = decrypt(private_key, encrypted_blocks)
            self.decrypted_edit.setText(decrypted_message)
        except ValueError as e:
            QMessageBox.warning(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    rsa_app = RSAApp()
    sys.exit(app.exec_())
