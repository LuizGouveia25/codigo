# Instruções para o Autenticador TOTP Jurídico

Este documento detalha as etapas para o deployment e a manutenção do arquivo `autenticador-totp.html` em um ambiente de hospedagem como o GitHub Pages.

## 1. Deployment no GitHub Pages

O GitHub Pages é uma excelente opção para hospedar este autenticador devido à sua simplicidade e ao fornecimento automático de HTTPS, que é **obrigatório** para o funcionamento da Web Crypto API utilizada na geração do TOTP.

Siga os passos abaixo para publicar seu autenticador:

1.  **Crie um Repositório Público no GitHub**: Acesse o GitHub e crie um novo repositório público. Sugere-se um nome descritivo como `totp-juridico`.
2.  **Faça Upload do Arquivo HTML**: Renomeie o arquivo `autenticador-totp.html` para `index.html` e faça o upload para a raiz do seu novo repositório GitHub. Você pode fazer isso diretamente pela interface web do GitHub ou via linha de comando (`git add index.html`, `git commit -m "Add TOTP authenticator"`, `git push`).
3.  **Configure o GitHub Pages**: No seu repositório, navegue até `Settings` (Configurações) > `Pages`.
    *   Em `Source` (Fonte), selecione `Deploy from a branch` (Publicar a partir de um branch).
    *   Em `Branch`, escolha o branch `main` (ou o branch onde você fez o upload do `index.html`).
    *   Certifique-se de que a pasta selecionada seja `/ (root)`.
4.  **Salve as Configurações**: Clique em `Save` (Salvar).
5.  **Aguarde a Publicação**: O GitHub Pages levará alguns minutos para construir e publicar seu site. Você pode verificar o status em `Settings` > `Pages`.
6.  **Acesse o Autenticador**: Uma vez publicado, seu autenticador estará acessível via HTTPS em um URL no formato `https://SEU_USUARIO.github.io/NOME_DO_REPOSITORIO/`. Por exemplo, se seu usuário for `meuusuario` e o repositório `totp-juridico`, o URL será `https://meuusuario.github.io/totp-juridico/`.

**Importante**: O GitHub Pages fornece HTTPS automaticamente, o que é crucial para a segurança e funcionalidade do autenticador. O acesso via HTTP (sem "s") não permitirá que a Web Crypto API funcione, e o sistema exibirá um aviso.

## 2. Manutenção do Autenticador

As configurações de usuários e senhas são gerenciadas diretamente no arquivo `index.html` (originalmente `autenticador-totp.html`). As senhas são armazenadas como hashes bcrypt para segurança. Abaixo estão as instruções para as tarefas de manutenção mais comuns.

### 2.1. Como Trocar a Senha de um Usuário

Para alterar a senha de um usuário existente, você precisará gerar um novo hash bcrypt para a nova senha e atualizar o arquivo HTML.

1.  **Gerar Novo Hash Bcrypt**: Utilize o script Python fornecido ou um método similar para gerar um novo hash bcrypt com fator de custo 12 para a nova senha. Exemplo em Python:

    ```python
    import bcrypt
    nova_senha = b"minha_nova_senha_forte*"
    novo_hash = bcrypt.hashpw(nova_senha, bcrypt.gensalt(rounds=12))
    print(novo_hash.decode())
    ```

2.  **Localizar a Constante `USERS`**: Abra o arquivo `index.html` (ou `autenticador-totp.html`) em um editor de texto e localize a seção JavaScript que define a constante `USERS`:

    ```javascript
    const USERS = {
        "luiz": "HASH_BCRYPT_DA_SENHA_luiz2601*",
        "alisson": "HASH_BCRYPT_DA_SENHA_alisson2833*",
        "barbara": "HASH_BCRYPT_DA_SENHA_barbara6782*"
    };
    ```

3.  **Substituir o Hash**: Encontre a linha correspondente ao usuário cuja senha você deseja alterar e substitua o hash antigo pelo novo hash gerado.
4.  **Salvar e Fazer Commit**: Salve o arquivo `index.html` e faça commit das alterações no seu repositório GitHub. O GitHub Pages será atualizado automaticamente.

### 2.2. Como Adicionar um Novo Usuário

Para adicionar um novo usuário ao sistema, siga os passos:

1.  **Gerar Hash Bcrypt para a Nova Senha**: Use o mesmo método descrito acima para gerar um hash bcrypt para a senha do novo usuário.
2.  **Adicionar Linha no Objeto `USERS`**: Abra o arquivo `index.html` e adicione uma nova entrada ao objeto `USERS` com o nome de usuário e o hash gerado:

    ```javascript
    const USERS = {
        // ... usuários existentes
        "novo_usuario": "HASH_BCRYPT_DA_SENHA_DO_NOVO_USUARIO"
    };
    ```

3.  **Salvar e Fazer Commit**: Salve o arquivo e faça commit das alterações no GitHub.

### 2.3. Como Remover um Usuário

Para remover um usuário do sistema:

1.  **Deletar a Linha Correspondente**: Abra o arquivo `index.html` e simplesmente remova a linha completa do objeto `USERS` que corresponde ao usuário que você deseja excluir.
2.  **Salvar e Fazer Commit**: Salve o arquivo e faça commit das alterações no GitHub.

### 2.4. Como Gerar Hash Bcrypt (Exemplo Python)

Para sua conveniência, aqui está o snippet de código Python para gerar hashes bcrypt com fator de custo 12:

```python
import bcrypt

def generate_bcrypt_hash(password_str):
    password_bytes = password_str.encode("utf-8")
    # Fator de custo 12, conforme especificado
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt(rounds=12))
    return hashed.decode("utf-8")

# Exemplo de uso:
# senha_luiz = "luiz2601*"
# hash_luiz = generate_bcrypt_hash(senha_luiz)
# print(f"Hash para luiz: {hash_luiz}")

# senha_alisson = "alisson2833*"
# hash_alisson = generate_bcrypt_hash(senha_alisson)
# print(f"Hash para alisson: {hash_alisson}")

# senha_barbara = "barbara6782*"
# hash_barbara = generate_bcrypt_hash(senha_barbara)
# print(f"Hash para barbara: {hash_barbara}")
```

## 3. Considerações de Segurança

*   **HTTPS Obrigatório**: O uso de HTTPS é fundamental para a segurança da comunicação e para o funcionamento da Web Crypto API. O GitHub Pages garante isso automaticamente.
*   **Chave TOTP e Senhas**: A chave TOTP nunca é armazenada no `localStorage` ou `sessionStorage`. As senhas são armazenadas apenas como hashes bcrypt, nunca em texto puro.
*   **Sessão**: A sessão do usuário é mantida no `sessionStorage`, o que significa que ela é apagada automaticamente quando a aba do navegador é fechada, aumentando a segurança.
*   **Logs de Auditoria**: Os logs de auditoria são armazenados no `localStorage` e são limitados aos 100 registros mais recentes para evitar o acúmulo excessivo de dados, mas fornecem um histórico importante de acessos e ações.
*   **Bloqueio por Tentativas**: O sistema implementa um bloqueio temporário após múltiplas tentativas de login falhas, mitigando ataques de força bruta.
