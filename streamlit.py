import streamlit as st
from rsa import generate_key_pair, encrypt, decrypt, split_message, split_blocks, join_blocks

def rsa_app():
    # Khởi tạo session state
    if 'history' not in st.session_state:
        st.session_state.history = []

    st.sidebar.title('Chọn Chức Năng')
    selected_option = st.sidebar.radio('', ['Mã hóa', 'Giải mã'])

    upload_option = st.radio('Chọn nguồn thông điệp:', ['Nhập thông điệp', 'Tải lên từ file'])
    message = ""

    if upload_option == 'Nhập thông điệp':
        message = st.text_area('Nhập thông điệp:', '')
    elif upload_option == 'Tải lên từ file':
        uploaded_file = st.file_uploader('Chọn file để mã hóa hoặc giải mã', type=['txt'])
        if uploaded_file is not None:
            message = uploaded_file.read().decode('utf-8')

    if selected_option == 'Mã hóa':
        st.title('RSA Encryptor')
        p = st.text_input('Nhập số nguyên tố (17, 19, 23, etc):')
        q = st.text_input('Nhập một số nguyên tố khác với số trên:')
        encrypt_button = st.button('Mã hóa')
        if encrypt_button and message:
            try:
                p = int(p)
                q = int(q)
                public, private = generate_key_pair(p, q)
                block_size = len(str(public[1])) - 1
                blocks = split_message(message, block_size)
                encrypted_blocks = [encrypt(public, block) for block in blocks]
                encrypted_message = join_blocks(encrypted_blocks)
                st.write('Thông điệp đã được mã hóa:', encrypted_message)
                st.write("key 'e':", public[0])
                st.write("key 'n':", public[1])
                st.write("key 'd':", private[0])
                
                history_entry = {
                    'type': 'Mã hóa',
                    'message': message,
                    'encrypted_message': encrypted_message,
                    'public_key': public,
                    'private_key': private
                }
                st.session_state.history.append(history_entry)  # Lưu lịch sử mã hóa

                # Xuất thông điệp đã mã hóa ra file .txt
                download_button = st.download_button(label="Xuất mã hóa ra file", data=encrypted_message, file_name='encrypted_message.txt')

            except ValueError as e:
                st.warning(str(e))

    elif selected_option == 'Giải mã':
        st.title('RSA Decryptor')
        private_key_d = st.text_input("Nhập key 'd' để giải mã:")
        private_key_n = st.text_input("Nhập key 'n' để giải mã:")
        decrypt_button = st.button('Giải mã')
        if decrypt_button and message:
            try:
                d = int(private_key_d)
                n = int(private_key_n)
                encrypted_blocks = split_blocks(message)
                decrypted_message = decrypt((d, n), encrypted_blocks)
                st.write('Thông điệp đã được giải mã:', decrypted_message)
                
                history_entry = {
                    'type': 'Giải mã',
                    'message': message,
                    'decrypted_message': decrypted_message,
                    'private_key_d': d,
                    'private_key_n': n
                }
                st.session_state.history.append(history_entry)  # Lưu lịch sử giải mã
            except ValueError as e:
                st.warning(str(e))

    # Hiển thị lịch sử mã hóa và giải mã khi người dùng nhấn nút 'Xem Lịch Sử'
    if st.button('Xem Lịch Sử'):
        st.title('Lịch Sử Mã Hóa và Giải Mã')
        for entry in st.session_state.history:
            st.write(f"Loại: {entry['type']}")
            st.write(f"Thông điệp: {entry['message']}")
            if 'encrypted_message' in entry:
                st.write(f"Thông điệp đã được mã hóa: {entry['encrypted_message']}")
                st.write(f"Khóa công khai: {entry['public_key']}")
                st.write(f"Khóa riêng tư: {entry['private_key']}")
            elif 'decrypted_message' in entry:
                st.write(f"Thông điệp đã được giải mã: {entry['decrypted_message']}")
                st.write(f"Khóa riêng tư 'd': {entry['private_key_d']}")
                st.write(f"Khóa riêng tư 'n': {entry['private_key_n']}")

    # Thêm nút để xóa lịch sử
    if st.button('Xóa Lịch Sử'):
        st.session_state.history = []

if __name__ == '__main__':
    rsa_app()
